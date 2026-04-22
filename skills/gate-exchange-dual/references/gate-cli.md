---
name: gate-exchange-dual-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for dual investment: plans/products query, holdings/order query, and dual order placement."
---

# Gate Dual Investment MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Dual investment plan/product queries
- User dual balance and order history
- Dual order placement

Out of scope:
- Non-dual earn products

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify dual investment endpoints are available.
2. Probe with plan or balance endpoint.

Fallback:
- If write endpoint unavailable, keep query-only mode.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required for account and order operations.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

- `gate-cli cex earn dual plans`
- `gate-cli cex earn dual balance`
- `gate-cli cex earn dual orders`
- `gate-cli cex earn dual place`

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
