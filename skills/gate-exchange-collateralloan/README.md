# Gate Exchange Multi-Collateral Loan

## Overview

AI Agent skill for **multi-collateral loan** on Gate: create current or fixed-term orders, repay, add/redeem collateral. Writes require user confirmation before `gate-cli` calls.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Create current loan** | `gate-cli cex mcl create` with `order` JSON (current) | "Pledge 100 USDT, borrow 7000 DOGE (current)" |
| **Create fixed loan** | Fix rate from `gate-cli cex mcl fix-rate`, then create with `order` JSON | "Pledge 0.01 BTC, borrow 100 USDT for 7 days" |
| **Repay** | `gate-cli cex mcl repay` (`repay_loan` JSON) | "Repay order 123456 in full" |
| **Add collateral** | `gate-cli cex mcl collateral` (append) | "Order 123456 add collateral 100 USDT" |
| **Redeem collateral** | `gate-cli cex mcl collateral` (redeem) | "Order 123456 redeem 100 USDT collateral" |
| **List / detail** | `gate-cli cex mcl orders`, `gate-cli cex mcl order` | "My collateral loan orders" |

## Architecture

```
User Query → gate-exchange-collateralloan Skill → gate-cli (cex_mcl_*) → Platform
```

## gate-cli command index (summary)

| Tool | Auth | Role |
|------|------|------|
| `gate-cli cex mcl fix-rate` | No | Fixed 7d/30d rates (list) |
| `gate-cli cex mcl ltv` | No | LTV thresholds |
| `gate-cli cex mcl current-rate` | No | Flexible borrow rates |
| `gate-cli cex mcl quota` | Yes | Quota |
| `gate-cli cex mcl create` | Yes | New loan (`order` JSON) |
| `gate-cli cex mcl orders` | Yes | List |
| `gate-cli cex mcl order` | Yes | Detail |
| `gate-cli cex mcl repay` | Yes | Repay (`repay_loan` JSON) |
| `gate-cli cex mcl collateral` | Yes | Add/redeem (`collateral_adjust` JSON) |
| `gate-cli cex mcl repay-records` | Yes | Repay history |
| `gate-cli cex mcl records` | Yes | Collateral history |

Full `gate-cli` arguments: **`references/mcl-gate-cli-tools.md`**. Scenarios: **`references/scenarios.md`**.

## Quick Start

1. Install [gate-cli](https://github.com/gate/gate-cli)
2. Load this skill
3. Example: _"Pledge 100 USDT, borrow 7000 DOGE (current)"_

## Safety & Compliance

- Writes require confirmation and a clear draft
- No investment advice; user bears liquidation risk
- On 401/403, prompt API key setup; never expose keys

## Related skills

| Intent | Skill |
|--------|-------|
| Simple Earn | gate-exchange-simpleearn |
| Multi-collateral loan | **gate-exchange-collateralloan** (this skill) |

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
