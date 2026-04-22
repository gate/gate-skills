---
name: gate-exchange-unified-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for Gate unified account operations: mode, borrow/repay, limits, leverage and collateral settings."
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

## 2. `gate-cli` detection and Fallback

Detection:
1. Confirm Gate `gate-cli` supports `get_unified_accounts` and `create_unified_loan`.
2. Probe with a read call (`get_unified_mode` or `get_unified_accounts`).

Fallback:
- MCP missing/auth failure: stop mutation and return setup/auth guidance.
- Partial tool failure: degrade to read-only summary where possible.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required.
- Mutation operations must stop on any permission/auth errors.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

### 5.1 Read commands

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

### 5.2 Write commandss

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
