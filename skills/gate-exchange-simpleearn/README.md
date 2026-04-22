# Gate Exchange Simple Earn

## Overview

An AI Agent skill that enables Gate Simple Earn **flexible (Uni)** and **fixed-term** operations, including subscribe, redeem, interest, positions, product-list, and change-min-rate workflows. This skill covers both the Uni reference set and the fixed-term reference set in this package.

### Core Capabilities

#### Flexible (Uni)

| Capability | Description | Example |
|------------|-------------|---------|
| **Subscribe (lend)** | Call `gate-cli cex earn uni lend` with `type: lend` after user confirmation | "Subscribe 100 USDT to Simple Earn" |
| **Redeem** | Call `gate-cli cex earn uni lend` with `type: redeem` after user confirmation | "Redeem 100 USDT from Simple Earn" |
| **Single-currency position** | Query Simple Earn position for one currency | "My USDT Simple Earn position" |
| **All positions** | Query all Simple Earn positions | "All Simple Earn positions" |
| **Single-currency interest** | Query cumulative interest for one currency | "How much USDT interest" |
| **Subscribe top APY** | Show top APY currency via `gate-cli cex earn uni rate`, confirm, then subscribe | "Subscribe to top APY currency" |
| **Change min rate** | Call `gate-cli cex earn uni change` after user confirmation | "Change min rate for USDT to 0.05" |

#### Fixed-term

| Capability | Description | Example |
|------------|-------------|---------|
| **Product list** | List all fixed-term products or products by currency | "Which Fixed Earn products are available for USDT?" |
| **Subscribe** | Call the fixed-term lend API after user confirmation | "Subscribe 1 SOL fixed-term for 10 days" |
| **Early redeem** | Call the fixed-term pre-redeem API after user confirmation | "Redeem order 5862443199" |
| **Positions** | Query current fixed-term positions or a single order | "My total fixed-term positions" |
| **History** | Query fixed-term subscription, redeem, interest, or bonus history | "Last month fixed-term subscription records" |
| **Order detail** | Query a single fixed-term order by order_id | "Check fixed-term order 5862443199" |

## Architecture

```
User Query
    │
    ▼
┌─────────────────────┐
│ gate-exchange-      │
│ simpleearn Skill    │
│ (Flexible + Fixed)  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ gate-cli commands      │
│ (API v4 Endpoints)  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Gate Platform       │
│ (Simple Earn)       │
└─────────────────────┘
```

## gate-cli command index

### Flexible (Uni)

| Tool | Method | Endpoint | Auth | Description |
|------|--------|----------|------|-------------|
| `gate-cli cex earn uni rate` | GET | `/api/v4/earn/uni/rate` | No | Estimated APY per currency (pair with get_uni_currency for min lend limits) |
| `gate-cli cex earn uni currency` | GET | `/api/v4/earn/uni/currencies/{currency}` | No | Single-currency details (min_rate for subscribe) |
| `gate-cli cex earn uni lend` | POST | `/api/v4/earn/uni/lends` | Yes | Subscribe (lend) or redeem |
| `gate-cli cex earn uni change` | PATCH | `/api/v4/earn/uni/lends` | Yes | Change min rate |
| `gate-cli cex earn uni lends` | GET | `/api/v4/earn/uni/lends` | Yes | User positions (optional currency filter) |
| `gate-cli cex earn uni interest` | GET | `/api/v4/earn/uni/interests/{currency}` | Yes | Single-currency cumulative interest |
| `gate-cli cex earn uni rate` | GET | `/api/v4/earn/uni/rate` | No | Estimated APY per currency (for top APY) |

### Fixed-term

| Tool | Method | Endpoint | Auth | Description |
|------|--------|----------|------|-------------|
| `gate-cli cex earn fixed products` | GET | `/api/product` | No | List all fixed-term products |
| `gate-cli cex earn fixed products-asset` | GET | `/api/product/{asset}/list` | No | List fixed-term products by currency |
| `gate-cli cex earn fixed create` | POST | `/api/user/lend` | Yes | Subscribe to a fixed-term product |
| `gate-cli cex earn fixed pre-redeem` | POST | `/api/user/pre-redeem` | Yes | Early redeem a fixed-term order |
| `gate-cli cex earn fixed lends` | GET | `/api/user/lend` | Yes | Fixed-term positions and order detail |
| `gate-cli cex earn fixed history` | GET | `/api/user/history` | Yes | Fixed-term history records |

Command arguments and response: `references/earn-uni-gate-cli-tools.md`, `references/fixed-earn-gate-cli-tools.md`.

## Quick Start

1. Install the [gate-cli](https://github.com/gate/gate-cli)
2. Load this skill into your AI Agent (Claude, Cursor, etc.)
3. Try: _"My USDT Simple Earn position"_, _"Subscribe 100 USDT"_, _"Which Fixed Earn products are available for USDT?"_, or _"Check fixed-term order 5862443199"_

## Safety & Compliance

- **Flexible (Uni) replies**: Do not show time-related fields from `gate-cli` (timestamps, chart times, history times); amounts/rates/status only.
- **Subscribe/redeem**: Always confirm currency/amount (and min_rate for flexible lend, or term/order_id for fixed-term) before calling.
- No investment advice is provided; APY and rates are for reference only.
- Sensitive user data (API keys, balances) is never logged or exposed in responses.
- On auth failure (401/403), prompt the user to configure Gate CEX API Key with earn/account permission; never expose keys.

## Authentication

This skill does **not** read secrets from chat. Configure **`gate-cli`** on the agent host with **`gate-cli config init`** or **`GATE_API_KEY`** / **`GATE_API_SECRET`**, with Earn-related API permissions. See [gate-cli](https://github.com/gate/gate-cli) and run `sh ./setup.sh` from this skill directory for installation.

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)

## Related skills

| User intent | Skill |
|-------------|-------|
| Spot, account | gate-exchange-spot |
| Futures, leverage | gate-exchange-futures |
| Simple Earn (flexible + fixed-term) | **gate-exchange-simpleearn** (this skill) |
| Multi-collateral loan | gate-exchange-collateralloan |
