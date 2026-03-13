---
name: gate-exchange-crossex
version: "2026.3.12-1"
updated: "2026-03-12"
description: 'Use this skill for Gate CrossEx cross-exchange  operations: order queries, position queries, and history queries across Gate, Binance, OKX and Bybit. Trigger phrases include "query positions", "order history", and "trade history".'
---

# Gate CrossEx Trading Suite

This skill is the unified entry point for Gate CrossEx cross-exchange trading. It supports lots of **core operations**:
order management, position query, and history query. User intents are routed to corresponding workflows.

## General Rules
- Read and follow the shared runtime rules before proceeding: → [exchange-runtime-rules.md](../exchange-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they exist in the MCP server.


## Module Overview

| Module        | Description                                 | Trigger Keywords                                                      |
|---------------|---------------------------------------------|-----------------------------------------------------------------------|
| **Orders**    | Query orders, order history                 | `query orders`, `order history`, `list orders`                        |
| **Positions** | Query all position types, history records   | `query positions`, `check positions`, `position history`, `positions` |
| **History**   | Query order/position/trade/interest history | `history query`, `trade history`, `interest history`, `history`       |

## Routing Rules

| Intent               | Example Phrases                                                                        | Route To                                    |
|----------------------|----------------------------------------------------------------------------------------|---------------------------------------------|
| **Order Management** | "Query all open orders", "Query order history"                                         | Read `references/order-management.md`       |
| **Position Query**   | "Query all my positions", "Show futures positions", "Position history"                 | Read `references/position-query.md`         |
| **History Query**    | "Query trade history", "Position history", "Margin interest history", "Account ledger" | Read `references/history-query.md`          |
| **Unclear**          | "Show account" , "Help me" , "Please Check my account"                                 | **Clarify**: Query account, then guide user |

## MCP Tools

This skill uses the **CrossEx MCP toolset** with the cex_crossex prefix as its only core tool family.

**Scope rule**: Only execute operations explicitly documented in this skill. Only call tools listed in the tables below or in `references/*.md`. Tools or operations not mentioned here must not be called.

### Tool Naming Convention

- List operations in the cex_crossex family query symbols, orders, positions, transfers, or history
- Get operations in the cex_crossex family query a single account setting, fee, rate, or order detail

### Symbol And Rule Tools

| Tool                                          | Purpose                                    |
|-----------------------------------------------|--------------------------------------------|
| `cex_crossex_list_crossex_rule_symbols`       | List supported CrossEx trading symbols     |
| `cex_crossex_list_crossex_rule_risk_limits`   | Query symbol risk limit rules              |
| `cex_crossex_list_crossex_transfer_coins`     | List assets supported for CrossEx transfer |
| `cex_crossex_get_crossex_fee`                 | Query CrossEx trading fee information      |
| `cex_crossex_get_crossex_interest_rate`       | Query CrossEx interest rates               |
| `cex_crossex_list_crossex_coin_discount_rate` | Query collateral discount rates            |

### Account Tools

| Tool                                    | Purpose                                     |
|-----------------------------------------|---------------------------------------------|
| `cex_crossex_get_crossex_account`       | Query CrossEx account overview and balances |
| `cex_crossex_list_crossex_account_book` | Query CrossEx account ledger entries        |

### Transfer And Convert Tools

| Tool                                 | Purpose                |
|--------------------------------------|------------------------|
| `cex_crossex_list_crossex_transfers` | Query transfer history |

### Order Tools

| Tool                                      | Purpose                   |
|-------------------------------------------|---------------------------|
| `cex_crossex_list_crossex_open_orders`    | Query current open orders |
| `cex_crossex_get_crossex_order`           | Query order details       |
| `cex_crossex_list_crossex_history_orders` | Query order history       |
| `cex_crossex_list_crossex_history_trades` | Query trade history       |

### Position And Leverage Tools

| Tool                                                | Purpose                         |
|-----------------------------------------------------|---------------------------------|
| `cex_crossex_list_crossex_positions`                | Query current futures positions |
| `cex_crossex_list_crossex_margin_positions`         | Query current margin positions  |
| `cex_crossex_get_crossex_positions_leverage`        | Query futures leverage settings |
| `cex_crossex_get_crossex_margin_positions_leverage` | Query margin leverage settings  |
| `cex_crossex_list_crossex_history_positions`        | Query futures position history  |
| `cex_crossex_list_crossex_history_margin_positions` | Query margin position history   |
| `cex_crossex_list_crossex_history_margin_interests` | Query margin interest history   |
| `cex_crossex_list_crossex_adl_rank`                 | Query ADL rank information      |

### Usage Guidance

- Use the cex_crossex MCP family as the default and only core MCP family for this skill.
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

- **Trading Pair**: Call `cex_crossex_list_crossex_rule_symbols` to verify
- **Account Balance**: Call `cex_crossex_get_crossex_account` to check if available margin is sufficient
- **Position Check**:
    - Margin Trading: Check existing positions to avoid direction conflicts
    - Futures Trading: Check dual-direction position mode
- **Exchange Status**: Verify target exchange is operating normally

### 3. Module Logic

#### Module A: Order Management

1. **Query Orders**:
    - Current open orders: Call `cex_crossex_list_crossex_open_orders`
    - Order details: Call `cex_crossex_get_crossex_order`
    - **Order History**: Call `cex_crossex_list_crossex_history_orders` (parameters: limit, page, from, to)
2. **Display Results**: Display order information in table format

#### Module B: Position Query

1. **Query Types**:
    - Futures positions: Call `cex_crossex_list_crossex_positions`
    - Margin positions: Call `cex_crossex_list_crossex_margin_positions`
    - Futures leverage: Call `cex_crossex_get_crossex_positions_leverage`
    - Margin leverage: Call `cex_crossex_get_crossex_margin_positions_leverage`
2. **History Query**:
    - **Position History**: Call `cex_crossex_list_crossex_history_positions` (parameters: limit, page, from, to)
    - **Margin Position History**: Call `cex_crossex_list_crossex_history_margin_positions`
    - **Trade History**: Call `cex_crossex_list_crossex_history_trades` (parameters: limit, page, from, to)
3. **Display Format**:
    - Current positions: Table format (pair, direction, quantity, entry price, unrealized PnL)
    - History records: Reverse chronological order, display recent N records

#### Module C: History Query

1. **Order History**:
    - Call `cex_crossex_list_crossex_history_orders`
    - Parameters: `limit` (max 100), `page`, `from` (start timestamp), `to` (end timestamp)
2. **Trade History**:
    - Call `cex_crossex_list_crossex_history_trades`
    - Same parameters as above
3. **Position History**:
    - Call `cex_crossex_list_crossex_history_positions`
    - Same parameters as above
4. **Margin Position History**:
    - Call `cex_crossex_list_crossex_history_margin_positions`
    - Same parameters as above
5. **Margin Interest History**:
    - Call `cex_crossex_list_crossex_history_margin_interests`
    - Same parameters as above

## Report Template

After each operation, output a concise standardized result.

## Safety Rules

- **Scope rule**: Only call tools documented in this skill. If the user requests an operation not documented here, respond that it is not supported by this skill.
- **Batch Operations**: Display operation scope and impact, require explicit confirmation

## Error Handling

| Error Code            | Handling                                                                    |
|-----------------------|-----------------------------------------------------------------------------|
| `SYMBOL_NOT_FOUND`    | Confirm trading pair format is correct (e.g., GATE_SPOT_BTC_USDT)           |
| `INVALID_PARAM_VALUE` | Check parameter format (qty is numeric string, position_side is LONG/SHORT) |
