---
name: gate-exchange-dual-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for dual investment: plans/products query, holdings/order query, and dual order placement."
---

# Gate Dual Investment MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Dual investment plan/product queries
- User dual balance and order history
- Dual order placement

Out of scope:
- Non-dual earn products

## 2. MCP Detection and Fallback

Detection:
1. Verify dual investment endpoints are available.
2. Probe with plan or balance endpoint.

Fallback:
- If write endpoint unavailable, keep query-only mode.

## 3. Authentication

- API key required for account and order operations.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

- `cex_earn_list_dual_investment_plans`
- `cex_earn_list_dual_balance`
- `cex_earn_list_dual_orders`
- `cex_earn_place_dual_order`

## 6. Execution SOP (Non-Skippable)

1. Resolve intent: product discovery vs holdings/orders vs place order.
2. For order placement, validate target plan and amount.
3. Show order draft and require explicit confirmation.
4. Execute place order.
5. Verify via dual orders query.

## 7. Output Templates

```markdown
## Dual Order Draft
- Plan: {plan_id_or_name}
- Amount: {amount}
- Settlement Context: {strike_or_settlement_summary}
Reply "Confirm order" to proceed.
```

```markdown
## Dual Order Result
- Status: {success_or_failed}
- Order ID: {order_id}
- Notes: {next_step_or_risk}
```

## 8. Safety and Degradation Rules

1. Never place dual orders without explicit immediate confirmation.
2. Preserve product constraints and settlement rules in output.
3. If plan not found/invalid, block and ask user to choose from listed plans.
4. Keep query-only fallback when write path is unavailable.
5. Do not provide guaranteed return wording.
