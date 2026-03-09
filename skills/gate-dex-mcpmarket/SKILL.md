---
name: gate-dex-mcpmarket
version: "2026.3.5-1"
updated: "2026-03-05"
description: "Gate Wallet market data and token info queries. K-line, trading stats,
  liquidity, token details, rankings, security audit, new token discovery. Use when
  user asks about quotes, price, token info. All queries require no auth. Not for
  executing trades."
---

# Gate Wallet Market Skill

> Market/Token domain — K-line, trading stats, liquidity, token details, rankings, security audit, new token discovery. 7 MCP tools, all require no auth.

**Trigger scenarios**: User mentions "quotes", "K-line", "price", "token info", "ranking", "security", "audit", "market", "kline", "chart", "token info", "ranking", "risk", "new token", or when other Skills need market data / security review support.

## MCP Server Connection Check

### First-Session Check

**Before the first MCP tool call in a session, run one connection probe to confirm Gate Wallet MCP Server is available. No need to repeat for later operations.**

Probe call:

```
CallMcpTool(server="gate-wallet", toolName="chain.config", arguments={chain: "eth"})
```

| Result | Action |
|--------|--------|
| Success | MCP Server available, proceed with business tools directly, no need to probe again |
| `server not found` / `unknown server` | Cursor not configured → Show configuration guide (see below) |
| `connection refused` / `timeout` | Remote unreachable → Prompt user to check URL and network |

### Runtime Error Fallback

If business tool calls fail later (connection error, timeout, etc.), handle as follows:

| Error Type | Action |
|------------|--------|
| `server not found` / `unknown server` | MCP Server config missing → Show configuration guide |
| `connection refused` / `timeout` | Service disconnected mid-session → Show connection failure message |
| `401` / `unauthorized` | API Key auth failed → Show auth failure message |
| Other business errors (e.g. token not found) | Normal business error, handle per "Edge Cases and Error Handling" section |

### When Cursor Is Not Configured

```
❌ Gate Wallet MCP Server Not Configured

No MCP Server named "gate-wallet" was found in Cursor. Please configure as follows:

Method 1: Via Cursor Settings (recommended)
  1. Open Cursor → Settings → MCP
  2. Click "Add new MCP server"
  3. Fill in:
     - Name: gate-wallet
     - Type: HTTP
     - URL: https://your-mcp-server-domain/mcp
  4. Save and retry

Method 2: Edit config file manually
  Edit ~/.cursor/mcp.json and add:
  {
    "mcpServers": {
      "gate-wallet": {
        "url": "https://your-mcp-server-domain/mcp"
      }
    }
  }

If you do not have an MCP Server URL yet, please contact your administrator.
```

### When Remote Service Is Unreachable

```
⚠️  Gate Wallet MCP Server Connection Failed

MCP Server config was found but the remote service cannot be reached. Please check:
1. Confirm the service URL is correct (is the configured URL reachable?)
2. Check network (VPN / firewall blocking?)
3. Confirm the remote service is running
```

### When API Key Auth Fails

```
🔑 Gate Wallet MCP Server Auth Failed

MCP Server is connected but API Key validation failed. The service uses AK/SK auth (x-api-key header).
Please contact your administrator for a valid API Key and confirm server-side config.
```

## Auth Note

All tools in this Skill **require no auth**. They are public market data queries only; no `mcp_token` needed.

## MCP Tool Usage

### 1. `market_get_kline` — Get K-line Data

Get K-line (candlestick) data for a token in a given time interval.

