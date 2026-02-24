import sys
import json
from solar_monitor import SolarMonitor
m = SolarMonitor('/dev/tty.usbmodem59810539351')
m.connect()
raw = m.read_realtime_data()
if raw:
    sig = m.sign_payload(raw)
    payload = {
        "action": "store_data",
        "pvPower": int(raw.get('pv_power', 0) * 100),
        "pvVoltage": int(raw.get('pv_voltage', 0) * 100),
        "battSOC": int(raw.get('batt_soc', 0)),
        "battVoltage": int(raw.get('batt_voltage', 0) * 100),
        "totalEnergy": int(raw.get('total_energy_generated', 0) * 100),
        "signature": sig
    }
    print("PAYLOAD:", json.dumps(payload))
m.disconnect()
