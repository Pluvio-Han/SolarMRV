from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from chain_client import ChainClient
c = ChainClient()
c.connect()
print(c.get_latest_data())
c.disconnect()
