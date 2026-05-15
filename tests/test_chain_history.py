from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
from eth_abi import decode
from chain_client import ChainClient
import config

c = ChainClient()
c.connect()

def get_data(i):
    selector = c._get_selector("getData", ["uint256"])
    data = "0x" + selector.hex() + hex(i)[2:].zfill(64)
    res = c._rpc_call("call", [
        config.GROUP_ID, 
        {"from": config.SENDER_ADDRESS, "to": config.CONTRACT_ADDRESS, "data": data}
    ])
    out = res.get("output", "0x")
    if out and out != "0x":
        d = decode(
            ["uint256", "uint256", "uint256", "uint256", "uint256", "uint256", "uint256", "string", "address"],
            bytes.fromhex(out[2:])
        )
        return d[7]
    return "error"

for i in range(191, 210):
    sig = get_data(i)
    print(f"Record {i} length:", len(sig), "startsWith:", sig[:10])

c.disconnect()
