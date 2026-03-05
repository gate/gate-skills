# Gate Trading Intelligence

## Overview

An AI Agent skill that monitors trading opportunities and risks in [Gate.io](https://www.gate.io) derivatives markets, combining basis/premium analysis, funding rate arbitrage scanning, and liquidation anomaly detection into a unified trading intelligence tool.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Basis Monitor** | Spot-futures basis analysis with Z-Score deviation detection | "how is BTC basis?" |
| **Funding Rate Arbitrage** | Full-market scan for funding rate arbitrage opportunities | "are there arbitrage opportunities?" |
| **Liquidation Monitor** | Abnormal liquidation spike and squeeze detection | "how are recent liquidations?" |
| **Arbitrage Signals** | Ranked opportunities with annualized return estimates | "funding-rate arbitrage scan" |
| **Pin-Bar Detection** | Liquidation-driven wick events with price recovery analysis | "did BTC have a wick event?" |

> 📈 **Three dimensions**: Basis analysis reveals market structure, funding rates expose positioning, liquidation data detects squeezes. Together they provide a comprehensive derivatives market picture.

---

## Architecture

```
Natural Language Input
    ↓
Intent Routing (basis / funding rate / liquidation)
    ↓
Gate MCP Tools
    ├── get_spot_tickers           → Spot prices for basis calculation
    ├── get_futures_tickers        → Futures prices, funding rate, open interest
    ├── get_futures_funding_rate   → Detailed funding rate history
    ├── get_futures_premium_index  → Historical premium / basis data
    ├── get_spot_order_book        → Depth for arbitrage execution check
    ├── list_futures_liq_orders    → Liquidation event data
    └── get_futures_candlesticks   → Price context for liquidation analysis
    ↓
Analysis & Signal Generation
    ↓
Structured Report → Agent interprets → Natural language response
```

**Sub-Modules:**
- `references/basis-monitor.md` — Basis/premium analysis workflow
- `references/funding-rate-arbitrage.md` — Funding rate arbitrage scanning workflow
- `references/liquidation-monitor.md` — Liquidation anomaly detection workflow

---

## Agent Use Cases

### 1. Arbitrage Opportunity Scanner
> "funding-rate arbitrage scan"

- Full-market scan with multi-step filtering pipeline
- Ranked by estimated annualized return
- For: quantitative traders, arbitrageurs

### 2. Market Sentiment Gauge
> "is the market mostly positive or negative basis?"

- Full-market basis scan showing contango vs backwardation distribution
- Funding rate direction analysis
- For: macro traders, market analysts

### 3. Risk Monitor
> "how are recent liquidations?"

- Aggregate liquidation data with anomaly detection
- Directional squeeze identification
- For: risk managers, position holders

### 4. Flash Crash Investigator
> "what caused BTC's recent flash crash?"

- Liquidation cascade analysis with pin-bar detection
- Price context and recovery assessment
- For: active traders, risk analysts

### 5. Multi-Dimension Analysis
> "BTC basis, funding rate, and liquidation status"

- Cross-reference all three dimensions for comprehensive view
- Unified sentiment interpretation
- For: professional traders, researchers

---

## Quick Start

### Prerequisites

1. Gate MCP configured and connected (use the `gate-mcp-installer` skill if needed)
2. No additional dependencies required

### Example Prompts

```
# Basis analysis
"how is BTC basis?"
"full-market basis scan"

# Funding rate arbitrage
"are there arbitrage opportunities now?"
"coins with highest funding rates"

# Liquidation monitoring
"how are recent liquidations?"
"which coin had the most liquidations?"

# Multi-dimension
"comprehensive BTC derivatives analysis"
"how is the derivatives market?"
```

See `references/scenarios.md` for more detailed scenario examples.

---

## File Structure

```
gate-trading/
├── README.md                            # This file
├── SKILL.md                             # Skill routing and instructions
├── CHANGELOG.md                         # Version history
└── references/
    ├── scenarios.md                     # All scenario examples
    ├── basis-monitor.md                 # Basis analysis workflow
    ├── funding-rate-arbitrage.md        # Funding rate arbitrage workflow
    └── liquidation-monitor.md           # Liquidation monitoring workflow
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