| Field | Description |
|-------|-------------|
| **Tool name** | `market_get_kline` |
| **Parameters** | `{ chain: string, token_address: string, interval?: string, limit?: number }` |
| **Returns** | K-line array; each item has `timestamp`, `open`, `high`, `low`, `close`, `volume` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain id (e.g. `"eth"`, `"bsc"`) |
| `token_address` | Yes | Token contract address. Use `"native"` for native token |
| `interval` | No | K-line interval (e.g. `"1m"`, `"5m"`, `"1h"`, `"4h"`, `"1d"`). Default `"1h"` |
| `limit` | No | Number of items to return. Default 100 |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="market_get_kline",
  arguments={
    chain: "eth",
    token_address: "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    interval: "1h",
    limit: 24
  }
)
```

Return example:

```json
[
  {
    "timestamp": 1700000000,
    "open": "1.0001",
    "high": "1.0005",
    "low": "0.9998",
    "close": "1.0002",
    "volume": "15000000"
  }
]
```

Agent behavior: Present K-line trend as text table or summary (high, low, change %, volume change, etc.).

---

### 2. `market_get_tx_stats` — Get Trading Stats

Get on-chain trading stats for a token (buy/sell count, volume, etc.).

| Field | Description |
|-------|-------------|
| **Tool name** | `market_get_tx_stats` |
| **Parameters** | `{ chain: string, token_address: string, period?: string }` |
| **Returns** | `{ buy_count: number, sell_count: number, buy_volume: string, sell_volume: string, unique_buyers: number, unique_sellers: number }` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain id |
| `token_address` | Yes | Token contract address |
| `period` | No | Stats period (e.g. `"24h"`, `"7d"`, `"30d"`). Default `"24h"` |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="market_get_tx_stats",
  arguments={
    chain: "eth",
    token_address: "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    period: "24h"
  }
)
```

Return example:

```json
{
  "buy_count": 12500,
  "sell_count": 11800,
  "buy_volume": "45000000",
  "sell_volume": "42000000",
  "unique_buyers": 3200,
  "unique_sellers": 2900
}
```

---

### 3. `market_get_pair_liquidity` — Get Pair Liquidity

Get liquidity pool info for a token pair.

| Field | Description |
|-------|-------------|
| **Tool name** | `market_get_pair_liquidity` |
| **Parameters** | `{ chain: string, token_address: string }` |
| **Returns** | `{ total_liquidity_usd: string, pairs: [{ dex: string, pair: string, liquidity_usd: string, volume_24h: string }] }` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain id |
| `token_address` | Yes | Token contract address |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="market_get_pair_liquidity",
  arguments={
    chain: "eth",
    token_address: "0xdAC17F958D2ee523a2206206994597C13D831ec7"
  }
)
```

Return example:

```json
{
  "total_liquidity_usd": "250000000",
  "pairs": [
    {
      "dex": "Uniswap V3",
      "pair": "USDT/ETH",
      "liquidity_usd": "120000000",
      "volume_24h": "35000000"
    },
    {
      "dex": "Uniswap V3",
      "pair": "USDT/USDC",
      "liquidity_usd": "80000000",
      "volume_24h": "22000000"
    }
  ]
}
```

---

### 4. `token_get_coin_info` — Get Token Details

Get detailed token info (name, symbol, market cap, holders, etc.).

| Field | Description |
|-------|-------------|
| **Tool name** | `token_get_coin_info` |
| **Parameters** | `{ chain: string, token_address: string }` |
| **Returns** | `{ name: string, symbol: string, decimals: number, total_supply: string, market_cap: string, holders: number, price: string, price_change_24h: string, website: string, socials: object }` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain id |
| `token_address` | Yes | Token contract address |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="token_get_coin_info",
  arguments={
    chain: "eth",
    token_address: "0xdAC17F958D2ee523a2206206994597C13D831ec7"
  }
)
```

Return example:

```json
{
  "name": "Tether USD",
  "symbol": "USDT",
  "decimals": 6,
  "total_supply": "40000000000",
  "market_cap": "40000000000",
  "holders": 5200000,
  "price": "1.0001",
  "price_change_24h": "0.01",
  "website": "https://tether.to",
  "socials": { "twitter": "@Tether_to" }
}
```

---

### 5. `token_ranking` — Token Rankings

