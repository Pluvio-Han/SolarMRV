from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import time
from chain_client import ChainClient
c = ChainClient()
c.connect()
print("Connected")
pv_power = 3.24
pv_voltage = 15.14
batt_soc = 87.0
batt_voltage = 13.52
total_energy = 0.06
sig = "de83402113b7aa757cb31aec2d25a394256018c7281d2a7e91ef5cb47d0333e164c74cdd78ce2059b17bbe0b052fc67a6a6a267a99261202f23f8839e8b2782b"
# Test long string
try:
    tx = c.store_data(
        pv_power=pv_power,
        pv_voltage=pv_voltage,
        batt_soc=batt_soc,
        batt_voltage=batt_voltage,
        total_energy=total_energy,
        signature=sig
    )
    print("Success:", tx)
except Exception as e:
    print("Failed:", e)
finally:
    c.disconnect()
