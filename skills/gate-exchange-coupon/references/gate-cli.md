---
name: gate-exchange-coupon-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for Gate coupon queries: list filtering, detail lookup, rule/source interpretation, and status-safe rendering."
---

# Gate Coupon MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- List coupons by status/type/time
- Query coupon detail
- Explain usage rules/source based on returned fields

Out of scope:
- Coupon redemption/execution actions outside read APIs

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify Gate main `gate-cli` supports coupon endpoints.
2. Probe with `gate-cli cex coupon list`.

Fallback:
- MCP/auth unavailable: return setup/auth guidance and stop.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required with coupon read permission.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

| Command | Purpose | Common errors |
|---|---|---|
| `gate-cli cex coupon list` | list/filter user coupons | empty list, invalid filter |
| `gate-cli cex coupon detail` | fetch single coupon details | detail id not found |

## 6. Execution SOP (Non-Skippable)

1. Parse user intent: list vs detail vs rule/source explanation.
2. For list requests, map filters (`coupon_type`, `expired`, `limit`, etc.).
3. For detail requests, require `detail_id` (or derive from selected list item).
4. Return structured output with strict coupon type mapping.

## 7. Output Templates

```markdown
## Coupon List Summary
- Total Returned: {count}
- Valid: {valid_count}
- Expired/Used: {expired_or_used_count}
- Top Items: {brief_rows}
```

```markdown
## Coupon Detail
- Type: {coupon_type_display}
- Status: {status}
- Expiry: {expire_time}
- Scope/Rules: {rule_summary}
- Source: {source_summary}
```

## 8. Safety and Degradation Rules

1. Do not conflate coupon types (especially `position_voucher` vs `contract_bonus`).
2. If no coupons are returned, report empty state explicitly.
3. Preserve backend status and time fields; do not invent availability.
4. Keep responses read-only; never imply redemption was executed.
5. Include rule limitations when user asks "can I use this now".
