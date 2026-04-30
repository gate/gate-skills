# Gate Smart Earn skill

## Overview

L2 earn assistant for Gate: Simple Earn (flexible and fixed), dual-currency products, and staking. It supports yield discovery, comparisons, position and interest reporting, and **confirmed** subscribe/redeem flows via `gate-cli`.

## Execution guardrail (mandatory)

Before any earn write (`gate-cli cex earn uni lend`, `gate-cli cex earn uni change`, `gate-cli cex earn fixed create`, `gate-cli cex earn dual place`, `gate-cli cex earn staking swap`):

1. Send an **Action Draft** (product, currency, amount, indicative APR or term, risk notes).
2. Wait for explicit **Y** or **N**.
3. Execute only after **Y** in the immediately previous user turn.

If confirmation is missing, ambiguous, or stale, stay in read-only or draft mode.

## Core capabilities

- Idle-fund earn browsing and conservative mix suggestions (read-only synthesis).
- Dual versus staking comparison for a coin; optional token security read.
- Position and yield review across flexible, fixed, dual, and staking (separate sections when the user asks not to merge).
- Flexible and fixed **subscribe** flows with balance pre-checks.
- Flexible **redeem** flows with redeemable amount checks.
- Dual plan discovery (for example filter by investment currency) and settled-order summaries.
- Auto-renew or parameter changes where the CLI exposes `uni change` (with Action Draft + Y).

## Architecture

```
gate-exchange-earn/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── setup.sh
└── references/
    ├── gate-cli.md
    ├── gate-runtime-rules.md
    └── scenarios.md
```

### Gate CLI install (`setup.sh`)

From this skill directory: `sh ./setup.sh` (see script header). Installs `gate-cli` to `$HOME/.openclaw/skills/bin` when possible, with checksum verification.

## Usage examples

```
"I have spare USDT; compare flexible APR, 7-day fixed, and BTC staking."
"List dual plans where I sell high on BTC."
"Subscribe 2,000 USDT flexible earn after checking my balance."
"Redeem 500 USDT from flexible; confirm draft first."
```

## Trigger phrases

- earn, Simple Earn, flexible earn, fixed earn
- dual investment, dual currency, staking, APR, APY
- subscribe earn, redeem earn, auto renew, earn positions

## Support

- **Issues**: https://github.com/gate/gate-skills/issues
- **Publisher**: https://www.gate.com

## Source

- **Repository**: https://github.com/gate/gate-skills
- **CLI**: https://github.com/gate/gate-cli
