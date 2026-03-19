---
name: gate-exchange-simpleearn
version: "2026.3.18-5"
updated: "2026-03-18"
description: Query Gate Simple Earn flexible (Uni) and fixed-term workflows, including product lists, positions, interest, subscribe, redeem, and change-min-rate intents. Use this skill whenever the user asks about Simple Earn, Uni, fixed-term, subscribe, redeem, positions, interest, or top APY. Trigger phrases include "Simple Earn", "Uni", "flexible earn", "fixed-term", "subscribe", "redeem", "positions", "interest", "top APY", or equivalent.
---

# Gate Exchange Simple Earn Skill

Provide Gate Simple Earn **flexible (Uni)** and **fixed-term** operations on Gate. Use the flexible Uni references for flexible positions, interest, subscribe, redeem, and change-min-rate workflows, and use the fixed-term references for fixed-term product lists, subscribe, early redeem, positions, and history. This skill treats both workflows as supported and routes each request to the matching MCP tool family.

## Trigger Conditions

Activate this skill when the user expresses any of the following intents:
- Simple Earn, Uni, flexible earn, fixed earn, fixed-term, subscribe, redeem, positions, interest, top APY
- Any request involving Simple Earn subscribe, redeem, position query, interest query, fixed-term product list, or fixed-term history query

## Prerequisites

