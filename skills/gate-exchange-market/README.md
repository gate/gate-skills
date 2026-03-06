# Gate-Exchange-Market

## Overview

An AI Agent skill that provides market tape analysis on [Gate.io](https://www.gate.io), covering liquidity, momentum, liquidation monitoring, funding rate arbitrage, basis (spot–futures) monitoring, manipulation risk, and order book explanation. All scenarios use a defined **MCP call order and output format** in `references/scenarios.md` so that implementations stay consistent.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Liquidity analysis** | Order book depth, 24h volume vs 30d avg, slippage | "How is ETH liquidity?" / "ETH 流动性如何" |
| **Momentum** | Buy vs sell share, funding rate, order book balance | "Is BTC more long or short in 24h?" |
| **Liquidation monitoring** | 1h liquidation vs baseline, squeeze direction, wicks | "Recent liquidations?" / "最近爆仓情况" |
| **Funding arbitrage** | High \|rate\| + volume, spot–futures spread, depth filter | "Any arbitrage opportunities?" |
| **Basis monitoring** | Spot vs futures price, premium index, trend | "What is the basis for BTC?" |
| **Manipulation risk** | Depth / 24h volume ratio, large same-side trades | "Is this coin easy to manipulate?" |
| **Order book explainer** | Bids/asks example, spread, depth vs volatility | "Explain the order book" |

> 📊 **Seven scenarios**: Ask about liquidity, momentum, liquidation, arbitrage, basis, manipulation risk, or order book; the skill routes to the right case and follows `references/scenarios.md`.

---

## Architecture

```
Natural Language Input
    ↓
Intent Routing (Case 1–7, spot vs futures)
    ↓
Gate MCP Tools
    ├── list_order_book / list_futures_order_book
    ├── list_tickers / list_futures_tickers
    ├── list_candlesticks / list_futures_candlesticks
    ├── list_trades / list_futures_funding_rate
    ├── list_futures_liq_orders (when available)
    └── list_futures_premium_index
    ↓
Analysis & Judgment Logic
    ↓
Structured Report → Agent interprets → Natural language response
```

**Sub-Modules:** `references/scenarios.md` — MCP call order, parameters, required fields, and report templates per case.

---

## Agent Use Cases

### 1. Liquidity check
> "How is ETH liquidity?" / "当前 ETH 的流动性如何"

- Depth levels, 24h volume vs 30d avg, slippage; liquidity rating (e.g. 1–5⭐).
- For perpetual/contract, use futures order book and candlesticks/tickers.

### 2. Momentum (buy vs sell)
> "Is BTC more long or short in 24h, and is it sustainable?"

- Trades → buy/sell share; tickers and candlesticks for volume; order book top 10 and funding rate for bias and sustainability.

### 3. Liquidation monitoring
> "Recent liquidations?" / "哪些币爆得多"

- Liquidation orders (if MCP provides), candlesticks and tickers for context; anomaly and squeeze labels.

### 4. Funding arbitrage scan
> "Any arbitrage opportunities?" / "费率异常的币"

- Screen by \|rate\| and volume; spot tickers and order book for spread and depth; exclude thin books.

### 5. Basis (spot–futures)
> "What is the basis for BTC?" / "基差怎么样"

- Spot and futures tickers, premium index; current vs history and widening/narrowing.

### 6. Manipulation risk
> "Is this coin easy to manipulate?" / "深度和成交比怎么样"

- Depth ratio (top 10 / 24h volume); large and consecutive same-side trades.

### 7. Order book explainer
> "Explain the order book" / "解释订单簿示例"

- Live order book (e.g. limit=10) + ticker; explain bids/asks, spread, depth and volatility.

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
Gate-Exchange-Market/
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
