# Gate DEX Market Skill

Market data and token information query Skill, providing read-only access to on-chain public data.

## Overview

`gate-dex-mcpmarket` is the market/token domain Skill in the Gate DEX MCP Skill set. Based on 7 public query tools from the Gate DEX MCP Server, it provides AI Agents with on-chain market data, token information, and security audit capabilities.

**Key features:**

- All tools are public data queries, **no authentication required** (no `mcp_token` needed)
- Read-only operations, no on-chain writes
- Often called cross-Skill by other Skills (swap, dapp) for token info and security review assistance

## Tool List

| # | Tool name | Function | Key parameters |
|---|-----------|----------|-----------------|
| 1 | `market_get_kline` | K-line data | `chain`, `token_address`, `interval`, `limit` |
| 2 | `market_get_tx_stats` | On-chain trading stats | `chain`, `token_address`, `period` |
| 3 | `market_get_pair_liquidity` | Pair liquidity | `chain`, `token_address` |
| 4 | `token_get_coin_info` | Token details | `chain`, `token_address` |
| 5 | `token_ranking` | Token rankings | `chain`, `sort_by`, `order`, `limit` |
| 6 | `token_get_coins_range_by_created_at` | New token discovery | `chain`, `start_time`, `end_time`, `limit` |
| 7 | `token_get_risk_info` | Security risk audit | `chain`, `address` |

## Operation Flows

| Flow | Scenario | Tools involved |
|------|----------|----------------|
| A | View token market | `market_get_kline` + `market_get_tx_stats` + `market_get_pair_liquidity` (parallel) |
| B | View token details | `token_get_coin_info` |
| C | Token rankings | `token_ranking` |
| D | Security review | `token_get_risk_info` |
| E | New token discovery | `token_get_coins_range_by_created_at` |

Run MCP Server connection check before first operation in a session; runtime error fallback for subsequent operations.

## Skill Routing

Post-market-data operation routing:

| User intent | Target Skill |
|-------------|--------------|
| Buy/sell token | `gate-dex-mcpswap` |
| Transfer token | `gate-dex-mcptransfer` |
| View holdings | `gate-dex-mcpwallet` |
| View trade/Swap history | `gate-dex-mcpwallet` |
| Interact with DApp | `gate-dex-mcpdapp` |

## Cross-Skill Collaboration

This Skill often acts as a **data provider** for other Skills:

| Caller | Scenario | Tools used |
|--------|----------|------------|
| `gate-dex-mcpswap` | Query token info before Swap | `token_get_coin_info` |
| `gate-dex-mcpswap` | Security review before Swap | `token_get_risk_info` |
| `gate-dex-mcpdapp` | Contract security review before DApp interaction | `token_get_risk_info` |

Typical cross-Skill workflow:

```
gate-dex-mcpmarket (query token info → security review)
  → gate-dex-mcpwallet (verify balance)
    → gate-dex-mcpswap (quote → confirm → execute)
```

## Prerequisites

Ensure Gate DEX MCP Server is configured in Cursor before use:

```
Name: gate-wallet
Type: HTTP
URL: https://your-mcp-server-domain/mcp
```

See [README.md](../../README.md) for detailed configuration.

## File Structure

```
gate-dex-mcpmarket/
├── README.md          # This file — Skill overview
├── SKILL.md           # Agent instruction file (tool specs, flows, security rules)
└── CHANGELOG.md       # Change log
```

## Related Skills

- [gate-dex-mcpauth](../gate-dex-mcpauth/) — Authentication (Google OAuth)
- [gate-dex-mcpwallet](../gate-dex-mcpwallet/) — Wallet/assets/trade history
- [gate-dex-mcptransfer](../gate-dex-mcptransfer/) — Transfer
- [gate-dex-mcpswap](../gate-dex-mcpswap/) — Swap/DEX
- [gate-dex-mcpdapp](../gate-dex-mcpdapp/) — DApp interaction
