# Gate Exchange Auto-Invest Skill

A skill for **fast auto-invest (DCA)** on Gate Exchange Earn: **plan lifecycle** (create, update, stop, top-up), **queries** (coins, minimums, records, orders, detail), and **spot / Simple Earn (Uni)** balance context via **named gate-cli tools only** (no REST paths in the skill text).

## Overview

This skill mirrors the **structure of `gate-exchange-staking`**: `SKILL.md` is the router (**`gate-cli` commands** + a short **Scenario map**—no exposed HTTP paths); detailed scenarios live in **sub-module** files (`autoinvest-plans.md`, `autoinvest-compliance.md`) with workflows, prompt examples, and response templates where applicable.

### Earn auto-invest `gate-cli` commands (11)

Listed in **`SKILL.md` → `gate-cli` commands**: `gate-cli cex earn auto-invest create`, `gate-cli cex earn auto-invest update`, `gate-cli cex earn auto-invest stop`, `gate-cli cex earn auto-invest add-position`, `gate-cli cex earn auto-invest plans`, `gate-cli cex earn auto-invest plan-detail`, `gate-cli cex earn auto-invest coins`, `gate-cli cex earn auto-invest min-amount`, `gate-cli cex earn auto-invest records`, `gate-cli cex earn auto-invest orders`, `gate-cli cex earn auto-invest config`.

### Core Capabilities

| Capability | Description | Primary references |
|------------|-------------|-------------------|
| Plan lifecycle | Create, update, stop, top-up (add position) | `autoinvest-plans.md`, `SKILL.md` (**`gate-cli` commands**) |
| Queries | Supported coins, min amount, records, orders, plan detail | `SKILL.md` (**`gate-cli` commands**) |
| Balance context | Spot + Uni before writes | `SKILL.md` → **`gate-cli` commands** (`gate-cli cex spot account get`, `gate-cli cex earn uni lends`) |
| Rules & compliance | USDT/BTC invest currency, region/compliance, funding source | `autoinvest-compliance.md` |

## Architecture

```
┌─────────────────────┐
│   User Request      │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Intent Detection   │
│  Plan / Query /     │
│  Compliance         │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  `gate-cli` command Call      │
│  11 auto-invest +   │
│  spot / Uni         │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Response Format    │
│  (templates in      │
│   sub-module refs)  │
└─────────────────────┘
```

## `gate-cli` commands

- **Earn auto-invest tools**: Fixed set of **11** names in `SKILL.md` → **`gate-cli` commands** (must match `gate-cli/cmd/cex/GATE_EXCHANGE_SKILLS_MCP_TO_GATE_CLI.md`).
- **Verified supporting tools**: `gate-cli cex spot account get`, `gate-cli cex earn uni lends`.

## Usage examples

```
"Create a weekly 100 USDT DCA into BTC"
"Stop my ETH auto-invest plan"
"What's the minimum amount per period for USDT?"
"Can I use ETH as the investment currency?"
```

## Files in this package

| File | Role |
|------|------|
| `SKILL.md` | Entry: **`gate-cli` commands**, **Feature Modules** / query scenarios, routing, execution, safety (no REST paths) |
| `references/scenarios.md` | Scenario index (16 scenarios); links to `SKILL.md` and sub-module refs |
| `references/autoinvest-plans.md` | Plan lifecycle scenarios (create, update, stop, top-up) |
| `references/autoinvest-compliance.md` | Rules & compliance (invest currency, region, funding) |
| `CHANGELOG.md` | Version history |

## Disclaimer

This skill does not provide investment advice. Product behavior and limits are determined by Gate APIs and the user’s account.
