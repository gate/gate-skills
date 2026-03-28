# Gate Exchange Trading Copilot

## Overview

An L2 **execution-first** skill for Gate (**Trading Copilot L2 Tool Calls spec v1.3**): it orchestrates **nine** L1 domains (spot, futures, margin, flash swap, assets, market analysis, unified account, Alpha, TradFi) via MCP tools. It routes spot, USDT-margined futures, margin (isolated uni loan and unified borrow/repay), flash swap, Alpha, and TradFi orders behind **Action Draft + explicit confirmation** for every write. Pre-trade clarification covers perpetual vs delivery, dual-position isolated vs cross, and unified account mode for cross-margin-style flows. It does **not** replace deep research skills, full asset-audit skills, or earn/staking products.

### Core Capabilities

| Capability | Description |
|------------|-------------|
| Multi-product execution | Spot, futures, margin legs, flash swap, Alpha, TradFi in one copilot flow |
| Signal-based routing | Combines S1–S8-style intents (spot, futures, margin, flash, query, order ops, TradFi, Alpha) |
| Strong confirmation | No write tools after a draft until the user replies **Y** for that scope |
| Query aggregation | Open orders, positions, balances across products without trading |
| Composite legs | Spot + futures or cancel-then-replace patterns with per-leg or combined confirmation |
| L1 alignment | Consults domain `skills/` packages (spot, futures, unified, flash swap, assets, market analysis, Alpha, TradFi) for semantics while L2 owns the workflow |
| Scenario catalog | **26** scenario slots in `references/scenarios.md`; **scenarios 6 and 19** (standalone single-leg flash; futures reduce plus flash) are **hidden**: **no MCP tools** in this skill—hand off to **`gate-exchange-flashswap`** / **`gate-exchange-futures`** or the app **without naming tools** |
| Pre-trade clarification | Perpetual vs delivery, isolated vs cross when dual positions conflict, `cex_unified_get_unified_mode` for cross-margin long |

## Architecture

```
gate-exchange-trading-copilot/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    └── scenarios.md
```

## Usage Examples

```
"Market buy 1000 USDT of BTC."
"Open 10x long on ETH_USDT with 500 USDT margin."
"Preview 500 USDT flash swap to ETH and execute if I say yes."
"Show my perp positions and spot BTC balance."
"Cancel my open BTC_USDT spot limit order."
"Buy 500 USDT BTC spot and open a BTC perp long with 1000 USDT notional."
```

## Trigger Phrases

- market buy / limit sell / amend / cancel
- open long / open short / close position / reduce only
- take profit / stop loss / trigger order
- margin borrow / repay / isolated margin
- flash swap / convert / swap coins
- Alpha buy / TradFi / gold / XAU

## Support

- **Repository**: [bitbucket.org/gateio/gate-github-skills](https://bitbucket.org/gateio/gate-github-skills) (this skills monorepo)
- **Publisher**: [Gate.com](https://www.gate.com)
- **MCP**: Requires Gate Exchange MCP configured and connected (API key); tool names may appear across bundled MCP server descriptors—use the allowlist in `SKILL.md`.
