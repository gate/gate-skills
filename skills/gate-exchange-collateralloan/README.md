# Gate Exchange Multi-Collateral Loan

## Overview

AI Agent skill for **multi-collateral loan** on Gate: create current or fixed-term orders, repay, add/redeem collateral. Writes require user confirmation before MCP calls.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Create current loan** | `cex_mcl_create_multi_collateral` with `order` JSON (current) | "Pledge 100 USDT, borrow 7000 DOGE (current)" |
| **Create fixed loan** | Fix rate from `cex_mcl_get_multi_collateral_fix_rate`, then create with `order` JSON | "Pledge 0.01 BTC, borrow 100 USDT for 7 days" |
| **Repay** | `cex_mcl_repay_multi_collateral_loan` (`repay_loan` JSON) | "Repay order 123456 in full" |
| **Add collateral** | `cex_mcl_operate_multi_collateral` (append) | "Order 123456 add collateral 100 USDT" |
| **Redeem collateral** | `cex_mcl_operate_multi_collateral` (redeem) | "Order 123456 redeem 100 USDT collateral" |
| **List / detail** | `cex_mcl_list_multi_collateral_orders`, `cex_mcl_get_multi_collateral_order_detail` | "My collateral loan orders" |

## Architecture

```
User Query → gate-exchange-collateralloan Skill → Gate MCP (cex_mcl_*) → Platform
```

## MCP Tools (summary)

| Tool | Auth | Role |
|------|------|------|
| `cex_mcl_get_multi_collateral_fix_rate` | No | Fixed 7d/30d rates (list) |
| `cex_mcl_get_multi_collateral_ltv` | No | LTV thresholds |
| `cex_mcl_get_multi_collateral_current_rate` | No | Flexible borrow rates |
| `cex_mcl_list_user_currency_quota` | Yes | Quota |
| `cex_mcl_create_multi_collateral` | Yes | New loan (`order` JSON) |
| `cex_mcl_list_multi_collateral_orders` | Yes | List |
| `cex_mcl_get_multi_collateral_order_detail` | Yes | Detail |
| `cex_mcl_repay_multi_collateral_loan` | Yes | Repay (`repay_loan` JSON) |
| `cex_mcl_operate_multi_collateral` | Yes | Add/redeem (`collateral_adjust` JSON) |
| `cex_mcl_list_multi_repay_records` | Yes | Repay history |
| `cex_mcl_list_multi_collateral_records` | Yes | Collateral history |

Full MCP arguments: **`references/mcl-mcp-tools.md`**. Scenarios: **`references/scenarios.md`**.

## Quick Start

1. Install [gate-mcp](https://github.com/gate/gate-mcp)
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
