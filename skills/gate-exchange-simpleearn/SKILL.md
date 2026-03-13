---
name: gate-exchange-simpleearn
version: "2026.3.12-2"
updated: "2026-03-12"
description: Query Gate Simple Earn (Uni) flexible. Use this skill whenever the user asks about Simple Earn, subscribe or redeem intent, position query, interest query, or top APY. Trigger phrases include "Simple Earn", "Uni", "subscribe", "redeem", "flexible earn", "positions", "interest", "top APY", or any request involving Simple Earn subscribe, redeem, positions, or interest.
---

# Gate Exchange Simple Earn Skill

Provide Simple Earn (Uni) flexible **read operations** on Gate: single-currency or all positions query, single-currency interest query, and estimated APY (rate) query. **Subscribe (lend), redeem, and change_uni_lend are disabled**—do not call `cex_earn_create_uni_lend` or `cex_earn_change_uni_lend`. When users ask to subscribe, redeem, or change settings, reply that the feature is currently not supported.

## Trigger Conditions

Activate this skill when the user expresses any of the following intents:
- Simple Earn, Uni, subscribe, redeem, positions, interest, top APY, one-click subscribe top APY
- Any request involving Simple Earn subscribe, redeem, position query, or interest query

## Prerequisites

- **MCP Dependency**: Requires [gate-mcp](https://github.com/gate/gate-mcp) to be installed.
- **Authentication**: Position and write operations require API key authentication; rate and currency queries are public.
- **Disclaimer**: Always append when showing APY or rates: _"This information is for reference only and does not constitute investment advice. APY may change. Please understand the product terms before subscribing."_

## Service Restrictions (Current)

- **Do not call subscribe or redeem APIs in any form**: This skill **must not** call `cex_earn_create_uni_lend` for subscribe (`type: lend`) or redeem (`type: redeem`). Regardless of user confirmation or provided amount/currency, **calling this API is forbidden**. When the user requests subscribe, redeem, or one-click subscribe top APY, reply only: "Simple Earn subscribe and redeem are currently not supported." Position query, interest query, and rate query (read-only) are unaffected.
- **Do not call the change-lend API in any form**: This skill **must not** call `cex_earn_change_uni_lend` (e.g. change min rate). Regardless of user confirmation or provided currency/min_rate, **calling this API is forbidden**. When the user requests changing Simple Earn settings (e.g. min rate), reply that the operation is not supported and do not call MCP.

## Available MCP Tools

| Tool | Auth | Description | Reference |
|------|------|-------------|-----------|
| `cex_earn_list_uni_currencies` | No | List Simple Earn currencies (min_rate, min_lend_amount, etc.) | [earn-uni-api.md](references/earn-uni-api.md) |
| `cex_earn_get_uni_currency` | No | Single-currency details (min_rate for subscribe) | [earn-uni-api.md](references/earn-uni-api.md) |
| `cex_earn_create_uni_lend` | Yes | **Do not use for subscribe/redeem**; API reference only, do not call | [earn-uni-api.md](references/earn-uni-api.md) |
| `cex_earn_change_uni_lend` | Yes | **Do not call in any form**; API reference only, do not call | [earn-uni-api.md](references/earn-uni-api.md) |
| `cex_earn_list_user_uni_lends` | Yes | User positions (optional currency filter) | [earn-uni-api.md](references/earn-uni-api.md) |
| `cex_earn_get_uni_interest` | Yes | Single-currency cumulative interest | [earn-uni-api.md](references/earn-uni-api.md) |
| `cex_earn_list_uni_rate` | No | Estimated APY per currency (for top APY) | [earn-uni-api.md](references/earn-uni-api.md) |

## Routing Rules

| Case | User Intent | Signal Keywords | Action |
|------|-------------|-----------------|--------|
| 1 | Subscribe (lend) | "subscribe", "lend to Simple Earn" | **Disabled**: Tell user "Simple Earn subscribe and redeem are currently not supported." Do not call MCP. |
| 2 | Redeem | "redeem", "redeem from Simple Earn" | **Disabled**: Tell user "Simple Earn subscribe and redeem are currently not supported." Do not call MCP. |
| 3 | Single-currency position | "my USDT Simple Earn", "position for one currency" | See [scenarios.md](references/scenarios.md) Scenario 3 |
| 4 | All positions | "all Simple Earn positions", "total positions" | See [scenarios.md](references/scenarios.md) Scenario 4 |
| 5 | Single-currency interest | "interest", "USDT interest" | See [scenarios.md](references/scenarios.md) Scenario 5 |
| 6 | Subscribe top APY | "top APY", "one-click subscribe top APY" | **Disabled**: Tell user "Simple Earn subscribe and redeem are currently not supported." Do not call MCP. |
| 7 | Change lend settings (e.g. min rate) | "change min_rate", "change Simple Earn settings" | **Disabled**: Do not call `cex_earn_change_uni_lend`; tell user the operation is not supported. |
| 8 | Auth failure (401/403) | MCP returns 401/403 | Do not expose keys; prompt user to configure Gate CEX API Key (earn). |

## Execution

1. Identify user intent from the Routing Rules table above.
2. For **Cases 1, 2, 6** (subscribe/redeem/one-click subscribe top APY): **Do not call** `cex_earn_create_uni_lend` (regardless of user confirmation). Reply only: "Simple Earn subscribe and redeem are currently not supported."
3. For **Case 7** (change lend/min rate): **Do not call** `cex_earn_change_uni_lend` (regardless of user confirmation). Reply that the operation is not supported; do not call MCP.
4. For Cases 3, 4, 5: Read the corresponding scenario in [scenarios.md](references/scenarios.md) and follow the workflow (position, interest read-only operations).
5. For Case 8: Do not expose API keys or raw errors; prompt the user to configure API key / log in again.
6. If the user's intent is ambiguous (e.g. missing currency or amount), ask a clarifying question before routing.

## Domain Knowledge

### Core Concepts

- **Subscribe (lend)**: User lends a specified amount of a currency to the Simple Earn pool. Interest is paid at each settlement time; min_rate from currency details should be passed to avoid rejections.
- **Redeem**: User redeems a specified amount from the pool. Redeemed funds arrive at the next settlement time; interest for the current period is still credited.
- **min_rate**: Minimum acceptable hourly rate for the currency (concept only; this skill does not perform subscribe, so do not call create_uni_lend).
- **est_rate**: Estimated APY from `cex_earn_list_uni_rate`; used to pick the top APY currency. Not guaranteed; for reference only.
- **Interest**: Cumulative interest for a currency from `cex_earn_get_uni_interest`.
- Settlement windows: Lend and redeem are not allowed in the two minutes before and after each whole hour (platform settlement); failed subscribe funds return immediately.

### Subscribe / Redeem (Case 1, 2, 6)

**Do not call subscribe/redeem API.** Do not show subscribe/redeem draft; do not call `cex_earn_create_uni_lend` (whether type is lend or redeem). Reply only: "Simple Earn subscribe and redeem are currently not supported."

## Safety Rules

- **Subscribe/redeem**: **Do not** call `cex_earn_create_uni_lend` for subscribe or redeem; reply not supported. This skill does not provide any subscribe/redeem API calls.
- **Change lend**: **Do not** call `cex_earn_change_uni_lend` in any form (e.g. change min rate); reply not supported; do not call MCP.
- **No investment advice**: Do not recommend specific currencies or predict rates. Present data (e.g. top APY from list_uni_rate) and let the user decide.
- **Sensitive data**: Never expose API keys, internal endpoint URLs, or raw error traces to the user.
- **Amount and currency**: Reject negative or zero amounts; validate currency is supported (e.g. from list_uni_currencies or get_uni_currency).

## Error Handling

| Condition | Response |
|-----------|----------|
| Auth endpoint returns 401/403 | "Please configure your Gate CEX API Key in MCP with earn/account permission." Do not expose keys or internal details. |
| User requests subscribe/redeem | Do not call API; reply "Simple Earn subscribe and redeem are currently not supported." |
| User requests change lend (e.g. min rate) | Do not call `cex_earn_change_uni_lend`; reply that the operation is not supported. |
| `cex_earn_list_user_uni_lends` or `cex_earn_get_uni_interest` fails | "Unable to load positions/interest. Please check your API key has earn/account read permission." |
| Empty positions or no rate data | "No positions found." / "No rate data available at the moment." |

## Prompt Examples & Scenarios

See [scenarios.md](references/scenarios.md) for full prompt examples and expected behaviors covering all six scenarios (subscribe, redeem, single-currency position, all positions, single-currency interest, subscribe top APY).
