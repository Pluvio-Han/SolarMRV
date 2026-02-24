"""
wallet_manager.py - 用户本地钱包管理工具
用于生成和加载以太坊/FISCO-BCOS兼容的 ECDSA 钱包 (secp256k1)
并将私钥加密保存为安全的 Keystore 格式。
"""
from eth_account import Account
import secrets
import json
import os

# 本地保存钱包的目录
WALLET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'wallets')

def create_wallet(password: str, filename: str = "user_wallet.json") -> tuple:
    """
    生成一个新的 ECDSA 钱包，并使用密码加密保存为 Keystore 格式
    :param password: 解锁密码
    :param filename: 钱包文件名
    :return: (address, filepath)
    """
    if not os.path.exists(WALLET_DIR):
        os.makedirs(WALLET_DIR)
        
    # 生成 32 字节高强度随机数作为私钥
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    
    # 从私钥派发 ECDSA 账户
    account = Account.from_key(private_key)
    address = account.address
    
    # 将私钥通过用户的密码加密，生成标准 EIP-1559 格式的 Keystore (V3 JSON)
    encrypted_keystore = Account.encrypt(private_key, password)
    
    # 添加一个方便肉眼识别的地址字段
    encrypted_keystore['address_hex'] = address
    
    filepath = os.path.join(WALLET_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(encrypted_keystore, f, indent=4)
        
    print(f"✅ 钱包已安全生成！")
    print(f"  🔑 钱包地址: {address}")
    print(f"  🔒 存储路径: {filepath}")
    
    return address, filepath

def load_wallet(filepath: str, password: str):
    """
    从 Keystore 文件加载钱包私钥
    :param filepath: 钱包文件路径
    :param password: 解锁密码
    :return: Account 对象
    """
    if not os.path.exists(filepath):
        print(f"❌ 钱包文件不存在: {filepath}")
        return None
        
    with open(filepath, 'r') as f:
        encrypted_keystore = json.load(f)
    
    try:
        # 尝试解密
        private_key = Account.decrypt(encrypted_keystore, password)
        account = Account.from_key(private_key)
        return account
    except ValueError:
        print(f"❌ 密码错误，无法解密钱包！")
        return None
    except Exception as e:
        print(f"❌ 读取钱包发生未知错误: {e}")
        return None

if __name__ == "__main__":
    print("="*50)
    print("🚀 光伏系统 - 资产账户生成器")
    print("="*50)
    
    # 生成用户的首个本地冷钱包
    default_password = "Solar_password_123!" # 测试密码，实际应用应让用户输入
    
    # 如果已存在，则不再覆盖
    default_wallet_path = os.path.join(WALLET_DIR, "user_wallet.json")
    if os.path.exists(default_wallet_path):
        print(f"⚠️ 发现现有钱包: {default_wallet_path}")
        print("正在校验密码...")
        acc = load_wallet(default_wallet_path, default_password)
        if acc:
            print(f"✅ 钱包验证通过，地址: {acc.address}")
    else:
        print("正在为您创建专属加密钱包...")
        addr, path = create_wallet(default_password, "user_wallet.json")
        print(f"\n⚠️ 请妥善保管您的密码: {default_password}")
        
    print("="*50)