- **MCP Dependency**: Requires [gate-mcp](https://github.com/gate/gate-mcp) to be installed.
- **Authentication**: Position and write operations require API key authentication; rate and currency queries are public.
- **Disclaimer**: Always append when showing APY or rates: _"This information is for reference only and does not constitute investment advice. APY may change. Please understand the product terms before subscribing."_

## Supported Workflows

### Flexible (Uni)
- Single-currency or all positions query
- Single-currency interest query
- Estimated APY query
- Subscribe (lend), redeem, and change min rate operations with user confirmation

### Fixed-term
- Product list and product list by currency
- Subscribe and early redeem with user confirmation
- Current total positions and single-order detail queries
- History queries for subscribe, redeem, interest, and extra bonus

## Available MCP Tools

### Flexible (Uni)

| Tool | Auth | Description | Reference |
|------|------|-------------|-----------|
| `cex_earn_list_uni_rate` | No | Estimated APY per currency (currency enumeration; use with get_uni_currency for limits) | `references/earn-uni-mcp-tools.md` |
| `cex_earn_get_uni_currency` | No | Single-currency details (min_rate for subscribe) | `references/earn-uni-mcp-tools.md` |
| `cex_earn_create_uni_lend` | Yes | Create lend (subscribe) or redeem | `references/earn-uni-mcp-tools.md` |
| `cex_earn_change_uni_lend` | Yes | Change min rate for lend | `references/earn-uni-mcp-tools.md` |
| `cex_earn_list_user_uni_lends` | Yes | User positions (optional currency filter) | `references/earn-uni-mcp-tools.md` |
| `cex_earn_get_uni_interest` | Yes | Single-currency cumulative interest | `references/earn-uni-mcp-tools.md` |
| `cex_earn_list_uni_rate` | No | Estimated APY per currency (for top APY) | `references/earn-uni-mcp-tools.md` |

### Fixed-term

| Tool | Auth | Description | Reference |
|------|------|-------------|-----------|
| `cex_earn_list_earn_fixed_term_products` | No | List all fixed-term products | `references/fixed-earn-mcp-tools.md` |
| `cex_earn_list_earn_fixed_term_products_by_asset` | No | List fixed-term products by currency | `references/fixed-earn-mcp-tools.md` |
| `cex_earn_create_earn_fixed_term_lend` | Yes | Create fixed-term lend (subscribe) | `references/fixed-earn-mcp-tools.md` |
| `cex_earn_create_earn_fixed_term_pre_redeem` | Yes | Early redeem fixed-term order | `references/fixed-earn-mcp-tools.md` |
| `cex_earn_list_earn_fixed_term_lends` | Yes | User fixed-term positions | `references/fixed-earn-mcp-tools.md` |
| `cex_earn_list_earn_fixed_term_history` | Yes | Fixed-term history records | `references/fixed-earn-mcp-tools.md` |

## Routing Rules

### Flexible requests

| Case | User Intent | Signal Keywords | Action |
|------|-------------|-----------------|--------|
| 1 | Subscribe (lend) | "subscribe", "lend to Simple Earn" | Collect currency/amount/min_rate and confirm, then call `cex_earn_create_uni_lend` with `type: lend`. |
| 2 | Redeem | "redeem", "redeem from Simple Earn" | Collect currency/amount and confirm, then call `cex_earn_create_uni_lend` with `type: redeem`. |
| 3 | Single-currency position | "my USDT Simple Earn", "position for one currency" | See `references/scenarios.md` flexible scenario section |
| 4 | All positions | "all Simple Earn positions", "total positions" | See `references/scenarios.md` flexible scenario section |
| 5 | Single-currency interest | "interest", "USDT interest" | See `references/scenarios.md` flexible scenario section |
| 6 | Subscribe top APY | "top APY", "one-click subscribe top APY" | Show top APY via `cex_earn_list_uni_rate`, ask confirmation, then call `cex_earn_create_uni_lend`. |
| 7 | Change lend settings (e.g. min rate) | "change min_rate", "change Simple Earn settings" | Collect currency/min_rate and confirm, then call `cex_earn_change_uni_lend`. |
| 8 | Auth failure (401/403) | MCP returns 401/403 | Do not expose keys; prompt user to configure Gate CEX API Key (earn). |

### Fixed-term requests

| Case | User Intent | Signal Keywords | Action |
|------|-------------|-----------------|--------|
| 1 | All fixed-term products | "fixed-term products" | See `references/scenarios.md` fixed-term section 1 and `references/fixed-earn-mcp-tools.md` §1 |
| 2 | Fixed-term products by currency | "USDT fixed-term products" | See `references/scenarios.md` fixed-term section 2 and `references/fixed-earn-mcp-tools.md` §2 |
| 3 | Fixed-term subscribe | "subscribe 1 SOL fixed-term" | Collect currency/amount/term and confirm, then call `cex_earn_create_earn_fixed_term_lend`. |
| 4 | Fixed-term early redeem | "redeem order 5862443199" | Collect `order_id` and confirm, then call `cex_earn_create_earn_fixed_term_pre_redeem`. |
| 5 | Fixed-term total positions | "total fixed-term positions", "current total fixed-term position amount" | Call `cex_earn_list_earn_fixed_term_lends` with `order_type: "1"`, `page`, and `limit`. |
| 6 | Single fixed-term order detail | "order 5862443199" | Call `cex_earn_list_earn_fixed_term_lends` with `order_type: "1"` and `order_id`. |
| 7 | Fixed-term history | "subscription records", "redeem records", "interest records" | Call `cex_earn_list_earn_fixed_term_history` with `type`, `page`, `limit`, and optional time range. |
| 8 | Compliance / region restriction | region restriction questions | Return the standard compliance error message if the API rejects the request. |
| 9 | Compliance check failure | compliance validation failed | Do not retry or expose internal logic; return the API error message when available. |

## Execution

1. Identify user intent from the routing rules above.
2. For flexible subscribe/redeem/top APY and fixed-term subscribe/early redeem: collect required params, confirm with the user, then call the corresponding MCP tool.
3. For flexible or fixed-term read-only queries: read the matching scenario section in `references/scenarios.md` and follow the workflow there.
4. For auth failures: do not expose API keys or raw errors; prompt the user to configure API key / log in again.
5. If the intent is ambiguous, ask a clarifying question before routing.

## Domain Knowledge

### Flexible (Uni)

- Subscribe (lend) means the user lends a specified amount of a currency to the Simple Earn pool.
- Redeem means the user redeems a specified amount from the pool.
- `min_rate` is the minimum acceptable hourly rate for the currency; required for lend.
- Settlement windows: lend and redeem are not allowed in the two minutes before and after each whole hour (use for errors/logic only; do not surface specific clock times or timestamps to the user unless the user explicitly asks when settlement applies).
- **User-facing display (flexible only)**: In any reply based on flexible Uni MCP data, **do not show time-related fields**—omit timestamps, dates, time-of-day, countdowns, chart time axes, history operation times, and any API field whose purpose is *when* something occurred. Show only non-time facts (currency, amounts, balances, rates/APY, `interest_status`, success/failure). If a tool returns only time-series data (e.g. APY chart), summarize without timestamps (e.g. latest estimated APY only) or skip the series.

### Fixed-term

- Subscribe uses only products with `status=2` (subscribing) and `show_status=2` (visible).
- Product list queries can be filtered by currency and product type.
- Fixed-term positions and history should be presented using the table formats defined in `references/scenarios.md` and `references/fixed-earn-mcp-tools.md`.
- Early redeem uses the fixed-term order ID and returns the redeemed principal.

## Safety Rules

- Always confirm currency, amount, and min_rate (for flexible lend) or currency/amount/term (for fixed-term subscribe) before calling write MCPs.
- Always confirm order_id before calling fixed-term early redeem.
- Do not recommend specific currencies or predict rates.
- Never expose API keys, internal endpoint URLs, or raw error traces to the user.
- Reject negative or zero amounts; validate that the currency is supported.

## Error Handling

| Condition | Response |
|-----------|----------|
| Auth endpoint returns 401/403 | "Please configure your Gate CEX API Key in MCP with earn/account permission." Do not expose keys or internal details. |
| Flexible subscribe/redeem or fixed-term write request fails validation | Validate inputs, confirm details, then call the corresponding write tool. |
| Position or history query fails | "Unable to load positions/history. Please check your API key has earn/account read permission." |
| Empty positions or no rate data | "No positions found." / "No rate data available at the moment." |

## Reference Files

- Flexible (Uni) MCP tools: `references/earn-uni-mcp-tools.md`
- Fixed-term MCP tools: `references/fixed-earn-mcp-tools.md`
- Prompt examples and routing: `references/scenarios.md`
