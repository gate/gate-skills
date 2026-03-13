---
name: gate-exchange-tradfi
version: "2026.3.13-6"
updated: "2026-03-13"
description: "Gate TradFi (traditional finance) read-only query skill using MCP tools prefixed with cex_tradfi. Use this skill whenever the user asks to query TradFi order list, order history, current or historical positions, category list, symbol list, ticker, symbol kline, user assets, or MT5 account info on Gate. Trigger phrases include 'TradFi orders', 'order history', 'positions', 'position history', 'category list', 'symbol list', 'ticker', 'kline', 'my assets', 'MT5 account', or any request to view TradFi data. Do not use for placing orders or transferring funds."
---

# Gate TradFi Query Suite

This skill is the single entry for Gate TradFi (traditional finance) **read-only** operations. All MCP tools used are prefixed with `cex_tradfi`. It supports four query modules: orders and order history, current and historical positions, market data (category list, symbol list, ticker, symbol kline), and user assets plus MT5 account information. No order placement or fund transfer.

## Sub-Modules


| Module              | Description                                      | Trigger keywords                                                                               |
| ------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| **Query orders**    | Order list, order history                       | `orders`, `open orders`, `order history`                                                        |
| **Query positions** | Current position list, position history          | `positions`, `my positions`, `position history`, `holdings`, `current position`                |
| **Query market**    | Category list, symbol list, ticker, symbol kline | `category`, `categories`, `symbol list`, `symbols`, `ticker`, `kline`, `candlestick`, `market` |
| **Query assets**    | User balance/asset info, MT5 account info        | `assets`, `balance`, `account`, `my funds`, `MT5`, `mt5 account`                               |


## Routing Rules


| Intent              | Example phrases                                                                             | Route to                                                             |
| ------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Query orders**    | "My TradFi orders", "order history", "show open orders", "order status"                     | Read `references/query-orders.md`                                    |
| **Query positions** | "My positions", "position history", "current holdings", "what am I holding"                 | Read `references/query-positions.md`                                 |
| **Query market**    | "TradFi categories", "category list", "symbol list", "ticker", "kline for X", "market data" | Read `references/query-market.md`                                    |
| **Query assets**    | "My assets", "balance", "account balance", "MT5 account", "my MT5 info"                     | Read `references/query-assets.md`                                    |
| **Unclear**         | "TradFi", "show me my TradFi"                                                               | **Clarify**: list the four modules or ask which data the user wants. |


## MCP Tools


| #  | Tool                                   | Purpose |
| ---| --------------------------------------- | ------- |
| 1  | `cex_tradfi_query_order_list`                | List open orders. Use only parameters documented in the MCP . |
| 2  | `cex_tradfi_query_order_history_list`   | Query order history list (filled/cancelled). Use only MCP-documented parameters. |
| 3  | `cex_tradfi_query_position_list`             | List current positions. |
| 4  | `cex_tradfi_query_position_history_list`      | List historical positions/settlements. |
| 5  | `cex_tradfi_query_categories`           | Query TradFi category list. |
| 6  | `cex_tradfi_query_symbols`               | List symbols (by category if supported). |
| 7  | `cex_tradfi_query_symbol_ticker`                | Get ticker(s) for symbol(s). |
| 8  | `cex_tradfi_query_symbol_kline`           | Get kline/candlestick for symbol. |
| 9  | `cex_tradfi_query_user_assets`               | Get user account/balance (assets). |
| 10 | `cex_tradfi_query_mt5_account_info`           | Get MT5 account info (or equivalent MT5 tool). |


## Execution

### 1. Intent and parameters

- Determine module: Query orders / Query positions / Query market / Query assets.
- For each MCP tool call, use **only the parameters defined in the Gate TradFi MCP tool definition**. Do not pass parameters that are not documented in the MCP.
- Extract from user message only those keys that the MCP actually supports for the chosen tool (e.g. symbol, category, interval, limit only if documented).
- **Missing**: If the user request is ambiguous (e.g. "my TradFi"), list the four modules and ask which data they want, or infer from keywords.

### 2. Read sub-module and call tools

- Load the corresponding reference under `references/` and follow its Workflow.
- Call MCP tools with the parameters extracted or prompted. This skill is **read-only**; do not call any create/cancel/amend/update tools.

### 3. Report

- Use the sub-module’s Report Template to format the response (tables for orders/positions/tickers, clear labels for assets).

## Domain Knowledge

- **TradFi** here means Gate’s traditional finance product set (e.g. FX, MT5, or other non-crypto instruments). Symbols and categories are product-specific.
- **Orders**: Open orders → `cex_tradfi_query_order_list`. Order history → `cex_tradfi_query_order_history_list`. Use only MCP-documented parameters.
- **Positions**: Current positions are live; history may be paginated or time-filtered.
- **Market**: **Category list** returns TradFi product categories; **symbol list** returns tradeable symbols (optionally by category). **Ticker** returns last price, 24h change, volume for symbol(s). **Kline** needs symbol, `interval` (e.g. 1m, 5m, 1d), and optional `limit` or time range.
- **Assets**: User account/balance may be per asset or aggregated. **MT5 account** info is separate (login, server, balance, etc.); use `cex_tradfi_query_mt5_account_info` or equivalent.

## Error Handling


| Situation                  | Action                                                                                                  |
| -------------------------- | ------------------------------------------------------------------------------------------------------- |
| Tool not found / 4xx/5xx   | Tell user the TradFi service or tool may be unavailable; suggest retry or check Gate MCP configuration. |
| Empty list                 | Report "No open orders" / "No positions" / "No symbols" etc., and do not assume error.                 |
| Invalid symbol / order not found | Report "Order not found" or "Symbol not found" and suggest checking symbol list.                      |
| Auth / permission error    | Do not expose credentials; ask user to check API key or MCP auth for TradFi.                            |


## Safety Rules

- **Read-only**: This skill must only query data. Do not call any order-placement, cancel, amend, or transfer tools.
- **Confirmation**: Not required for query-only flows; only display data after tool success.
- **Sensitive data**: When showing balances or positions, do not log or store; display only in the current response.

## Report Template

After each query, output a short standardized result:

- **Orders**: Table with columns such as symbol, side, size, price, status, time (from list response).
- **Positions**: Table with position fields (e.g. symbol, side, size, entry, margin) or "No open positions."
- **Market**: Category list table; or symbol list table; or ticker table (symbol, last, 24h change, volume); or symbol kline summary (interval, range, OHLC).
- **Assets**: List of assets and balances (available, locked if applicable), or "Unable to load assets" on error. **MT5**: Account/server/balance/equity table or "Unable to load MT5 account" on error.