Get on-chain token rankings (by market cap, change %, volume, etc.).

| Field | Description |
|-------|-------------|
| **Tool name** | `token_ranking` |
| **Parameters** | `{ chain: string, sort_by?: string, order?: string, limit?: number }` |
| **Returns** | Token ranking array; each item has `rank`, `name`, `symbol`, `price`, `market_cap`, `change_24h`, `volume_24h` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain id |
| `sort_by` | No | Sort dimension: `"market_cap"`, `"volume_24h"`, `"change_24h"`, `"holders"`. Default `"market_cap"` |
| `order` | No | Sort direction: `"desc"` (descending), `"asc"` (ascending). Default `"desc"` |
| `limit` | No | Number of items to return. Default 20 |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="token_ranking",
  arguments={
    chain: "eth",
    sort_by: "volume_24h",
    order: "desc",
    limit: 10
  }
)
```

Return example:

```json
[
  {
    "rank": 1,
    "name": "Tether USD",
    "symbol": "USDT",
    "price": "1.0001",
    "market_cap": "40000000000",
    "change_24h": "0.01",
    "volume_24h": "5000000000"
  }
]
```

---

### 6. `token_get_coins_range_by_created_at` — New Token Discovery

Get newly listed tokens by creation time range.

| Field | Description |
|-------|-------------|
| **Tool name** | `token_get_coins_range_by_created_at` |
| **Parameters** | `{ chain: string, start_time?: number, end_time?: number, limit?: number }` |
| **Returns** | Token array; each item has `name`, `symbol`, `token_address`, `created_at`, `price`, `market_cap`, `holders` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain id |
| `start_time` | No | Start timestamp (seconds). Default 24 hours ago |
| `end_time` | No | End timestamp (seconds). Default current time |
| `limit` | No | Number of items to return. Default 20 |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="token_get_coins_range_by_created_at",
  arguments={
    chain: "eth",
    limit: 10
  }
)
```

---

### 7. `token_get_risk_info` — Token/Contract Security Audit

Get security risk assessment for a token or contract (audit status, risk labels, etc.).

| Field | Description |
|-------|-------------|
| **Tool name** | `token_get_risk_info` |
| **Parameters** | `{ chain: string, address: string }` |
| **Returns** | `{ risk_level: string, is_audited: boolean, risk_items: [{ type: string, description: string, severity: string }], contract_verified: boolean, owner_renounced: boolean }` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain id |
| `address` | Yes | Token contract address or any contract address |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="token_get_risk_info",
  arguments={
    chain: "eth",
    address: "0xdAC17F958D2ee523a2206206994597C13D831ec7"
  }
)
```

Return example:

```json
{
  "risk_level": "low",
  "is_audited": true,
  "risk_items": [],
  "contract_verified": true,
  "owner_renounced": false
}
```

`risk_level` meanings:

| risk_level | Meaning | Agent Behavior |
|------------|---------|----------------|
| `low` | Low risk | Proceed normally |
| `medium` | Medium risk | Warn user, list risk items |
| `high` | High risk | Strong warning, advise against interaction. If user insists, show security warning confirmation |
| `unknown` | No audit data | Note that no security info was found, suggest user verify |

Agent behavior: This tool is often called by `gate-dex-mcpdapp` and `gate-dex-mcpswap` across Skills for pre-trade contract security review.

## Skill Routing

Based on user intent after viewing market data, route to the right Skill:

| User Intent | Route To |
|-------------|----------|
| Wants to buy/sell the token | `gate-dex-mcpswap` |
| Wants to transfer the token | `gate-dex-mcptransfer` |
| View own holdings | `gate-dex-mcpwallet` |
| View trade/Swap history | `gate-dex-mcpwallet` |
| Wants to interact with DApp | `gate-dex-mcpdapp` |

## Workflows

> Before running any workflow below for the first time in a session, run the MCP Server connection check (see above). After a successful check, run business tools directly. If a connection error occurs later, follow the runtime error fallback rules.

### Flow A: View Token Quotes (K-line + Stats)

```
Step 1: Intent detection + parameter collection
  Extract from user input:
  - Token name/symbol or contract address
  - Chain (optional, infer from context)
  - K-line interval (optional, default 1h)
  - Stats period (optional, default 24h)

  If user provides token symbol but not contract address:
  - Call token_get_coin_info or infer address from context
  ↓

