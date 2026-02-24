from chain_client import ChainClient
import config
c = ChainClient()
c.connect()
print("Sealers:", c._rpc_call("getSealerList", [config.GROUP_ID]))
print("NodeID List:", c._rpc_call("getNodeIDList", [config.GROUP_ID]))
# Check consensus view specifically
print("Consensus Status:", c._rpc_call("getConsensusStatus", [config.GROUP_ID]))
c.disconnect()
