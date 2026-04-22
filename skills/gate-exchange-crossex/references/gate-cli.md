---
name: gate-exchange-crossex-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for CrossEx operations across exchanges: account/position/order/history query, transfer, convert, order and leverage management."
---

# Gate CrossEx MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Cross-exchange account/order/position/history queries
- CrossEx order create/cancel/update
- Leverage and mode updates
- CrossEx transfer/convert operations

Out of scope:
- Non-CrossEx spot/futures workflows

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify `cex_crx_*` toolset is available.
2. Probe with account endpoint (`gate-cli cex cross-ex account get`).

Fallback:
- If read probe endpoints are unavailable (for example 404/permission/route errors), treat CrossEx as unavailable in this runtime, stop CrossEx execution, and route user to an alternative supported skill path.
- If read endpoints are available but write endpoints are unavailable, stay in query-only CrossEx mode.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required.
- Mutation actions require explicit confirmation.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

Namespace note:
- `cex_crx` is the base namespace prefix used by CrossEx module tools.

### Read tools
- `gate-cli cex cross-ex account get`
- `gate-cli cex cross-ex market fee`
- `gate-cli cex cross-ex market interest-rate`
- `gate-cli cex cross-ex position margin-leverage`
- `gate-cli cex cross-ex position leverage`
- `gate-cli cex cross-ex order get`
- `gate-cli cex cross-ex order list`
- `gate-cli cex cross-ex position list`
- `gate-cli cex cross-ex position margin-list`
- `gate-cli cex cross-ex order history`
- `gate-cli cex cross-ex position history`
- `gate-cli cex cross-ex order trades`
- `gate-cli cex cross-ex position margin-history`
- `gate-cli cex cross-ex position margin-interests`
- `gate-cli cex cross-ex account book`
- `gate-cli cex cross-ex position adl-rank`
- `gate-cli cex cross-ex market discount-rate`
- `gate-cli cex cross-ex market symbols`
- `gate-cli cex cross-ex market risk-limits`
- `gate-cli cex cross-ex market transfer-coins`
- `gate-cli cex cross-ex transfer list`

### Write tools
- `gate-cli cex cross-ex order create`
- `gate-cli cex cross-ex order cancel`
- `gate-cli cex cross-ex order update`
- `gate-cli cex cross-ex position close`
- `gate-cli cex cross-ex transfer create`
- `gate-cli cex cross-ex convert quote`
- `gate-cli cex cross-ex convert create`
- `gate-cli cex cross-ex account update`
- `gate-cli cex cross-ex position set-margin-leverage`
- `gate-cli cex cross-ex position set-leverage`

## 6. Execution SOP (Non-Skippable)

1. Resolve target domain inside CrossEx (spot/margin/futures/transfer/convert/query).
2. Run read probe first (`gate-cli cex cross-ex account get` or equivalent). If probe fails, stop and degrade as module-unavailable.
3. Pre-check account and product rules (`rule_symbols`, leverage/risk limits as needed).
4. For every mutation, build action draft and require explicit confirmation.
5. Execute write call.
6. Verify resulting state with corresponding read endpoint.

## 7. Output Templates

```markdown
## CrossEx Action Draft
- Action: {order_or_transfer_or_convert_or_update}
- Target: {symbol_or_account}
- Parameters: {key_params}
- Risk: cross-exchange execution and margin/liquidation risk.
Reply "Confirm action" to proceed.
```

```markdown
## CrossEx Result
- Status: {success_or_failed}
- Object ID: {order_or_transfer_id}
- Post-State: {verification_summary}
```

## 8. Safety and Degradation Rules

1. Never execute CrossEx mutations without explicit immediate confirmation.
2. Validate exchange/symbol compatibility before write calls.
3. Surface leverage/risk-limit implications before changing leverage/mode.
4. Preserve backend error details and do not mask risk failures.
5. Degrade to query-only mode when write permissions are unavailable.