Step 2: Fetch market data
  Call in parallel (if applicable):
  - market_get_kline({ chain, token_address, interval, limit })
  - market_get_tx_stats({ chain, token_address, period })
  - market_get_pair_liquidity({ chain, token_address })
  ↓

Step 3: Format output

  ────────────────────────────
  📈 {token_name} ({symbol}) Quotes

  Current price: ${price}
  24h change: {change_24h}%
  24h high: ${high_24h}
  24h low: ${low_24h}

  ── Trading stats (24h) ──
  Buys: {buy_count} txs / ${buy_volume}
  Sells: {sell_count} txs / ${sell_volume}
  Unique buyers: {unique_buyers}
  Unique sellers: {unique_sellers}

  ── Liquidity ──
  Total liquidity: ${total_liquidity_usd}
  Main pairs:
  | DEX | Pair | Liquidity | 24h Volume |
  |-----|------|-----------|------------|
  | {dex} | {pair} | ${liquidity} | ${volume} |
  ────────────────────────────

  ↓

Step 4: Suggest next steps
  - Buy this token → gate-dex-mcpswap
  - View security info → token_get_risk_info
  - Browse more tokens → token_ranking
```

### Flow B: View Token Details

```
Step 1: Run query
  Call token_get_coin_info({ chain, token_address })
  ↓

Step 2: Format output

  ────────────────────────────
  🪙 Token Details

  Name: {name} ({symbol})
  Contract: {token_address}
  Chain: {chain_name}
  Decimals: {decimals}
  Total supply: {total_supply}
  Market cap: ${market_cap}
  Holders: {holders}
  Current price: ${price}
  24h change: {price_change_24h}%
  Website: {website}
  ────────────────────────────

  ↓

Step 3: Suggest next steps
  - View K-line quotes → market_get_kline
  - View security audit → token_get_risk_info
  - Buy this token → gate-dex-mcpswap
```

### Flow C: Token Rankings

```
Step 1: Parameter collection
  Determine sort dimension (market cap/volume/change), chain, count
  ↓

Step 2: Run query
  Call token_ranking({ chain, sort_by, order, limit })
  ↓

Step 3: Format output

  ────────────────────────────
  🏆 {chain_name} Token Rankings (by {sort_by})

  | # | Token | Price | 24h Change | Market Cap | 24h Volume |
  |---|-------|-------|------------|------------|------------|
  | 1 | {symbol} | ${price} | {change}% | ${mcap} | ${vol} |
  | 2 | ... | ... | ... | ... | ... |
  ────────────────────────────
```

### Flow D: Security Review

```
Step 1: Run query
  Call token_get_risk_info({ chain, address })
  ↓

Step 2: Format output

  When risk_level == "low":

  ────────────────────────────
  🛡️ Security Audit Result

  Contract: {address}
  Chain: {chain_name}
  Risk level: Low ✅
  Contract verified: Yes
  Audited: Yes
  Owner renounced: {Yes/No}
  Risk items: None
  ────────────────────────────

  When risk_level == "high":

  ────────────────────────────
  ⚠️ Security Audit Result

  Contract: {address}
  Chain: {chain_name}
  Risk level: High ⚠️
  Contract verified: {Yes/No}
  Audited: {Yes/No}

  Risk items:
  - [{severity}] {description}
  - [{severity}] {description}

  Recommendation: Interact with this contract with caution; there is risk of asset loss.
  ────────────────────────────
```

### Flow E: New Token Discovery

```
Step 1: Parameter collection
  Determine chain and time range
  ↓

