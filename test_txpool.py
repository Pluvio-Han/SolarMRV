from chain_client import ChainClient
import config
c = ChainClient()
c.connect()
rpc = getattr(c, '_rpc_call')
print("Pending Tx Size:", rpc("getPendingTxSize", [config.GROUP_ID]))
c.disconnect()
