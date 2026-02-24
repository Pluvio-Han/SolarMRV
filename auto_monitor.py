import time
import pandas as pd
import matplotlib
matplotlib.use('Agg') # 设置非交互式后端，防止每5分钟弹窗
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
from solar_monitor import SolarMonitor
from telegram_notify import TelegramNotifier
from chain_client import ChainClient

import config

# 配置参数 (从 config.py 读取)
DURATION_HOURS = config.DURATION_HOURS
INTERVAL_MINUTES = config.INTERVAL_MINUTES
TOTAL_LOOPS = int((DURATION_HOURS * 60) / INTERVAL_MINUTES)
PORT = config.MONITOR_PORT

# 生成带日期的文件名
CSV_FILE = config.CSV_FILE
CHART_FILE = config.CHART_FILE

def main():
    print(f"📊 启动自动监测程序")
    print(f"总时长: {DURATION_HOURS} 小时")
    print(f"采样间隔: {INTERVAL_MINUTES} 分钟 (共 {TOTAL_LOOPS} 次采样)")
    print(f"数据将保存至: {CSV_FILE}")
    print(f"图表将生成至: {CHART_FILE}")

    # 初始化 Monitor
    monitor = SolarMonitor(port=PORT)
    if not monitor.connect():
        print("❌ 无法连接设备，程序退出")
        return

    # 初始化 Telegram Bot
    bot = TelegramNotifier()
    try:
        bot.send_message("🚀 光伏自动监测已启动 (8小时任务)")
    except:
        pass

    # 初始化区块链客户端
    chain = ChainClient()
    chain_connected = False
    try:
        chain.connect()
        chain_connected = True
        count = chain.get_data_count()
        print(f"⛓️  区块链已连接 (链上已有 {count} 条记录)")
    except Exception as e:
        print(f"⚠️ 区块链连接失败: {e} (将仅本地记录，不上链)")

    data_list = []
    
    # 尝试加载已有数据
    if os.path.exists(CSV_FILE):
        try:
            print(f"📂 发现已有数据文件: {CSV_FILE}")
            existing_df = pd.read_csv(CSV_FILE)
            if not existing_df.empty:
                # 转换时间列格式
                existing_df['Time'] = pd.to_datetime(existing_df['Time'])
                data_list = existing_df.to_dict('records')
                print(f"✅ 已加载 {len(data_list)} 条历史记录，将继续追加...")
        except Exception as e:
            print(f"⚠️ 加载历史数据失败: {e} (将开始新记录)")

    # 计算每小时的循环数
    loops_per_hour = 60 // INTERVAL_MINUTES

    try:
        start_time = datetime.now()
        
        for i in range(TOTAL_LOOPS):
            current_time = datetime.now()
            # 记录总序号
            total_count = len(data_list) + 1
            print(f"\n--- 第 {total_count} 次采样 (本次运行 {i+1}/{TOTAL_LOOPS}) ({current_time.strftime('%H:%M:%S')}) ---")
            
            # 读取数据
            raw_data = monitor.read_realtime_data()
            
            # 如果读取失败，尝试重连一次
            if not raw_data:
                print("⚠️ 读取失败，尝试重连设备...")
                monitor.disconnect()
                time.sleep(2)
                if monitor.connect():
                    print("✅ 重连成功，重试读取...")
                    raw_data = monitor.read_realtime_data()
                else:
                    print("❌ 重连失败")

            # 处理数据
            if raw_data:
                # 打印当前摘录
                print(f"☀️ PV功率: {raw_data.get('pv_power', 0)} W")
                print(f"🔋 电池电量: {raw_data.get('batt_soc', 0)} %")
                
                # 添加到列表
                record = {
                    'Time': current_time,
                    'PV_Power_W': raw_data.get('pv_power', 0),
                    'PV_Voltage_V': raw_data.get('pv_voltage', 0),
                    'Batt_SOC_Pct': raw_data.get('batt_soc', 0),
                    'Batt_Voltage_V': raw_data.get('batt_voltage', 0),
                    'Total_Energy_kWh': raw_data.get('total_energy_generated', 0)
                }
                data_list.append(record)
                
                # 保存 CSV (覆盖写入，包含历史记录)
                df = pd.DataFrame(data_list)
                df.to_csv(CSV_FILE, index=False)
                
                # 生成/更新图表
                try:
                    generate_chart(df)
                    print(f"✅ 数据已保存，图表已更新: {CHART_FILE}")
                except Exception as e:
                    print(f"⚠️ 图表生成失败: {e}")

                # 上链
                chain_record_count = "N/A"
                if chain_connected:
                    try:
                        # 4. SM2 签名集成 (Optimization #4)
                        sig = monitor.sign_payload(raw_data)
                        
                        # 1. & 3. 快速上链 & 错误处理 (Optimizations)
                        chain.store_data(
                            pv_power=raw_data.get('pv_power', 0),
                            pv_voltage=raw_data.get('pv_voltage', 0),
                            batt_soc=raw_data.get('batt_soc', 0),
                            batt_voltage=raw_data.get('batt_voltage', 0),
                            total_energy=raw_data.get('total_energy_generated', 0),
                            signature=sig
                        )
                        
                        # ----- 新增: Phase 2 预言机自动铸币 -----
                        print("🤖 触发预言机: 正在向 RWA 合约同步电量并尝试铸造绿电代币...")
                        mint_success, mint_tx = chain.mint_token(
                            device_id="NODE_001",
                            total_energy=raw_data.get('total_energy_generated', 0)
                        )
                        if mint_success:
                            print(f"✅ RWA 结算完成, Token Minting 触发成功!")
                        # ----------------------------------------

                        # 更新链上记录数用于通知
                        try:
                            # 2. 获取链状态 (Optimization #2)
                            count = chain.get_data_count()
                            chain_record_count = str(count)
                        except:
                            pass
                    except Exception as e:
                        print(f"⚠️ 上链失败: {e} (数据已本地保存)")

            # 判断是否整点 (每小时发送一次通知)
            if (i + 1) % loops_per_hour == 0:
                print("🔔 触发整点通知...")
                try:
                    # 情况A: 有数据 -> 发送图表和详情
                    if raw_data:
                        current_power = raw_data.get('pv_power', 0)
                        current_soc = raw_data.get('batt_soc', 0)
                        total_energy = raw_data.get('total_energy_generated', 0)
                        
                        # 获取完整链状态摘要
                        chain_info = ""
                        if chain_connected:
                            try:
                                cs = chain.get_chain_summary()
                                sync = cs.get("sync", {})
                                consensus = cs.get("consensus", {})
                                
                                # 构建节点同步状态 (3台服务器 × 2节点)
                                peer_names = ["Gwen node1", "Miles node0", "Miles node1", "Peter node0", "Peter node1"]
                                peer_lines = []
                                my_height = cs.get("block_height", "N/A")
                                peer_lines.append(f"  📍 Gwen node0(本机): #{my_height}")
                                for idx, p in enumerate(sync.get("peers", [])):
                                    name = peer_names[idx] if idx < len(peer_names) else f"Node{idx}"
                                    peer_lines.append(f"  📍 {name}: #{p.get('height', '?')}")
                                
                                node_status_text = "\n".join(peer_lines) if peer_lines else "  ⚠️ 无法获取"
                                
                                chain_info = (
                                    f"\n⛓️ 区块链状态\n"
                                    f"➖➖➖➖➖➖➖➖\n"
                                    f"📦 区块高度: #{cs.get('block_height', 'N/A')}\n"
                                    f"📊 链上记录: {cs.get('record_count', 'N/A')} 条\n"
                                    f"🌐 连接节点: {cs.get('peer_count', 'N/A')} 个\n"
                                    f"🔗 共识节点: {consensus.get('node_count', 'N/A')} 个\n"
                                    f"🔄 同步状态: {'同步中' if sync.get('is_syncing') else '已同步 ✅'}\n"
                                    f"📡 节点详情:\n{node_status_text}\n"
                                )
                            except Exception as ce:
                                chain_info = f"\n⛓️ 链状态查询异常: {ce}\n"
                        
                        caption = (
                            f"⏱️ 监测报告 ({current_time.strftime('%H:%M')})\n"
                            f"➖➖➖➖➖➖➖➖\n"
                            f"☀️ 当前功率: {current_power} W\n"
                            f"🔋 电池电量: {current_soc} %\n"
                            f"📊 累计发电: {total_energy} kWh\n"
                            f"{chain_info}"
                            f"➖➖➖➖➖➖➖➖\n"
                            f"📈 运行状态: 正常 ✅"
                        )
                        # 尝试发送图片，如果失败则发送文本
                        if not bot.send_photo(CHART_FILE, caption=caption):
                            bot.send_message(caption + "\n(⚠️ 图片发送失败)")
                            
                    # 情况B: 没数据 (读取失败) -> 发送报警
                    else:
                        alert_msg = (
                            f"⚠️ 监测异常 ({current_time.strftime('%H:%M')})\n"
                            f"无法读取设备数据！\n"
                            f"可能原因: USB连接断开或设备休眠。\n"
                            f"程序仍在尝试重连运行..."
                        )
                        bot.send_message(alert_msg)
                        
                except Exception as e:
                    print(f"⚠️ Telegram 推送逻辑异常: {e}")
            
            # 等待下一次 (绝对时间调度，消除漂移)
            if i < TOTAL_LOOPS - 1:
                next_schedule = start_time + timedelta(minutes=INTERVAL_MINUTES * (i + 1))
                wait_seconds = (next_schedule - datetime.now()).total_seconds()
                
                if wait_seconds > 0:
                    print(f"⏳ 等待 {wait_seconds:.1f} 秒 (下次采样: {next_schedule.strftime('%H:%M:%S')})...")
                    time.sleep(wait_seconds)
                else:
                    print(f"⚠️ 采样滞后 {abs(wait_seconds):.1f} 秒，立即执行...")
                
        print("\n🎉 监测任务完成！")
        bot.send_message("✅ 监测任务已完成！负载即将关闭。")
        
    except KeyboardInterrupt:
        print("\n🛑 用户中断监测")
    except Exception as e:
        print(f"\n❌ 程序发生未捕获异常: {e}")
        bot.send_message(f"💥 程序崩溃: {e}")
    finally:
        # P2: 自动关闭负载
        print("💡 正在关闭负载...")
        monitor.set_load_state(False)
        
        monitor.disconnect()
        if chain_connected:
            chain.disconnect()

