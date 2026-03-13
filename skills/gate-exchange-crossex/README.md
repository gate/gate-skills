# Gate CrossEx Cross-Exchange Trading

## Overview

[Gate CrossEx](https://www.gate.com/crossex) is an AI Agent skill for Gate's cross-exchange unified trading platform. It
allows users to trade across multiple mainstream exchanges (Gate, Binance, OKX, Bybit) through a single account,
providing complete account management, asset transfer, order placement, and position management features.

### Core Capabilities

| Module        | Description                                 | Example                               |
|---------------|---------------------------------------------|---------------------------------------|
| **Orders**    | Query orders                                | "Query all GATE_SPOT_BTC_USDT orders" |
| **Positions** | Query all position types, history records   | "Query all my positions"              |
| **History**   | Query order/position/trade/interest history | "Query trade history"                 |

---

## Supported Exchanges

| Exchange    | Code      | Spot | Margin | Futures |
|-------------|-----------|------|--------|---------|
| **Gate**    | `GATE`    | ✅    | ✅      | ✅       |
| **Binance** | `BINANCE` | ✅    | ✅      | ✅       |
| **OKX**     | `OKX`     | ✅    | ✅      | ✅       |
| **Bybit**   | `BYBIT`   | ✅    | ❎      | ✅       |

---

## Architecture

This skill uses a routing architecture. The main `SKILL.md` handles intent detection and routing, while detailed
workflows live in `references/*.md`.

### Routing

Intents are routed to corresponding reference documents via keywords:

| Intent           | Keywords                                                | Reference                              |
|------------------|---------------------------------------------------------|----------------------------------------|
| Order Management | query orders, cancel order, amend order, list orders    | `references/order-management.md`       |
| Position Query   | query positions, check positions, positions             | `references/position-query.md`         |
| History Query    | history query, trade history, interest history, history | `references/history-query.md`          |
| Asset Query      | query assets, total assets, available margin, assets    | Call `cex_crossex_get_crossex_account` |

---

## Quick Start

### Prerequisites

- Gate MCP configured and connected

### Example Prompts

```
# Spot Trading
"Buy 100 USDT worth of BTC"
"Sell 0.5 BTC spot"

# Margin Trading
"Long 50 USDT worth of XRP on margin"
"Short BTC with 10x leverage"

# Futures Trading
"Open 1 BTC futures long position"
"Market short 5 ETH futures"

# Cross-Exchange Transfer
"Transfer 100 USDT from Gate to Binance"

# Convert Trading
"Flash convert 10 USDT to BTC"

# Query Positions
"Query all my positions"
"Show futures positions"
```

---

### File Structure

```
gate-crossex/
├── README.md
├── SKILL.md
├── CHANGELOG.md
└── references/
    ├── order-management.md       # Order management scenarios
    ├── position-query.md         # Position query scenarios
    └── history-query.md          # History query scenarios
```

---

## Trading Pair Naming Rules

Format: `{EXCHANGE}_{BUSINESS_TYPE}_{BASE}_{QUOTE}`

### Examples

| Type    | Format                             | Example                   |
|---------|------------------------------------|---------------------------|
| Spot    | `{EXCHANGE}_SPOT_{BASE}_{QUOTE}`   | `GATE_SPOT_BTC_USDT`      |
| Margin  | `{EXCHANGE}_MARGIN_{BASE}_{QUOTE}` | `BINANCE_MARGIN_ETH_USDT` |
| Futures | `{EXCHANGE}_FUTURE_{BASE}_{QUOTE}` | `OKX_FUTURE_SOL_USDT`     |

---

## Security

- Only call `cex_crossex_*` mcp functions
- All trading operations require user confirmation before execution
- Does not handle or store credentials in the skill

**⚠️ Important Notice**:
> Never reveal your API Key or Secret to anyone (including customer support).
> If your API Key is accidentally leaked, delete it immediately and recreate.

---

## License

MIT

---

## Technical Support

### Official Documentation

- [Gate CrossEx API Documentation](https://www.gate.com/docs/developers/crossex)
- [Gate API v4 Documentation](https://www.gate.com/docs/developers/apiv4)
- [Gate CrossEx Product Page](https://www.gate.com/crossex)

### Technical Support

- **Online Ticket**: Submit ticket after login
- **Email Support**: [mm@gate.com](mailto:mm@gate.com)
