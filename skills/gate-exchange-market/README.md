# Gate Market Intelligence

## Overview

An AI Agent skill that provides comprehensive market data analysis on [Gate.io](https://www.gate.io), combining single-coin deep analysis and multi-coin screening/ranking into a unified market intelligence tool.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Coin Deep Analysis** | 6-step data pipeline covering trend, liquidity, sentiment, risk | "analyze BTC in detail" |
| **Multi-Coin Screener** | Dynamic filtering by volume, price change, funding rate, etc. | "find the top-gaining coin" |
| **Comparative Analysis** | Side-by-side comparison of multiple coins | "compare BTC and ETH" |
| **Volume Anomaly Detection** | Spike detection vs 7-day average | "which coins have volume spikes today?" |
| **Risk Flag System** | Quantitative risk checks (Long Crowding, Heavy Selling Pressure, Abnormal Volume Spike) | "what are the risks for BTC?" |

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
> "analyze BTC in detail"

- Full 6-step data pipeline with structured report
- Covers fundamentals, technicals, liquidity, and sentiment
- For: researchers, long-term investors

### 2. Market Scanning
> "which coins are top gainers today?"

- Scan entire spot market for top movers
- Rank by change percentage, volume, or custom metric
- For: day traders, market watchers

### 3. Alpha Discovery
> "find coins rising with volume expansion"

- Composite conditions to find coins with momentum
- Volume spike detection combined with price movement
- For: swing traders, alpha hunters

### 4. Pre-Trade Due Diligence
> "I want to long ETH, please check it for me"

- Emphasis on risk flags and key levels
- Include funding cost for futures positions
- For: active traders evaluating entries

### 5. Screen-to-Analyze Pipeline
> "find the top-gaining coin, then analyze #1 in detail"

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
"analyze BTC in detail"
"how is ETH?"
"deep analysis of SOL"

# Multi-coin screening
"which coins are top gainers today?"
"top 20 coins by volume"
"coins under $1 with gain above 5%"

# Combined
"find top 10 gainers, then analyze the first one"
```

See `references/scenarios.md` for more detailed scenario examples.

---

## File Structure

```
gate-exchange-market/
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
