from gmssl import sm2, func
import argparse
import random
import math
from pymodbus.client import ModbusSerialClient
import time
import json
from datetime import datetime
import binascii

import config

class SolarMonitor:
    def __init__(self, port, baudrate=115200, slave_id=1, simulate=False):
        self.port = port
        self.baudrate = baudrate
        self.slave_id = slave_id
        self.simulate = simulate
        
        # 从 config 获取密钥 (支持环境变量)
        self.private_key = config.SM2_PRIVATE_KEY
        self.public_key = config.SM2_PUBLIC_KEY
        
        # 初始化加解密对象
        self.sm2_crypt = sm2.CryptSM2(public_key=self.public_key, private_key=self.private_key)
        
        if not self.simulate:
            self.client = ModbusSerialClient(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1
            )
        else:
            print("⚠️ 运行在模拟模式 (Simulation Mode)")

    def connect(self):
        """连接到串口"""
        if self.simulate:
            print("🔌 [模拟] 串口连接成功")
            return True
            
        print(f"🔌 正在连接端口: {self.port} ...")
        if self.client.connect():
            print("✅ 串口连接成功")
            return True
        else:
            print("❌ 串口连接失败")
            return False

    def disconnect(self):
        """断开连接"""
        if not self.simulate:
            self.client.close()
        print("🔌 连接已关闭")

    def _read_register(self, address, scale=100.0, count=1):
        """读取寄存器并应用缩放因子"""
        if self.simulate:
            return 0  # 模拟模式下不调用真实硬件
            
        try:
            result = self.client.read_input_registers(address, count=count, slave=self.slave_id)
            if result.isError():
                print(f"⚠️ 读取地址 {hex(address)} 失败: {result}")
                return None
            
            if count == 1:
                return result.registers[0] / scale
            elif count == 2:
                # 32位数据：低位在前，高位在后 (L, H)
                low = result.registers[0]
                high = result.registers[1]
                value = (high << 16) | low
                return value / scale
        except Exception as e:
            print(f"💥 读取异常: {e}")
            return None

    def _simulate_pv_data(self):
        """模拟光伏数据 (基于时间生成正弦波曲线)"""
        now = datetime.now()
        hour = now.hour + now.minute / 60.0
        
        # 简单模拟：早6点到晚6点有光照
        if 6 <= hour <= 18:
            # 正弦波模拟光照强度 (0 到 1)
            intensity = math.sin((hour - 6) * math.pi / 12)
            pv_voltage = 30.0 + random.uniform(-1, 1) # 30V 左右浮动
            pv_power = 200.0 * intensity + random.uniform(-5, 5)
            pv_current = pv_power / pv_voltage if pv_voltage > 0 else 0
            
            # 累积发电量 (简单模拟，每次增加一点)
            total_energy = (hour - 6) * 0.1 
        else:
            pv_voltage = 0.0
            pv_current = 0.0
            pv_power = 0.0
            total_energy = 1.2 # 假设白天发了1.2度电
            
        return {
            'pv_voltage': round(pv_voltage, 2),
            'pv_current': round(pv_current, 2),
            'pv_power': round(pv_power, 2),
            'batt_voltage': 13.2 + random.uniform(-0.1, 0.1),
            'batt_current': round(pv_current * 2.5, 2), # 假设MPPT效率和电压变换
            'batt_soc': 80 + random.uniform(-1, 1),
            'total_energy_generated': round(total_energy, 2)
        }

    def read_realtime_data(self):
        """读取实时光伏数据"""
        if self.simulate:
            data = self._simulate_pv_data()
        else:
            data = {}
            # --- PV 阵列数据 ---
            data['pv_voltage'] = self._read_register(0x3100)
            data['pv_current'] = self._read_register(0x3101)
            data['pv_power'] = self._read_register(0x3102, count=2)

            # --- 电池数据 ---
            data['batt_voltage'] = self._read_register(0x3104)
            data['batt_current'] = self._read_register(0x3105)
            data['batt_soc'] = self._read_register(0x311A, scale=1.0)
            
            # --- 统计数据 ---
            data['total_energy_generated'] = self._read_register(0x3312, scale=100.0, count=2)
        
        # 添加时间戳
        data['timestamp'] = datetime.now().isoformat()
        
        # 过滤掉 None 值
        return {k: v for k, v in data.items() if v is not None}

    def set_load_state(self, state: bool):
        """控制负载开关 (True=ON, False=OFF)"""
        if self.simulate:
            print(f"💡 [模拟] 负载已{'开启' if state else '关闭'}")
            return True
            
        try:
            # EPEVER 负载控制 Coil 0x0002
            result = self.client.write_coil(0x0002, state, slave=self.slave_id)
            if result.isError():
                print(f"❌ 设置负载失败: {result}")
                return False
            else:
                print(f"✅ 负载已{'开启' if state else '关闭'}")
                return True
        except Exception as e:
            print(f"💥 设置负载异常: {e}")
            return False

    def sign_payload(self, payload):
        """对 Payload 生成数字签名 (SM2)"""
        # 将 payload 排序并转换为字节串
        canonical_json = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')
        
        # SM2 签名 (默认使用 SM3 作为摘要算法)
        # sign_with_sm3 需要传入 bytes 这一步库会自动做 hash
        signature = self.sm2_crypt.sign_with_sm3(canonical_json, func.random_hex(16))
        return signature

    def get_mrv_payload(self):
        """生成符合 MRV 链上存证格式的 JSON Payload（中文键名）

        MRV = Monitoring–Reporting–Verification（监测—报告—核查）
        本方法输出经国密 SM2 签名的设备发电数据包，作为后续减排量核算与第三方核查的可信底层证据。
        """
        raw_data = self.read_realtime_data()
        if not raw_data:
            return None

        # 1. 核心运行数据（中文键名，便于核查方人工核对）
        device_data = {
            "累计发电量_千瓦时": raw_data.get('total_energy_generated', 0),
            "当前功率_瓦": raw_data.get('pv_power', 0),
            "当前电流_安": raw_data.get('pv_current', 0.0),
            "光伏电压_伏": raw_data.get('pv_voltage', 0),
            "电池电量_百分比": raw_data.get('batt_soc', 0),
            "电池电压_伏": raw_data.get('batt_voltage', 0.0)
        }

        # 2. 构造基础 Payload
        payload = {
            "设备ID": "SOLAR_NODE_001",
            "时间戳": raw_data.get('timestamp'),
            "运行数据": device_data,
            "状态": "运行中" if raw_data.get('pv_voltage', 0) > 5 else "待机"
        }

        # 3. 生成 SM2 签名并附加
        signature = self.sign_payload(payload)
        payload['SM2数字签名'] = signature
        payload['设备公钥'] = self.public_key

        return json.dumps(payload, indent=2, ensure_ascii=False)

    # 兼容旧调用名：转发至 get_mrv_payload，等下一次大改时移除
    def get_rwa_payload(self):  # noqa: D401 — DEPRECATED 别名
        """DEPRECATED 2026-02：早期命名，请使用 get_mrv_payload()。"""
        return self.get_mrv_payload()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SolarMRV - 分布式光伏 MRV 数据采集与签名工具')
    parser.add_argument('--simulate', action='store_true', help='开启模拟模式')
    parser.add_argument('--load-on', action='store_true', help='开启负载 (灯泡)')
    parser.add_argument('--load-off', action='store_true', help='关闭负载 (灯泡)')
    args = parser.parse_args()

    # 使用之前确认的端口
    PORT = '/dev/tty.usbmodem59810539351'
    monitor = SolarMonitor(port=PORT, simulate=args.simulate)
    
    if monitor.connect():
        try:
            # 优先处理负载控制命令
            if args.load_on:
                print("\n💡 收到[开启负载]指令...")
                monitor.set_load_state(True)
                # 操作完这步就等待一会，不必每次都运行监控
            elif args.load_off:
                print("\n🌑 收到[关闭负载]指令...")
                monitor.set_load_state(False)
            else:
                # 默认监控逻辑
                print("\n正在读取数据 ...")
                # 连续读取 3 次测试稳定性
                for i in range(3):
                    print(f"\n--- 第 {i+1} 次读取 ---")
                    json_data = monitor.get_mrv_payload()
                    print(json_data)
                    time.sleep(2)
        finally:
            monitor.disconnect()
