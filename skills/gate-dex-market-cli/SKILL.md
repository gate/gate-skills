---
name: gate-dex-market-cli
version: "2026.5.7-1"
updated: "2026-05-07"
description: "gate-dex CLI market & token data skill: K-line, liquidity, trading stats, token info, security audit, rankings, new listings, chain config, and raw RPC. Read-only; no signing. Use this skill whenever the user asks for on-chain market data, token info, or security audits via the gate-dex CLI. Trigger phrases include K-line, token price, market cap, token risk, honeypot check, token rankings, new tokens, liquidity, tx stats, chain config, rpc."
user-invocable: true
---

# Gate DEX CLI — Market & Token Data

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.
- **Only use the `gate-dex` CLI subcommands explicitly listed in this skill and its references.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

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

## Workflow

### Step 1: Classify intent

Map the user request to one of: `kline`, `liquidity`, `tx-stats`, `token-info`, `token-risk`, `token-rank`, `new-tokens`, `swap-tokens` (discovery), `bridge-tokens`, `chain-config`, or `rpc`.

Key data to extract:
- `intent`: matched command
- `chain`: chain name (case-insensitive; e.g. `eth`, `bsc`, `arb`, `sol`)
- `address`: token contract address (when applicable)

### Step 2: Resolve missing parameters

- If the user gave a token symbol but no address → run `gate-dex swap-tokens --chain <chain> --search <symbol>` and confirm the resolved address.
- If `chain` is missing for a per-chain command → ask the user; do not guess.
- For `rpc`, ensure `--params` is a valid JSON array string.

Key data to extract:
- `resolved_address`
- `resolved_chain`

### Step 3: Run the read-only command

Call exactly one `gate-dex` subcommand from the table in **CLI Commands**. No write or signing commands are available in this skill.

Key data to extract:
- `cli_stdout`: raw CLI output

### Step 4: Render the report

Format the output per **Report Template** below; surface the Risk Disclosure when the response includes price/security/analytical content.

## Judgment Logic Summary

| User Intent | Trigger Phrases | Command |
|-------------|-----------------|---------|
| Price chart / candlesticks | "K-line", "candlestick", "OHLCV" | `gate-dex kline` |
| Liquidity events | "liquidity pool", "add/remove liquidity" | `gate-dex liquidity` |
| Trading volume / activity | "tx stats", "trading volume", "buy/sell stats" | `gate-dex tx-stats` |
| Price / market cap | "token info", "market cap", "price of" | `gate-dex token-info` |
| Security audit | "is it safe", "honeypot", "audit token" | `gate-dex token-risk` |
| Top movers | "rankings", "top gainers", "leaderboard" | `gate-dex token-rank` |
| Recently listed | "new tokens", "just launched", "newly listed" | `gate-dex new-tokens` |
| Resolve address | "address of", "find token", "search symbol" | `gate-dex swap-tokens --search` |
| Bridge pairs | "bridge tokens", "cross-chain pairs" | `gate-dex bridge-tokens` |
| Chain metadata | "chain config", "RPC endpoint", "chain id" | `gate-dex chain-config` |
| Raw RPC | "eth_call", "eth_getBalance", "rpc" | `gate-dex rpc` |

## Report Template

For data-bearing commands (`token-info`, `token-rank`, `kline`, `tx-stats`, `liquidity`, `new-tokens`, `chain-config`):

```
========== {Command Title} ==========
Chain:        {resolved_chain}
Address:      {resolved_address}
Result:
{key_value_table_or_compact_summary}
========================================
{Optional follow-up suggestions}

Risk Disclosure: For informational purposes only; not investment, financial, tax, or legal advice. Verify on-chain data independently.
```

For `token-risk`:

```
========== Token Risk Audit ==========
Chain:               {chain}
Address:             {address}
Honeypot:            {yes/no/unknown}
Contract ownership:  {renounced/owner_known}
Trading restrictions:{summary}
Liquidity lock:      {locked_until/unlocked/unknown}
========================================
{Warning if any flag is set; recommend confirmation before swap}
```

For `rpc`:

```
========== RPC Result ==========
Chain:   {chain}
Method:  {method}
Params:  {params_json}
Result:  {raw_json_response}
================================
```

## Security Rules

1. **Audit before swapping unfamiliar tokens**: Run `token-risk` first.
2. **RPC params must be valid JSON**: `--params` must be a JSON array string.
3. **Read-only**: All commands here are read-only — no signing or fund movement.

---

## Risk Disclosure

The above is for informational purposes only and does not constitute investment, financial, tax, or legal advice. AI-assisted outputs are for general information only and do not constitute any representation, warranty, or guarantee by Gate. Digital asset prices, market data, and security audits may be incomplete or delayed; always verify on-chain data independently before acting.
