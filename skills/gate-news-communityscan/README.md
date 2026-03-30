# gate-news-communityscan

## Overview

An AI Agent skill for **community and social sentiment** with **X/Twitter** as the primary surface via Gate-News MCP. Parallel calls: `news_feed_search_x` and `news_feed_get_social_sentiment`; LLM synthesizes narratives, KOL angles, and quantitative sentiment. **Known limitation**: multi-platform UGC (e.g. Reddit/Discord) not online — label outputs **X/Twitter only**. Read-only.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Community pulse** | Qualitative X discussion + sentiment metrics | "What does the community think about ETH" |
| **KOL / narrative scan** | Themes from X search + sentiment score | "Twitter sentiment on Bitcoin" |
| **Routing** | Pure news → `gate-news-briefing`; coin deep-dive → `gate-info-coinanalysis`; why price moved → `gate-news-eventexplain` | Per SKILL.md |

### Routing

| User intent | Action |
|-------------|--------|
| Community / X / KOL / social sentiment | Execute this skill |
| Recent headlines only | Route to `gate-news-briefing` |
| Reddit/Discord-specific (unsupported) | State UGC unavailable; X-only for now |
| Single-coin full analysis | Route to `gate-info-coinanalysis` |

### Architecture

- **Input**: Optional `coin`, `topic`; build `query` for X search per SKILL.md.
- **Tools**: `news_feed_search_x`, `news_feed_get_social_sentiment` only.
- **Output**: Report template (X discussion, sentiment table, takeaways), **Decision Logic**, **Error Handling**, **Cross-Skill**, **Safety** (no fabricated quotes) — see SKILL.md.

## Documentation

- `SKILL.md` — Tools, execution workflow, report templates, Trigger update, routing.
- `references/scenarios.md` — Scenario prompts and expected behavior (for testing and QA).

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
