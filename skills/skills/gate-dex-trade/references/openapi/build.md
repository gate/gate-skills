# OpenAPI: Build + Approve

> Load after quote confirmed. Covers ERC20 approve check and unsigned transaction building.

---

## ERC20 Allowance Check

**When needed**: EVM/Tron chain AND token_in is NOT native token (not `"-"`, `is_native_token != 1`).

**Skip entirely** if token_in is native (ETH, BNB, POL, etc.) or chain is Solana/SUI/Ton.

**Use the helper script**:

```bash
python3 gate-dex-trade/scripts/check-allowance.py "<rpc_url>" "<token_address>" "<owner>" "<spender>" "<amount>" "<decimals>"
```

Example:
```bash
python3 gate-dex-trade/scripts/check-allowance.py "https://eth.llamarpc.com" \
  "0xdAC17F958D2ee523a2206206994597C13D831ec7" \
  "0xOwnerWallet" \
  "0xRouterContract" \
  "100.5" \
  "6"
```

Output: `{"allowance_sufficient": true/false, ...}`

- `spender` = the `unsigned_tx.to` from build response (router contract)
- `decimals` = from quote response `from_token.decimal`

If `allowance_sufficient: false` → need approve (see below).

---

## Action: trade.swap.approve_transaction

**When to call**: All of: (1) EVM/Tron, (2) token_in not native, (3) allowance insufficient.

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| user_wallet | string | Yes | User wallet address |
| approve_amount | string | Yes | Amount (human-readable, = transaction amount) |
| quote_id | string | Yes | From quote step |

**Call**:
```bash
python3 gate-dex-trade/scripts/gate-api-call.py "trade.swap.approve_transaction" '{"user_wallet":"0xBb43...","approve_amount":"0.001","quote_id":"6e7b2c..."}'
```

**Response fields**:
- `data` — Approve calldata (hex)
- `approve_address` — Contract to approve to (use as `to` for signing)
- `gas_limit` — Recommended gas limit

**After response**:
1. Show: "Need to approve [token] to router [approve_address], amount [approve_amount]"
2. Ask user to confirm
3. Sign the approve tx (to=approve_address, data=response.data, value=0, gas_limit=response.gas_limit)
4. Keep signed approve for submit step

---

## Action: trade.swap.build

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| chain_id | int | Yes | Chain ID |
| amount_in | string | Yes | Input amount |
| token_in | string | Yes | Input token address |
| token_out | string | Yes | Output token address |
| slippage | string | Yes | Slippage |
| slippage_type | string | Yes | 1=percentage, 2=fixed |
| user_wallet | string | Yes | User wallet |
| receiver | string | Yes | Receiver (usually = user_wallet) |
| quote_id | string | No | From quote (strongly recommended) |
| sol_tip_amount | string | No | Solana Jito MEV tip (lamports) |
| sol_priority_fee | string | No | Solana priority fee (micro-lamports/CU) |

**Call**:
```bash
python3 gate-dex-trade/scripts/gate-api-call.py "trade.swap.build" '{"chain_id":1,"amount_in":"0.01","token_in":"0xdAC...","token_out":"0xC02...","slippage":"0.50","slippage_type":"1","user_wallet":"0xBb43...","receiver":"0xBb43...","quote_id":"c0a8..."}'
```

**Key response fields**:
- `unsigned_tx.to` — Target contract
- `unsigned_tx.data` — Call data (hex for EVM, base64 for Solana)
- `unsigned_tx.value` — Native token value
- `unsigned_tx.gas_limit` — Gas limit
- `unsigned_tx.chain_id` — Chain ID
- `order_id` — Required for submit and status

**Solana special**: `unsigned_tx.data` is base64 VersionedTransaction. Must refresh `recentBlockhash` before signing.

**Errors**: 31501 = insufficient balance, 31502 = slippage too low, 31500 = parameter error.
