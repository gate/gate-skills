# Gate Exchange Dual Investment

## Overview

The dual investment function of Gate Exchange — an AI Agent skill for product discovery, settlement simulation, position management, and balance queries.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Product Discovery** | Browse and compare dual plans with APY, target price, delivery details; filter by coin | "What BTC dual investment plans are available?" |
| **Settlement Simulation** | Calculate settlement outcomes under different price scenarios | "Sell-high target 62000, what if it goes to 65000?" |
| **Position Summary** | View ongoing dual orders and locked amounts | "Dual position summary" |
| **Settlement Records** | Check settlement results of matured orders | "My BTC order last month — got crypto or USDT?" |
| **Balance Query** | View total dual holdings and accumulated interest | "How much is locked in dual?" |
| **Risk Education** | Explain currency conversion risks and missed gains | "Will I lose principal with dual investment?" |

## Architecture

```
User Query
    │
    ▼
┌─────────────────────┐
│  gate-exchange-dual  │
│  Skill               │
│  (13 Cases Routing   │
│   + Domain Knowledge)│
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Gate MCP Tools      │
│                      │
│                      │
│  • cex_earn_list_    │
│    dual_investment_  │
│    plans             │
│  • cex_earn_list_    │
│    dual_orders       │
│  • cex_earn_list_    │
│    dual_balance      │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Gate Platform       │
│  (Dual Investment)   │
└─────────────────────┘
```

## MCP Tools

| Tool | Auth | Description |
|------|------|-------------|
| `cex_earn_list_dual_investment_plans` | Yes | List dual plans (optional param: plan_id) |
| `cex_earn_list_dual_orders` | Yes | Order history (params: status, investment_type, from, to, page, limit; limit max 100) |
| `cex_earn_list_dual_balance` | Yes | Balance & interest |

## Quick Start

1. Install the [Gate MCP server](https://github.com/gate/gate-mcp)
2. Load this skill into your AI Agent (Claude, ChatGPT, etc.)
3. Try: _"What dual investment plans are available?"_ or _"Show me BTC dual investment plans"_

## Safety & Compliance

- Risk disclaimers are included in every response involving financial products
- No investment advice is provided; all data is for informational purposes only
- Dual investment is interest-guaranteed but not principal-protected — this is clearly communicated in every response
- Sensitive user data (API keys, balances) is never logged or exposed in responses

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
