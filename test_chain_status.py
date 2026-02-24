import json, time
from chain_client import ChainClient
c = ChainClient()
c.connect()
for i in range(3):
    print("--- Chain Status ---")
    print(json.dumps(c.get_chain_summary(), indent=2))
    time.sleep(2)
c.disconnect()
