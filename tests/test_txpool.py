from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from chain_client import ChainClient
import config
c = ChainClient()
c.connect()
rpc = getattr(c, '_rpc_call')
print("Pending Tx Size:", rpc("getPendingTxSize", [config.GROUP_ID]))
c.disconnect()
