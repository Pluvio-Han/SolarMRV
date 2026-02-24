from chain_client import ChainClient
import json
c = ChainClient()
c.connect()
print(json.dumps(c.get_chain_summary(), indent=2))
c.disconnect()
