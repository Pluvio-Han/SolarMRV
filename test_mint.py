"""
test_mint.py - 测试预言机自动铸币 (Mint Token) 功能
用于验证 Python 客户端调用 SolarRWA 合约发放 SLG 绿电积分的能力
"""
import time
from chain_client import ChainClient

def main():
    client = ChainClient()
    try:
        client.connect()
        print("\n✅ 区块链双路隧道连接成功 (JSON-RPC + Relay)")
        
        device_id = "NODE_001"
        # 模拟产生 1.25 kWh 的累计电量 (假设之前是 0，那么将增发 1.25 个 Token)
        mock_energy = 1.25
        
        print(f"\n🚀 正在触发预言机：向设备 {device_id} 报告累计电量 {mock_energy} kWh...")
        
        success, tx = client.mint_token(device_id, mock_energy)
        
        if success:
            print("\n🎉 预言机执行成功！")
            print(f"📦 交易哈希: {tx}")
        else:
            print("\n❌ 预言机执行失败！")
            
    except Exception as e:
        print(f"发生异常: {e}")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
