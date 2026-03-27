---
name: gate-exchange-dual
version: "2026.3.23-1"
updated: "2026-03-23"
description: The dual investment function of Gate Exchange — query products, simulate settlements, place orders, and manage positions. Use this skill whenever the user asks about dual investment, dual currency, target price settlement simulation, placing dual orders, or checking dual investment positions. Trigger phrases include "dual investment", "dual currency", "target price", "exercise price", "dual orders", "dual balance", "shuang-bi", "sell-high", "buy-low", "place dual order", "subscribe dual", or any request involving dual investment product queries, order placement, or checking dual investment balance.
---

# Gate Exchange Dual Investment Skill

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate (main) | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- cex_earn_list_dual_balance
- cex_earn_list_dual_investment_plans
- cex_earn_list_dual_orders

**Execution Operations (Write)**

- cex_earn_place_dual_order

### Authentication
- API Key Required: Yes (see skill doc/runtime MCP deployment)
- Permissions: Earn:Write
- Get API Key: https://www.gate.io/myaccount/profile/api-key/manage

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## Prerequisites

- **MCP Dependency**: Requires [gate-mcp](https://github.com/gate/gate-mcp) to be installed.
- **Authentication**: All endpoints require API key authentication.
- **Risk Disclaimer**: Always append: _"This information is for reference only and does not constitute investment advice. Dual investment is not principal-protected. You may receive settlement in a different currency than your investment. Please understand the product terms before investing."_

## Available MCP Tools

| Tool | Auth | Description |
|------|------|-------------|
| `cex_earn_list_dual_investment_plans` | Yes | List available dual investment plans (optional param: plan_id) |
| `cex_earn_list_dual_orders` | Yes | List dual investment orders. **`page` and `limit` are required**: always pass `page=1, limit=100`. Optional: `from`, `to`. **MUST loop all pages (increment page until returned rows < limit) before drawing any conclusion.** |
| `cex_earn_list_dual_balance` | Yes | Get dual investment balance & interest stats |
| `cex_earn_place_dual_order` | Yes | Place a dual investment order. Params: `plan_id` (required), `amount` (required), `text` (optional, must start with `t-`, max 28 bytes after prefix, alphanumeric/`_`/`-`/`.` only). |

## Routing Rules

| Case | User Intent | Signal Keywords | Action |
|------|-------------|----------------|--------|
| 1 | Browse dual product list | "dual products", "sell-high / buy-low options" | See `references/product-query.md` |
| 3 | Product details | "min investment", "BTC sell-high" | See `references/product-query.md` (filter locally by currency; show matching plans, skip min amount) |
| 4 | Settlement simulation | "what happens at delivery", "if price reaches X" | See `references/product-query.md` (simulation) |
| 5 | Position summary (ongoing) | "how much locked", "active positions" | See `references/product-query.md` (ongoing + balance) |
| 6 | Settlement records | "settlement records", "got crypto or USDT", "last month orders" | See `references/product-query.md` (settled) |
| 7 | Sell-high order (invest crypto) | "sell high for me", "sell high with BTC", "sell high order" | See `references/subscription.md` |
| 8 | Buy-low order (invest stablecoin) | "buy low for me", "buy low BTC with USDT", "buy low order" | See `references/subscription.md` |
| 9 | Amount eligibility for order | "can I buy", "is 5000U enough" | See `references/subscription.md` |
| 10 | Min purchase check for order | "minimum to buy", "can I buy dual with 50U" | See `references/subscription.md` |
| 11 | Settlement result query | "what did I receive", "settlement result" | See `references/settlement-assets.md` (settlement) |
| 12 | Dual asset briefing | "dual balance", "total locked" | See `references/settlement-assets.md` (balance) |
| 13 | Currency conversion risk | "will I lose principal", "risk", "principal-protected?" | Domain Knowledge (no API) |
| 14 | Missed gains explanation | "did I lose money", "missed gains", "price surged" | Domain Knowledge (no API) |
| 15 | Restricted region | "can I buy dual in [region]", "which regions supported" | See `references/subscription.md` (compliance) |
| 17 | Compliance check failure | "subscription failed", "compliance check not passed" | See `references/subscription.md` (compliance) |

## Execution

1. Identify user intent from the Routing Rules table above.
2. For Cases 1–6, 11–12: Read the corresponding sub-module document in `references/` and follow the Workflow.
3. For Cases 7–10: Read `references/subscription.md` and follow the order placement Workflow.
4. For Cases 15, 17: Read `references/subscription.md` and follow the compliance handling Workflow. These cases are triggered by `cex_earn_place_dual_order` error responses or by the user asking about region restrictions.
5. For Cases 13–14: Answer directly using Domain Knowledge below (no API call needed).
6. If the user's intent is ambiguous, ask a clarifying question before routing.

## Domain Knowledge

### Core Concepts

- **Sell High (Call)**: User invests crypto, target price above current price. If settlement price ≥ target price → receive USDT (principal × target price × (1 + interest)); if settlement price < target price → get back crypto + interest.
- **Buy Low (Put)**: User invests stablecoins, target price below current price. If settlement price ≤ target price → receive crypto; if settlement price > target price → get back USDT + interest.
- **Target Price**: The price that determines settlement outcome at delivery. Gate official term.
- **Settlement Price**: Market price of the underlying asset at delivery time, compared against target price.
- **Interest-guaranteed, not principal-protected**: Principal + interest are always received, but the settlement currency may change due to price movement.
- The closer the target price is to the current price, the higher the APY, but also the higher the probability of currency conversion.
- Once placed, dual investment orders cannot be cancelled. Settlement is automatic at delivery time.
- **Order type derivation**: `cex_earn_list_dual_orders` has NO `type` field. Derive from `invest_currency`: crypto (BTC, ETH…) → Sell High (Call); stablecoin (USDT) → Buy Low (Put). Filter by coin using `invest_currency` or `exercise_currency` — there is NO `instrument_name`.
- **Order status values**: `INIT` (Pending), `PROCESSING` (In Position), `SETTLEMENT_SUCCESS` (Settled), `SETTLEMENT_PROCESSING` (Settling), `CANCELED` (Canceled), `FAILED` (Failed), `REFUND_SUCCESS` / `REFUND_PROCESSING` / `REFUND_FAILED` → display as "Early Redemption", never "Refund". Early-redeemed orders have zero yield.

### Settlement Rules (Gate Examples)

**Sell High**: Invest 1 BTC, target price 20,000 USDT, 31 days, 100% APY
- Settlement price < 20,000 → payout = 1 × (1 + 100%/365×31) = **1.0849 BTC**
- Settlement price ≥ 20,000 → payout = 1 × 20,000 × (1 + 100%/365×31) = **21,698.63 USDT**

**Buy Low**: Invest 20,000 USDT, target price 20,000 USDT, 31 days, 100% APY
- Settlement price ≤ 20,000 → payout = 20,000/20,000 × (1 + 100%/365×31) = **1.0849 BTC**
- Settlement price > 20,000 → payout = 20,000 × (1 + 100%/365×31) = **21,698.63 USDT**

### Risk FAQ (Cases 13–14)

**Q: Will I lose principal? (Case 13)**
A: Interest-guaranteed, not principal-protected. You always receive principal + interest, but the settlement currency may change. Sell-high may return crypto instead of USDT; buy-low may return USDT instead of crypto. The closer the target price to the current price, the higher the yield but also the higher the conversion risk.

**Q: I sold high on BTC and it surged — did I lose money? (Case 14)**
A: When settlement price ≥ target price, you successfully sell at the target price and receive USDT, but miss gains above the target price. When settlement price < target price, you get back crypto + interest. This product suits sideways or mildly bullish markets; in strong bull markets you may "miss out" on excess gains.

## Safety Rules

- **Timestamp fields (CRITICAL)**: All time fields (`delivery_time`, `create_time`, `complete_time`, `delivery_timest`) are Unix timestamps (seconds). Do NOT convert them to dates or display them to the user in any form. This includes: (1) Do NOT show timestamps as table columns. (2) Do NOT convert timestamps to dates and use them as section headers or grouping labels (e.g. "Delivery Time: 2026-03-17"). (3) Do NOT mention delivery dates in order confirmations. Simply omit all time-related information from user-facing output.
- **APY display (CRITICAL — applies to ALL dual tools)**: Any APY/rate field (`apy`, `apy_display`, `apy_settlement`, `apyDisplay`, or any other rate field) returned by any dual investment tool is a **raw value — NOT a percentage**. You **MUST multiply by 100** then append `%` for display. **NEVER** display the raw value directly as a percentage. Common mistake: values like `1.1343` or `16.133` look like percentages but they are NOT — `1.1343` → **113.43%**, `16.133` → **1613.3%**. Another example: `0.0619` → **6.19%**, `2.7814` → **278.14%**. Use the raw value only in settlement formulas. This rule applies to ALL dual tools (`cex_earn_list_dual_investment_plans`, `cex_earn_list_dual_orders`, `cex_earn_list_dual_balance`, etc.).
- **APY sanity check (MANDATORY before responding)**: After formatting ALL APY values, scan every value in your output. Typical correct ranges after ×100: crypto sell-high plans → 10%–2000%; stablecoin buy-low plans → 5%–1800%. **If you see any APY displayed as 0.05%–20% (single or low-double digits), you almost certainly forgot to multiply by 100. STOP, go back, and recompute ALL APY values before responding.** For example, if a raw value is `19.9378`, the correct display is `1993.78%` — NOT `19.94%`.
- **No investment advice**: Do not recommend specific plans or predict prices. Present data and let the user decide.
- **Non-principal-protected**: Always clearly communicate that dual investment is NOT principal-protected and the user may receive a different currency.
- **Order placement confirmation**: Before calling `cex_earn_place_dual_order`, MUST show the user the full order details (plan, amount, target price, APY, settlement scenarios) and get **explicit user confirmation**. NEVER place an order without confirmation.
- **Sensitive data**: Never expose API keys, internal endpoint URLs, or raw error traces to the user.

## Error Handling

| Condition | Response |
|-----------|----------|
| Auth endpoint returns "not login" | "Please log in to your Gate account first." |
| `cex_earn_list_dual_investment_plans` returns empty | "No dual investment plans available at the moment." |
| `cex_earn_list_dual_orders` returns empty | "No dual investment orders found for the specified criteria." |
| `cex_earn_place_dual_order` returns region restriction error | See Case 15 in `references/subscription.md` |
| `cex_earn_place_dual_order` returns other compliance error | See Case 17 in `references/subscription.md` |
| `cex_earn_place_dual_order` returns insufficient balance | "Insufficient balance. Please ensure your account has enough funds and try again." |
| `cex_earn_place_dual_order` returns other failure | Display the error message returned by the API to the user. |

## Prompt Examples & Scenarios

See `references/scenarios.md` for full prompt examples and expected behaviors covering all 17 cases.
