---
name: gate-exchange-simpleearn-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for Simple Earn: product discovery, positions/history, uni lend operations, fixed-term subscribe/redeem flows."
---

# Gate SimpleEarn MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Query Simple Earn products/positions/history/rates
- Uni lend adjustments and lend/redeem actions
- Fixed-term subscribe/redeem actions

Out of scope:
- Non-earn trading actions

## 2. MCP Detection and Fallback

Detection:
1. Verify `cex_earn_*` toolset availability.
2. Probe with `cex_earn_list_uni_rate` or product listing endpoint.

Fallback:
- If write tools are unavailable, stay in query-only mode.

## 3. Authentication

- API key required for account/product operations.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

### Read tools
- `cex_earn_list_uni_rate`
- `cex_earn_get_uni_currency`
- `cex_earn_get_uni_interest`
- `cex_earn_list_user_uni_lends`
- `cex_earn_list_earn_fixed_term_products`
- `cex_earn_list_earn_fixed_term_products_by_asset`
- `cex_earn_list_earn_fixed_term_lends`
- `cex_earn_list_earn_fixed_term_history`
- `cex_earn_change_uni_lend`

### Write tools
- `cex_earn_create_uni_lend`
- `cex_earn_create_earn_fixed_term_lend`
- `cex_earn_create_earn_fixed_term_pre_redeem`

## 6. Execution SOP (Non-Skippable)

1. Classify query vs action.
2. For actions, pre-check product/amount eligibility.
3. Show **Earn Action Draft** (asset, amount, product, expected constraints).
4. Require explicit confirmation.
5. Execute write call and re-query state.

## 7. Output Templates

```markdown
## SimpleEarn Action Draft
- Action: {lend_or_redeem_or_subscribe}
- Asset/Product: {asset_or_product}
- Amount: {amount}
- Constraint: {lockup_or_rate_or_rule}
Reply "Confirm action" to proceed.
```

```markdown
## SimpleEarn Result
- Status: {success_or_failed}
- Asset/Product: {asset_or_product}
- Amount: {amount}
- Follow-up: {position_or_history_hint}
```

## 8. Safety and Degradation Rules

1. Never execute lend/redeem/subscribe without explicit immediate confirmation.
2. Preserve lock period and redemption constraints in user output.
3. If eligibility checks fail, block execution and explain exact reason.
4. Mark unavailable write capability as query-only degraded mode.
5. Keep API values exact; avoid silent rounding.
