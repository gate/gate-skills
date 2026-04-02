# Gate Exchange Auto-Invest Skill

A skill for **fast auto-invest (DCA)** on Gate Exchange Earn: **plan lifecycle** (create, update, stop, top-up), **queries** (coins, minimums, records, orders, detail), and **spot / Simple Earn (Uni)** balance context via **named Gate MCP tools only** (no REST paths in the skill text).

## Overview

This skill mirrors the **structure of `gate-exchange-staking`**: `SKILL.md` is the router (**MCP tools** + a short **Scenario map**—no exposed HTTP paths); detailed scenarios live in **sub-module** files (`autoinvest-plans.md`, `autoinvest-compliance.md`) with workflows, prompt examples, and response templates where applicable.

### Earn auto-invest MCP tools (11)

Listed in **`SKILL.md` → MCP tools**: `cex_earn_create_auto_invest_plan`, `cex_earn_update_auto_invest_plan`, `cex_earn_stop_auto_invest_plan`, `cex_earn_add_position_auto_invest_plan`, `cex_earn_list_auto_invest_plans`, `cex_earn_get_auto_invest_plan_detail`, `cex_earn_list_auto_invest_coins`, `cex_earn_get_auto_invest_min_amount`, `cex_earn_list_auto_invest_plan_records`, `cex_earn_list_auto_invest_orders`, `cex_earn_list_auto_invest_config`.

### Core Capabilities

| Capability | Description | Primary references |
|------------|-------------|-------------------|
| Plan lifecycle | Create, update, stop, top-up (add position) | `autoinvest-plans.md`, `SKILL.md` (**MCP tools**) |
| Queries | Supported coins, min amount, records, orders, plan detail | `SKILL.md` (**MCP tools**) |
| Balance context | Spot + Uni before writes | `SKILL.md` → **MCP tools** (`cex_spot_get_spot_accounts`, `cex_earn_list_user_uni_lends`) |
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
│  MCP Tool Call      │
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

## MCP tools

- **Earn auto-invest tools**: Fixed set of **11** names in `SKILL.md` → **MCP tools** (must match gate-mcp).
- **Verified supporting tools**: `cex_spot_get_spot_accounts`, `cex_earn_list_user_uni_lends`.

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
| `SKILL.md` | Entry: **MCP tools**, **Feature Modules** / query scenarios, routing, execution, safety (no REST paths) |
| `references/scenarios.md` | Scenario index (16 scenarios); links to `SKILL.md` and sub-module refs |
| `references/autoinvest-plans.md` | Plan lifecycle scenarios (create, update, stop, top-up) |
| `references/autoinvest-compliance.md` | Rules & compliance (invest currency, region, funding) |
| `CHANGELOG.md` | Version history |

## Disclaimer

This skill does not provide investment advice. Product behavior and limits are determined by Gate APIs and the user’s account.
