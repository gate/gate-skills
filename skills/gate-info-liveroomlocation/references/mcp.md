---
name: gate-info-liveroomlocation-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for Gate live/replay listing by tag, coin, sort, and count."
---

# Gate Live Room Location MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Live/replay list retrieval with tag/coin/sort/limit filters
- Standardized list output with clickable links

Out of scope:
- Trading advice, order execution, or unrelated content discovery

Misroute examples:
- If user asks for market analysis itself, route to analysis skills rather than stream listing.

## 2. MCP Detection and Fallback

Detection:
1. Verify live/replay endpoint availability.
2. Validate filter parameters before request.

Fallback:
- If endpoint fails or returns empty list, return no-result guidance and avoid fabricated entries.

## 3. Authentication

- No API key required in standard public runtime.
- If runtime policy restricts access, return login/availability guidance.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

Single endpoint policy:
- `GET /live/gate_ai/tag_coin_live_replay`

Parameter rules:
- `tag`: optional, default empty
- `coin`: optional, default empty
- `sort`: `hot` or `new`, default `hot`
- `limit`: 1-10, default 10

## 6. Execution SOP (Non-Skippable)

1. Parse intent and map filters.
2. Apply default values for missing filters.
3. Perform single-endpoint query.
4. Map each item by `content_type` to title + URL.
5. Return ordered list and no-result message when needed.

## 7. Output Templates

```markdown
## Live/Replay List
- [Live] {title} - {url}
- [Replay] {title} - {url}
```

## 8. Safety and Degradation Rules

1. Never fabricate live/replay entries.
2. Respect restricted-region block policy when applicable.
3. Keep scope to listing only; no investment claims.
4. Preserve `live` vs `video` link format rules.
