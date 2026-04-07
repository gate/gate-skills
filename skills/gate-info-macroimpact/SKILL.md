---
name: gate-info-macroimpact
version: "2026.4.6-1"
updated: "2026-04-06"
description: "Macro-driven crypto via Gate-Info and Gate-News MCP. Use this skill whenever macro (CPI, NFP, Fed, rates, payrolls) ties to crypto, calendar, or indicator-price links. Trigger phrases include CPI and BTC, macro today, Fed, NFP, rates. Route: price/technicals → gate-info-coinanalysis or gate-info-trendanalysis; headlines → gate-news-briefing; attribution → gate-news-eventexplain. Tools: info_macro_* (calendar, indicator, summary), news_feed_search_news, info_marketsnapshot_get_market_snapshot."
required_credentials: []
required_env_vars: []
required_permissions: []
---

# gate-info-macroimpact

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read `./references/gate-runtime-rules.md`
→ Also read `./references/info-news-runtime-rules.md` for gate-info / gate-news shared rules (tool degradation, report standards, security, and output standards).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

> The Macro-Economic Impact Analysis Skill. When the user asks about the impact of macro data/events on the crypto market, the system calls MCP tools in parallel to fetch economic calendar, macro indicators (or summary), related news, and correlated coin market data, then the LLM produces a structured correlation analysis report.

**Trigger Scenarios**: User mentions macroeconomic events/indicators and crypto market impact, e.g., "how does non-farm payroll affect BTC", "any macro data today", "Fed meeting impact on the market", "has CPI been released".

---

## MCP Dependencies

### Required MCP Servers

| MCP Server | Status |
|------------|--------|
| Gate-Info | ✅ Required |
| Gate-News | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- info_macro_get_economic_calendar
- info_macro_get_macro_indicator
- info_macro_get_macro_summary (use when no specific indicator is named)
- news_feed_search_news
- info_marketsnapshot_get_market_snapshot

### Authentication
- API Key Required: No
- Credentials Source: None; this skill uses read-only Gate Info / Gate News MCP access only.

### Installation Check
- Required: Gate-Info, Gate-News
- Install: Use the local Gate MCP installation flow for the current host IDE before continuing.
- Continue only after the required Gate MCP server is available in the current environment.

## Routing Rules

| User Intent | Keywords | Action |
|-------------|----------|--------|
| Macro event impact on crypto | "non-farm payroll BTC" "CPI crypto impact" "Fed decision market" | Execute this Skill's full workflow |
| Upcoming economic calendar | "any macro data today" "economic calendar this week" | Execute this Skill (calendar-focused mode) |
| Specific macro indicator query | "what's the current CPI" "latest GDP data" | Execute this Skill (indicator-focused mode) |
| Pure coin analysis without macro angle | "analyze SOL" "how is BTC" | Route to `gate-info-coinanalysis` |
| Market overview | "how's the market" | Route to `gate-info-marketoverview` |
| News only | "any crypto news" | Route to `gate-news-briefing` |
| Why price moved | "why did BTC crash" | Route to `gate-news-eventexplain` |

---

## Execution Workflow

### Step 0: Multi-Dimension Intent Check

- If the query is about macro-economic impact on crypto, proceed with this Skill.
- If the query also mentions coin-specific fundamentals, risk check, or on-chain data beyond the macro angle, route to `gate-info-research` (if available).

### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:

- `event_keyword`: Macro event/indicator name (e.g., "CPI", "non-farm payroll", "Fed meeting", "interest rate")
- `coin` (optional): Related coin (default: BTC if not specified)
- `time_range`: Time window for calendar/news (default: 7d for calendar, 24h for news)

If the macro event cannot be identified, ask the user to clarify — do not guess.

### Step 2: Call MCP Tools in Parallel

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `info_macro_get_economic_calendar` | `start_date={today}, end_date={today+14d}` | Upcoming economic events | Yes |
| 1b | `info_macro_get_macro_indicator` | `mode="latest", indicator={event_keyword}` | Latest value of the specific macro indicator | Yes |
| 1c | `news_feed_search_news` | `query={event_keyword}, limit=5, sort_by="importance"` | Related news articles | Yes |
| 1d | `info_marketsnapshot_get_market_snapshot` | `symbol={coin}, timeframe="1d"` | Current market data for the correlated coin | Yes |

