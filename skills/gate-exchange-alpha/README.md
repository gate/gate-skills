# Gate Exchange Alpha

## Overview

A comprehensive skill for Gate Alpha platform covering token discovery, market viewing, trading (buy/sell), account management, transaction history, and order management.

### Core Capabilities

| Capability | Description |
|------------|-------------|
| Token Discovery | Browse all tradable currencies, filter by chain/platform/address, view token details |
| Market Viewing | Check all or specific Alpha token prices, 24h changes, and trading volumes |
| Trading (Buy) | Buy tokens with USDT using default or custom slippage, with optional order tracking |
| Trading (Sell) | Sell tokens (full or partial position), with optional order tracking |
| Account & Holdings | View Alpha account balances and calculate portfolio market value |
| Account Book | View account transaction history by time range |
| Order Management | Check order status, view historical orders, search by time range |

## Architecture

```
gate-exchange-alpha/
├── SKILL.md              # Routing entry + MCP tools + domain knowledge
├── README.md             # Human-readable documentation
├── CHANGELOG.md          # Version history
└── references/
    ├── token-discovery.md    # Cases 1-5: Token browsing and filtering
    ├── market-viewing.md     # Cases 6-7: Market tickers and prices
    ├── trading-buy.md        # Cases 8-10: Buy operations
    ├── trading-sell.md       # Cases 11-13: Sell operations
    ├── account-holdings.md   # Cases 14-15: Account balances and portfolio valuation
    ├── account-book.md       # Cases 16-17: Transaction history
    └── order-management.md   # Cases 18-21: Order queries and tracking
```

## MCP Tools Used

| Tool | Auth Required | Purpose |
|------|--------------|---------|
| `cex_alpha_list_alpha_currencies` | No | List tradable currencies with details |
| `cex_alpha_list_alpha_tokens` | No | Filter tokens by chain, platform, or address |
| `cex_alpha_list_alpha_tickers` | No | Get market tickers and prices |
| `cex_alpha_list_alpha_accounts` | Yes | Query account balances |
| `cex_alpha_quote_alpha_order` | Yes | Get price quote for buy/sell (quote_id valid 1 min) |
| `cex_alpha_place_alpha_order` | Yes | Place buy/sell order with quote_id |
| `cex_alpha_get_alpha_order` | Yes | Get single order details by order_id |
| `cex_alpha_list_alpha_orders` | Yes | List orders with filters |
| `cex_alpha_list_alpha_account_book` | Yes | Query transaction history by time range |

## Usage Examples

```
"What coins can I trade on Alpha?"
"Show me Solana tokens."
"What's the price of trump?"
"帮我买 5u ELON"
"买 100u trump，滑点 10%"
"把 ELON 全部卖掉"
"卖掉一半的 trump"
"What coins do I hold on Alpha?"
"How much is my Alpha portfolio worth?"
"最近一周的资产变动记录"
"我刚才那笔买单成功了吗？"
"看看我买 ELON 的所有成功订单"
```

## Trigger Phrases

- alpha tokens / alpha coins / what's on alpha
- alpha price / alpha market / alpha ticker
- buy alpha / 买 / 购买 / 帮我买
- sell alpha / 卖 / 卖出 / 清仓
- alpha holdings / alpha balance / alpha portfolio
- 流水 / 资产变动 / transaction history
- 订单 / order status / 买单 / 卖单

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
