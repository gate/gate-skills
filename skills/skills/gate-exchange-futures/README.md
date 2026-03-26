# Gate Exchange Futures

## Overview

AI Agent skill for [Gate](https://www.gate.com) USDT perpetual futures. Supports **seven operations**: open position, close position, cancel order, amend order, take profit / stop loss (TP/SL), conditional open, and price-triggered order management.

### Core Capabilities

| Module | Description | Example |
|--------|-------------|---------|
| **Open** | Limit/market open long or short, cross/isolated mode | "BTC_USDT long 100U, limit 65000" |
| **Close** | Full close, partial close, reverse position | "Close all BTC", "Reverse to short" |
| **Cancel** | Cancel single or batch orders | "Cancel all orders", "Cancel that buy order" |
| **Amend** | Change order price or size | "Change price to 60000" |
| **TP/SL** | Set take profit or stop loss on an existing position | "Set BTC TP at 72000", "SL at 58000" |
| **Conditional Open** | Open a position when price reaches a level | "Long BTC if it drops to 60000" |
| **Manage Triggers** | List, cancel, or amend price-triggered orders | "Cancel my BTC stop loss", "Move TP to 75000" |

---

## Architecture

This skill uses a **routing architecture**: `SKILL.md` routes user intent by keywords to the corresponding sub-module reference document, which contains the detailed workflow.

| Intent | Keywords | Reference |
|--------|----------|-----------|
| Open position | long, short, buy, sell, open | `references/open-position.md` |
| Close position | close, close all, reverse | `references/close-position.md` |
| Cancel order | cancel, revoke | `references/cancel-order.md` |
| Amend order | amend, modify | `references/amend-order.md` |
| Take Profit / Stop Loss | take profit, stop loss, TP, SL, 止盈, 止损 | `references/tp-sl.md` |
| Conditional Open | conditional order, when price reaches, breakout, 条件单, 触价开仓 | `references/conditional.md` |
| Manage triggered orders | list triggers, cancel TP/SL, amend trigger, 查询条件单, 取消止盈止损 | `references/manage.md` |

---

## Quick Start

### Prerequisites

- Gate MCP configured and connected

### Example Prompts

```
# Open
"Open long 1 contract BTC_USDT at 65000"
"BTC_USDT long 100U, limit 65000"

# Close
"Close all BTC_USDT"
"Close half"

# Cancel
"Cancel all BTC_USDT orders"

# Amend
"Change that buy order price to 64000"

# Take Profit / Stop Loss
"Set BTC_USDT take profit at 72000"
"SL at 58000 for my BTC long, execute at market"
"Set TP 72000 and SL 58000 for BTC"

# Conditional Open
"Open long 2 BTC_USDT contracts if BTC drops to 60000"
"Short ETH_USDT when it breaks above 3200, 50U margin"

# Manage
"List my BTC TP/SL orders"
"Cancel my BTC stop loss"
"Move TP to 75000"
"Cancel all conditional orders"
```

---

## File Structure

```
gate-exchange-futures/
├── README.md
├── SKILL.md
├── CHANGELOG.md
└── references/
    ├── open-position.md
    ├── close-position.md
    ├── cancel-order.md
    ├── amend-order.md
    ├── tp-sl.md
    ├── conditional.md
    └── manage.md
```

---

## Security

- Uses Gate MCP tools only
- Open/close/cancel/amend and all price-triggered order operations require user confirmation before execution
- No credential handling or storage in this skill

## License

MIT

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
