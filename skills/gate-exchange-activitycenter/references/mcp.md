---
name: gate-exchange-activitycenter-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for activity center queries: my activity entry, activity types, and activity listings with filters."
---

# Gate ActivityCenter MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Query my activity entry
- Query available activity types
- Query activity list with filters/pagination

Out of scope:
- Executing activity participation actions not exposed by MCP tools

## 2. MCP Detection and Fallback

Detection:
1. Verify activity tools are available.
2. Probe with `cex_activity_get_my_activity_entry`.

Fallback:
- If listing endpoint fails, return entry/type info only.

## 3. Authentication

- API key required for user-specific activity entry.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

- `cex_activity_get_my_activity_entry`
- `cex_activity_list_activity_types`
- `cex_activity_list_activities`

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
