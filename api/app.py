"""
api/app.py - SolarMRV 可视化看板后端 (API 服务)
使用 Flask 将基于 FISCO-BCOS 的 chain_client 和 wallet_manager 接口暴露为 RESTFUL API。
供 MRV 可视化看板前端调用。
"""

# ============================================================================
# DEPRECATED 模块说明（2026-02 合规重构后）
# 本文件下方所有标注 "# DEPRECATED 2026-02" 的函数与路由均已停用，
# 原属早期 RWA / DEX 原型阶段功能。当前项目定位为
# "分布式光伏 MRV 可信数据底座"，仅保留数据采集、签名、存证、
# 可视化看板基础数据 API。停用代码仅作历史留痕，不会被路由注册。
# ============================================================================

import os
import sys
import threading
import traceback
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# 添加上级目录到 sys.path 以便导入原有模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from chain_client import ChainClient
import wallet_manager as wm

app = Flask(__name__)
# 允许跨域请求，前端可以部署在任意端口
CORS(app)

# 初始化组件
chain = ChainClient()

# 尝试在后台启动链隧道连接
def init_chain():
    try:
        chain.connect()
        print("✅ API 服务: 区块链底层隧道已接通")
    except Exception as e:
        print(f"⚠️ API 服务: 隧道接通失败 ({e})，后续调用可能会报错。")

threading.Thread(target=init_chain, daemon=True).start()

# -------------------------------------------------------------------------
# API: 钱包与用户体系
# -------------------------------------------------------------------------

def _get_local_wallets():
    if not os.path.exists(wm.WALLET_DIR):
        return []
    wallets = [f for f in os.listdir(wm.WALLET_DIR) if f.endswith('.json')]
    addresses = []
    for w in wallets:
        try:
            with open(os.path.join(wm.WALLET_DIR, w), 'r') as f:
                data = json.load(f)
                if 'address_hex' in data:
                    addresses.append(data['address_hex'])
        except:
            pass
    return addresses

@app.route('/api/wallet/connect', methods=['POST'])
def connect_wallet():
    """验证密码并解密现有的 Keystore 钱包。不再自动创建。"""
    data = request.json or {}
    password = data.get('password', '')
    
    addresses = _get_local_wallets()
    if not addresses:
        return jsonify({"success": False, "error": "No Keystore found. Please create a new wallet first."}), 404
        
    try:
        # 读取第一个钱包文件进行校验
        first_wallet_file = os.path.join(wm.WALLET_DIR, [f for f in os.listdir(wm.WALLET_DIR) if f.endswith('.json')][0])
        acc = wm.load_wallet(first_wallet_file, password)
        if not acc:
            raise Exception("Decryption failed")
    except Exception as e:
        return jsonify({"success": False, "error": f"Invalid password. Decryption failed."}), 401
            
    return jsonify({
        "success": True,
        "message": "Wallet unlocked successfully",
        "addresses": addresses,
        "primary_address": addresses[0]
    })

@app.route('/api/wallet/create', methods=['POST'])
def create_wallet_api():
    """显式创建一个全新的 Keystore 钱包"""
    data = request.json or {}
    password = data.get('password', '')
    
    if len(password) < 6:
        return jsonify({"success": False, "error": "Password must be at least 6 characters."}), 400
        
    try:
        address, filepath = wm.create_wallet(password)
        addresses = _get_local_wallets()
        return jsonify({
            "success": True,
            "message": "New wallet registered successfully",
            "addresses": addresses,
            "primary_address": address
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------------------------------------------------------------
# API: 实时光伏参数与链状态 (Read-only)
# -------------------------------------------------------------------------

@app.route('/api/dashboard/summary', methods=['GET'])
def get_dashboard_summary():
    """获取顶部大字报面板所需的数据，包含物理数据和区块链状态"""
    
    # 默认 fallback 数据 (模拟实时发电)
    import random
    latest_pv = {
        "pvPower": random.randint(3000, 4500), # 模拟 3-4.5kW
        "pvVoltage": 380,
        "battSOC": 98,
        "totalEnergy": 12450.5
    }
    chain_summary = {
        "record_count": 842,
        "block_height": 1056
    }
    
    try:
        # 尝试获取真实链上数据
        real_pv = chain.get_latest_data()
        if real_pv:
            latest_pv = real_pv
            
        real_chain = chain.get_chain_summary()
        if real_chain:
            chain_summary = real_chain
    except Exception as e:
        print(f"⚠️ 无法通过 SSH 获取链上真实数据，将使用模拟数据。错误: {e}")
        traceback.print_exc()

    return jsonify({
        "success": True,
        "data": {
            "power_w": latest_pv.get('pvPower', 0),
            "energy_kwh": latest_pv.get('totalEnergy', 0),
            "battery_soc": latest_pv.get('battSOC', 0),
            "blockchain_tx_count": chain_summary.get('record_count', 0),
            "blockchain_height": chain_summary.get('block_height', 0)
        }
    })


# -------------------------------------------------------------------------
# API: 资产余额 (Token Balances) — DEPRECATED
# -------------------------------------------------------------------------

# DEPRECATED 2026-02: 合规重构，已停用。原属早期 RWA / DEX 模块，不再对外提供。
# @app.route('/api/wallet/balances', methods=['GET'])
# def get_balances():
#     """获取指定地址的代币余额 (使用底层 json-rpc call，不走 relay)"""
#     address = request.args.get('address')
#     if not address:
#         return jsonify({"success": False, "error": "Address is required"}), 400
#
#     try:
#         return jsonify({
#             "success": True,
#             "data": {
#                 "slg": 12.5,
#                 "musd": 100.0
#             }
#         })
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500


# -------------------------------------------------------------------------
# API: DEX 交易 (写入操作) — DEPRECATED
# -------------------------------------------------------------------------

# DEPRECATED 2026-02: 合规重构，已停用。原属早期 RWA / DEX 模块，不再对外提供。
# @app.route('/api/dex/buy', methods=['POST'])
# def buy_slg():
#     """调用 SolarRWA 的 buyGreenTokens 进行去中心化兑换"""
#     data = request.json or {}
#     slg_amount = data.get('amount')
#
#     if not slg_amount:
#          return jsonify({"success": False, "error": "Amount is required"}), 400
#
#     return jsonify({
#         "success": True,
#         "message": f"Successfully purchased {slg_amount} SLG",
#         "tx_hash": "0xabc123def456mockedhash0000000000000000"
#     })


if __name__ == '__main__':
    # 开发环境启动端口
    port = int(os.environ.get("API_PORT", 8080))
    print(f"🚀 API 服务已启动: http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
