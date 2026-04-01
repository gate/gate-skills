---
name: gate-exchange-collateralloan-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for multi-collateral loans: quota/rate/ltv/order checks, collateral adjustments, create loan and repay operations."
---

# Gate CollateralLoan MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Multi-collateral loan quota/rate/LTV query
- Loan order query and records
- Collateral add/withdraw and repay operations
- New loan creation

Out of scope:
- Spot/futures trading actions

## 2. MCP Detection and Fallback

Detection:
1. Verify `cex_mcl_*` tools are available.
2. Probe with LTV or order-list endpoint.

Fallback:
- If write tools fail, keep query-only risk view.

## 3. Authentication

- API key required.
- Mutating loan/collateral operations require explicit confirmation.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

### Read tools
- `cex_mcl_get_multi_collateral_current_rate`
- `cex_mcl_get_multi_collateral_fix_rate`
- `cex_mcl_get_multi_collateral_ltv`
- `cex_mcl_get_multi_collateral_order_detail`
- `cex_mcl_list_multi_collateral_orders`
- `cex_mcl_list_multi_collateral_records`
- `cex_mcl_list_multi_repay_records`
- `cex_mcl_list_user_currency_quota`
- `cex_mcl_operate_multi_collateral`

### Write tools
- `cex_mcl_create_multi_collateral`
- `cex_mcl_repay_mcl`

## 6. Execution SOP (Non-Skippable)

1. Classify intent: risk/query vs mutation.
2. For mutations, pre-check quota and LTV constraints.
3. Build action draft (loan amount/collateral change/repay amount + risk note).
4. Require explicit confirmation.
5. Execute write call and re-check LTV/order state.

## 7. Output Templates

```markdown
## Collateral Loan Action Draft
- Action: {create_loan_or_repay_or_adjust_collateral}
- Assets: {collateral_and_borrow_assets}
- Amount: {amount}
- Risk: LTV/liquidation sensitivity.
Reply "Confirm action" to proceed.
```

```markdown
## Collateral Loan Result
- Status: {success_or_failed}
- Order/Record: {id_or_summary}
- Updated LTV: {ltv}
- Notes: {next_step_or_warning}
```

## 8. Safety and Degradation Rules

1. Never execute loan/collateral mutations without explicit immediate confirmation.
2. Surface LTV and risk warnings before mutation.
3. If quota is insufficient, block and provide max allowable values.
4. Preserve backend failure reasons for risk troubleshooting.
5. Keep query-only fallback when write capability is degraded.
