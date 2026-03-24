# Gate Spot Exchange Skill

## Overview

An integrated execution skill for Gate spot trading, covering buy/sell actions, conditional monitoring orders, order management, fill verification, and account asset queries.

### Core Capabilities

- Buy and account queries (balance checks, full-balance buy, asset valuation, minimum order checks)
- Smart monitoring and trading (place limit orders by percentage/fixed price spread)
- Trigger and TP/SL automation (price-triggered placement, dual-leg TP/SL setup, trigger progress checks, and single/batch trigger cancellations)
- Order management and amendments (list open orders, amend orders, cancel orders)
- Post-trade verification (trade history + current holdings reconciliation)
- Combined actions (buy then place sell order, sell then rebuy for asset swap)
- Advanced utilities (batch cancel by ids, batch amend by ids, slippage simulation, batch orders, fee comparison, account-book reconciliation)

## Execution Guardrail (Mandatory)

Before any real trading action (`cex_spot_create_spot_order`, `cex_spot_create_spot_batch_orders`, or `cex_spot_create_spot_price_triggered_order`), the assistant must:

1. Send an **Order Draft** first (pair, side, type, amount/value, estimated fill/cost, risk note)
2. Wait for explicit user confirmation (for example: `Confirm order`, `Confirm`, `Proceed`)
3. Place the real order only after confirmation

If confirmation is missing or ambiguous, the assistant must stay in query/estimation mode and must not execute trading.

Hard gate rules:
- NEVER call `cex_spot_create_spot_order`, `cex_spot_create_spot_batch_orders`, or `cex_spot_create_spot_price_triggered_order` without explicit confirmation in the immediately previous user turn.
- Any parameter/topic change invalidates old confirmation and requires a new draft + reconfirmation.
- For multi-leg actions, require per-leg confirmation before each order placement.

## Architecture

```
gate-exchange-spot/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    └── scenarios.md
```

## Usage Examples

```
"I want to buy 100 USDT of BTC. Check whether my balance is enough first."
"Convert all my USDT into ETH."
"If BTC drops by 5%, sell it for me."
"Did my BTC buy just go through? How much do I hold now?"
"Swap all my DOGE into BTC if it is worth at least 10 USDT."
```

## Trigger Phrases

- buy / sell / rebalance
- monitor market / buy at target price / sell at target price / stop-loss request
- cancel order / amend order / unfilled order handling
- did it fill / how much received / total account value
- spot trading / buy / sell / amend / cancel

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
