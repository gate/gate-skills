# gate-news-listing

## Overview

An AI Agent skill that **tracks exchange listing, delisting, and maintenance announcements** and supplements key new coins with fundamentals and market data. **Step 1**: `news_feed_get_exchange_announcements` (exchange, coin, announcement_type, limit). **Step 2**: For top 3-5 newly listed coins, parallel `info_coin_get_coin_info` + `info_marketsnapshot_get_market_snapshot`. LLM aggregates into Exchange Activity Report. Use when the user asks about new listings, what an exchange listed, or delisting/maintenance. Read-only.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Listing tracker** | Latest listing announcements, featured new coins with fundamentals + market data | "Any new coins listed recently" / "What did Binance list" |
| **Delisting / maintenance** | Filter by announcement type; remind users to manage positions | "Any coins getting delisted" |
| **4-section report** | Latest Listing Announcements, Featured New Coins, Delisting/Maintenance Notices, Activity Summary + Risk Warnings | Per SKILL.md Report Template |

### Routing

| User intent | Action |
|-------------|--------|
| Exchange listings / delisting / maintenance | Execute this skill |
| General news | Route to `gate-news-briefing` |
| New coin analysis | Route to `gate-info-coinanalysis` |
| New coin contract safe | Route to `gate-info-riskcheck` |

### Architecture

- **Input**: Optional exchange, coin, announcement_type (default listing); limit default 10.
- **Tools**: `news_feed_get_exchange_announcements` first; then for listing-type results supplement with `info_coin_get_coin_info` and `info_marketsnapshot_get_market_snapshot` (parallel per coin).
- **Output**: Exchange Activity Report. **Decision Logic** (post-listing volatility, volume, multi-exchange listing, delisting urgency), **Error Handling**, **Safety** (no listing prediction, new-coin risk reminder) — see SKILL.md.
