---
name: gate-exchange-assets-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for cross-account asset query: spot, margin, futures, options, unified, earn, tradfi and total balance aggregation."
---

# Gate Assets MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Read-only asset overview across account systems
- Account-book and holdings query
- Total balance valuation

Out of scope:
- Any trade/transfer/mutation operations

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify Gate MCP read tools are available (`gate-cli cex wallet balance total` + account-specific reads).
2. Probe with total balance endpoint.

Fallback:
- If one account module fails, return partial asset report with degraded marker.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required for account-level read data.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

- `gate-cli cex wallet balance total`
- `gate-cli cex spot account get`
- `gate-cli cex spot account book`
- `gate-cli cex margin account list`
- `gate-cli cex futures account get`
- `gate-cli cex delivery account get`
- `gate-cli cex options account get`
- `gate-cli cex unified account get`
- `gate-cli cex earn dual balance`
- `gate-cli cex earn dual orders`
- `cex_earn_list_structured_orders` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)
- `gate-cli cex tradfi account assets`

## 6. Execution SOP (Non-Skippable)

1. Identify requested account scope (all vs specific module).
2. Fetch requested modules in parallel where independent.
3. Normalize balances and valuation units.
4. Return layered summary + per-module details.

## 7. Output Templates

```markdown
## Assets Overview
- Total Balance: {total_balance}
- Spot: {spot_summary}
- Margin: {margin_summary}
- Futures/Delivery/Options: {derivatives_summary}
- Unified: {unified_summary}
- Earn/TradFi: {earn_tradfi_summary}
- Notes: {degraded_modules_or_time_window}
```

## 8. Safety and Degradation Rules

1. Keep responses strictly read-only.
2. Preserve API precision and raw valuation values.
3. Mark missing account modules explicitly.
4. Do not infer hidden balances for unavailable modules.
5. Distinguish snapshot values vs account-book historical changes.
