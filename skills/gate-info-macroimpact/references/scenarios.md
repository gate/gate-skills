# gate-info-macroimpact — Scenarios & Prompt Examples

## Scenario 1: Macro indicator impact on BTC

**Context**: User links a macro release (e.g. CPI) to crypto.

**Prompt Examples**:
- "How does CPI affect BTC?"
- "Non-farm payroll just came out — impact on crypto?"

**Expected Behavior**:
1. Extract `event_keyword`, optional `coin` (default BTC), `time_range` per `SKILL.md`.
2. Run in parallel: `info_macro_get_economic_calendar`, `info_macro_get_macro_indicator` (or `info_macro_get_macro_summary` if no specific indicator), `news_feed_search_news`, `info_marketsnapshot_get_market_snapshot` for the coin.
3. Produce **Macro-Economic Impact Analysis** report with calendar, indicator, news context, and market correlation sections.

## Scenario 2: Upcoming macro calendar

**Context**: User asks what macro events are scheduled.

**Prompt Examples**:
- "Any macro data today?"
- "Economic calendar this week for crypto traders"

**Expected Behavior**:
1. Emphasize `info_macro_get_economic_calendar` over the forward window in `SKILL.md`.
2. Still run parallel news + snapshot if the user ties the question to crypto; otherwise calendar-first with brief guidance.
3. Label pending vs released events clearly.

## Scenario 3: Partial tool failure

**Context**: Indicator call fails; calendar and news still work.

**Prompt Examples**:
- "Fed meeting impact" (assume `info_macro_get_macro_indicator` fails)

**Expected Behavior**:
1. Per **Error Handling**: omit indicator detail; use calendar and news if available; omit or shorten market snapshot section if that tool fails.
2. State which dimensions are unavailable without exposing raw script or MCP error stacks to the end user (per `info-news-runtime-rules.md`).
3. Never invent CPI/NFP/Fed values.

## Scenario 4: Route to pure coin analysis

**Context**: User wants technicals or coin report without macro angle.

**Prompt Examples**:
- "Analyze BTC for me" (no macro mention)
- "SOL technical outlook"

**Expected Behavior**:
1. Route to `gate-info-coinanalysis` or `gate-info-trendanalysis` per **Routing Rules**; do not run the full macro parallel quartet unless the user adds macro context.
