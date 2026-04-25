---
name: gate-exchange-tradfi
description: "Gate TradFi (traditional finance) skill. Use when the user asks to query or trade traditional finance assets like forex or commodities on Gate. Triggers on 'TradFi orders', 'MT5 account', 'TradFi positions'. Do NOT use for fund transfer."
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "💱"
    os:
      - darwin
      - linux
    primaryEnv: GATE_API_KEY
    requires:
      bins:
        - gate-cli
      env:
        - GATE_API_KEY
        - GATE_API_SECRET

    install:
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux x64)"
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux arm64)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Intel)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Apple Silicon)"
---

### Resolving `gate-cli` (binary path)

Resolve **`gate-cli`** in order: **(1)** **`command -v gate-cli`** and **`gate-cli --version`** succeeds; **(2)** **`${HOME}/.local/bin/gate-cli`** if executable; **(3)** **`${HOME}/.openclaw/skills/bin/gate-cli`** if executable. Canonical rules: [`exchange-runtime-rules.md`](https://github.com/gate/gate-skills/blob/master/skills/exchange-runtime-rules.md) §4 (or [`gate-runtime-rules.md`](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) §4).


# Gate TradFi Suite

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

## Skill Dependencies


### gate-cli commands used

**Query Operations (Read-only)**

- `gate-cli cex tradfi market categories`
- `gate-cli cex tradfi account info`
- `gate-cli cex tradfi order history`
- `gate-cli cex tradfi order list`
- `gate-cli cex tradfi position history`
- `gate-cli cex tradfi position list`
- `gate-cli cex tradfi market symbol`
- `gate-cli cex tradfi market kline`
- `gate-cli cex tradfi market ticker`
- `gate-cli cex tradfi market symbols`
- `gate-cli cex tradfi account assets`

**Execution Operations (Write)**

- `gate-cli cex tradfi position close`
- `gate-cli cex tradfi order create`
- `gate-cli cex tradfi order cancel`
- `gate-cli cex tradfi order update`
- `gate-cli cex tradfi position update`

### Authentication
- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- **Permissions:** Tradfi:Write
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- **Required:** `gate-cli` (run `sh ./setup.sh` from this skill directory if missing; optional `GATE_CLI_SETUP_MODE=release`).
- Add `$HOME/.openclaw/skills/bin` to **`PATH`** if you invoke `gate-cli` by name (or the directory where [`setup.sh`](./setup.sh) installs it).
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`** — that is equivalent valid config for `gate-cli`. When **both** are unset or empty, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Do not proceed with authenticated calls until the CLI behaves as expected (e.g. **`gate-cli --version`** or a read-only **`gate-cli cex ...`** command from this skill); confirm credentials resolve before mutating operations.

## Execution mode

**Read and strictly follow** [`references/gate-cli.md`](./references/gate-cli.md), then execute this skill's TradFi workflow.

- `SKILL.md` keeps routing and domain constraints.
- `references/gate-cli.md` is the authoritative `gate-cli` execution contract for query/mutation separation, confirmation gates, and post-action verification.

## Sub-Modules


| Module | Description | Trigger keywords |
| ------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| **Query orders** | Order list, order history | `orders`, `open orders`, `order history` |
| **Query positions** | Current position list, position history | `positions`, `my positions`, `position history`, `holdings`, `current position` |
| **Query market** | Category list, symbol list, ticker, symbol kline | `category`, `categories`, `symbol list`, `symbols`, `ticker`, `kline`, `candlestick`, `market` |
| **Query assets** | User balance/asset info, MT5 account info | `assets`, `balance`, `account`, `my funds`, `MT5`, `mt5 account` |
| **Place order** | Create new order (supports take-profit/stop-loss at creation) | `place order`, `create order`, `open order`, `buy`, `sell`, `long`, `short`, `take-profit`, `stop-loss` |
| **Amend order** | Change order price, take-profit, or stop-loss (size not supported) | `amend order`, `modify order`, `change price`, `take-profit`, `stop-loss` |
| **Cancel order** | Cancel one or more orders | `cancel order`, `revoke order`, `cancel` |
| **Modify position** | Change position take-profit/stop-loss only (leverage, margin not supported) | `modify position`, `take-profit`, `stop-loss`, `change take-profit`, `change stop-loss` |
| **Close position** | Full or partial close | `close position`, `close`, `close all`, `flat` |


## Routing Rules

| Intent | Example phrases | Route to |
| ------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Query orders** | "My TradFi orders", "order history", "show open orders", "order status" | Read `references/query-orders.md` |
| **Query positions** | "My positions", "position history", "current holdings", "what am I holding" | Read `references/query-positions.md` |
| **Query market** | "TradFi categories", "category list", "symbol list", "ticker", "kline for X", "market data" | Read `references/query-market.md` |
| **Query assets** | "My assets", "balance", "account balance", "MT5 account", "my MT5 info" | Read `references/query-assets.md` |
| **Place order** | "Place order", "buy EURUSD", "sell XAUUSD 0.1", "open long", "order with take-profit/stop-loss" | Read `references/place-order.md` |
| **Amend order** | "Amend order", "change price to X", "take-profit", "stop-loss" | Read `references/amend-order.md` |
| **Cancel order** | "Cancel order", "cancel all orders", "revoke order" | Read `references/cancel-order.md` |
| **Modify position** | "Modify position", "take-profit", "stop-loss", "change take-profit/stop-loss" | Read `references/modify-position.md` |
| **Close position** | "Close position", "close all", "close half", "flat" | Read `references/close-position.md` |
| **Unclear** | "TradFi", "show me my TradFi" | **Clarify**: list query and trading modules or ask which the user wants. |


## gate-cli command index

**Query (read-only)** — use only MCP-documented parameters.

| # | Tool | Purpose |
| ---| --------------------------------------- | ------- |
| 1 | `gate-cli cex tradfi order list` | List open orders. |
| 2 | `gate-cli cex tradfi order history` | Query order history list (filled/cancelled). |
| 3 | `gate-cli cex tradfi position list` | List current positions. |
| 4 | `gate-cli cex tradfi position history` | List historical positions/settlements. |
| 5 | `gate-cli cex tradfi market categories` | Query TradFi category list. |
| 6 | `gate-cli cex tradfi market symbols` | List symbols (by category if supported). |
| 7 | `gate-cli cex tradfi market ticker` | Get ticker(s) for symbol(s). |
| 8 | `gate-cli cex tradfi market symbol` | Get symbol config (required before place order: leverages, min_order_volume, step_order_volume). If no result, symbol may not exist — do not place order. |
| 9 | `gate-cli cex tradfi market kline` | Get kline/candlestick for symbol. |
| 10 | `gate-cli cex tradfi account assets` | Get user account/balance (assets). |
| 11 | `gate-cli cex tradfi account info` | Get MT5 account info. |

**Trading (write)** — exact tool names and parameters must match the Gate TradFi MCP tool definition. Conditions and value limits (required/optional, ranges, allowed symbols) must be declared in the skill and in each reference; do not pass undocumented parameters.

| # | Tool (name per MCP) | Purpose |
| ---| ---------------------------------| ------- |
| 12 | `gate-cli cex tradfi order create` | Place new order; supports take-profit/stop-loss. Before calling: use `gate-cli cex tradfi market symbol` to validate symbol and get min_order_volume, step_order_volume, leverages. |
| 13 | `gate-cli cex tradfi order update` | Amend order price, take-profit, stop-loss only (size not supported). |
| 14 | `gate-cli cex tradfi order cancel` | Cancel/delete one order. Does not support batch; one order per call. |
| 15 | `gate-cli cex tradfi position update` | Modify position take-profit/stop-loss price only (leverage, margin not supported). |
| 16 | `gate-cli cex tradfi position close` (or MCP equivalent) | Close position (full or partial). Full close: position identifier only, do not pass size/close_volume. |


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
- **Order id for cancel/amend**: The order id used by `gate-cli cex tradfi order cancel` and `gate-cli cex tradfi order update` **must** come from **`gate-cli cex tradfi order list`**. Do **not** use the `id` or `log_id` returned by `gate-cli cex tradfi order create` for cancel or amend.

## Error Handling

| Situation | Action |
| -------------------------- | ------------------------------------------------------------------------------------------------------- |
| Tool not found / 4xx/5xx | Tell user the TradFi service or tool may be unavailable; suggest retry or check Gate MCP configuration. |
| Empty list | Report "No open orders" / "No positions" / "No symbols" etc., and do not assume error. |
| Invalid symbol / order not found | Report "Order not found" or "Symbol not found" and suggest checking symbol list. |
| Auth / permission error | Do not expose credentials; ask user to check API key or MCP auth for TradFi. |
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
