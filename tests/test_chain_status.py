from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json, time
from chain_client import ChainClient
c = ChainClient()
c.connect()
for i in range(3):
    print("--- Chain Status ---")
    print(json.dumps(c.get_chain_summary(), indent=2))
    time.sleep(2)
c.disconnect()
