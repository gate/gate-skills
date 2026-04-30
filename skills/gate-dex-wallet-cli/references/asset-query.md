---
name: gate-dex-wallet-cli-asset-query
version: "2026.4.23-2"
updated: "2026-04-23"
description: "gate-wallet CLI asset query module. Balance (USD total), wallet addresses (EVM + Solana), token list with balances, transaction history, swap history. Read-only; no signing involved."
---

# Gate Wallet CLI — Asset Query

> Read-only module — portfolio value, wallet addresses, token balances, transaction and swap history. No GV checkin or signing involved.

## Applicable Scenarios

- "Check my balance", "how much do I have", "total assets"
- "What's my wallet address", "show my ETH address", "Solana address"
- "List my tokens", "show holdings", "what tokens do I own"
- "Transaction history", "past txs", "recent transfers"
- "Swap history", "past swaps", "what swaps did I make"
- "Transaction details for hash 0x..."

---

## CLI Commands

### Balance

```bash
gate-wallet balance
```

Returns total portfolio value in USD across all chains.

### Wallet Addresses

```bash
gate-wallet address
```

Returns EVM address and Solana address from the local auth file. No network call needed.

Output example:
```json
{
  "evm_address": "0xAbCd...1234",
  "sol_address": "BTYzG...bfxE"
}
```

### Token List

```bash
gate-wallet tokens
gate-wallet tokens --chain ETH
gate-wallet tokens --chain ETH,SOL
gate-wallet tokens --chain ARB --page 2 --size 50
```

| Option | Description | Default |
|--------|-------------|---------|
| `--chain <keys>` | Filter by network key (comma-separated, e.g. `ETH,SOL,ARB`) | all chains |
| `--page <n>` | Page number | 1 |
| `--size <n>` | Items per page | 20 |

Network keys are case-insensitive. Common values: `ETH`, `BSC`, `ARB`, `POLYGON`, `BASE`, `OP`, `AVAX`, `SOL`.

### Transaction History

```bash
gate-wallet tx-history
gate-wallet tx-history --page 2 --limit 20
```

| Option | Default |
|--------|---------|
| `--page <n>` | 1 |
| `--limit <n>` | 20 |
| `--start <unix_sec>` | — |
| `--end <unix_sec>` | — |

### Transaction Detail

```bash
gate-wallet tx-detail <hash>
```

Returns on-chain transaction details for the given hash.

### Swap History

```bash
gate-wallet swap-history
```

Returns list of past swap orders.

### Swap Order Detail

```bash
gate-wallet swap-detail <order_id>
```

Returns detail for a specific swap order.

---

## Common Patterns

**Check if I have enough ETH for a transfer:**
```bash
gate-wallet tokens --chain ETH
```
Look for the `ETH` entry in the result — check `balance` field.

**Get Solana address before sending SOL:**
```bash
gate-wallet address
# or check sol_address field
```

**Confirm a transfer went through:**
```bash
gate-wallet tx-detail 0xabcd...1234
```

---

## Output Format

All commands output JSON. Key fields in token list result:

| Field | Description |
|-------|-------------|
| `symbol` | Token symbol (e.g., ETH, USDT) |
| `balance` | Human-readable balance |
| `price` | Token price in USD |
| `value` | Total value in USD |
| `chain` / `networkKey` | Chain identifier |
| `contractAddress` | ERC20/SPL contract address (native = empty or "NATIVE") |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Not logged in` | Run `gate-wallet login` first |
| Token not showing | Try without `--chain` filter; L2 balances may have indexing delay |
| Balance appears 0 | Use `gate-wallet rpc --chain ETH --method eth_getBalance` to verify on-chain |
| Solana balance missing | Check with `gate-wallet rpc --chain SOL --method getBalance` |

---

## Post-Query Suggestions

**After balance / token query:**
```
You can also:
- Transfer tokens: gate-wallet send --chain ETH --to 0x... --amount 0.1
- Swap tokens: gate-wallet swap --from-chain 1 --to-chain 1 --from - --to <token> --amount 0.01
- Check token security: gate-wallet token-risk --chain eth --address <contract>
```

| User Follow-up | Route |
|----------------|-------|
| Transfer / send tokens | ./transfer.md |
| Swap / exchange tokens | ./swap.md |
| Token price, K-line, security audit | ./market.md |
| Login / session issue | ./auth.md |