**Note:** If a specific indicator is not mentioned, use `info_macro_get_macro_summary` instead of `info_macro_get_macro_indicator` for Step 1b.

All four primary tools run in parallel when applicable.

### Step 3: LLM Aggregation

The LLM must:

- Match the user's query to relevant economic calendar events
- Compare actual vs forecast vs previous values (surprise factor)
- Correlate macro data with crypto price action
- Reference historical patterns where appropriate
- Combine with latest news for context

---

## Report Template

```markdown
## Macro-Economic Impact Analysis

> Generated: {timestamp} | Related Asset: {coin}

### Economic Calendar

| Date | Event | Previous | Forecast | Actual | Impact |
|------|-------|----------|----------|--------|--------|
| {date} | {event_name} | {previous} | {forecast} | {actual or "Pending"} | {High/Medium/Low} |

### Key Indicator: {indicator_name}

| Metric | Value |
|--------|-------|
| Latest Value | {value} |
| Previous Value | {previous} |
| Change | {change} ({direction}) |

**Interpretation**: {LLM analysis}

### Crypto Market Correlation

| Metric | Value | Context |
|--------|-------|---------|
| {coin} Price | ${price} | — |
| 24h Change | {change_24h}% | — |

**Historical Pattern**: {LLM analysis}

### Related News

1. [{title}]({source}) — {time}

### Impact Assessment

{LLM: 3–5 sentences on surprise factor, risk-on/risk-off, levels to watch, upcoming events}

### Risk Factors

{Data-driven risk alerts}

> Macroeconomic impacts on crypto are complex and non-deterministic. This does not constitute investment advice.
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| Actual > Forecast (inflation metrics like CPI) | Hotter-than-expected — may delay rate cuts, bearish for risk assets |
| Actual < Forecast (inflation metrics) | Cooler-than-expected — supports rate cut narrative, bullish for risk assets |
| Actual > Forecast (employment data) | Stronger labor market — mixed (growth positive but rate cut delay) |
| Actual < Forecast (employment data) | Weakening labor market — supports cuts but signals slowdown |
| Event status = Pending | Upcoming — markets may position ahead of release |
| BTC 24h change > 5% coinciding with macro event | Significant move correlating with macro release |
| No related news found | Limited market commentary — event may not yet be widely covered |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| `info_macro_get_economic_calendar` fails | Skip calendar section; focus on indicator + news |
| `info_macro_get_macro_indicator` fails | Skip indicator detail; use calendar data if available |
| `news_feed_search_news` fails | Skip news section |
| `info_marketsnapshot_get_market_snapshot` fails | Skip market correlation section |
| All Tools fail | Return error; suggest user try again later |
| Indicator not found | Suggest similar indicators; ask user to clarify |
| No upcoming macro events | Inform user; show recent past events if available |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Analyze BTC for me" | `gate-info-coinanalysis` |
| "What's the technical outlook?" | `gate-info-trendanalysis` |
| "How's the overall market?" | `gate-info-marketoverview` |
| "Why did BTC crash?" | `gate-news-eventexplain` |
| "What about DeFi impact?" | `gate-info-defianalysis` |
| "Any crypto news?" | `gate-news-briefing` |

---

## Safety Rules

1. **No price predictions**: Describe potential impacts and historical patterns, not specific price targets.
2. **Correlation ≠ causation**: State that macro–crypto links are probabilistic.
3. **Data transparency**: Label source, time, and reference period for each data point.
4. **No trading advice**: Do not recommend specific trades based on macro data.
5. **Flag uncertainty**: When data is pending, label forecast vs actual clearly.
6. **Historical patterns disclaimer**: Past performance does not guarantee future results.
7. **Age & eligibility**: Intended for users **aged 18 or above** with **full civil capacity** in their jurisdiction.
8. **Data flow**: The host agent processes user prompts; this skill directs **read-only** **Gate-Info** and **Gate-News** MCP tools listed above. The LLM synthesizes from tool results. This skill does not invoke additional third-party data services.
