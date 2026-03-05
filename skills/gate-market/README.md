# Gate Market Intelligence

## Overview

An AI Agent skill that provides comprehensive market data analysis on [Gate.io](https://www.gate.io), combining single-coin deep analysis and multi-coin screening/ranking into a unified market intelligence tool.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Coin Deep Analysis** | 6-step data pipeline covering trend, liquidity, sentiment, risk | "帮我分析一下 BTC" |
| **Multi-Coin Screener** | Dynamic filtering by volume, price change, funding rate, etc. | "找出涨幅最大的币" |
| **Comparative Analysis** | Side-by-side comparison of multiple coins | "对比 BTC 和 ETH" |
| **Volume Anomaly Detection** | Spike detection vs 7-day average | "哪些币今天放量了？" |
| **Risk Flag System** | Quantitative risk checks (多头拥挤, 卖压较重, 异常放量) | "BTC 有什么风险？" |

> 📊 **Two modes**: Ask about a specific coin for a deep dive, or describe criteria to screen across the entire market. The skill automatically routes to the right analysis mode.

---

## Architecture

```
Natural Language Input
    ↓
Intent Routing (single-coin vs multi-coin)
    ↓
Gate MCP Tools
    ├── get_currency              → Basic coin info
    ├── get_currency_pair         → Trading pair details
    ├── get_spot_tickers          → Spot market data (all pairs)
    ├── get_spot_candlesticks     → K-line / trend data
    ├── get_spot_order_book       → Depth snapshot
    ├── get_spot_trades           → Recent trade history
    ├── get_futures_tickers       → Futures market data
    └── get_futures_funding_rate  → Sentiment indicator
    ↓
Analysis & Judgment Logic
    ↓
Structured Report → Agent interprets → Natural language response
```

**Sub-Modules:**
- `references/coin-deep-analysis.md` — Single-coin deep dive workflow
- `references/multi-coin-screener.md` — Multi-coin screening workflow

---

## Agent Use Cases

### 1. Comprehensive Coin Research
> "帮我分析一下 BTC"

- Full 6-step data pipeline with structured report
- Covers fundamentals, technicals, liquidity, and sentiment
- For: researchers, long-term investors

### 2. Market Scanning
> "今天涨幅最大的币有哪些？"

- Scan entire spot market for top movers
- Rank by change percentage, volume, or custom metric
- For: day traders, market watchers

### 3. Alpha Discovery
> "找出放量上涨的币"

- Composite conditions to find coins with momentum
- Volume spike detection combined with price movement
- For: swing traders, alpha hunters

### 4. Pre-Trade Due Diligence
> "我想做多 ETH，帮我看看"

- Emphasis on risk flags and key levels
- Include funding cost for futures positions
- For: active traders evaluating entries

### 5. Screen-to-Analyze Pipeline
> "找出涨幅最大的币，然后详细分析第一名"

- Screen first, then deep dive into selected results
- Seamless flow between screening and analysis
- For: systematic traders

---

## Quick Start

### Prerequisites

1. Gate MCP configured and connected (use the `gate-mcp-installer` skill if needed)
2. No additional dependencies required

### Example Prompts

```
# Single-coin analysis
"帮我分析一下 BTC"
"ETH 怎么样？"
"SOL 深度分析"

# Multi-coin screening
"今天涨幅最大的币有哪些？"
"成交量最大的20个币"
"价格低于1美元且涨幅超过5%的币"

# Combined
"找出涨幅最大的10个币，然后帮我分析第一名"
```

See `references/scenarios.md` for more detailed scenario examples.

---

## File Structure

```
gate-market/
├── README.md                          # This file
├── SKILL.md                           # Skill routing and instructions
├── CHANGELOG.md                       # Version history
└── references/
    ├── scenarios.md                   # All scenario examples
    ├── coin-deep-analysis.md          # Single-coin analysis workflow
    └── multi-coin-screener.md         # Multi-coin screening workflow
```

---

## Security

- No external scripts or executable code
- Uses Gate MCP tools only — no direct API calls
- No credential handling or storage
- Read-only market data analysis, no trading operations
- No file system writes
- No data collection, telemetry, or analytics

## License

MIT
