---
name: gate-exchange-coupon-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for Gate coupon queries: list filtering, detail lookup, rule/source interpretation, and status-safe rendering."
---

# Gate Coupon MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- List coupons by status/type/time
- Query coupon detail
- Explain usage rules/source based on returned fields

Out of scope:
- Coupon redemption/execution actions outside read APIs

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate main MCP exposes coupon endpoints.
2. Probe with `cex_coupon_list_user_coupons`.

Fallback:
- MCP/auth unavailable: return setup/auth guidance and stop.

## 3. Authentication

- API key required with coupon read permission.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

| Tool | Purpose | Common errors |
|---|---|---|
| `cex_coupon_list_user_coupons` | list/filter user coupons | empty list, invalid filter |
| `cex_coupon_get_user_coupon_detail` | fetch single coupon details | detail id not found |

## 6. Execution SOP (Non-Skippable)

1. Parse user intent: list vs detail vs rule/source explanation.
2. For list requests, map filters (`coupon_type`, `expired`, `limit`, etc.).
3. For detail requests, require `detail_id` (or derive from selected list item).
4. Return structured output with strict coupon type mapping.

## 7. Output Templates

```markdown
## Coupon List Summary
- Total Returned: {count}
- Valid: {valid_count}
- Expired/Used: {expired_or_used_count}
- Top Items: {brief_rows}
```

```markdown
## Coupon Detail
- Type: {coupon_type_display}
- Status: {status}
- Expiry: {expire_time}
- Scope/Rules: {rule_summary}
- Source: {source_summary}
```

## 8. Safety and Degradation Rules

1. Do not conflate coupon types (especially `position_voucher` vs `contract_bonus`).
2. If no coupons are returned, report empty state explicitly.
3. Preserve backend status and time fields; do not invent availability.
4. Keep responses read-only; never imply redemption was executed.
5. Include rule limitations when user asks "can I use this now".
