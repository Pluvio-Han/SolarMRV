from pymodbus.client import ModbusSerialClient
import time

# --- 核心配置 ---
# 这里的端口号就是从你截图里找到的那个
PORT_NAME = '/dev/tty.usbmodem59810539351' 

def read_data():
    print(f"🔌 正在连接端口: {PORT_NAME} ...")
    
    # EPEVER 默认参数: 波特率 115200
    client = ModbusSerialClient(
        port=PORT_NAME,
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=1
    )

    if not client.connect():
        print("❌ 无法打开串口，请检查：")
        print("1. 线插紧了吗？")
        print("2. 端口号变了吗？")
        return

    try:
        print("✅ 串口打开成功！正在请求数据...")
        
        # 读取电池电压 (寄存器地址 0x3104)
        # slave=1 是控制器的默认 ID
        # read_input_registers 是读取只读数据
        result = client.read_input_registers(0x3104, count=1, slave=1)
        
        if result.isError():
            print(f"❌ 读取失败: {result}")
            print("可能原因：")
            print("- 控制器没设成 'S' 模式 (请检查屏幕是否显示 '5')")
            print("- 电池没电了")
        else:
            # EPEVER 的电压数据通常要除以 100
            voltage = result.registers[0] / 100.0
            print("-" * 30)
            print(f"🎉 成功读取硬件数据！")
            print(f"🔋 电池电压: {voltage} V")
            print("-" * 30)

    except Exception as e:
        print(f"💥 程序发生异常: {e}")
    finally:
        client.close()
        print("连接已关闭。")

if __name__ == "__main__":
    read_data()