---
name: gate-exchange-tradfi
version: "2026.3.23-1"
updated: "2026-03-23"
description: "Gate TradFi (traditional finance) skill using MCP tools prefixed with cex_tradfi. Use this skill whenever the user asks to query or trade TradFi on Gate: query order list, order history, positions, category/symbol list, ticker, kline, user assets, MT5 account; or place order, amend order, cancel order, modify position, close position. Trigger phrases include 'TradFi orders', 'order history', 'positions', 'place order', 'amend order', 'cancel order', 'modify position', 'close position', 'symbol list', 'ticker', 'kline', 'my assets', 'MT5 account'. Do not use for fund transfer."
---

# Gate TradFi Suite

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

- cex_tradfi_query_categories
- cex_tradfi_query_mt5_account_info
- cex_tradfi_query_order_history_list
- cex_tradfi_query_order_list
- cex_tradfi_query_position_history_list
- cex_tradfi_query_position_list
- cex_tradfi_query_symbol_detail
- cex_tradfi_query_symbol_kline
- cex_tradfi_query_symbol_ticker
- cex_tradfi_query_symbols
- cex_tradfi_query_user_assets

**Execution Operations (Write)**

- cex_tradfi_close_position
- cex_tradfi_create_tradfi_order
- cex_tradfi_delete_order
- cex_tradfi_update_order
- cex_tradfi_update_position

### Authentication
- API Key Required: Yes (see skill doc/runtime MCP deployment)
- Permissions: Tradfi:Write
- Get API Key: https://www.gate.io/myaccount/profile/api-key/manage

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## Sub-Modules


| Module              | Description                                      | Trigger keywords                                                                               |
| ------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| **Query orders**    | Order list, order history                       | `orders`, `open orders`, `order history`                                                        |
| **Query positions** | Current position list, position history          | `positions`, `my positions`, `position history`, `holdings`, `current position`                |
| **Query market**    | Category list, symbol list, ticker, symbol kline | `category`, `categories`, `symbol list`, `symbols`, `ticker`, `kline`, `candlestick`, `market` |
| **Query assets**    | User balance/asset info, MT5 account info        | `assets`, `balance`, `account`, `my funds`, `MT5`, `mt5 account`                               |
| **Place order**     | Create new order (supports take-profit/stop-loss at creation) | `place order`, `create order`, `open order`, `buy`, `sell`, `long`, `short`, `take-profit`, `stop-loss` |
| **Amend order**     | Change order price, take-profit, or stop-loss (size not supported) | `amend order`, `modify order`, `change price`, `take-profit`, `stop-loss`                        |
| **Cancel order**    | Cancel one or more orders                       | `cancel order`, `revoke order`, `cancel`                                                            |
| **Modify position** | Change position take-profit/stop-loss only (leverage, margin not supported) | `modify position`, `take-profit`, `stop-loss`, `change take-profit`, `change stop-loss`            |
| **Close position**  | Full or partial close                           | `close position`, `close`, `close all`, `flat`                                                    |


## Routing Rules

| Intent              | Example phrases                                                                             | Route to                                                             |
| ------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Query orders**    | "My TradFi orders", "order history", "show open orders", "order status"                     | Read `references/query-orders.md`                                    |
| **Query positions** | "My positions", "position history", "current holdings", "what am I holding"                 | Read `references/query-positions.md`                                 |
| **Query market**    | "TradFi categories", "category list", "symbol list", "ticker", "kline for X", "market data" | Read `references/query-market.md`                                    |
| **Query assets**    | "My assets", "balance", "account balance", "MT5 account", "my MT5 info"                     | Read `references/query-assets.md`                                    |
| **Place order**     | "Place order", "buy EURUSD", "sell XAUUSD 0.1", "open long", "order with take-profit/stop-loss" | Read `references/place-order.md`                                     |
| **Amend order**     | "Amend order", "change price to X", "take-profit", "stop-loss"                             | Read `references/amend-order.md`                                     |
| **Cancel order**    | "Cancel order", "cancel all orders", "revoke order"                                         | Read `references/cancel-order.md`                                    |
| **Modify position** | "Modify position", "take-profit", "stop-loss", "change take-profit/stop-loss"               | Read `references/modify-position.md`                                 |
| **Close position**  | "Close position", "close all", "close half", "flat"                                         | Read `references/close-position.md`                                  |
| **Unclear**         | "TradFi", "show me my TradFi"                                                               | **Clarify**: list query and trading modules or ask which the user wants. |


