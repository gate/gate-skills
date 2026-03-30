# gate-info-macroimpact

## Overview

An AI Agent skill for **macro-economic impact on crypto** via Gate-Info and Gate-News MCP. Recognizes macro events/indicators (CPI, NFP, Fed, rates, etc.), then calls tools **in parallel**: economic calendar, macro indicator or macro summary (when no specific indicator is named), related news, and market snapshot for a correlated coin (default BTC). **Decision logic** for inflation vs employment surprises. Read-only.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Macro + crypto link** | Calendar, indicator/summary, news, price context in one structured report | "How does CPI affect BTC" |
| **Upcoming data** | Calendar-focused mode for releases this week / today | "Any macro data today" |
| **Indicator lookup** | Latest macro series when user names a specific indicator | "What's the latest CPI" |
| **Routing** | Pure coin or technicals without macro → `gate-info-coinanalysis` / `gate-info-trendanalysis`; news-only → `gate-news-briefing`; why price moved → `gate-news-eventexplain` | Per SKILL.md |

### Routing

| User intent | Action |
|-------------|--------|
| Macro impact on crypto / calendar / indicator | Execute this skill |
| Pure coin analysis (no macro angle) | Route to `gate-info-coinanalysis` |
| Technicals only | Route to `gate-info-trendanalysis` |
| Headlines only | Route to `gate-news-briefing` |
| Event / why price moved | Route to `gate-news-eventexplain` |

### Architecture

- **Input**: User message; extract `event_keyword`, optional `coin`, `time_range` per SKILL.md. Do not guess the macro event — ask if unclear.
- **Tools** (parallel): `info_macro_get_economic_calendar`, `info_macro_get_macro_indicator` or `info_macro_get_macro_summary`, `news_feed_search_news`, `info_marketsnapshot_get_market_snapshot`.
- **Output**: Report template (calendar, indicator, correlation, news, impact assessment, risks), **Decision Logic**, **Error Handling**, **Cross-Skill**, **Safety** — see SKILL.md.

## Documentation

- `SKILL.md` — Tools, execution workflow, report templates, Trigger update, routing.
- `references/scenarios.md` — Scenario prompts and expected behavior (for testing and QA).

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