def generate_chart(df):
    # P2: 图表美化 (暗色主题)
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 8))
    
    # 子图1: 光伏功率 & 电池电量
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(df['Time'], df['PV_Power_W'], label='PV Power (W)', color='#ffd700', linewidth=2)
    ax1.fill_between(df['Time'], df['PV_Power_W'], alpha=0.2, color='#ffd700')
    ax1.set_ylabel('Power (W)', color='white')
    ax1.set_title(f'Solar Generation Monitor ({df["Time"].iloc[0].strftime("%Y-%m-%d")})', color='white', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left')
    
    # 标注峰值
    if not df.empty:
        max_node = df.loc[df['PV_Power_W'].idxmax()]
        ax1.annotate(f'Peak: {max_node["PV_Power_W"]}W', 
                     xy=(max_node['Time'], max_node['PV_Power_W']),
                     xytext=(10, 10), textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', color='white'), color='white')

    # 双轴显示 SOC
    ax2 = ax1.twinx()
    ax2.plot(df['Time'], df['Batt_SOC_Pct'], label='Battery SOC (%)', color='#00ff00', linestyle='--', linewidth=1.5)
    ax2.set_ylabel('SOC (%)', color='#00ff00')
    ax2.set_ylim(0, 100)
    ax2.legend(loc='upper right')

    # 子图2: 电压变化
    ax3 = plt.subplot(2, 1, 2)
    ax3.plot(df['Time'], df['PV_Voltage_V'], label='PV Voltage (V)', color='#ff6b6b')
    ax3.plot(df['Time'], df['Batt_Voltage_V'], label='Battery Voltage (V)', color='#4ecdc4')
    ax3.set_xlabel('Time', color='white')
    ax3.set_ylabel('Voltage (V)', color='white')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    plt.tight_layout()
    plt.savefig(CHART_FILE, facecolor='black')
    plt.close()

if __name__ == "__main__":
    main()
