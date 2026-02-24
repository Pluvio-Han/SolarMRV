from chain_client import ChainClient
c = ChainClient()
c.connect()
print(c.get_latest_data())
c.disconnect()
