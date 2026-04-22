---
name: gate-exchange-activitycenter-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for activity center queries: my activity entry, activity types, and activity listings with filters."
---

# Gate ActivityCenter MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Query my activity entry
- Query available activity types
- Query activity list with filters/pagination

Out of scope:
- Executing activity participation actions not exposed by `gate-cli` commands

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify activity tools are available.
2. Probe with `gate-cli cex activity get-entry`.

Fallback:
- If listing endpoint fails, return entry/type info only.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required for user-specific activity entry.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

- `gate-cli cex activity get-entry`
- `gate-cli cex activity types`
- `gate-cli cex activity list`

## 6. Execution SOP (Non-Skippable)

1. Identify intent: entry vs list vs filtered recommendation.
2. Apply filters (`type`, `keywords`, `sort`, pagination).
3. Return activity cards with essential metadata and links.

## 7. Output Templates

```markdown
## Activity Center Summary
- My Entry: {entry_summary}
- Activity Types: {type_list}
- Recommended Activities: {top_items}
- Filters Applied: {filters}
```

## 8. Safety and Degradation Rules

1. Keep activity availability/status exactly from API.
2. Do not fabricate rewards, quotas, or deadlines.
3. If no activities found under filter, return explicit empty-state guidance.
4. Preserve pagination/ordering transparency.
5. Skill is read-only for activity data.
