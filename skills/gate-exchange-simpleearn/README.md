# Gate Exchange Simple Earn

## Overview

An AI Agent skill that enables Simple Earn (Uni) flexible **query** operations; **subscribe and redeem API calls are disabled**. Reply "Simple Earn subscribe and redeem are currently not supported" when the user asks to subscribe or redeem.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Subscribe (lend)** | **No API call**; reply "Simple Earn subscribe and redeem are currently not supported" | "Subscribe 100 USDT to Simple Earn" → reply not supported |
| **Redeem** | **No API call**; reply "Simple Earn subscribe and redeem are currently not supported" | "Redeem 100 USDT from Simple Earn" → reply not supported |
| **Single-currency position** | Query Simple Earn position for one currency | "My USDT Simple Earn position" |
| **All positions** | Query all Simple Earn positions | "All Simple Earn positions" |
| **Single-currency interest** | Query cumulative interest for one currency | "How much USDT interest" |
| **Subscribe top APY** | **No subscribe API call**; may show top APY currency and rate; if user wants to subscribe, reply not supported | "Subscribe to top APY currency" → may show data, do not execute subscribe |

## Architecture

```
User Query
    │
    ▼
┌─────────────────────┐
│  gate-exchange-     │
│  simpleearn Skill   │
│  (6 Scenarios +     │
│   Domain Knowledge) │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Gate MCP Tools     │
│  (API v4 Endpoints) │
│                     │
│  • cex_earn_list_   │
│    uni_currencies   │
│  • cex_earn_get_    │
│    uni_currency     │
│  • cex_earn_create_ │
│    uni_lend         │
│  • cex_earn_list_   │
│    user_uni_lends   │
│  • cex_earn_get_    │
│    uni_interest     │
│  • cex_earn_list_   │
│    uni_rate         │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Gate Platform     │
│  (Simple Earn/Uni) │
└─────────────────────┘
```

## MCP Tools

| Tool | Method | Endpoint | Auth | Description |
|------|--------|----------|------|-------------|
| `cex_earn_list_uni_currencies` | GET | `/api/v4/earn/uni/currencies` | No | List Simple Earn currencies (min_rate, min_lend_amount, etc.) |
| `cex_earn_get_uni_currency` | GET | `/api/v4/earn/uni/currencies/{currency}` | No | Single-currency details (min_rate for subscribe) |
| `cex_earn_create_uni_lend` | POST | `/api/v4/earn/uni/lends` | Yes | **Do not use for subscribe/redeem** (API reference only) |
| `cex_earn_list_user_uni_lends` | GET | `/api/v4/earn/uni/lends` | Yes | User positions (optional currency filter) |
| `cex_earn_get_uni_interest` | GET | `/api/v4/earn/uni/interests/{currency}` | Yes | Single-currency cumulative interest |
| `cex_earn_list_uni_rate` | GET | `/api/v4/earn/uni/rate` | No | Estimated APY per currency (for top APY) |

Full mapping and request/response details: **references/earn-uni-api.md**.

## Quick Start

1. Install the [Gate MCP server](https://github.com/gate/gate-mcp)
2. Load this skill into your AI Agent (Claude, Cursor, etc.)
3. Try: _"My USDT Simple Earn position"_ or _"How much USDT interest"_ (subscribe/redeem will only reply not supported; no API call)

## Safety & Compliance

- **Subscribe/redeem**: This skill does not call subscribe or redeem APIs; reply "Simple Earn subscribe and redeem are currently not supported."
- No investment advice is provided; APY and rates are for reference only
- Sensitive user data (API keys, balances) is never logged or exposed in responses
- On auth failure (401/403), prompt the user to configure Gate CEX API Key with earn/account permission; never expose keys

## Related skills

| User intent | Skill |
|-------------|-------|
| Spot, account | gate-exchange-spot |
| Futures, leverage | gate-exchange-futures |
| Simple Earn (position/interest/rate query; subscribe and redeem not provided) | **gate-exchange-simpleearn** (this skill) |
| Multi-collateral loan | gate-exchange-collateralloan |
