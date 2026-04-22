---
name: gate-exchange-simpleearn-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for Simple Earn: product discovery, positions/history, uni lend operations, fixed-term subscribe/redeem flows."
---

# Gate SimpleEarn MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Query Simple Earn products/positions/history/rates
- Uni lend adjustments and lend/redeem actions
- Fixed-term subscribe/redeem actions

Out of scope:
- Non-earn trading actions

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify `cex_earn_*` toolset availability.
2. Probe with `gate-cli cex earn uni rate` or product listing endpoint.

Fallback:
- If write tools are unavailable, stay in query-only mode.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required for account/product operations.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

### Read tools
- `gate-cli cex earn uni rate`
- `gate-cli cex earn uni currency`
- `gate-cli cex earn uni interest`
- `gate-cli cex earn uni lends`
- `gate-cli cex earn fixed products`
- `gate-cli cex earn fixed products-asset`
- `gate-cli cex earn fixed lends`
- `gate-cli cex earn fixed history`
- `gate-cli cex earn uni change`

### Write tools
- `gate-cli cex earn uni lend`
- `gate-cli cex earn fixed create`
- `gate-cli cex earn fixed pre-redeem`

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
