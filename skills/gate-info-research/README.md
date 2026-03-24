# gate-info-research

## Overview

An L2 composite AI Agent skill — **Market Research Copilot** — that orchestrates **12 read-only MCP tools** across Gate-Info MCP (8 tools) and Gate-News MCP (4 tools) to produce structured, citation-backed market intelligence reports. Covers market overviews, single-coin deep dives, multi-coin comparisons, technical trend analyses, event attribution, and token risk checks. **No trading, swaps, staking, or any fund-moving operations.**

### Core Capabilities

| Capability | Description | Example Prompts |
|------------|-------------|-----------------|
| **Market Overview Brief** | Aggregates BTC/ETH snapshots, DeFi metrics, top events, and sentiment into a daily market brief | "Give me a market briefing today" |
| **Single-Coin Deep Dive** | Fundamentals + market data + technicals + news + sentiment for one coin | "Analyze SOL" / "Research XRP" |
| **Multi-Coin Comparison** | Side-by-side comparison of 2+ coins across price, market cap, technicals, and risk | "Compare BTC, ETH, and SOL" |
| **Technical Trend Analysis** | K-line, RSI/MACD/Bollinger history, multi-timeframe signals, support/resistance | "Show me DOT support and resistance levels" |
| **Event Attribution** | Identifies root causes for market movements with event detail and on-chain evidence | "Why did the market crash yesterday?" |
| **Token Risk Check** | Contract security audit (honeypot, tax, holder concentration) + fundamentals cross-check | "Is ADA safe? Check the risk" |
| **Screening Mode** | Fetches top-coin snapshots, ranks by criteria, then deep-dives into selected coins | "Which coins are oversold right now?" |

### Routing (when NOT to use)

| Intent | Route Instead |
|--------|---------------|
| Buy / sell / place order | `gate-exchange-spot` or `gate-exchange-futures` |
| Swap / convert | `gate-exchange-flashswap` |
| Stake / earn | `gate-exchange-staking` or `gate-exchange-simpleearn` |
| Check account assets | `gate-exchange-assets` |
| DEX / on-chain address tracking | `gate-dex-market` or `gate-info-addresstracker` |
| NFT or options | Specialized skill for that category |

## Architecture

- **Type**: L2 composite skill (orchestrates 7 L1 skills' underlying tools)
- **Input**: Natural language query expressing research intent
- **Signal Detection**: 5-dimension signal model (Market/Macro, Fundamentals, Technicals, News/Sentiment, Security) — non-exclusive, multiple dimensions can activate simultaneously
- **Tools**: 12 unique MCP tools (Gate-Info: 8, Gate-News: 4) — all read-only, no authentication required
- **Execution**: Parallel within each Phase; serial between Phases when data dependencies exist (screening mode, attribution branching)
- **Output**: Structured report selected from 5 templates (Market Brief, Single-Coin, Multi-Coin, Event Attribution, Risk Check)

### MCP Service Dependencies

| MCP Service | Tool Prefix | Auth Required | Tools Used |
|-------------|-------------|---------------|------------|
| Gate-Info MCP | `info_*` | No (public read) | 8 |
| Gate-News MCP | `news_*` | No (public read) | 4 |

### Signal-to-Tool Mapping

| Signal | Dimension | Core Tools |
|--------|-----------|------------|
| S1 | Market / Macro | `info_marketsnapshot_get_market_snapshot`, `info_platformmetrics_get_defi_overview`, `news_events_get_latest_events` |
| S2 | Fundamentals | `info_coin_get_coin_info`, `info_marketsnapshot_get_market_snapshot` |
| S3 | Technicals | `info_markettrend_get_kline`, `info_markettrend_get_indicator_history`, `info_markettrend_get_technical_analysis` |
| S4 | News / Sentiment | `news_events_get_latest_events`, `news_feed_search_news`, `news_feed_get_social_sentiment`, `news_events_get_event_detail` (conditional) |
| S5 | Security / Risk | `info_compliance_check_token_security`, `info_coin_get_coin_info` |

## Support

- **Email**: support@gate.com (general support), business@gate.com (business inquiries)
- **Help Center**: [https://www.gate.com/help](https://www.gate.com/help)
- **GitHub Issues**: Report bugs or feature requests via the repository's Issues page.

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
