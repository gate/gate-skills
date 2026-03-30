# gate-info-macroimpact — Scenarios & Prompt Examples

## Scenario 1: Named macro event vs BTC

**Context**: User links a specific release (CPI, NFP, Fed) to crypto.

**Prompt Examples**:
- "How does CPI affect BTC"
- "Non-farm payroll impact on crypto"

**Expected Behavior**:
1. Extract `event_keyword` and optional `coin` (default BTC). If the event cannot be identified, ask the user — do not guess.
2. Call in parallel: `info_macro_get_economic_calendar`, `info_macro_get_macro_indicator` (or `info_macro_get_macro_summary` if no specific indicator), `news_feed_search_news`, `info_marketsnapshot_get_market_snapshot`.
3. Output SKILL.md **Report Template**; apply **Decision Logic** for surprise vs forecast.

## Scenario 2: Upcoming macro calendar

**Context**: User asks what macro events are coming.

**Prompt Examples**:
- "Any macro data today"
- "Economic calendar this week"

**Expected Behavior**:
1. Calendar-focused mode: still run the parallel set per SKILL.md; emphasize calendar section if indicator/news are thin.
2. Label pending vs released events clearly.

## Scenario 3: Specific indicator only

**Context**: User wants latest value for one macro series.

**Prompt Examples**:
- "What's the latest CPI reading"
- "Current Fed funds expectations" (map to available indicator API)

**Expected Behavior**:
1. Use `info_macro_get_macro_indicator` when a specific indicator is named; use `info_macro_get_macro_summary` when the query is broad.
2. Correlate with `info_marketsnapshot_get_market_snapshot` for the user's coin if provided.

## Scenario 4: One tool fails

**Context**: Partial MCP failure.

**Prompt Examples**:
- "How does CPI affect BTC" (with calendar or news API error)

**Expected Behavior**:
1. Follow SKILL.md **Error Handling**: skip failed sections, continue with available data; if all fail, return error and suggest retry.

## Scenario 5: Route away

**Context**: No macro angle — pure TA or pure news.

**Prompt Examples**:
- "RSI on ETH" → `gate-info-trendanalysis`
- "Any crypto news" → `gate-news-briefing`
- "Why did BTC crash" → `gate-news-eventexplain`

**Expected Behavior**:
1. Apply **Routing Rules**; do not force macro tools when intent is out of scope.
