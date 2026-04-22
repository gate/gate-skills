---
name: gate-exchange-collateralloan-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for multi-collateral loans: quota/rate/ltv/order checks, collateral adjustments, create loan and repay operations."
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

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify `cex_mcl_*` tools are available.
2. Probe with LTV or order-list endpoint.

Fallback:
- If write tools fail, keep query-only risk view.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required.
- Mutating loan/collateral operations require explicit confirmation.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

### Read tools
- `gate-cli cex mcl current-rate`
- `gate-cli cex mcl fix-rate`
- `gate-cli cex mcl ltv`
- `gate-cli cex mcl order`
- `gate-cli cex mcl orders`
- `gate-cli cex mcl records`
- `gate-cli cex mcl repay-records`
- `gate-cli cex mcl quota`
- `gate-cli cex mcl collateral`

### Write tools
- `gate-cli cex mcl create`
- `gate-cli cex mcl repay`

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
