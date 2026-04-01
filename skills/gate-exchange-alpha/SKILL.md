---
name: gate-exchange-alpha
version: "2026.3.23-1"
updated: "2026-03-23"
description: "Gate Alpha token discovery, market viewing, trading, account, and order management skill. Use this skill whenever the user asks to browse Alpha tokens, check Alpha market tickers, buy or sell Alpha tokens, view Alpha holdings, check transaction history, or manage Alpha orders. Trigger phrases include 'alpha tokens', 'alpha market', 'alpha holdings', 'alpha portfolio', 'buy alpha', 'sell alpha', 'alpha order', 'alpha history', or any request involving Gate Alpha operations."
---

# Gate Alpha Assistant

This skill is the single entry for Gate Alpha operations. It supports **seven modules**: Token Discovery, Market Viewing, Trading (Buy), Trading (Sell), Account & Holdings, Account Book, and Order Management. User intent is routed to the matching workflow.

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate (main) | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- cex_alpha_get_alpha_order
- cex_alpha_list_alpha_account_book
- cex_alpha_list_alpha_accounts
- cex_alpha_list_alpha_currencies
- cex_alpha_list_alpha_orders
- cex_alpha_list_alpha_tickers
- cex_alpha_list_alpha_tokens
- cex_alpha_quote_alpha_order

**Execution Operations (Write)**

- cex_alpha_place_alpha_order

### Authentication
- API Key Required: Yes (see skill doc/runtime MCP deployment)
- Permissions: Alpha:Write
- Get API Key: https://www.gate.io/myaccount/profile/api-key/manage

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## Module Overview

| Module | Description | Trigger Keywords |
|--------|-------------|------------------|
| **Token Discovery** | Browse tradable currencies, filter tokens by chain/platform/address, check token details | `alpha tokens`, `what coins`, `which chain`, `token address`, `token details` |
| **Market Viewing** | Check all or specific Alpha token tickers, prices, 24h changes | `alpha price`, `market`, `ticker`, `how much is`, `what price` |
| **Trading (Buy)** | Buy Alpha tokens with USDT, support default or custom slippage, optional order tracking | `buy`, `买`, `购买`, `入手`, `帮我买` |
| **Trading (Sell)** | Sell Alpha tokens (full or partial), optional order tracking | `sell`, `卖`, `卖出`, `清仓`, `卖掉` |
| **Account & Holdings** | View Alpha account balances and calculate portfolio market value | `my holdings`, `my balance`, `portfolio value`, `how much do I have` |
| **Account Book** | View Alpha account transaction history by time range | `transaction history`, `流水`, `资产变动`, `account book`, `变动记录` |
| **Order Management** | Check order status, view historical buy/sell orders, search orders by time | `order status`, `订单`, `买单`, `卖单`, `order history` |

## Routing Rules

| Intent | Example Phrases | Route To |
|--------|-----------------|----------|
| **Token discovery** | "What coins can I trade on Alpha?", "Show me Solana tokens", "Look up this address" | Read `references/token-discovery.md` |
| **Market viewing** | "What's the price of trump?", "How's the Alpha market?" | Read `references/market-viewing.md` |
| **Trading (buy)** | "帮我买 5u ELON", "Buy 100u trump with 10% slippage" | Read `references/trading-buy.md` |
| **Trading (sell)** | "把 ELON 全部卖掉", "卖掉一半的 trump" | Read `references/trading-sell.md` |
| **Account & holdings** | "What coins do I hold?", "How much is my Alpha portfolio worth?" | Read `references/account-holdings.md` |
| **Account book** | "最近一周的资产变动记录", "看看昨天的资产变动" | Read `references/account-book.md` |
| **Order management** | "我刚才那笔买单成功了吗？", "看看我买 ELON 的订单" | Read `references/order-management.md` |
| **Unclear** | "Tell me about Alpha", "Help with Alpha" | **Clarify**: ask which module the user needs |

## MCP Tools

| # | Tool | Auth | Purpose |
|---|------|------|---------|
| 1 | `cex_alpha_list_alpha_currencies` | No | List all tradable Alpha currencies with chain, address, precision, status |
| 2 | `cex_alpha_list_alpha_tokens` | No | Filter tokens by chain, launch platform, or contract address |
| 3 | `cex_alpha_list_alpha_tickers` | No | Get latest price, 24h change, volume, market cap for Alpha tokens |
| 4 | `cex_alpha_list_alpha_accounts` | Yes | Query Alpha account balances (available + locked per currency) |
| 5 | `cex_alpha_quote_alpha_order` | Yes | Get a price quote for a buy/sell order (returns quote_id, valid 1 min) |
| 6 | `cex_alpha_place_alpha_order` | Yes | Place a buy/sell order using a quote_id |
| 7 | `cex_alpha_get_alpha_order` | Yes | Get details of a single order by order_id |
| 8 | `cex_alpha_list_alpha_orders` | Yes | List orders with filters (currency, side, status, time range) |
| 9 | `cex_alpha_list_alpha_account_book` | Yes | Query account transaction history by time range |

