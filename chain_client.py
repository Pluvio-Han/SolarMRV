"""
chain_client.py - FISCO-BCOS 链客户端
用于从 Mac 端连接 Gwen 服务器，调用 SolarDataStore 智能合约

写入: 通过 SSH 调用 Gwen 上的控制台命令 (可靠、已验证)
读取: 通过 SSH 隧道 + JSON-RPC (快速、轻量)
"""

# ============================================================================
# DEPRECATED 模块说明（2026-02 合规重构后）
# 本文件下方所有标注 "# DEPRECATED 2026-02" 的函数均已停用，
# 原属早期 RWA / DEX 原型阶段功能（如 mint_token 等调用 SolarRWA 合约的操作）。
# 当前项目定位为"分布式光伏 MRV 可信数据底座"，仅保留 SolarDataStore 合约
# 相关的数据存证与链上查询功能。停用代码仅作历史留痕。
# ============================================================================
import json
import os
import time
import socket
import subprocess
import requests
from eth_abi import decode
from eth_utils import keccak

import config

# ============================================================
#                    配置信息 (从 config.py 读取)
# ============================================================

GWEN_HOST = config.GWEN_HOST
GWEN_SSH_USER = config.GWEN_SSH_USER
GWEN_RPC_PORT = config.GWEN_RPC_PORT
CONTRACT_ADDRESS = config.CONTRACT_ADDRESS
GROUP_ID = config.GROUP_ID
SENDER = config.SENDER_ADDRESS
CONSOLE_PATH = "~/fisco/console"


