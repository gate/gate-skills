# Gate Exchange TradFi Query Skill

## Overview

AI Agent skill for querying Gate TradFi (traditional finance) data in read-only mode. All MCP tools used are prefixed with `cex_tradfi`. It supports four query areas: order list and order history, current and historical positions, market data (category list, symbol list, ticker, symbol kline), and user assets plus MT5 account info. **No order placement, fund transfer, or balance transfer.**

### Core Capabilities

| Module              | Description                                           | Example prompts                                                       |
| ------------------- | ----------------------------------------------------- | --------------------------------------------------------------------- |
| **Query orders**    | Order list, order history                             | "My TradFi orders", "Order history"                                  |
| **Query positions** | Current position list, position history               | "My positions", "Position history", "Current holdings"               |
| **Query market**    | Category list, symbol list, ticker, symbol kline      | "TradFi categories", "Symbol list", "Ticker for X", "Kline 1d"       |
| **Query assets**    | User balance/asset info, MT5 account info             | "My assets", "Balance", "MT5 account", "My MT5 info"                 |

## Architecture

This skill uses a **routing architecture**:

- **SKILL.md** defines the four sub-modules, routing rules, MCP tool list (all `cex_tradfi_*`), and execution flow. Intent is mapped to one of the reference documents.
- **references/** holds one document per module:
  - `query-orders.md` — order list, order history
  - `query-positions.md` — current position list, position history
  - `query-market.md` — category list, symbol list, ticker, symbol kline
  - `query-assets.md` — user assets/balance, MT5 account info

Each reference contains a Workflow (steps and tool calls), Report Template, and scenarios with Context, Prompt Examples, and Expected Behavior. The agent loads the matching reference and follows its workflow to call the appropriate `cex_tradfi_*` MCP tools and format the response.

## Prerequisites

- Gate MCP configured and connected with TradFi tools (all prefixed with `cex_tradfi_`, e.g. `cex_tradfi_query_order_list`, `cex_tradfi_query_categories`, `cex_tradfi_query_mt5_account_info`). If your MCP uses different tool names, map them in SKILL.md or in the reference docs.

## Example Prompts

```
# Orders
"My TradFi open orders"
"Order history"

# Positions
"My positions"
"Position history"

# Market
"TradFi category list"
"Symbol list"
"Ticker for EURUSD"
"Kline 1d for EURUSD"

# Assets
"My TradFi balance"
"Account balance"
"MT5 account"
"My MT5 info"
```

## File Structure

```
gate-exchange-tradfi/
├── README.md
├── SKILL.md
├── CHANGELOG.md
└── references/
    ├── query-orders.md
    ├── query-positions.md
    ├── query-market.md
    └── query-assets.md
```

## Security and Scope

- **Read-only**: This skill only queries data. It does **not** place or cancel orders, and does **not** perform fund transfers or balance transfers.
- No credentials are stored or logged; balance, position, and MT5 account data are displayed only in the current response.
- Confirmation is not required for query-only flows.
