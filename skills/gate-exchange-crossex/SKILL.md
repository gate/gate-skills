---
name: gate-exchange-crossex
description: "Gate CrossEx cross-exchange skill. Use when the user asks to trade or query positions across Gate, Binance, OKX, and Bybit simultaneously. Triggers on 'cross exchange', 'Binance order', 'OKX position'."
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


# Gate CrossEx Trading Suite

This skill is the unified entry point for Gate CrossEx cross-exchange trading. It supports lots of **core operations**:
order management, position query, and history query. User intents are routed to corresponding workflows.

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

## Skill Dependencies


### gate-cli commands used

**Query Operations (Read-only)**

- `gate-cli cex cross-ex account get`
- `gate-cli cex cross-ex market fee`
- `gate-cli cex cross-ex market interest-rate`
- `gate-cli cex cross-ex position margin-leverage`
- `gate-cli cex cross-ex order get`
- `gate-cli cex cross-ex position leverage`
- `gate-cli cex cross-ex account book`
- `gate-cli cex cross-ex position adl-rank`
- `gate-cli cex cross-ex market discount-rate`
- `gate-cli cex cross-ex position margin-interests`
- `gate-cli cex cross-ex position margin-history`
- `gate-cli cex cross-ex order history`
- `gate-cli cex cross-ex position history`
- `gate-cli cex cross-ex order trades`
- `gate-cli cex cross-ex position margin-list`
- `gate-cli cex cross-ex order list`
- `gate-cli cex cross-ex position list`
- `gate-cli cex cross-ex market risk-limits`
- `gate-cli cex cross-ex market symbols`
- `gate-cli cex cross-ex market transfer-coins`
- `gate-cli cex cross-ex transfer list`

**Execution Operations (Write)**

- `gate-cli cex cross-ex order cancel`
- `gate-cli cex cross-ex position close`
- `gate-cli cex cross-ex convert create`
- `gate-cli cex cross-ex convert quote`
- `gate-cli cex cross-ex order create`
- `gate-cli cex cross-ex transfer create`
- `gate-cli cex cross-ex account update`
- `gate-cli cex cross-ex position set-margin-leverage`
- `gate-cli cex cross-ex order update`
- `gate-cli cex cross-ex position set-leverage`