def _find_free_port():
    """找到一个可用的本地端口"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


class ChainClient:
    """FISCO-BCOS 链客户端 (双通道: JSON-RPC读 + Relay写)"""

    def __init__(self):
        self.tunnel_proc = None
        self.rpc_port = None
        self.relay_port = None

    def connect(self):
        """建立双路 SSH 隧道 (JSON-RPC + Relay)"""
        self.rpc_port = _find_free_port()
        self.relay_port = _find_free_port()
        
        print(f"🔗 正在建立双路 SSH 隧道...")
        print(f"   - JSON-RPC (读): 127.0.0.1:{self.rpc_port} -> {GWEN_HOST}:{GWEN_RPC_PORT}")
        print(f"   - Relay    (写): 127.0.0.1:{self.relay_port} -> {GWEN_HOST}:{config.GWEN_RELAY_PORT}")

        self.tunnel_proc = subprocess.Popen(
            [
                "ssh", "-N", 
                "-L", f"{self.rpc_port}:127.0.0.1:{GWEN_RPC_PORT}",
                "-L", f"{self.relay_port}:127.0.0.1:{config.GWEN_RELAY_PORT}",
                f"{GWEN_SSH_USER}@{GWEN_HOST}",
                "-o", "StrictHostKeyChecking=no",
                "-o", "ServerAliveInterval=30"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        for i in range(40):
            time.sleep(0.5)
            if self._check_port(self.rpc_port) and self._check_port(self.relay_port):
                print("✅ 双路隧道已建立")
                return
        raise ConnectionError("❌ SSH 隧道建立超时")

    def _check_port(self, port):
        try:
            s = socket.create_connection(("127.0.0.1", port), timeout=0.5)
            s.close()
            return True
        except (ConnectionRefusedError, OSError):
            return False

    def disconnect(self):
        """关闭 SSH 隧道"""
        if self.tunnel_proc:
            self.tunnel_proc.terminate()
            self.tunnel_proc.wait()
            print("🔌 SSH 隧道已关闭")

    @property
    def rpc_url(self):
        return f"http://127.0.0.1:{self.rpc_port}"

    @property
    def relay_url(self):
        return f"http://127.0.0.1:{self.relay_port}"

    def _rpc_call(self, method, params):
        """JSON-RPC 请求 (读取)"""
        try:
            payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
            resp = requests.post(self.rpc_url, json=payload, timeout=5, 
                                 proxies={"http": None, "https": None})
            result = resp.json()
            if "error" in result:
                raise Exception(f"RPC Error: {result['error']}")
            return result.get("result")
        except Exception as e:
            raise Exception(f"RPC 通信失败: {e}")

    def _get_selector(self, func_name, param_types):
        sig = f"{func_name}({','.join(param_types)})"
        return keccak(text=sig)[:4]

    # ============================================================
    #                    写入函数 (通过 Relay Service)
    # ============================================================

    def _reconnect_tunnel(self):
        """重新建立 SSH 隧道"""
        print("🔄 正在重连 SSH 隧道...")
        self.disconnect()
        time.sleep(1)
        try:
            self.connect()
            print("✅ SSH 隧道重连成功")
            return True
        except Exception as e:
            print(f"❌ SSH 隧道重连失败: {e}")
            return False

    def store_data(self, pv_power, pv_voltage, batt_soc, batt_voltage, total_energy, signature):
        """
        通过 Relay 服务快速上链 (含重试 & 自动重连)
        """
        # 放大 100 倍
        payload = {
            "action": "store_data",
            "pvPower": int(pv_power * 100),
            "pvVoltage": int(pv_voltage * 100),
            "battSOC": int(batt_soc),
            "battVoltage": int(batt_voltage * 100),
            "totalEnergy": int(total_energy * 100),
            "signature": signature
        }
        
        last_error = None
        for attempt in range(3):
            try:
                # 检查隧道端口是否通畅
                if not self._check_port(self.relay_port):
                    print("⚠️ 检测到隧道断开，尝试重连...")
                    if not self._reconnect_tunnel():
                        raise ConnectionError("隧道重连失败")

                resp = requests.post(self.relay_url, json=payload, timeout=45,
                                     proxies={"http": None, "https": None})
                result = resp.json()
                
                if result.get("success"):
                    tx_hash = result.get("tx_hash", "unknown")
                    print(f"⛓️  数据已上链! TX: {tx_hash[:18]}... (Relay)")
                    return tx_hash
                else:
                    output_str = result.get('output', '')
                    if "Transaction receipt timeout" in output_str:
                        print("   ⏳ 控制台返回超时，正在交叉验证链上记录...")
                        # 轮询 3 次，每次等待 3 秒
                        for _ in range(3):
                            time.sleep(3)
                            latest = self.get_latest_data()
                            if latest and latest.get("signature") == signature:
                                print(f"⛓️  数据已确认上链 (延时)! 链上ID: {latest.get('id')} (Relay)")
                                return f"delayed_tx_{latest.get('id')}"
                    
                    last_error = f"Relay Error: {result.get('error')} | Output: {output_str[:100]}"
                    if attempt < 2:
                        print(f"  ⚠️ 第{attempt+1}次尝试失败，{3}秒后重试...")
                        time.sleep(3)
                    
            except (requests.exceptions.RequestException, ConnectionError) as e:
                last_error = f"Relay 连接失败: {e}"
                if attempt < 2:
                    print(f"  ⚠️ 连接异常，尝试重连隧道并重试...")
                    self._reconnect_tunnel()
                    time.sleep(3)
        
        raise Exception(last_error)

    # DEPRECATED 2026-02: 合规重构，已停用。原属早期 RWA / DEX 模块，不再对外提供。
    # def mint_token(self, device_id, total_energy):
    #     """
    #     向 SolarRWA 合约报告最新累计发电量，如果存在增量则由 RWA 合约自动结算并铸造绿电代币给用户。
    #     :param device_id: 设备唯一ID (例如 NODE_001)
    #     :param total_energy: 当前累计发电量 (Float, 比如 1.25 kWh)
    #     :return: 布尔值 (是否成功), TX Hash
    #     """
    #     payload = {
    #         "action": "mint_token",
    #         "contractAddr": config.SOLAR_RWA_ADDR,
    #         "deviceId": device_id,
    #         "totalEnergy": int(total_energy * 100)
    #     }
    #
    #     last_error = None
    #     for attempt in range(3):
    #         try:
    #             if not self._check_port(self.relay_port):
    #                 print("⚠️ 检测到隧道断开，尝试重连...")
    #                 if not self._reconnect_tunnel():
    #                     raise ConnectionError("隧道重连失败")
    #
    #             resp = requests.post(self.relay_url, json=payload, timeout=45,
    #                                  proxies={"http": None, "https": None})
    #             result = resp.json()
    #
    #             if result.get("success"):
    #                 tx_hash = result.get("tx_hash", "unknown")
    #                 print(f"💰  绿电铸币成功! TX: {tx_hash[:18]}... (Relay)")
    #                 return True, tx_hash
    #             else:
    #                 output_str = result.get('output', '')
    #                 if "Transaction receipt timeout" in output_str:
    #                     return True, "delayed_minting_tx"
    #
    #                 last_error = f"Mint Error: {result.get('error')} | Output: {output_str[:100]}"
    #                 if attempt < 2:
    #                     print(f"  ⚠️ 第{attempt+1}次尝试失败，{3}秒后重试...")
    #                     time.sleep(3)
    #
    #         except (requests.exceptions.RequestException, ConnectionError) as e:
    #             last_error = f"Relay 连接失败: {e}"
    #             if attempt < 2:
    #                 print(f"  ⚠️ 连接异常，尝试重连隧道并重试...")
    #                 self._reconnect_tunnel()
    #                 time.sleep(3)
    #
    #     print(f"❌ 绿电铸币失败: {last_error}")
    #     return False, None

    # ============================================================
    #                    读取函数 (通过 JSON-RPC)
    # ============================================================

    def get_block_number(self):
        """获取当前区块高度"""
        result = self._rpc_call("getBlockNumber", [GROUP_ID])
        return int(result, 16)

    def get_data_count(self):
        """获取链上记录总数"""
        selector = self._get_selector("getDataCount", [])
        data = "0x" + selector.hex()
        result = self._rpc_call("call", [
            GROUP_ID, {"from": SENDER, "to": CONTRACT_ADDRESS, "data": data}
        ])
        output = result.get("output", "0x")
        if output and output != "0x":
            return decode(["uint256"], bytes.fromhex(output[2:]))[0]
        return 0

    def get_latest_data(self):
        """获取最新一条链上数据"""
        selector = self._get_selector("getLatestData", [])
        data = "0x" + selector.hex()
        result = self._rpc_call("call", [
            GROUP_ID, {"from": SENDER, "to": CONTRACT_ADDRESS, "data": data}
        ])
        output = result.get("output", "0x")
        if output and output != "0x":
            d = decode(
                ["uint256", "uint256", "uint256", "uint256",
                 "uint256", "uint256", "uint256", "string", "address"],
                bytes.fromhex(output[2:])
            )
            return {
                "id": d[0], "timestamp": d[1],
                "pvPower": d[2] / 100.0, "pvVoltage": d[3] / 100.0,
                "battSOC": d[4], "battVoltage": d[5] / 100.0,
                "totalEnergy": d[6] / 100.0,
                "signature": d[7], "uploader": d[8]
            }
        return None

    def get_peers(self):
        """获取连接的节点数"""
        result = self._rpc_call("getPeers", [GROUP_ID])
        return len(result) if isinstance(result, list) else 0

    def get_consensus_status(self):
        """获取共识状态 (PBFT view, 共识节点数)"""
        try:
            result = self._rpc_call("getConsensusStatus", [GROUP_ID])
            if isinstance(result, list) and len(result) > 0:
                base = result[0]
                # FISCO-BCOS 用 sealer.0, sealer.1 ... 格式
                sealer_count = sum(1 for k in base if k.startswith("sealer."))
                return {
                    "node_count": sealer_count,
                    "view": base.get("currentView", base.get("toView", "N/A")),
                }
            return {"node_count": 0, "view": "N/A"}
        except Exception as e:
            # P1: 修复裸 except
            print(f"⚠️ 获取共识状态失败: {e}")
            return {"node_count": 0, "view": "N/A"}

    def get_sync_status(self):
        """获取同步状态"""
        try:
            result = self._rpc_call("getSyncStatus", [GROUP_ID])
            if isinstance(result, dict):
                peers = result.get("peers", [])
                peer_info = []
                for p in peers:
                    peer_info.append({
                        "node_id": p.get("nodeId", "")[:8] + "...",
                        "height": int(p.get("blockNumber", "0x0"), 16) if isinstance(p.get("blockNumber"), str) else p.get("blockNumber", 0),
                    })
                return {
                    "is_syncing": result.get("isSyncing", False),
                    "current_height": int(result.get("blockNumber", "0x0"), 16) if isinstance(result.get("blockNumber"), str) else result.get("blockNumber", 0),
                    "peers": peer_info,
                }
            return {"is_syncing": False, "current_height": 0, "peers": []}
        except Exception as e:
            # P1: 修复裸 except
            print(f"⚠️ 获取同步状态失败: {e}")
            return {"is_syncing": False, "current_height": 0, "peers": []}

    def get_chain_summary(self):
        """
        获取完整链状态摘要 (用于 Telegram 通知)
        返回字典包含: block_height, record_count, peer_count, consensus, sync_status
        """
        summary = {}
        
        try:
            summary["block_height"] = self.get_block_number()
        except Exception:
            summary["block_height"] = "N/A"
        
        try:
            summary["record_count"] = self.get_data_count()
        except Exception:
            summary["record_count"] = "N/A"
        
        try:
            summary["peer_count"] = self.get_peers()
        except Exception:
            summary["peer_count"] = "N/A"
        
        try:
            summary["consensus"] = self.get_consensus_status()
        except Exception:
            summary["consensus"] = {"node_count": 0, "view": "N/A"}
        
        try:
            summary["sync"] = self.get_sync_status()
        except Exception:
            summary["sync"] = {"is_syncing": False, "current_height": 0, "peers": []}
        
        return summary


