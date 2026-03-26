# gate-news-eventexplain

## Overview

An AI Agent skill that **explains why a coin pumped or dumped** by tracing triggering events, cross-referencing market data and on-chain anomalies, and delivering an event-impact-chain report. Use when the user asks why a price moved (e.g. "why did BTC crash", "what just happened"). **Phase 1**: parallel `news_events_get_latest_events` + `info_marketsnapshot_get_market_snapshot`. **Branch**: if event found → `news_events_get_event_detail` + `info_onchain_get_token_onchain`; else → `news_feed_search_news` + `info_onchain_get_token_onchain`. Read-only.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Event attribution** | Match volatility to triggering event; event → impact chain → market reaction | "Why did BTC crash" / "Why did ETH pump" |
| **Multi-step workflow** | Event search + market verification → event detail or expanded news + on-chain | Per SKILL.md Execution Workflow |
| **Structured report** | Volatility Summary, Core Triggering Event, Event→Impact Chain, On-chain Verification, Ripple Effects, Forward Outlook; or "No event identified" template | Per SKILL.md Report Template |

### Routing

| User intent | Action |
|-------------|--------|
| Reason for price move | Execute this skill |
| General news | Route to `gate-news-briefing` |
| Full coin analysis | Route to `gate-info-coinanalysis` |
| Technical analysis | Route to `gate-info-trendanalysis` |
| Market overview | Route to `gate-info-marketoverview` |

### Architecture

- **Input**: User message with coin (optional) and time hint (default past 24h).
- **Tools**: Phase 1 — `news_events_get_latest_events`, `info_marketsnapshot_get_market_snapshot`. Phase 2a — `news_events_get_event_detail`, `info_onchain_get_token_onchain`. Phase 2b — `news_feed_search_news`, `info_onchain_get_token_onchain`. See SKILL.md for params.
- **Output**: Attribution report or "No clear event" composite analysis. **Reasoning Logic** (event matching, volatility magnitude, on-chain anomaly), **Error Handling**, **Safety** (no causal certainty, no predictions) — see SKILL.md.

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
