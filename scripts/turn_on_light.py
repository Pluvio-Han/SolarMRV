from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from solar_monitor import SolarMonitor
import config
import time

print("正在连接设备并点亮灯泡...")
try:
    monitor = SolarMonitor(config.MONITOR_PORT)
    if monitor.connect():
        monitor.set_load_state(True)
        print("✅ 灯泡已开启，准备开始监测。")
        time.sleep(1) # 给继电器一些响应时间
        monitor.disconnect()
    else:
        print("❌ 设备连接失败，请检查串口占用。")
except Exception as e:
    print(f"❌ 发生异常: {e}")
