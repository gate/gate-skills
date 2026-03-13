---
name: gate-exchange-dual
version: "2026.3.12-1"
updated: "2026-03-12"
description: The dual investment function of Gate Exchange — query products, simulate settlements, and manage positions. Use this skill whenever the user asks about dual investment, dual currency, target price settlement simulation, or checking dual investment positions. Trigger phrases include "dual investment", "dual currency", "target price", "exercise price", "dual orders", "dual balance", "shuang-bi", "sell-high", "buy-low", or any request involving dual investment product queries or checking dual investment balance.
---

## General Rules
Read and follow the shared runtime rules before proceeding:
→ [exchange-runtime-rules.md](../exchange-runtime-rules.md)
---

# Gate Exchange Dual Investment Skill

Provide dual investment product discovery, settlement simulation, order history, and balance queries on Gate. Dual investment allows users to earn enhanced yield by setting a target price — if the market price reaches the target at delivery, the settlement is in the exercise currency; otherwise, the user keeps the original investment plus yield.

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

## Routing Rules

| Case | User Intent | Signal Keywords | Action |
|------|-------------|----------------|--------|
| 1 | Browse dual product list | "dual products", "sell-high / buy-low options" | See [product-query.md](references/product-query.md) |
| 3 | Product details | "min investment", "BTC sell-high" | See [product-query.md](references/product-query.md) (filter locally by currency; show matching plans, skip min amount) |
| 4 | Settlement simulation | "what happens at delivery", "if price reaches X" | See [product-query.md](references/product-query.md) (simulation) |
| 5 | Position summary (ongoing) | "how much locked", "active positions" | See [product-query.md](references/product-query.md) (ongoing + balance) |
| 6 | Settlement records | "settlement records", "got crypto or USDT", "last month orders" | See [product-query.md](references/product-query.md) (settled) |
| 7 | Sell-high order (invest crypto) | "sell high for me", "sell high with BTC", "sell high order" | Reply: not supported yet |
| 8 | Buy-low order (invest stablecoin) | "buy low for me", "buy low BTC with USDT", "buy low order" | Reply: not supported yet |
| 9 | Amount eligibility for order | "can I buy", "is 5000U enough" | Reply: not supported yet |
| 10 | Min purchase check for order | "minimum to buy", "can I buy dual with 50U" | Reply: not supported yet |
| 11 | Settlement result query | "what did I receive", "settlement result" | See [settlement-assets.md](references/settlement-assets.md) (settlement) |
| 12 | Dual asset briefing | "dual balance", "total locked" | See [settlement-assets.md](references/settlement-assets.md) (balance) |
| 13 | Currency conversion risk | "will I lose principal", "risk", "principal-protected?" | Domain Knowledge (no API) |
| 14 | Missed gains explanation | "did I lose money", "missed gains", "price surged" | Domain Knowledge (no API) |

## Execution

1. Identify user intent from the Routing Rules table above.
2. For Cases 1–6, 11–12: Read the corresponding sub-module document in `references/` and follow the Workflow.
3. For Cases 7–10: Reply "Order placement is not supported yet. Please visit the Gate official website or App to subscribe." (no API call).
4. For Cases 13–14: Answer directly using Domain Knowledge below (no API call needed).
5. If the user's intent is ambiguous, ask a clarifying question before routing.

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
- **Order status values**: `INIT` (Pending), `SETTLEMENT_SUCCESS` (Settled), `SETTLEMENT_PROCESSING` (Settling), `CANCELED` (Canceled), `FAILED` (Failed), `REFUND_SUCCESS` / `REFUND_PROCESSING` / `REFUND_FAILED` → display as "Early Redemption", never "Refund". Early-redeemed orders have zero yield.

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

- **Timestamp display**: All time fields are Unix timestamps (seconds). Format as **`yyyy-MM-dd`** in **UTC+0** timezone. Label table headers with "(UTC)". Do NOT assume the user's local timezone.
- **Delivery date field**: For orders, "Delivery date" / "Expiry date" must always use **`delivery_time`**. For plans, use **`delivery_timest`**. Do NOT use any other timestamp field for delivery date — using the wrong field will produce incorrect dates.
- **APY display (applies to ALL dual tools — orders, plans, balance, etc.)**: Any APY/rate field (`apy`, `apy_display`, `apy_settlement`, or any other rate field) returned by any dual investment tool is a **raw decimal** (e.g. `0.85` means 85%). You **MUST multiply by 100** then append `%` for display. Use the raw decimal only in formulas. This rule applies to `cex_earn_list_dual_investment_plans`, `cex_earn_list_dual_orders`, `cex_earn_list_dual_balance`, and any other dual tool.
- **Lock period display**: Use the `invest_days` field (integer). Display as a whole number — **no decimals**. Do NOT derive from `invest_hours` by dividing.
- **No investment advice**: Do not recommend specific plans or predict prices. Present data and let the user decide.
- **Non-principal-protected**: Always clearly communicate that dual investment is NOT principal-protected and the user may receive a different currency.
- **Sensitive data**: Never expose API keys, internal endpoint URLs, or raw error traces to the user.

## Error Handling

| Condition | Response |
|-----------|----------|
| Auth endpoint returns "not login" | "Please log in to your Gate account first." |
| `cex_earn_list_dual_investment_plans` returns empty | "No dual investment plans available at the moment." |
| `cex_earn_list_dual_orders` returns empty | "No dual investment orders found for the specified criteria." |

## Prompt Examples & Scenarios

See [scenarios.md](references/scenarios.md) for full prompt examples and expected behaviors covering all 13 cases.
