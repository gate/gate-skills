---
name: gate-dex-market-cli
version: "2026.4.23-2"
updated: "2026-04-23"
description: "gate-dex CLI market & token data skill. K-line, liquidity pool events, trading stats, token info (price/mcap), token security audit, token rankings, new token listings, chain config, and raw RPC calls. Read-only; no signing involved."
homepage: https://git.fulltrust.link/web3/ai/gate-dex-cli
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "os": ["linux", "darwin"],
        "requires": {
          "bins": ["gate-dex"]
        },
        "install": [
          {
            "id": "download-linux-x64",
            "kind": "download",
            "os": ["linux"],
            "url": "https://gate-dex-cli-test.gateweb3.cc/v1.0.0/gate-dex-linux-x64",
            "bins": ["gate-dex"],
            "label": "Download gate-dex (Linux x64)"
          },
          {
            "id": "download-macos-arm64",
            "kind": "download",
            "os": ["darwin"],
            "url": "https://gate-dex-cli-test.gateweb3.cc/v1.0.0/gate-dex-darwin-arm64",
            "bins": ["gate-dex"],
            "label": "Download gate-dex (macOS arm64)"
          }
        ]
      }
  }
---

# Gate DEX CLI — Market & Token Data

> Read-only market data via CLI. K-line, liquidity, trading stats, token info/risk/rank, new listings, chain config, and raw RPC. No GV checkin or signing involved.

## Skill Boundaries

| This skill | Route to other skill |
|-----------|----------------|
| K-line, liquidity, trading stats | Auth / login issues → `gate-dex-wallet-cli` |
| Token info (price, market cap) | Balance, address, token list → `gate-dex-wallet-cli` |
| Token security audit | Token transfers (send) → `gate-dex-wallet-cli` |
| Token rankings & new listings | Swap / exchange tokens → `gate-dex-trade-cli` |
| Chain config & raw RPC calls | — |
| Token address lookup (swap-tokens) | — |

---

## Applicable Scenarios

- "K-line for token 0x...", "price chart", "candlestick data"
- "Token info for 0x...", "price of this token", "market cap"
- "Is this token safe?", "audit contract", "honeypot check", "security scan"
- "Token rankings", "top gainers", "price change leaderboard"
- "New tokens", "recently listed", "new listings"
- "Liquidity pool data", "trading volume", "tx stats"
- "List swappable tokens", "find token address by symbol"
- "Chain config", "RPC call", "eth_getBalance", "getBalance"

---

## CLI Commands

### K-Line (Candlestick)

```bash
gate-dex kline --chain eth --address 0xTokenAddress
gate-dex kline --chain sol --address <token_mint>
```

Returns OHLCV candlestick data for the token.

### Liquidity Pool Events

```bash
gate-dex liquidity --chain eth --address 0xTokenAddress
```

Returns recent liquidity add/remove events.

### Trading Volume Stats

```bash
gate-dex tx-stats --chain eth --address 0xTokenAddress
```

Returns trading volume, transaction count, buy/sell stats.

### Token Info (Price, Market Cap)

```bash
gate-dex token-info --chain eth --address 0xTokenAddress
gate-dex token-info --chain sol --address <token_mint>
```

Returns price, market cap, 24h volume, price change, total supply.

### Token Security Audit

```bash
gate-dex token-risk --chain eth --address 0xTokenAddress
gate-dex token-risk --chain sol --address <token_mint>
```

Returns security risk: honeypot check, contract ownership, trading restrictions, liquidity lock status.

**Always run `token-risk` before swapping an unfamiliar token.**

### Token Rankings

```bash
gate-dex token-rank                     # all chains
gate-dex token-rank --chain eth         # Ethereum only
gate-dex token-rank --chain arb --limit 20
```

### New Token Listings

```bash
gate-dex new-tokens
gate-dex new-tokens --chain eth
gate-dex new-tokens --chain sol --start 2026-04-01T00:00:00Z
```

| Option | Description |
|--------|-------------|
| `--chain <name>` | Filter by chain |
| `--start <RFC3339>` | Filter tokens created after this timestamp |

### Swappable Token List

```bash
gate-dex swap-tokens
gate-dex swap-tokens --chain eth
gate-dex swap-tokens --chain sol --search USDC
```

Use `--search` to look up a token address by symbol.

### Cross-Chain Bridge Tokens

```bash
gate-dex bridge-tokens
gate-dex bridge-tokens --src-chain eth --dest-chain arb
```

### Chain Configuration

```bash
gate-dex chain-config          # all chains
gate-dex chain-config eth
gate-dex chain-config sol
```

### Raw JSON-RPC Call

```bash
# ETH balance
gate-dex rpc --chain ETH --method eth_getBalance \
  --params '["0xYourAddress", "latest"]'

# ERC20 balanceOf
gate-dex rpc --chain ETH --method eth_call \
  --params '[{"to":"0xContractAddr","data":"0x70a08231000...yourAddress"},"latest"]'

# Solana: get SOL balance
gate-dex rpc --chain SOL --method getBalance \
  --params '["YourSolAddress"]'

# Current gas price
gate-dex rpc --chain ETH --method eth_gasPrice
```

| Option | Required | Description |
|--------|----------|-------------|
| `--chain <name>` | Yes | Chain name |
| `--method <m>` | Yes | JSON-RPC method name |
| `--params '<json>'` | No | JSON array of parameters |

---

## Common Patterns

**Find token contract address by symbol:**
```bash
gate-dex swap-tokens --chain arb --search USDC
```

**Verify on-chain balance when `tokens` shows 0:**
```bash
gate-dex rpc --chain ETH --method eth_getBalance \
  --params '["0xYourAddress", "latest"]'
```

**Security check before swapping new token:**
```bash
gate-dex token-risk --chain eth --address 0xNewToken
```

---

## Chain Names

Case-insensitive. Common: `eth`, `bsc`, `polygon`, `arb`/`arbitrum`, `op`/`optimism`, `avax`, `base`, `sol`.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Not logged in` | Run `gate-dex login` |
| K-line returns empty | Token may have low liquidity or be too new |
| Token risk data unavailable | Token may be too new; trade with caution |
| RPC call fails | Check that `--params` is a valid JSON array string |

---

## Post-Query Suggestions

**After token-info / token-risk:**
```
You can also:
- Swap this token: gate-dex swap --from-chain <id> --from - --to <address> --amount <n>
- Check your holdings: gate-dex tokens --chain <chain>
- View K-line: gate-dex kline --chain <chain> --address <address>
```

| User Follow-up | Route |
|----------------|-------|
| Swap the token | gate-dex-trade-cli skill |
| Transfer tokens | gate-dex-wallet-cli skill |
| Check balance / holdings | gate-dex-wallet-cli skill |

---

## Security Rules

1. **Audit before swapping unfamiliar tokens**: Run `token-risk` first.
2. **RPC params must be valid JSON**: `--params` must be a JSON array string.
3. **Read-only**: All commands here are read-only — no signing or fund movement.
