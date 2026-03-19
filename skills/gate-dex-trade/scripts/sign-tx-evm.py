#!/usr/bin/env python3
"""
EVM transaction signing (EIP-1559 Type 2).
Signs an unsigned transaction from the Gate DEX build API response.

Usage:
    python3 sign-tx-evm.py <unsigned_tx_json> <rpc_url>

    Private key is read from stdin (never passed as CLI argument for security):
    echo "0xYOUR_PRIVATE_KEY" | python3 sign-tx-evm.py '<unsigned_tx_json>' 'https://rpc-url'

Input:
    unsigned_tx_json: The "unsigned_tx" field from trade.swap.build response (JSON string)
    rpc_url: Chain RPC endpoint URL

Output (JSON to stdout):
    {
        "signed_tx_string": "[\"0x02f8...\"]",   # JSON array format required by submit API
        "wallet_address": "0xABC...",
        "tx_hash": "0x..."
    }

Requirements: pip3 install web3
"""

import json
import sys
import os

try:
    from web3 import Web3
    from eth_account import Account
except ImportError:
    print(json.dumps({
        "error": "web3 package not installed",
        "fix": "pip3 install web3"
    }))
    sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage: echo '<private_key>' | python3 sign-tx-evm.py '<unsigned_tx_json>' '<rpc_url>'",
              file=sys.stderr)
        sys.exit(1)

    try:
        unsigned_tx = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid unsigned_tx JSON: {e}"}))
        sys.exit(1)

    rpc_url = sys.argv[2]

    # Read private key from stdin
    private_key = sys.stdin.readline().strip()
    if not private_key:
        print(json.dumps({"error": "Private key must be provided via stdin"}))
        sys.exit(1)

    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        account = Account.from_key(private_key)

        # Build EIP-1559 transaction dict
        tx = {
            "chainId": int(unsigned_tx.get("chainId", unsigned_tx.get("chain_id", 1))),
            "to": Web3.to_checksum_address(unsigned_tx["to"]),
            "value": int(unsigned_tx.get("value", "0"), 16) if isinstance(unsigned_tx.get("value"), str) else int(unsigned_tx.get("value", 0)),
            "data": unsigned_tx.get("data", "0x"),
            "nonce": w3.eth.get_transaction_count(account.address),
            "gas": int(unsigned_tx.get("gas", unsigned_tx.get("gasLimit", 300000))),
            "maxFeePerGas": int(unsigned_tx.get("maxFeePerGas", 0)),
            "maxPriorityFeePerGas": int(unsigned_tx.get("maxPriorityFeePerGas", 0)),
            "type": 2,  # EIP-1559
        }

        # If maxFeePerGas not provided, estimate from RPC
        if tx["maxFeePerGas"] == 0:
            latest = w3.eth.get_block("latest")
            base_fee = latest.get("baseFeePerGas", 30 * 10**9)
            tx["maxPriorityFeePerGas"] = w3.eth.max_priority_fee
            tx["maxFeePerGas"] = base_fee * 2 + tx["maxPriorityFeePerGas"]

        signed = account.sign_transaction(tx)
        signed_hex = "0x" + signed.raw_transaction.hex()

        # Format as JSON array string (required by Gate submit API)
        signed_tx_string = json.dumps([signed_hex])

        print(json.dumps({
            "signed_tx_string": signed_tx_string,
            "wallet_address": account.address,
            "tx_hash": signed.hash.hex(),
        }))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