### Authentication
- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- **Permissions:** Crx:Write
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- **Required:** `gate-cli` (run `sh ./setup.sh` from this skill directory if missing; optional `GATE_CLI_SETUP_MODE=release`).
- Add `$HOME/.openclaw/skills/bin` to **`PATH`** if you invoke `gate-cli` by name (or the directory where [`setup.sh`](./setup.sh) installs it).
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`** — that is equivalent valid config for `gate-cli`. When **both** are unset or empty, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Do not proceed with authenticated calls until the CLI behaves as expected (e.g. **`gate-cli --version`** or a read-only **`gate-cli cex ...`** command from this skill); confirm credentials resolve before mutating operations.

## Execution mode

**Read and strictly follow** [`references/gate-cli.md`](./references/gate-cli.md), then execute this skill's CrossEx workflow.

- `SKILL.md` keeps route dispatch and feature boundaries.
- `references/gate-cli.md` is the authoritative `gate-cli` execution contract for query/mutation sequencing, confirmation gates, and risk-aware updates.

## Module Overview

| Module | Description | Trigger Keywords |
|---------------|-------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| **Spot** | Limit/market buy/sell, cross-exchange arbitrage | `spot buy`, `spot sell`, `buy spot`, `sell spot` |
| **Margin** | Long/short trading, margin management, auto-borrowing | `margin long`, `margin short`, `long margin`, `short margin` |
| **Futures** | USDT perpetual contracts, dual-direction positions, leverage adjustment | `futures long`, `futures short`, `open long`, `open short` |
| **Transfer** | Cross-exchange fund transfer | `fund transfer`, `cross-exchange transfer`, `transfer`, `move funds` |
| **Convert** | Flash convert and conversion quote workflow | `convert trading`, `flash convert`, `convert`, `quote convert` |
| **Orders** | Query, cancel, amend orders, order history | `query orders`, `cancel order`, `amend order`, `order history`, `list orders` |
| **Positions** | Query all position types, history records | `query positions`, `check positions`, `position history`, `positions` |
| **History** | Query order/position/trade/interest history | `history query`, `trade history`, `interest history`, `history` |

## Routing Rules

| Intent | Example Phrases | Route To |
|-----------------------------|----------------------------------------------------------------------------------------------|---------------------------------------------|
| **Spot Trading** | "Buy 100 USDT worth of BTC", "Sell 0.5 BTC", "Market buy ETH spot" | Read `references/spot-trading.md` |
| **Margin Trading** | "Long 50 USDT worth of XRP on margin", "Short BTC on margin", "10x leverage long" | Read `references/margin-trading.md` |
| **Futures Trading** | "Open 1 BTC futures long position", "Market short ETH", "Adjust leverage to 20x" | Read `references/futures-trading.md` |
| **Cross-Exchange Transfer** | "Transfer 100 USDT from Gate to Binance", "Move ETH from OKX to Gate" | Read `references/transfer.md` |
| **Convert Trading** | "Flash convert 10 USDT to BTC", "Convert 50 USDT to ETH on Gate" | Read `references/convert-trading.md` |
| **Order Management** | "Query all open orders", "Cancel that buy order", "Amend order price", "Query order history" | Read `references/order-management.md` |
| **Position Query** | "Query all my positions", "Show futures positions", "Position history" | Read `references/position-query.md` |
| **History Query** | "Query trade history", "Position history", "Margin interest history", "Account ledger" | Read `references/history-query.md` |
| **Unclear** | "Show account" , "Help me" , "Please Check my account" | **Clarify**: Query account, then guide user |

## gate-cli command index

This skill uses the **CrossEx MCP toolset** with the cex_crx prefix as its only core tool family.

**Scope rule**: Only execute operations explicitly documented in this skill. Only call tools listed in the tables below
or in `references/*.md`. Tools or operations not mentioned here must not be called.

### Tool Naming Convention

- List operations in the cex_crx family query symbols, orders, positions, transfers, or history
- Get operations in the cex_crx family query a single account setting, fee, rate, or order detail
- Create operations in the cex_crx family create an order, transfer, convert quote, or convert order
- Update operations in the cex_crx family update account settings, leverage, or existing orders
- Cancel operations in the cex_crx family cancel an existing order
- Close operations in the cex_crx family close an existing position

### Symbol And Rule Tools

| Tool | Purpose |
|---------------------------------------|--------------------------------------------|
| `gate-cli cex cross-ex market symbols` | List supported CrossEx trading symbols |
| `gate-cli cex cross-ex market risk-limits` | Query symbol risk limit rules |
| `gate-cli cex cross-ex market transfer-coins` | List assets supported for CrossEx transfer |
| `gate-cli cex cross-ex market fee` | Query CrossEx trading fee information |
| `gate-cli cex cross-ex market interest-rate` | Query CrossEx interest rates |
| `gate-cli cex cross-ex market discount-rate` | Query collateral discount rates |

### Account Tools

| Tool | Purpose |
|---------------------------------|---------------------------------------------|
| `gate-cli cex cross-ex account get` | Query CrossEx account overview and balances |
| `gate-cli cex cross-ex account update` | Update CrossEx account settings |
| `gate-cli cex cross-ex account book` | Query CrossEx account ledger entries |

### Transfer And Convert Tools

| Tool | Purpose |
|------------------------------------|----------------------------------|
| `gate-cli cex cross-ex transfer list` | Query transfer history |
| `gate-cli cex cross-ex transfer create` | Create a cross-exchange transfer |
| `gate-cli cex cross-ex convert quote` | Get a flash convert quote |
| `gate-cli cex cross-ex convert create` | Execute a flash convert order |

### Order Tools

| Tool | Purpose |
|-----------------------------------|---------------------------|
| `gate-cli cex cross-ex order list` | Query current open orders |
| `gate-cli cex cross-ex order create` | Create a CrossEx order |
| `gate-cli cex cross-ex order get` | Query order details |
| `gate-cli cex cross-ex order update` | Amend an existing order |
| `gate-cli cex cross-ex order cancel` | Cancel a single order |
| `gate-cli cex cross-ex order history` | Query order history |
| `gate-cli cex cross-ex order trades` | Query trade history |

### Position And Leverage Tools

| Tool | Purpose |
|------------------------------------------------|------------------------------------|
| `gate-cli cex cross-ex position list` | Query current futures positions |
| `gate-cli cex cross-ex position margin-list` | Query current margin positions |
| `gate-cli cex cross-ex position close` | Close an existing CrossEx position |
| `gate-cli cex cross-ex position leverage` | Query futures leverage settings |
| `gate-cli cex cross-ex position set-leverage` | Update futures leverage |
| `gate-cli cex cross-ex position margin-leverage` | Query margin leverage settings |
| `gate-cli cex cross-ex position set-margin-leverage` | Update margin leverage |
| `gate-cli cex cross-ex position history` | Query futures position history |
| `gate-cli cex cross-ex position margin-history` | Query margin position history |
| `gate-cli cex cross-ex position margin-interests` | Query margin interest history |
| `gate-cli cex cross-ex position adl-rank` | Query ADL rank information |

### Usage Guidance

- Use the cex_crx MCP family as the default and only core MCP family for this skill.
- Use list/get tools to query symbol rules, fees, balances, leverage, or supported assets.
- Prefer history and account-book tools when the user asks for records, audit trails, or status verification.

## Execution

### 1. Intent and Parameter Identification

- Determine module (orders/positions/history)
- Extract key parameters:
 - **Trading Pair**: `GATE_SPOT_BTC_USDT`, `GATE_MARGIN_XRP_USDT`, `GATE_FUTURE_ETH_USDT`
 - **Exchange**: `GATE`, `BINANCE`, `OKX`, `BYBIT`
 - **Direction**: `BUY` (buy/long), `SELL` (sell/short)
 - **Quantity**: USDT amount, coin quantity, contract size
 - **Price**: Limit, market
 - **Leverage**: Leverage multiplier (margin/futures only)
 - **Position Side**: `LONG` (long), `SHORT` (short, margin/futures only)
- **Missing Parameters**: If required parameters are missing, ask user

### 2. Pre-checks

- **Trading Pair**: Call `gate-cli cex cross-ex market symbols` to verify
- **Account Balance**: Call `gate-cli cex cross-ex account get` to check if available margin is sufficient
- **Position Check**:
 - Margin Trading: Check existing positions to avoid direction conflicts
 - Futures Trading: Check dual-direction position mode
- **Minimum Amount**: Query `min_quote_amount` (typically 3 USDT)
- **Exchange Status**: Verify target exchange is operating normally

### 3. Module Logic

#### Module A: Spot Trading

1. **Parameter Confirmation**:
 - Trading pair format: `GATE_SPOT_{BASE}_{QUOTE}`
 - Buy parameters: `quote_qty` (USDT amount)
 - Sell parameters: `qty` (coin quantity)
2. **Minimum Amount Check**: Call `gate-cli cex cross-ex market symbols` to query minimum amount
3. **Pre-order Confirmation**: Display order summary (pair, direction, quantity, price), require user confirmation
4. **Place Order**: Call `gate-cli cex cross-ex order create`
5. **Verification**: Call `gate-cli cex cross-ex order get` to confirm order status

#### Module B: Margin Trading

1. **Parameter Confirmation**:
 - Trading pair format: `GATE_MARGIN_{BASE}_{QUOTE}`
 - Required parameters: `qty` (coin quantity), `position_side` (`LONG` or `SHORT`)
 - Optional parameters: `quote_qty` (USDT amount)
2. **Leverage Check**: Query current leverage, adjust if user specifies
3. **Position Direction**:
 - Long (`LONG`): Buy coin, borrow USDT
 - Short (`SHORT`): Sell coin, borrow coin
4. **Minimum Amount Check**: Call `gate-cli cex cross-ex market symbols` to query minimum amount
5. **Pre-order Confirmation**: Display order summary (pair, direction, quantity, leverage), require confirmation
6. **Place Order**: Call `gate-cli cex cross-ex order create` with parameter `position_side`
7. **Verification**: Call `gate-cli cex cross-ex position margin-list` with a `symbol` filter to confirm position

#### Module C: Futures Trading

1. **Parameter Confirmation**:
 - Trading pair format: `GATE_FUTURE_{BASE}_{QUOTE}`
 - Required parameters: `qty` (contract size), `position_side` (`LONG` or `SHORT`)
2. **Leverage Adjustment**: If user specifies leverage, call `gate-cli cex cross-ex position leverage` and
 `gate-cli cex cross-ex position set-leverage`
3. **Contract Size Calculation** (if ordering by value):
 - Get `quanto_multiplier` and current price
 - Round down to ensure overspending is avoided
4. **Minimum Size Check**: Call `gate-cli cex cross-ex market symbols` to query minimum size
5. **Pre-order Confirmation**: Display order summary (pair, direction, size, leverage), require confirmation
6. **Place Order**: Call `gate-cli cex cross-ex order create` with parameter `position_side`
7. **Verification**: Call `gate-cli cex cross-ex position list` with a `symbol` filter to confirm position

#### Module D: Cross-Exchange Transfer

1. **Transfer Type**:
 - Cross-exchange transfer: `gate-cli cex cross-ex transfer create` (Exchange A -> Exchange B)
2. **Parameter Confirmation**:
 - Cross-exchange transfer: `from`, `to`, `coin`, `amount`
 - **From/To Account Rules**:
 | Coin | Mode | Valid `from` / `to` | Defaults |
 |------|------|--------------------|---------|
 | USDT | Cross-Exchange | `SPOT` ↔ `CROSSEX` | `CROSSEX_{exchange_type}` → `CROSSEX` |
 | USDT | Sub-Exchange | `SPOT` ↔ `CROSSEX_{exchange_type}` or `CROSSEX_{exchange_type}` ↔ `CROSSEX_{exchange_type}` | `CROSSEX` → `CROSSEX_GATE` |
 | Non-USDT | Any | Must use `CROSSEX_{exchange_type}` (never `CROSSEX` alone). Cross-exchange transfers allowed (e.g., `CROSSEX_BINANCE` ↔ `CROSSEX_GATE`). | — |
3. **Supported Coin Check**: Call `gate-cli cex cross-ex market transfer-coins` to verify
4. **Balance Check**: Confirm source account has sufficient balance
5. **Pre-transfer Confirmation**: Display transfer summary (source, destination, coin, quantity), require confirmation
6. **Execute Transfer**: Call `gate-cli cex cross-ex transfer create`
7. **Verification**: Call `gate-cli cex cross-ex transfer list` to query transfer history and confirm

#### Module E: Convert Trading

1. **Convert Type**:
 - Flash convert quote: `gate-cli cex cross-ex convert quote`
 - Flash convert execution: `gate-cli cex cross-ex convert create`
2. **Parameter Confirmation**:
 - Flash convert: `from_coin`, `to_coin`, `from_amount`, `exchange_type`
3. **Balance Check**: Confirm source account has sufficient balance for the convert pair
4. **Pre-convert Confirmation**: Display source asset, target asset, rate, and expected receive amount, then require
 confirmation
5. **Quote**: Call `gate-cli cex cross-ex convert quote`
6. **Execute Convert**: Call `gate-cli cex cross-ex convert create` with the returned `quote_id`
7. **Verification**: Call `gate-cli cex cross-ex account get` to confirm resulting balances

#### Module F: Order Management

1. **Query Orders**:
 - Current open orders: Call `gate-cli cex cross-ex order list`
 - Order details: Call `gate-cli cex cross-ex order get`
 - **Order History**: Call `gate-cli cex cross-ex order history` (parameters: limit, page, from, to)
2. **Cancel Orders**:
 - Single cancel: Call `gate-cli cex cross-ex order cancel`
3. **Amend Orders**:
 - Check order status must be `open`
 - Call `gate-cli cex cross-ex order update` to amend price or quantity
4. **Display Results**: Display order information in table format

#### Module G: Position Query

1. **Query Types**:
 - Futures positions: Call `gate-cli cex cross-ex position list`
 - Margin positions: Call `gate-cli cex cross-ex position margin-list`
 - Futures leverage: Call `gate-cli cex cross-ex position leverage`
 - Margin leverage: Call `gate-cli cex cross-ex position margin-leverage`
2. **History Query**:
 - **Position History**: Call `gate-cli cex cross-ex position history` (parameters: limit, page, from, to)
 - **Margin Position History**: Call `gate-cli cex cross-ex position margin-history`
 - **Trade History**: Call `gate-cli cex cross-ex order trades` (parameters: limit, page, from, to)
3. **Display Format**:
 - Current positions: Table format (pair, direction, quantity, entry price, unrealized PnL)
 - History records: Reverse chronological order, display recent N records

#### Module H: History Query

1. **Order History**:
 - Call `gate-cli cex cross-ex order history`
 - Parameters: `limit` (max 100), `page`, `from` (start timestamp), `to` (end timestamp)
2. **Trade History**:
 - Call `gate-cli cex cross-ex order trades`
 - Same parameters as above
3. **Position History**:
 - Call `gate-cli cex cross-ex position history`
 - Same parameters as above
4. **Margin Position History**:
 - Call `gate-cli cex cross-ex position margin-history`
 - Same parameters as above
5. **Margin Interest History**:
 - Call `gate-cli cex cross-ex position margin-interests`
 - Same parameters as above

## Report Template

After each operation, output a concise standardized result.

## Safety Rules

- **Credentials**: Never prompt or induce the user to paste API Secret Key into chat; prefer secure local MCP configuration.
- **User-to-User Transfer**: This skill does not support P2P or user-to-user transfers; only transfers between the user's own accounts (e.g., SPOT ↔ CROSSEX) are allowed.
- **Trade Orders**: Display complete order summary (pair, direction, quantity, price, leverage), require user
 confirmation before placing order
- **Cross-Exchange Transfer**: Display transfer details (source, destination, quantity, arrival time), require
 confirmation
- **Scope rule**: Only call tools documented in this skill. If the user requests an operation not documented here,
 respond that it is not supported by this skill.
- **Batch Operations**: Display operation scope and impact, require explicit confirmation

Example: *"Reply 'confirm' to execute the above operation."*

## Error Handling

| Error Code | Handling |
|----------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `USER_NOT_EXIST` | Please confirm if a GATE CrossEx account has been opened. Refer to the GATE Help Center -> CrossEx Trading -> CrossEx Account Operation Guide for instructions. |
| `TRADE_INVALID_QUOTE_ORDER_QTY` | ⚠️ Incorrect parameter name: Market buy must use `quote_qty` |
| `TRADE_INVALID_ORDER_QTY` | ⚠️ Limit order error: Limit orders must use `qty` (coin quantity) + `price` |
| `TRADE_ORDER_AMOUNT_MIN_ERROR` | Order amount below minimum notional value (typically 3 USDT), increase quantity or amount |
| `CONVERT_TRADE_QUOTE_EXCHANGE_INVALID_ERROR` | ⚠️ Flash convert: `exchange_type` parameter value must be uppercase exchange code (e.g., `GATE`) |
| `TRADE_MARGIN_INVALID_PZ_SIDE_ERROR` | Prompt that margin/futures trading must specify `position_side` (LONG/SHORT) |
| `BALANCE_NOT_ENOUGH` | Insufficient available margin, suggest reducing trade amount or depositing |
| `SYMBOL_NOT_FOUND` | Confirm trading pair format is correct (e.g., GATE_SPOT_BTC_USDT) |
| `INVALID_PARAM_VALUE` | Check parameter format (qty is numeric string, position_side is LONG/SHORT) |
| `POSITION_NOT_EMPTY` | Prompt to close position before reversing direction |
| `TRADE_ORDER_LOT_SIZE_ERROR` | Suggest adjusting quantity to minimum unit of the trading pair |
| `RATE_LIMIT_EXCEEDED` | Prompt user about rate limit; suggest retrying later or reducing request frequency |
| `TRADE_INVALID_EXCHANGE_TYPE` | Invalid exchange type; please check the `exchange_type` parameter (e.g., GATE, BINANCE, OKX, BYBIT) |
