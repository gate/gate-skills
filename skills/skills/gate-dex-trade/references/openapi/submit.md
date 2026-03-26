# OpenAPI: Submit + Status + History

> Load after signing. Covers transaction submission, status polling, and history queries.

---

## Action: trade.swap.submit

Two modes: API broadcast (priority) or self-broadcast + report hash.

### Mode A: API Broadcast (Priority)

Pass `signed_tx_string` to let Gate API broadcast:

```bash
python3 gate-dex-trade/scripts/gate-api-call.py "trade.swap.submit" '{"order_id":"0x4202...","signed_tx_string":"[\"0x02f8b2...\"]"}'
```

If approve was also signed, pass both:
```bash
python3 gate-dex-trade/scripts/gate-api-call.py "trade.swap.submit" '{"order_id":"0x4202...","signed_tx_string":"[\"0x02f8b2...\"]","signed_approve_tx_string":"[\"0x02f871...\"]"}'
```

**Critical**: `signed_tx_string` MUST be JSON array format string. Raw hex causes error 50005.

### Mode B: Self-Broadcast + Report Hash (Fallback)

If Mode A fails (format errors, 50005):

1. Broadcast via RPC (e.g., `eth_sendRawTransaction`)
2. Get `tx_hash`
3. Report to API:

```bash
python3 gate-dex-trade/scripts/gate-api-call.py "trade.swap.submit" '{"order_id":"0x4202...","tx_hash":"0x3911b4f..."}'
```

**Recommended flow**: Try Mode A first. If status polling shows error 50005, switch to Mode B (requires re-quote → build → sign → self-broadcast → submit hash).

---

## Action: trade.swap.status

Auto-poll after submit success.

```bash
python3 gate-dex-trade/scripts/gate-api-call.py "trade.swap.status" '{"chain_id":1,"order_id":"0x4202...","tx_hash":""}'
```

**Polling rules**:
- Every 5 seconds
- Max 60 seconds (12 polls)
- Show: "Waiting for on-chain confirmation... (Xs elapsed)"
- Stop when: status != pending
- After 60s still pending: show "Transaction still processing" + block explorer link

**Display final result**: status, actual output amount, gas fee, block explorer link.

---

## Action: trade.swap.history

```bash
python3 gate-dex-trade/scripts/gate-api-call.py "trade.swap.history" '{"user_wallet":["0xBb43..."],"pageNum":1,"pageSize":10}'
```

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| user_wallet | string[] | Yes | Wallet address array |
| page_number | int | No | Page (default 1) |
| page_size | int | No | Per page (default 100, max 100) |
| chain_id | int | No | Filter by chain |

Display as table: time, chain, from → to, amount, status.

Error 31701 = no history → "No history records found."
