from telegram_notify import TelegramNotifier
from chain_client import ChainClient
import os
from datetime import datetime

# 查找已有图表文件
EXISTING_CHARTS = [f for f in os.listdir('.') if f.startswith('solar_chart_') and f.endswith('.png')]
TARGET_FILE = EXISTING_CHARTS[-1] if EXISTING_CHARTS else None

def test_send_with_chain_stats():
    print("🚀 开始测试 Telegram 通知 (含完整链上状态)...\n")
    bot = TelegramNotifier()
    
    # 1. 获取完整链状态
    chain_info = ""
    try:
        print("🔗 连接区块链...")
        chain = ChainClient()
        chain.connect()
        
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
        
        print(f"✅ 链状态获取成功!")
        print(f"   区块高度: {cs.get('block_height')}")
        print(f"   记录数:   {cs.get('record_count')}")
        print(f"   节点数:   {cs.get('peer_count')} peers + 本机")
        
        chain.disconnect()
    except Exception as e:
        print(f"⚠️ 获取链状态失败: {e}")
        chain_info = "\n⛓️ 链状态: 获取失败\n"

    # 2. 构造完整测试消息
    current_time = datetime.now().strftime("%H:%M")
    caption = (
        f"⏱️ 监测报告 [测试] ({current_time})\n"
        f"➖➖➖➖➖➖➖➖\n"
        f"☀️ 当前功率: 123.45 W (模拟)\n"
        f"🔋 电池电量: 88 % (模拟)\n"
        f"📊 累计发电: 1.23 kWh (模拟)\n"
        f"{chain_info}"
        f"➖➖➖➖➖➖➖➖\n"
        f"📈 运行状态: 正常 ✅"
    )

    print(f"\n📩 准备发送消息:\n{'='*40}\n{caption}\n{'='*40}\n")

    # 3. 发送 (优先图片)
    if TARGET_FILE and os.path.exists(TARGET_FILE):
        print(f"📷 发送带图消息 ({TARGET_FILE})...")
        if bot.send_photo(TARGET_FILE, caption=caption):
            print("✅ 图片消息发送成功!")
        else:
            print("❌ 图片消息发送失败，尝试文本...")
            bot.send_message(caption)
    else:
        print("📝 发送纯文本消息...")
        if bot.send_message(caption):
            print("✅ 文本消息发送成功!")
        else:
            print("❌ 文本消息发送失败")

if __name__ == "__main__":
    test_send_with_chain_stats()
