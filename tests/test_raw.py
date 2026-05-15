from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from solar_monitor import SolarMonitor
m = SolarMonitor('/dev/null')
print(m.read_realtime_data())
