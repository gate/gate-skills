---
name: gate-exchange-pay-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for Gate Pay charge execution via cex_pay_create_ai_order_pay."
---

# Gate Pay MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Execute Gate Pay charge for a prepared merchant order
- Return success/failure receipt

Out of scope:
- Merchant browsing, product discovery, or checkout creation
- Non-Gate-Pay payment channels

Misroute examples:
- If user asks transfer/trading/deposit, route to corresponding exchange skills.

## 2. MCP Detection and Fallback

Detection:
1. Verify payment tool `cex_pay_create_ai_order_pay` is available.
2. Validate required input fields exist before execution.

Fallback:
- If payment endpoint unavailable, stop before execution and provide retry/support guidance.

## 3. Authentication

- API key and valid payment authorization are required.
- If auth is missing/expired, block execution and guide re-authorization.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

Write tool:
- `cex_pay_create_ai_order_pay`

Required input gate:
- Merchant order identifier
- Amount
- Currency
- Any additional required fields per runtime `inputSchema`

Common errors:
- insufficient balance
- invalid/expired authorization
- order not found or expired
- duplicate payment attempts

## 6. Execution SOP (Non-Skippable)

1. Confirm user selected Gate Pay and has explicit pay intent in current turn.
2. Validate required fields and authorization state.
3. Optionally show charge preview (order_id, amount, currency, method).
4. Execute single charge call.
5. Return receipt or failure guidance; never auto-retry duplicate charge.

## 7. Output Templates

```markdown
## Gate Pay Planned Charge
- Merchant Order: {order_id}
- Amount: {amount} {currency}
- Method: Gate Pay
```

```markdown
## Gate Pay Result
- Status: {success_or_failed}
- Merchant Order: {order_id}
- Paid Amount: {amount} {currency}
- Time: {timestamp_if_available}
- Note: Digital asset payments are generally irreversible.
```

## 8. Safety and Degradation Rules

1. Never charge without explicit user payment intent.
2. Never execute with missing required fields.
3. Never claim success when API result is failure/unknown.
4. Never expose raw internal error stacks to user.
5. Never perform duplicate payment as a status-check substitute.
