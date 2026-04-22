---
name: gate-exchange-affiliate-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for affiliate/partner analytics: eligibility, application status, partner commission/transaction/sub-user reports."
---

# Gate Affiliate MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Partner eligibility/application status queries
- Partner commission and transaction history
- Partner subordinate/user relationship reports

Out of scope:
- Direct application submission workflows not exposed in this skill

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify rebate/partner endpoints are available.
2. Probe `gate-cli cex rebate partner eligibility`.

Fallback:
- If history endpoints fail, return eligibility/status only.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required with partner/rebate permissions.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

- `gate-cli cex rebate partner eligibility`
- `gate-cli cex rebate partner application`
- `gate-cli cex rebate partner commissions`
- `gate-cli cex rebate partner transactions`
- `gate-cli cex rebate partner sub-list`

## 6. Execution SOP (Non-Skippable)

1. Classify intent: eligibility/application vs commission/transaction analytics.
2. Normalize time range (respect endpoint constraints).
3. Fetch minimal required endpoints.
4. Aggregate into partner report with key KPIs.

## 7. Output Templates

```markdown
## Affiliate Partner Snapshot
- Eligibility: {eligible_or_not}
- Application Status: {recent_application_state}
- Commission: {commission_summary}
- Transactions: {transaction_summary}
- Subordinate Stats: {sub_list_summary}
```

## 8. Safety and Degradation Rules

1. Respect endpoint time-range limitations and disclose truncation.
2. Do not fabricate partner metrics when no data is returned.
3. Keep user-level data privacy boundaries in summaries.
4. If permission is insufficient, report required role clearly.
5. Keep outputs read-only.
