# Gate.io Futures Trading

## Overview

AI Agent skill for [Gate.io](https://www.gate.io) USDT perpetual futures. Supports **four operations only**: open position, close position, cancel order, amend order. No market monitoring or arbitrage scanning.

### Core Capabilities

| Module | Description | Example |
|--------|-------------|---------|
| **开仓 (Open)** | Limit/market open long or short, cross/isolated mode | "BTC_USDT 开多 100U，限价 65000" |
| **平仓 (Close)** | Full close, partial close, reverse position | "全平 BTC", "反手做空" |
| **撤单 (Cancel)** | Cancel single or batch orders | "撤销所有挂单", "撤掉那个买单" |
| **改单 (Amend)** | Change order price or size | "把价格改成 60000" |

---

## Routing

Intent is routed by keywords to the corresponding reference:

| Intent | Keywords | Reference |
|--------|-----------|-----------|
| Open position | 开多, 开空, 下单, buy, sell, open | `references/open-position.md` |
| Close position | 平仓, 全平, 反手, close, reverse | `references/close-position.md` |
| Cancel order | 撤单, 取消, cancel, revoke | `references/cancel-order.md` |
| Amend order | 改单, 修改, amend, modify | `references/amend-order.md` |

---

## Quick Start

### Prerequisites

- Gate MCP configured and connected

### Example Prompts

```
# 开仓
"帮我在 BTC_USDT 合约开多 1 张，限价 65000"
"BTC_USDT 开多 100U，限价 65000"

# 平仓
"全平 BTC_USDT"
"平掉一半"

# 撤单
"撤销 BTC_USDT 所有挂单"

# 改单
"把刚才的买单价格改成 64000"
```

---

## File Structure

```
gate-futures/
├── README.md
├── SKILL.md
├── CHANGELOG.md
└── references/
    ├── open-position.md
    ├── close-position.md
    ├── cancel-order.md
    └── amend-order.md
```

---

## Security

- Uses Gate MCP tools only
- Open/close/cancel/amend require user confirmation before execution
- No credential handling or storage in this skill

## License

MIT
