# Gate.io Spot Trading Assistant Skill

## Overview

面向 Gate.io 现货交易的一体化执行 Skill，覆盖买币、卖币、盯盘条件单、订单管理、成交核实与资产查询。

## Core Capabilities

- 买币与账户查询（余额检查、全仓买入、资产估值、最小下单检查）
- 智能盯盘与买卖（按百分比/固定价差挂限价单）
- 订单管理与改价（查挂单、改单、撤单）
- 交易后核验（成交记录 + 当前持仓核对）
- 组合动作（买后挂卖、先卖后买置换）

## Skill Structure

```
gate-spot-trading-assistant/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    └── scenarios.md
```

## Usage Examples

```
"我想买 100 块钱的 BTC，先看看余额够不够。"
"帮我把所有 USDT 买成 ETH。"
"如果 BTC 跌 5% 就帮我卖掉。"
"我刚才买 BTC 成功了吗？现在一共有多少？"
"帮我把 DOGE 全换成 BTC，够 10U 就执行。"
```

## Trigger Phrases

- 买币 / 卖币 / 换仓
- 盯盘 / 到价买 / 到价卖 / 止损
- 撤单 / 改单 / 未成交处理
- 成交了吗 / 到账多少 / 账户总值
- spot trading / buy / sell / amend / cancel

## Scenario Test Script

- Real API integration mode (default, read checks only):
  - `GATE_API_KEY=... GATE_API_SECRET=... python3 spot-skills/gate-spot-trading-assistant/tests/run_spot_skill_scenarios.py`
- Real API integration mode (with write smoke checks):
  - `GATE_API_KEY=... GATE_API_SECRET=... python3 spot-skills/gate-spot-trading-assistant/tests/run_spot_skill_scenarios.py --mode real --real-allow-write --pair BTC_USDT --real-quote-amount 3.5`
- Mock mode (optional, local logic regression only):
  - `python3 spot-skills/gate-spot-trading-assistant/tests/run_spot_skill_scenarios.py --mode mock`

Report output default:
- `spot-skills/gate-spot-trading-assistant/tests/TEST_RESULTS.md`
