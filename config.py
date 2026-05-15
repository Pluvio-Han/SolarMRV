"""
config.py - 光伏监控系统统一配置
管理环境变量、敏感密钥、硬件参数及区块链设置
"""
import os
from datetime import datetime

# ============================================================
#                    系统环境与路径
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHART_DIR = os.path.join(BASE_DIR, "charts")

# 确保目录存在
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
if not os.path.exists(CHART_DIR):
    os.makedirs(CHART_DIR)

# 生成带日期的文件名
TODAY_STR = datetime.now().strftime("%Y%m%d_%H%M")
CSV_FILE = os.path.join(DATA_DIR, f"solar_data_{TODAY_STR}.csv")
CHART_FILE = os.path.join(CHART_DIR, f"solar_chart_{TODAY_STR}.png")

# ============================================================
#                    硬件与监控参数
# ============================================================
MONITOR_PORT = os.environ.get("SOLAR_PORT", "/dev/tty.usbmodem59810539351")
MONITOR_BAUDRATE = 115200
MONITOR_SLAVE_ID = 1

# 自动运行配置
DURATION_HOURS = 8
INTERVAL_MINUTES = 5

# ============================================================
#                    敏感密钥 (优先环境变量)
# ============================================================
# Telegram Bot
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8455087751:AAEycX3BEurx2oiBaVKFKmbZndNRxb1heBU")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8425455901")

# SM2 密钥对 (测试用固定密钥，生产环境请务必通过环境变量注入)
SM2_PRIVATE_KEY = os.environ.get("SM2_PRIVATE_KEY", "00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5")
SM2_PUBLIC_KEY = os.environ.get("SM2_PUBLIC_KEY", "B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E2465E99E")

# ============================================================
#                    区块链配置
# ============================================================
GWEN_HOST = os.environ.get("CHAIN_HOST", "1.12.43.152")
GWEN_SSH_USER = os.environ.get("CHAIN_USER", "ubuntu")
GWEN_RPC_PORT = 8545
GWEN_RELAY_PORT = 5555

# 旧版纯数据上链合约 (SolarDataStore)
CONTRACT_ADDRESS = os.environ.get("CHAIN_CONTRACT", "0x075d963d8567395f024da3edce3d63bd2f5f4be3")

# Phase 2 资产化代币合约 — DEPRECATED 2026-02: 合规重构停用
# SOLAR_TOKEN_ADDR = os.environ.get("SOLAR_TOKEN_ADDR", "0x5644c316cca1fda89640ce576613b9f6044e5d48")    # DEPRECATED 2026-02: 合规重构停用
# STABLE_COIN_ADDR = os.environ.get("STABLE_COIN_ADDR", "0x3709d04c3a05b15cceb32d6c0ae251e5c99a2f33")    # DEPRECATED 2026-02: 合规重构停用
# SOLAR_RWA_ADDR = os.environ.get("SOLAR_RWA_ADDR", "0x6b48181d6edeeccbc1143f276f5e60cdd90421b8")          # DEPRECATED 2026-02: 合规重构停用

GROUP_ID = 1
SENDER_ADDRESS = "0x4a8d475c38c355734dcb786cd9be43773939b793"
