# gate-exchange-marketanalysis

## Overview

An AI Agent skill that provides market tape analysis on [Gate](https://www.gate.com), covering liquidity, momentum, liquidation monitoring, funding rate arbitrage, basis (spot–futures) monitoring, manipulation risk, and order book explanation. All scenarios use a defined **MCP call order and output format** in `references/scenarios.md`.

---

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Liquidity analysis** | Order book depth, 24h vs 30d volume, slippage | "How is ETH liquidity?" |
| **Momentum** | Buy vs sell share, funding rate | "Is BTC more long or short in 24h?" |
| **Liquidation monitoring** | 1h liq vs baseline, squeeze, wicks | "Recent liquidations?" |
| **Funding arbitrage** | Rate + volume, spot–futures spread | "Any arbitrage opportunities?" |
| **Basis monitoring** | Spot–futures price, premium index | "What is the basis for BTC?" |
| **Manipulation risk** | Depth/volume ratio, large orders | "Is this coin easy to manipulate?" |
| **Order book explainer** | Bids/asks, spread, depth | "Explain the order book" |

> 📊 **Seven scenarios:** Ask about liquidity, momentum, liquidation, arbitrage, basis, manipulation risk, or order book; the skill routes to the right case and follows `references/scenarios.md`.

---

## Architecture

```
Natural Language Input
    ↓
Intent Routing (Case 1–7, spot vs futures)
    ↓
Gate MCP Tools
    ├── get_spot_order_book / get_futures_order_book
    ├── get_spot_tickers / get_futures_tickers
    ├── get_spot_candlesticks / get_futures_candlesticks
    ├── get_spot_trades / list_futures_funding_rate
    ├── list_futures_liq_orders (when available)
    └── list_futures_premium_index
    ↓
Analysis & Judgment Logic
    ↓
Structured Report → Natural language response
```

**Sub-Modules:** `references/scenarios.md` — MCP call order, parameters, required fields, and report templates per case.

---

## Agent Use Cases

### 1. Liquidity check
> "How is ETH liquidity?"

Depth levels, 24h vs 30d volume, slippage; liquidity rating. For perpetual/contract, use futures order book and candlesticks/tickers.

### 2. Momentum (buy vs sell)
> "Is BTC more long or short in 24h, and is it sustainable?"

Trades → buy/sell share; tickers, candlesticks, order book top 10, funding rate for bias and sustainability.

### 3. Liquidation monitoring
> "Recent liquidations?"

Liquidation orders (if MCP provides), candlesticks, tickers; anomaly and squeeze labels.

### 4. Funding arbitrage scan
> "Any arbitrage opportunities?"

Screen by |rate| and volume; spot tickers and order book; exclude thin books.

### 5. Basis (spot–futures)
> "What is the basis for BTC?"

Spot and futures tickers, premium index; current vs history, widening/narrowing.

### 6. Manipulation risk
> "Is this coin easy to manipulate?"

Depth ratio (top 10 / 24h volume); large and consecutive same-side trades.

### 7. Order book explainer
> "Explain the order book"

Live order book (e.g. limit=10) + ticker; explain bids/asks, spread, depth.

---

## Quick Start

### Prerequisites

1. Gate MCP configured and connected (use the `gate-mcp-installer` skill if needed).
2. No extra dependencies.

### Example Prompts

```
# Liquidity
"How is ETH liquidity?"
"BTC perpetual depth"

# Momentum
"BTC 24h more long or short, sustainable?"

# Liquidation
"Recent liquidations?"

# Arbitrage
"Any funding rate arbitrage opportunities?"

# Basis
"What is the basis for ETH?"

# Manipulation
"Is PEPE easy to manipulate?"

# Order book
"Explain the order book with an example"
```

See `references/scenarios.md` for full MCP call order and report templates.

---

## File Structure

```
gate-exchange-marketanalysis/
├── README.md                          # This file
├── SKILL.md                           # Skill routing and instructions
├── CHANGELOG.md                       # Version history
└── references/
    ├── scenarios.md                   # MCP call order, judgment logic, report templates per case
    └── case-test-report.md            # Optional: simulation test summary
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
