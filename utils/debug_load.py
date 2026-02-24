from pymodbus.client import ModbusSerialClient
import time

# 配置串口
PORT_NAME = '/dev/tty.usbmodem59810539351'

def debug_load():
    client = ModbusSerialClient(
        port=PORT_NAME,
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=1
    )

    if not client.connect():
        print("❌ 无法连接串口")
        return

    try:
        print("🔌 连接成功，正在诊断负载状态...")
        
        # 1. 读取电池电压 (0x3104)
        result_batt = client.read_input_registers(0x3104, count=1, slave=1)
        if not result_batt.isError():
            batt_v = result_batt.registers[0] / 100.0
            print(f"🔋 电池电压: {batt_v} V")
            if batt_v < 11.1:
                print("⚠️ 警告: 电池电压过低！负载可能被低压保护切断。")
        
        # 2. 读取光伏电压 (0x3100)
        result_pv = client.read_input_registers(0x3100, count=1, slave=1)
        if not result_pv.isError():
            pv_v = result_pv.registers[0] / 100.0
            print(f"☀️ 光伏电压: {pv_v} V")

        # 3. 读取负载状态 (0x3202 - 负载状态位)
        # EPEVER Load Status: D0=1 (Over Voltage), D1=1 (Short Circuit), ... 
        # 但我们要看 Coil 0x0002 (Manual Control)
        
        # 尝试强制开启负载 (写线圈 0x0002)
        print("\n💡 正在尝试强制开启负载...")
        # 注意:有些型号写 Coil 2，有些是 Register 9008
        # EPEVER 通常支持通过 Coil 0x0002 控制负载开关 (Manual Mode)
        
        # 写 True (ON)
        write_result = client.write_coil(0x0002, True, slave=1)
        if write_result.isError():
            print(f"❌ 开启负载失败: {write_result}")
            print("尝试方法 2: 写入寄存器...")
        else:
            print("✅ 指令已发送: 负载开启 (ON)")
            
        time.sleep(2)
        
        # 4. 再次读取负载电流/功率
        result_load = client.read_input_registers(0x310C, count=4, slave=1)
        if not result_load.isError():
            l_vol = result_load.registers[0] / 100.0
            l_cur = result_load.registers[1] / 100.0
            l_pow = (result_load.registers[2] | (result_load.registers[3] << 16)) / 100.0
            print(f"\n💡 负载状态:")
            print(f"   电压: {l_vol} V")
            print(f"   电流: {l_cur} A")
            print(f"   功率: {l_pow} W")
            
            if l_cur > 0:
                print("🎉 负载工作正常！灯应该亮了。")
            else:
                print("⚠️ 负载似乎没有电流，请检查灯泡接线。")

    except Exception as e:
        print(f"💥 异常: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    debug_load()
