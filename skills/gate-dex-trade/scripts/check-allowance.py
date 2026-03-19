#!/usr/bin/env python3
"""
ERC20 allowance check with precision-aligned comparison.
Checks if a spender has sufficient allowance for a token amount.

Usage:
    python3 check-allowance.py <rpc_url> <token_address> <owner> <spender> <amount> <decimals>

Example:
    python3 check-allowance.py "https://eth.llamarpc.com" "0xdAC17F958D2ee523a2206206994597C13D831ec7" \
        "0xOwner..." "0xSpender..." "100.5" "6"

Output (JSON):
    {
        "allowance_sufficient": true,
        "current_allowance": "1000000000",
        "current_allowance_human": "1000.0",
        "required_amount": "100500000",
        "required_amount_human": "100.5"
    }
"""

import json
import sys
import os

try:
    from urllib.request import Request, urlopen
except ImportError:
    print(json.dumps({"error": "urllib not available"}))
    sys.exit(1)


def eth_call(rpc_url, to, data):
    """Execute eth_call via JSON-RPC."""
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{"to": to, "data": data}, "latest"],
        "id": 1,
    })

    req = Request(rpc_url, data=payload.encode(), headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())

    if "error" in result:
        raise Exception(f"RPC error: {result['error']}")

    return result.get("result", "0x0")


def pad_address(addr):
    """Pad address to 32 bytes (64 hex chars)."""
    return addr.lower().replace("0x", "").zfill(64)


def main():
    if len(sys.argv) < 7:
        print("Usage: python3 check-allowance.py <rpc_url> <token> <owner> <spender> <amount> <decimals>",
              file=sys.stderr)
        sys.exit(1)

    rpc_url = sys.argv[1]
    token_address = sys.argv[2]
    owner = sys.argv[3]
    spender = sys.argv[4]
    amount_human = sys.argv[5]
    decimals = int(sys.argv[6])

    try:
        # allowance(address,address) selector = 0xdd62ed3e
        calldata = "0xdd62ed3e" + pad_address(owner) + pad_address(spender)

        result_hex = eth_call(rpc_url, token_address, calldata)
        current_allowance = int(result_hex, 16)

        # Convert human amount to raw
        required_raw = int(float(amount_human) * (10 ** decimals))

        sufficient = current_allowance >= required_raw

        print(json.dumps({
            "allowance_sufficient": sufficient,
            "current_allowance": str(current_allowance),
            "current_allowance_human": str(current_allowance / (10 ** decimals)),
            "required_amount": str(required_raw),
            "required_amount_human": amount_human,
        }))

        sys.exit(0 if sufficient else 1)

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
