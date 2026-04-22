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

Before any real trading action (`gate-cli cex spot order buy` / `gate-cli cex spot order sell`, `gate-cli cex spot order batch-create`, or `gate-cli cex spot price-trigger create`), the assistant must:

1. Send an **Order Draft** first (pair, side, type, amount/value, estimated fill/cost, risk note)
2. Wait for explicit user confirmation (for example: `Confirm order`, `Confirm`, `Proceed`)
3. Place the real order only after confirmation

If confirmation is missing or ambiguous, the assistant must stay in query/estimation mode and must not execute trading.

Hard gate rules:
- NEVER call `gate-cli cex spot order buy` / `gate-cli cex spot order sell`, `gate-cli cex spot order batch-create`, or `gate-cli cex spot price-trigger create` without explicit confirmation in the immediately previous user turn.
- Any parameter/topic change invalidates old confirmation and requires a new draft + reconfirmation.
- For multi-leg actions, require per-leg confirmation before each order placement.

## Architecture

```
gate-exchange-spot/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── setup.sh          # GateClaw/OpenClaw: installs gate-cli to ~/.openclaw/skills/bin (see script header)
└── references/
    ├── gate-cli.md      # Execution contract for gate-cli (commands, auth, SOP)
    ├── gate-runtime-rules.md
    └── scenarios.md
```

### GateClaw / OpenClaw setup (`setup.sh`)

On skill install, GateClaw runs `setup.sh` if present. It installs **`gate-cli`** to **`$HOME/.openclaw/skills/bin/gate-cli`** (for the default `node` user this is `/home/node/.openclaw/skills/bin/gate-cli`), with mode **755**.

From a checkout of this skill directory, the same script is: **`sh ./setup.sh`**.

- **Default** (`GATE_CLI_SETUP_MODE=release`): runs the official installer `curl -fsSL https://raw.githubusercontent.com/gate/gate-cli/main/install.sh | sh` (see [install.sh](https://github.com/gate/gate-cli/blob/main/install.sh)), then **copies** the installed `gate-cli` binary to **`$HOME/.openclaw/skills/bin/gate-cli`** (or `GATE_OPENCLAW_SKILLS_BIN/gate-cli`). Requires `curl` and `sh`; optional `GATE_CLI_VERSION=v0.x.y` is passed through as `sh -s -- --version "$GATE_CLI_VERSION"`.
- **Build from source** (`GATE_CLI_SETUP_MODE=build`): clone [gate/gate-cli](https://github.com/gate/gate-cli) and compile with `go build`. Requires `git` and `go`.

Override install directory: `GATE_OPENCLAW_SKILLS_BIN=/path/to/bin`.

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
