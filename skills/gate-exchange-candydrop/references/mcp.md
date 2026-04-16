---
name: gate-exchange-candydrop-mcp
version: "2026.4.14-1"
updated: "2026-04-14"
description: "MCP execution specification for CandyDrop: activity/rule queries, registration, task progress, and participation/airdrop records."
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

## 2. MCP Detection and Fallback

Detection:
1. Verify CandyDrop endpoints are available on both Gate (main) and Gate (trading) servers.
2. Probe with public activity listing endpoint (`cex_launch_get_candy_drop_activity_list_v4`).

Fallback:
- If authenticated (trading) endpoints unavailable, keep read-only public mode (activity list + rules only).
- If public endpoints unavailable, inform user that CandyDrop features are temporarily unavailable.

## 3. Authentication

- API key required for: registration, task progress, participation records, airdrop records.
- Public access for: activity list, activity rules.
- Register is a write operation requiring explicit user confirmation.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

- `cex_launch_get_candy_drop_activity_list_v4` (Gate main, public)
- `cex_launch_get_candy_drop_activity_rules_v4` (Gate main, public)
- `cex_launch_get_candy_drop_task_progress_v4` (Gate trading, auth)
- `cex_launch_get_candy_drop_participation_records_v4` (Gate trading, auth)
- `cex_launch_get_candy_drop_airdrop_records_v4` (Gate trading, auth)
- `cex_launch_register_candy_drop_v4` (Gate trading, write)

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