# ============================================================
#                    测试入口
# ============================================================
if __name__ == "__main__":
    client = ChainClient()
    try:
        client.connect()

        # 1. 查询链状态
        block_num = client.get_block_number()
        peers = client.get_peers()
        count = client.get_data_count()
        print(f"📦 当前区块高度: {block_num}")
        print(f"🌐 连接节点数:   {peers}")
        print(f"📊 链上记录数:   {count}")

        # 2. 存入测试数据
        print("\n🔄 正在上链测试数据...")
        tx_hash = client.store_data(
            pv_power=5.65,
            pv_voltage=18.39,
            batt_soc=96,
            batt_voltage=13.80,
            total_energy=0.06,
            signature="test_from_python_sdk"
        )

        # 3. 验证
        count = client.get_data_count()
        print(f"📊 上链后记录数: {count}")

        latest = client.get_latest_data()
        if latest:
            print(f"\n📋 最新链上数据:")
            print(f"   ID:       {latest['id']}")
            print(f"   功率:     {latest['pvPower']} W")
            print(f"   电压:     {latest['pvVoltage']} V")
            print(f"   SOC:      {latest['battSOC']} %")
            print(f"   电池电压: {latest['battVoltage']} V")
            print(f"   累计发电: {latest['totalEnergy']} kWh")
            print(f"   签名:     {latest['signature']}")
    finally:
        client.disconnect()