## Domain Knowledge

### Alpha Platform Overview

- Gate Alpha is a platform for early-stage token trading, supporting tokens across multiple blockchains.
- Tokens are identified by `currency` symbol (e.g., `memeboxtrump`) rather than standard ticker symbols.
- Trading status values: `1` = actively trading, `2` = suspended, `3` = delisted.

### Supported Chains

solana, eth, bsc, base, world, sui, arbitrum, avalanche, polygon, linea, optimism, zksync, gatelayer

**Note**: Chain names may be returned in different cases depending on the endpoint (e.g., `SOLANA` vs `solana`). Normalize to lowercase when comparing.

### Supported Launch Platforms

meteora_dbc, fourmeme, moonshot, pump, raydium_launchlab, letsbonk, gatefun, virtuals

### Trading Mechanics

- **Buy amount**: USDT quantity (e.g., `amount="5"` means spend 5 USDT).
- **Sell amount**: Token quantity (e.g., `amount="1000"` means sell 1000 tokens).
- **Quote validity**: `quote_id` from `cex_alpha_quote_alpha_order` expires after **1 minute**. Re-quote if expired.
- **Gas modes**: Input `"speed"` (default) or `"custom"` (with slippage). API returns `gasMode` as `"1"` (speed) or `"2"` (custom).
- **Order statuses**: `1` = Processing, `2` = Success, `3` = Failed, `4` = Cancelled, `5` = Transferring, `6` = Cancelling transfer. Terminal statuses: 2, 3, 4.

### API Field Naming Conventions

All API endpoints use **snake_case** naming. Key fields by endpoint:
- `/alpha/currencies`: `currency`, `name`, `chain`, `address`, `amount_precision`, `precision`, `status`
- `/alpha/tickers`: `currency`, `last`, `change`, `volume`, `market_cap`
- `/alpha/accounts`: `currency`, `available`, `locked`, `token_address`, `chain`
- `/alpha/account_book`: `id`, `time`, `currency`, `change`, `balance`
- `/alpha/orders` (GET): `order_id`, `tx_hash`, `side`, `usdt_amount`, `currency`, `currency_amount`, `status`, `gas_mode`, `chain`, `gas_fee`, `transaction_fee`, `create_time`, `failed_reason`
- Empty query results may return `[{}, {}]` (array with empty objects) instead of `[]`. Check for valid fields before processing.

### Key Constraints

- All market data endpoints (`currencies`, `tickers`, `tokens`) are public and do not require authentication.
- Account, trading, and order endpoints require API Key authentication.
- Pagination: use `page` and `limit` parameters for large result sets.
- Rate limits: quote 10r/s, place order 5r/s, other endpoints 200r/10s.

## Execution

### 1. Intent Classification

Classify the user request into one of seven modules: Token Discovery, Market Viewing, Trading (Buy), Trading (Sell), Account & Holdings, Account Book, or Order Management.

### 2. Route and Load

Load the corresponding reference document and follow its workflow.

### 3. Return Result

Return the result using the report template defined in each sub-module.

## Error Handling

| Error Type | Typical Cause | Handling Strategy |
|------------|---------------|-------------------|
| Currency not found | Invalid or misspelled currency symbol | Suggest searching via `cex_alpha_list_alpha_currencies` or `cex_alpha_list_alpha_tokens` |
| Token suspended | Trading status is 2 (suspended) | Inform user that the token is currently suspended from trading |
| Token delisted | Trading status is 3 (delisted) | Inform user that the token has been delisted |
| Empty result | No tokens match the filter criteria | Clarify filter parameters (chain, platform, address) and suggest alternatives |
| Authentication required | Calling authenticated endpoint without credentials | Inform user that API Key authentication is needed; guide to setup |
| Pagination overflow | Requested page beyond available data | Return last available page and inform user of total count |
| Quote expired | quote_id used after 1-minute validity window | Re-call `cex_alpha_quote_alpha_order` to obtain a fresh quote_id |
| Insufficient balance | Sell amount exceeds available balance | Inform user of actual available balance and suggest adjusting the amount |
| Order failed | On-chain transaction failed | Report the `failed_reason` from the order detail and suggest retrying |
| Order timeout | Polling exceeded 60 seconds without terminal status | Inform user the order is still processing; provide order_id for manual follow-up |
| Rate limit exceeded | Too many requests in short period | Wait briefly and retry; inform user if persistent |

## Safety Rules

- **Order confirmation**: NEVER place a buy or sell order without showing the quote details and receiving explicit user confirmation.
- **Token validation**: Always verify `status=1` before initiating a trade. Abort if suspended or delisted.
- **Balance verification**: Before selling, always confirm `available >= sell_amount`. Report actual balance if insufficient.
- **Quote freshness**: Always check quote_id validity (1-minute window). Re-quote if the user delays confirmation.
- Never fabricate token data. If a query returns empty results, report it honestly.
- When displaying token addresses, show the full address to avoid confusion between similarly named tokens.
- Always verify trading status before suggesting a token is tradable.