Step 2: Run query
  Call token_get_coins_range_by_created_at({ chain, start_time?, end_time?, limit })
  ↓

Step 3: Format output

  ────────────────────────────
  🆕 {chain_name} Newly Listed Tokens

  | Token | Contract | Created | Price | Market Cap | Holders |
  |-------|----------|---------|-------|------------|---------|
  | {symbol} | {addr_short} | {time} | ${price} | ${mcap} | {holders} |

  Note: New tokens carry higher risk; consider checking security audit info before trading.
  ────────────────────────────

  ↓

Step 4: Suggest next steps
  - View security info for a token → token_get_risk_info
  - View token details → token_get_coin_info
```

## Cross-Skill Workflow

### Called by Other Skills

This Skill provides market data and security info and is often called by:

| Caller | Scenario | Tools Used |
|--------|----------|------------|
| `gate-dex-mcpswap` | Query token info before Swap to help resolve address | `token_get_coin_info` |
| `gate-dex-mcpswap` | Security review of target token before Swap | `token_get_risk_info` |
| `gate-dex-mcpdapp` | Contract security review before DApp trade | `token_get_risk_info` |

### Query → Review → Trade Workflow

```
gate-dex-mcpmarket (token_get_coin_info → token info)
  → gate-dex-mcpmarket (token_get_risk_info → security review)
    → gate-dex-mcpwallet (check balance)
      → gate-dex-mcpswap (quote → confirm → execute)
```

## Display Rules

### Price Display

- **Above $1**: 2 decimal places (e.g. `$1,920.50`)
- **$0.01 ~ $1**: 4 decimal places (e.g. `$0.0521`)
- **Below $0.01**: 6–8 significant digits (e.g. `$0.00000142`)
- **Percentages**: 2 decimal places (e.g. `+2.15%`, `-0.32%`)
- **Large numbers**: Thousands separator; very large numbers use abbreviations (e.g. `$1.2B`, `$350M`)

### Address Display

- When showing full contract address, include chain info
- For short references use masked format: `0xdAC1...1ec7`
- Provide block explorer links for verification

### Time Display

- Use user's local timezone
- Format: `YYYY-MM-DD HH:mm:ss`
- Relative time: within 24h use "X minutes ago", "X hours ago"

## Edge Cases and Error Handling

| Scenario | Action |
|----------|--------|
| MCP Server not configured | Abort all operations, show Cursor config guide |
| MCP Server unreachable | Abort all operations, show network check prompt |
| Invalid token contract address | Prompt that address format is wrong, ask user to confirm |
| Token not found on specified chain | Prompt that token was not found, suggest checking chain and address |
| `market_get_kline` returns empty | Prompt that no K-line data for this token, may be new or very low volume |
| `token_get_risk_info` returns `unknown` | Prompt that no security audit info was found, suggest user investigate |
| `token_ranking` returns empty list | Prompt that no ranking data for this chain |
| Query timeout | Prompt network issue, suggest retry later |
| MCP Server returns unknown error | Show error message as-is |
| User provides token symbol instead of address | Try resolving via `token_get_coin_info` or context to contract address |
| Unsupported chain id | Show list of supported chains |

## Security Rules

1. **Read-only**: This Skill only queries public data; no on-chain writes, no auth, no trade confirmation gate.
2. **Objective security audit display**: Present `token_get_risk_info` results as-is; do not add subjective judgment. For high risk, clearly label but do not decide for the user.
3. **New token risk notice**: When showing new token lists, add a risk reminder; new tokens generally carry higher risk.
4. **No operations when MCP Server unavailable**: If first connection check fails, abort all further steps; on connection errors during runtime, show prompt promptly.
5. **Transparent MCP Server errors**: Show all MCP Server error messages to the user as-is; do not hide or alter.
6. **No investment advice**: Market data is for reference only; Agent does not recommend or judge token investment value.
