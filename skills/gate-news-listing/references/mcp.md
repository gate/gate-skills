---
name: gate-news-listing-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for exchange listing radar: announcements retrieval, market/fundamental enrichment, and listing-focused reporting."
---

# Gate News Listing MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Exchange listing/delisting/maintenance announcement tracking
- Enrichment with market snapshot and token fundamentals

Out of scope:
- Generic news briefing -> `gate-news-briefing`
- Event causality deep explanation -> `gate-news-eventexplain`

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate-News and supporting Info tools are available.
2. Probe `news_feed_get_exchange_announcements`.

Fallback:
- If announcement tool fails, stop and report no listing feed.
- If enrichment tools fail, return announcement-only report with degraded markers.

## 3. Authentication

- API key not required.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

| Tool | Role |
|---|---|
| `news_feed_get_exchange_announcements` | primary listing/delisting source |
| `info_marketsnapshot_get_market_snapshot` | market move context for listed coins |
| `info_coin_get_coin_info` | project/fundamental enrichment |
| `info_coin_get_coin_rankings` | optional ranking context |

## 6. Execution SOP (Non-Skippable)

1. Parse exchange/time scope and announcement type filters.
2. Retrieve exchange announcements first.
3. Extract high-interest symbols and run enrichment calls.
4. Deduplicate and classify announcements (listing/delisting/maintenance).
5. Output listing-focused report with clear evidence source.

## 7. Output Templates

```markdown
## Listing Radar
- Exchange Scope: {exchange_or_all}
- Time Window: {time_range}
- New Listings: {count}
- Delistings/Maintenance: {count}

### Key Items
1. {announcement_item}
2. {announcement_item}

### Coin Enrichment
- {symbol}: {brief_fundamental_and_market_context}
```

## 8. Safety and Degradation Rules

1. Treat exchange announcement feed as source of truth for listing status.
2. Do not infer "listed" from price moves alone.
3. Clearly distinguish confirmed listing vs rumor/speculation.
4. If enrichment is missing, keep announcement facts and mark missing context.
5. Preserve announcement timestamps/exchange names exactly.
