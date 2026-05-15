from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from chain_client import ChainClient
import config

print("Target Contract:", config.CONTRACT_ADDRESS)
chain = ChainClient()
chain.connect()
print("Starting records:", chain.get_data_count())
try:
    chain.store_data(
        pv_power=100.0,
        pv_voltage=30.0,
        batt_soc=80.0,
        batt_voltage=12.5,
        total_energy=10.0,
        signature="test_sig"
    )
    print("Store data call succeeded.")
    print("New records:", chain.get_data_count())
except Exception as e:
    print("Store data failed:", e)
finally:
    chain.disconnect()
