from solar_monitor import SolarMonitor
m = SolarMonitor('/dev/null')
raw = {'pv_power': 10}
sig = m.sign_payload(raw)
print(type(sig))
print(sig)
from chain_client import ChainClient
c = ChainClient()
c.connect()
print(c.store_data(
    pv_power=raw.get('pv_power', 0),
    pv_voltage=0,
    batt_soc=0,
    batt_voltage=0,
    total_energy=0,
    signature=sig
))
c.disconnect()
