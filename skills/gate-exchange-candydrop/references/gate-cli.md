---
name: gate-exchange-candydrop-gate-cli
version: "2026.4.14-1"
updated: "2026-04-14"
description: "gate-cli execution specification for CandyDrop: activity/rule queries, registration, task progress, and participation/airdrop records."
---

# Gate CandyDrop MCP Specification

**Authoring language:** This file is maintained in **English** (Gate skill standard).

## 1. Scope and Trigger Boundaries

In scope:
- CandyDrop activity listing and filtering
- Activity rules (prize pools and tasks) query
- Activity registration (with confirmation)
- Task progress query for enrolled users
- Participation records query
- Airdrop records query

Out of scope:
- Non-CandyDrop earn modules
- LaunchPool or SimpleEarn operations

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify CandyDrop endpoints are available on both Gate (main) and Gate (trading) servers.
2. Probe with public activity listing endpoint (`gate-cli cex launch candy-drop activities`).

Fallback:
- If authenticated (trading) endpoints unavailable, keep read-only public mode (activity list + rules only).
- If public endpoints unavailable, inform user that CandyDrop features are temporarily unavailable.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required for: registration, task progress, participation records, airdrop records.
- Public access for: activity list, activity rules.
- Register is a write operation requiring explicit user confirmation.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

- `gate-cli cex launch candy-drop activities` (Gate main, public)
- `gate-cli cex launch candy-drop rules` (Gate main, public)
- `gate-cli cex launch candy-drop progress` (Gate trading, auth)
- `gate-cli cex launch candy-drop participations` (Gate trading, auth)
- `gate-cli cex launch candy-drop airdrops` (Gate trading, auth)
- `gate-cli cex launch candy-drop register` (Gate trading, write)

## 6. Execution SOP (Non-Skippable)

1. Resolve intent: query (activities/rules/progress/records) vs register. For **activity list** queries, output **only** title + table (no tutorial or mapping tables). **Localize `rule_name`** in cells per `references/activities.md` when the user is not using English.
2. For registration, validate `currency` (required) and optional `activity_id`.
3. Present registration preview with currency and activity details.
4. Require explicit confirmation.
5. Execute registration and verify.
6. For records queries, follow timestamp strategy (see `references/records.md`). Apply **time cell display** (strip redundant trailing `(UTC)` when the column header already marks UTC) and, for airdrops, **amount unit display** (`rewards` + row `currency` only; do **not** show `convert_amount`).

## 7. Output Templates

```markdown
## CandyDrop Action Draft
- Action: {register}
- Currency: {currency}
- Activity ID: {activity_id or "auto-matched"}
- Notes: {activity_summary}
Reply "Confirm action" to proceed.
```

```markdown
## CandyDrop Result
- Status: {success_or_failed}
- Currency: {currency}
- Follow-up: {record_check_hint}
```

## 8. Safety and Degradation Rules

1. Never execute registration without explicit immediate confirmation.
2. Preserve `currency` and `activity_id` exactly as user-confirmed.
3. If activity not found or parameters invalid, block and explain why.
4. Keep read-only fallback when authenticated endpoints are unavailable.
5. Do not promise reward outcomes or airdrop amounts.
6. For time-based records queries, always follow the Timestamp Strategy in `references/records.md` — do NOT attempt to mentally compute unix timestamps without the anchor table.