## MCP Tools

**Query (read-only)** — use only MCP-documented parameters.

| #  | Tool                                   | Purpose |
| ---| --------------------------------------- | ------- |
| 1  | `cex_tradfi_query_order_list`           | List open orders. |
| 2  | `cex_tradfi_query_order_history_list`   | Query order history list (filled/cancelled). |
| 3  | `cex_tradfi_query_position_list`       | List current positions. |
| 4  | `cex_tradfi_query_position_history_list` | List historical positions/settlements. |
| 5  | `cex_tradfi_query_categories`           | Query TradFi category list. |
| 6  | `cex_tradfi_query_symbols`              | List symbols (by category if supported). |
| 7  | `cex_tradfi_query_symbol_ticker`        | Get ticker(s) for symbol(s). |
| 8  | `cex_tradfi_query_symbol_detail`        | Get symbol config (required before place order: leverages, min_order_volume, step_order_volume). If no result, symbol may not exist — do not place order. |
| 9  | `cex_tradfi_query_symbol_kline`         | Get kline/candlestick for symbol. |
| 10 | `cex_tradfi_query_user_assets`          | Get user account/balance (assets). |
| 11 | `cex_tradfi_query_mt5_account_info`     | Get MT5 account info. |

**Trading (write)** — exact tool names and parameters must match the Gate TradFi MCP tool definition. Conditions and value limits (required/optional, ranges, allowed symbols) must be declared in the skill and in each reference; do not pass undocumented parameters.

| #  | Tool (name per MCP)              | Purpose |
| ---| ---------------------------------| ------- |
| 12 | `cex_tradfi_create_tradfi_order` | Place new order; supports take-profit/stop-loss. Before calling: use `cex_tradfi_query_symbol_detail` to validate symbol and get min_order_volume, step_order_volume, leverages. |
| 13 | `cex_tradfi_update_order`        | Amend order price, take-profit, stop-loss only (size not supported). |
| 14 | `cex_tradfi_delete_order`       | Cancel/delete one order. Does not support batch; one order per call. |
| 15 | `cex_tradfi_update_position`    | Modify position take-profit/stop-loss price only (leverage, margin not supported). |
| 16 | `cex_tradfi_close_position` (or MCP equivalent) | Close position (full or partial). Full close: position identifier only, do not pass size/close_volume. |


## Parameter conditions and limits

- For each MCP tool, **input conditions and limits** (required/optional parameters, value ranges, allowed symbols, precision) are defined in the MCP. This skill and each reference document must **declare** those conditions and limits so the agent and user know what can be sent.
- In each trading reference (`place-order.md`, `amend-order.md`, `cancel-order.md`, `modify-position.md`, `close-position.md`), include a **Parameters** section that states: required/optional params, value constraints, and any MCP-specific rules. Do not add parameters that the MCP does not document.
- If the user provides a value outside allowed range or a missing required param, ask for correction before building the confirmation payload.


## User confirmation (trading only)

- **Before** calling any trading MCP tool (place order, amend order, cancel order, modify position, close position): **output all parameters** that will be sent to the MCP so the user can review them. Ask the user to confirm (e.g. "Confirm: place order with symbol=X, side=Y, size=Z, price=W. Reply yes to execute."). **Do not** call the tool until the user explicitly confirms.
- This applies to every write operation; query-only flows do not require confirmation.


