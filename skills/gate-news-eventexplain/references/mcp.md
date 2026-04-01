---
name: gate-news-eventexplain-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for event-causality explanation: event detail, related headlines, market snapshot and on-chain context synthesis."
---

# Gate News EventExplain MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Explain why price/event happened
- Build causal chain from events + market + on-chain context

Out of scope:
- Generic daily briefing -> `gate-news-briefing`
- Listing tracker -> `gate-news-listing`

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate-News and Gate-Info tool availability in current environment.
2. Probe one news tool and one market/info tool.

Fallback:
- If one domain unavailable, keep partial explanation and mark uncertainty explicitly.

## 3. Authentication

- API key not required.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

| Tool | Role |
|---|---|
| `news_events_get_event_detail` | primary event fact source |
| `news_events_get_latest_events` | adjacent/related events timeline |
| `news_feed_search_news` | narrative/source corroboration |
| `info_marketsnapshot_get_market_snapshot` | price/volume/volatility context |
| `info_onchain_get_token_onchain` | on-chain participation/liquidity context |

## 6. Execution SOP (Non-Skippable)

1. Normalize target event/asset/time window.
2. Pull event detail first, then parallel fetch supporting context.
3. Build causality chain: trigger -> market reaction -> on-chain reaction -> second-order effects.
4. Mark confidence per causal link (high/medium/low).

## 7. Output Templates

```markdown
## Event Explanation
- Event: {event_title}
- Time: {event_time}
- Immediate Impact: {price_volume_change}
- Causal Chain:
  1. {cause_1}
  2. {cause_2}
  3. {cause_3}
- Confidence: {confidence_level}
- Watchpoints: {followup_risks}
```

## 8. Safety and Degradation Rules

1. Distinguish confirmed facts vs inferred causality.
2. If key data source is missing, reduce confidence and disclose missing source.
3. Do not claim single-cause certainty for complex market moves.
4. Preserve source attribution when available.
5. Avoid trading recommendations; stay explanatory.
