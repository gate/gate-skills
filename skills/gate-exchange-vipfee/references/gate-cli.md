---
name: gate-exchange-vipfee-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for VIP tier and trading fee queries on Gate Exchange."
---

# Gate VIP Fee MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Query user VIP level/account detail
- Query spot/futures fee rates

Out of scope:
- Any order placement or account mutation

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify Gate `gate-cli` supports `gate-cli cex account detail` and `gate-cli cex wallet market trade-fee`.
2. Probe with account detail query.

Fallback:
- If MCP unavailable/auth invalid, return setup/auth guidance.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required for user-specific fee data.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

| Command | Purpose | Common errors |
|---|---|---|
| `gate-cli cex account detail` | fetch VIP/account profile context | auth denied |
| `gate-cli cex wallet market trade-fee` | fetch spot/futures fee rates | market/pair filter mismatch |

## 6. Execution SOP (Non-Skippable)

1. Determine query type (VIP level, fee rates, combined).
2. Call minimal required read tools.
3. Normalize fee rendering (maker/taker, spot/futures context).
4. Return structured summary.

## 7. Output Templates

```markdown
## VIP & Fee Summary
- VIP Level: {vip_level}
- Spot Fee: maker {spot_maker}, taker {spot_taker}
- Futures Fee: maker {fx_maker}, taker {fx_taker}
- Notes: {conditions_or_scope}
```

## 8. Safety and Degradation Rules

1. Keep values as returned by API; no fabricated discounts.
2. Distinguish spot and futures fee contexts clearly.
3. If unavailable for a market/pair, mark as unavailable instead of defaulting.
4. This skill is read-only.
5. Preserve timestamp/context when fee values are queried for specific pairs.
