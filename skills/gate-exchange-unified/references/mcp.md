---
name: gate-exchange-unified-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for Gate unified account operations: mode, borrow/repay, limits, leverage and collateral settings."
---

# Gate Unified MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Unified account overview and mode query/switch
- Borrowable/transferable limit query
- Borrow/repay execution
- Leverage and collateral settings
- Loan and interest records

Out of scope:
- Spot/futures order execution
- On-chain wallet operations

## 2. MCP Detection and Fallback

Detection:
1. Confirm Gate MCP exposes `get_unified_accounts` and `create_unified_loan`.
2. Probe with a read call (`get_unified_mode` or `get_unified_accounts`).

Fallback:
- MCP missing/auth failure: stop mutation and return setup/auth guidance.
- Partial tool failure: degrade to read-only summary where possible.

## 3. Authentication

- API key required.
- Mutation operations must stop on any permission/auth errors.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

### 5.1 Read tools

- `get_unified_accounts`
- `get_unified_mode`
- `get_unified_borrowable`
- `get_unified_transferable`
- `list_unified_loan_records`
- `list_unified_loan_interest_records`
- `list_unified_currencies`
- `get_unified_estimate_rate`
- `get_user_leverage_currency_setting`
- `list_currency_discount_tiers`

### 5.2 Write tools

- `create_unified_loan`
- `set_unified_mode`
- `set_user_leverage_currency_setting`
- `set_unified_collateral`

## 6. Execution SOP (Non-Skippable)

1. Classify request: query vs mutation.
2. For mutation, run pre-check (limits/mode compatibility/risk context).
3. Build **Action Draft** with exact amount/value and risk note.
4. Require immediate explicit confirmation.
5. Execute mutation.
6. Return post-state verification via read endpoint.

## 7. Output Templates

```markdown
## Unified Action Draft
- Action: {borrow_or_repay_or_mode_or_leverage_or_collateral}
- Target: {currency_or_mode_or_setting}
- Value: {amount_or_config}
- Pre-check: {limit_or_current_state}
- Risk: {key_risk_note}
Reply "Confirm action" to proceed.
```

```markdown
## Unified Execution Result
- Status: {success_or_failed}
- Core Output: {mode_or_amount_or_setting}
- IMR/MMR: {totalInitialMarginRate}/{totalMaintenanceMarginRate}
- Notes: {error_or_next_step}
```

## 8. Safety and Degradation Rules

1. Keep API numeric strings exact; do not auto-round.
2. Mutation calls always require explicit confirmation.
3. If amount exceeds borrowable/transferable limits, block and return max allowable value.
4. If mode/leverage/collateral change fails, do not chain extra mutations automatically.
5. If unified account is not enabled, place warning at top of response and stop mutation.