## Response parameter explanation (trading only)

- **After** the trading MCP tool returns: in the response to the user, **explain the parameters that were used** (e.g. symbol, side, size, price, order_id, or position identifier) and the outcome (e.g. order created, order amended, order cancelled, position modified, position closed). Include a short summary table or list of the sent parameters and the result (success or error code/message). This is declared in this skill so the agent always reports back what was sent and what happened.


## Execution

### 1. Intent and parameters

- Determine module: Query (orders, positions, market, assets) or Trading (place, amend, cancel, modify position, close).
- For each MCP tool call, use **only the parameters defined in the Gate TradFi MCP tool definition**. Do not pass parameters that are not documented in the MCP.
- Extract from user message only those keys that the MCP actually supports. Respect conditions and limits declared in the skill and in the reference.

### 2. Read sub-module and call tools

- Load the corresponding reference under `references/` and follow its Workflow.
- **Query**: Call query tools with extracted/prompted parameters; no confirmation needed.
- **Trading**: Build the parameter set per the reference and MCP; **output parameters for user confirmation**; only after user confirms, call the trading MCP tool; then **in the response, explain the parameters used and the outcome**.

### 3. Report

- **Query**: Use the sub-module Report Template (tables for orders/positions/tickers, assets).
- **Trading**: Use the reference Report Template; include **parameter summary** (what was sent) and **result** (success or error).

## Domain Knowledge

- **TradFi**: Gate’s traditional finance product set (e.g. FX, MT5). Symbols and categories are product-specific.
- **Query**: Orders, positions, market, assets — use only MCP-documented parameters.
- **Trading**: Place/amend/cancel orders and modify/close positions — use only MCP-documented tools and parameters; declare conditions/limits; require user confirmation before execution; explain parameters and outcome in the response.
- **Order id for cancel/amend**: The order id used by `cex_tradfi_delete_order` and `cex_tradfi_update_order` **must** come from **`cex_tradfi_query_order_list`**. Do **not** use the `id` or `log_id` returned by `cex_tradfi_create_tradfi_order` for cancel or amend.

## Error Handling

| Situation                  | Action                                                                                                  |
| -------------------------- | ------------------------------------------------------------------------------------------------------- |
| Tool not found / 4xx/5xx   | Tell user the TradFi service or tool may be unavailable; suggest retry or check Gate MCP configuration. |
| Empty list                 | Report "No open orders" / "No positions" / "No symbols" etc., and do not assume error.                  |
| Invalid symbol / order not found | Report "Order not found" or "Symbol not found" and suggest checking symbol list.                       |
| Auth / permission error    | Do not expose credentials; ask user to check API key or MCP auth for TradFi.                           |
| Trading error (e.g. insufficient margin, invalid price) | Show the error message; in the response, restate the parameters that were sent and suggest correction. |


## Safety Rules

- **Query**: No confirmation required; display data after tool success.
- **Trading**: **Always** output parameters for user confirmation before calling place/amend/cancel/modify/close; **never** execute a write operation without explicit user confirmation. After execution, **always** explain in the response the parameters that were used and the outcome.
- **Sensitive data**: Do not log or store credentials or balances; display only in the current response.

## Report Template

**Query** — After each query:
- **Orders**: Table with columns such as symbol, side, size, price, status, time (from list response).
- **Positions**: Table with position fields (e.g. symbol, side, size, entry, margin) or "No open positions."
- **Market**: Category list; symbol list; ticker table (symbol, last, 24h change, volume); or symbol kline summary (interval, range, OHLC).
- **Assets**: List of assets and balances; or MT5 account/server/balance/equity table; or "Unable to load" on error.

**Trading** — After each place/amend/cancel/modify/close:
- **Parameters used**: List or table of the parameters sent to the MCP (e.g. symbol, side, size, price, order_id).
- **Result**: Success (e.g. order id, status) or error (code/message). Suggest next step if error.

