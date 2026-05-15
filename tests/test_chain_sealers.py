from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from chain_client import ChainClient
import config
c = ChainClient()
c.connect()
print("Sealers:", c._rpc_call("getSealerList", [config.GROUP_ID]))
print("NodeID List:", c._rpc_call("getNodeIDList", [config.GROUP_ID]))
# Check consensus view specifically
print("Consensus Status:", c._rpc_call("getConsensusStatus", [config.GROUP_ID]))
c.disconnect()
