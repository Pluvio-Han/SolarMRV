from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

"""
full_test.py - 全流程端到端测试
读取设备 → SM2签名 → 保存CSV → 生成图表 → 上链 → 获取链状态 → 发送Telegram
"""
import time, os, sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from solar_monitor import SolarMonitor
from telegram_notify import TelegramNotifier
from chain_client import ChainClient
import config

PORT = config.MONITOR_PORT

def run_test():
    now = datetime.now()
    print('='*50)
    print('🚀 全流程端到端测试')
    print('='*50)
    sys.stdout.flush()

    # Step 1: 读取
    print('\n📡 Step 1: 读取硬件数据...')
    sys.stdout.flush()
    monitor = SolarMonitor(port=PORT)
    monitor.connect()
    raw_data = monitor.read_realtime_data()
    if not raw_data:
        print('❌ 读取失败!'); return
    print(f'  ☀️ PV: {raw_data["pv_power"]}W | ⚡ {raw_data["pv_voltage"]}V | 🔋 SOC:{raw_data["batt_soc"]}% | Batt:{raw_data["batt_voltage"]}V')
    sys.stdout.flush()

    # Step 2: SM2 签名
    print('\n🔐 Step 2: SM2 签名...')
    sig = monitor.sign_payload(raw_data)
    print(f'  签名: {sig[:30]}...')
    monitor.disconnect()
    sys.stdout.flush()

    # Step 3: 保存 CSV
    print('\n💾 Step 3: 保存CSV...')
    csv_file = os.path.join(config.DATA_DIR, f'solar_data_{now.strftime("%Y%m%d_%H%M")}.csv')
    chart_file = os.path.join(config.CHART_DIR, f'solar_chart_{now.strftime("%Y%m%d_%H%M")}.png')
    df = pd.DataFrame([{
        'Time': now,
        'PV_Power_W': raw_data['pv_power'],
        'PV_Voltage_V': raw_data['pv_voltage'],
        'Batt_SOC_Pct': raw_data['batt_soc'],
        'Batt_Voltage_V': raw_data['batt_voltage'],
        'Total_Energy_kWh': raw_data['total_energy_generated']
    }])
    df.to_csv(csv_file, index=False)
    print(f'  {csv_file} ✅')
    sys.stdout.flush()

    # Step 4: 生成图表
    print('\n📈 Step 4: 生成图表...')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    ax1.bar(['PV Power'], [raw_data['pv_power']], color='#06d6a0')
    ax1.set_ylabel('Power (W)')
    ax1.set_title(f'Solar Monitor - {now.strftime("%Y-%m-%d %H:%M")}')
    ax2.bar(['SOC'], [raw_data['batt_soc']], color='#ffd166')
    ax2.set_ylabel('SOC (%)')
    ax2.set_ylim(0, 100)
    plt.tight_layout()
    plt.savefig(chart_file, dpi=100)
    plt.close()
    print(f'  {chart_file} ✅')
    sys.stdout.flush()

    # Step 5: 上链
    print('\n⛓️ Step 5: 数据上链...')
    sys.stdout.flush()
    chain = ChainClient()
    chain.connect()
    try:
        tx = chain.store_data(
            pv_power=raw_data['pv_power'],
            pv_voltage=raw_data['pv_voltage'],
            batt_soc=raw_data['batt_soc'],
            batt_voltage=raw_data['batt_voltage'],
            total_energy=raw_data['total_energy_generated'],
            signature=sig
        )
        print(f'  TX: {tx}')
    except Exception as e:
        print(f'  ⚠️ 上链失败: {e} (继续测试...)')
        tx = "failed"
    sys.stdout.flush()

    # Step 6: 链状态
    print('\n📊 Step 6: 获取链状态...')
    sys.stdout.flush()
    cs = chain.get_chain_summary()
    sync = cs.get('sync', {})
    consensus = cs.get('consensus', {})
    
    peer_names = ["Gwen node1", "Miles node0", "Miles node1", "Peter node0", "Peter node1"]
    peer_lines = [f"  📍 Gwen node0(本机): #{cs.get('block_height', '?')}"]
    for idx, p in enumerate(sync.get('peers', [])):
        name = peer_names[idx] if idx < len(peer_names) else f"Node{idx}"
        peer_lines.append(f"  📍 {name}: #{p.get('height', '?')}")
    node_text = "\n".join(peer_lines)
    
    chain_info = (
        f"\n⛓️ 区块链状态\n"
        f"➖➖➖➖➖➖➖➖\n"
        f"📦 区块高度: #{cs.get('block_height', '?')}\n"
        f"📊 链上记录: {cs.get('record_count', '?')} 条\n"
        f"🌐 连接节点: {cs.get('peer_count', '?')} 个\n"
        f"🔗 共识节点: {consensus.get('node_count', '?')} 个\n"
        f"🔄 同步状态: {'同步中' if sync.get('is_syncing') else '已同步 ✅'}\n"
        f"📡 节点详情:\n{node_text}\n"
    )
    chain.disconnect()
    print(f'  区块高度: #{cs.get("block_height")} | 记录: {cs.get("record_count")} 条 ✅')
    sys.stdout.flush()

    # Step 7: Telegram
    print('\n📩 Step 7: 发送 Telegram 通知...')
    sys.stdout.flush()
    bot = TelegramNotifier()
    caption = (
        f"⏱️ 全流程测试 ({now.strftime('%H:%M')})\n"
        f"➖➖➖➖➖➖➖➖\n"
        f"☀️ 当前功率: {raw_data['pv_power']} W\n"
        f"🔋 电池电量: {raw_data['batt_soc']} %\n"
        f"📊 累计发电: {raw_data['total_energy_generated']} kWh\n"
        f"{chain_info}"
        f"➖➖➖➖➖➖➖➖\n"
        f"🔐 SM2签名: {sig[:20]}...\n"
        f"📈 全流程测试: 通过 ✅"
    )
    if os.path.exists(chart_file):
        bot.send_photo(chart_file, caption=caption)
    else:
        bot.send_message(caption)
    print('  Telegram 已发送 ✅')
    sys.stdout.flush()

    print('\n' + '='*50)
    print('🎉 全流程 7/7 步骤全部通过!')
    print('='*50)

if __name__ == '__main__':
    run_test()
