---
name: gate-exchange-marketanalysis
version: "2026.3.23-1"
updated: "2026-03-23"
description: "Calculates liquidity depth, estimates slippage impact, detects funding-rate arbitrage opportunities, identifies liquidation squeezes, and assesses manipulation risk on Gate Exchange using read-only MCP market-data tools. Use when the user asks for deep market metrics. Triggers on 'liquidity', 'depth', 'slippage', 'momentum', 'buy/sell pressure', 'squeeze', 'funding rate', 'arbitrage', 'basis', 'premium', 'support', 'resistance', 'breakout', 'allocation', 'portfolio'."
---

# gate-exchange-marketanalysis

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

Market tape analysis covering thirteen scenarios, such as liquidity, momentum, liquidation monitoring, funding arbitrage, basis monitoring, manipulation risk, order book explanation, slippage simulation, K-line breakout/support–resistance, and liquidity with weekend vs weekday. This skill provides structured market insights by orchestrating Gate MCP tools; call order and judgment logic are defined in `references/scenarios.md`.

---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate (main) | ✅ Required |

### Authentication
- API Key Required: Not necessarily
- Note: This skill is read-only and primarily uses public market-data surfaces. In many runtimes these calls work without authentication, though some deployments may still route them through an authenticated MCP layer.

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this skill's market analysis workflow.

- `SKILL.md` keeps intent routing, scenario mapping, and output semantics.
- `references/mcp.md` is the authoritative MCP execution layer for tool sequencing, parameter checks, and degradation rules.

## Scenario Routing

Match user intent to one of 13 cases. Each case's full MCP call order, thresholds, and report template lives in `references/scenarios.md`.

| Case | Module | Keywords | Market | Key Thresholds |
|------|--------|----------|--------|----------------|
| 1 | Liquidity | liquidity, depth, slippage | spot / futures | depth < 10 levels → low liquidity; slippage > 0.5% → high risk |
| 2 | Momentum | buy vs sell, momentum | spot / futures | buy share > 70% → buy-side strong; 24h vol > 30d avg → active |
| 3 | Liquidation | liquidation, squeeze | futures only | 1h liq > 3× daily avg → anomaly; one-sided > 80% → squeeze |
| 4 | Funding arbitrage | arbitrage, funding rate | futures | \|rate\| > 0.05% and 24h vol > $10M → candidate |
| 5 | Basis | basis, premium | futures | basis widening/narrowing for sentiment |
| 6 | Manipulation risk | manipulation, depth vs volume | spot / futures | top-10 depth / 24h vol < 0.5% → thin; repeated large orders → suspect |
| 7 | Order book explainer | order book, spread | spot / futures | spread vs last price; depth and volatility context |
| 8 | Slippage simulation | slippage simulation, market buy $X | spot / futures | **Requires** pair + quote amount — prompt user if missing |
| 9 | K-line breakout | breakout, support, resistance, K-line | spot / futures | candlestick support/resistance + 24h momentum |
| 10 | Liquidity weekend/weekday | weekend vs weekday, liquidity | spot / futures | 90d candles split by day-of-week for volume/return |
| 11 | Technical analysis | technical analysis, what to do, long or short | spot + futures | short + long timeframe K-line; funding rate for bias |
| 12 | Multi-asset allocation | watchlist, want to buy, allocate budget | spot / futures | per-asset 7d candles + order book + funding; output allocation % |
| 13 | Portfolio review | portfolio, allocation reasonable, adjust | spot / futures | same data as Case 12; assess and suggest adjustments |

**Spot vs futures detection:** Keywords "perpetual", "contract", "future", "perp" → futures APIs; "spot" or unspecified → spot.

---

## Execution Workflow

1. **Route intent** — Match user query to a case (1–13) in the Scenario Routing table and determine market type (spot/futures).
2. **Read scenario spec** — Open the corresponding case in `references/scenarios.md` for MCP call order and required fields.
3. **Validate inputs** — For **Case 8**, the user must provide both a currency pair and a quote amount; prompt if either is missing. For all cases, confirm the symbol exists before proceeding.
4. **Execute MCP calls** — Call Gate MCP tools in the exact order defined for the case. Example (Case 1, spot liquidity):
   ```
   Step 1: cex_spot_get_spot_order_book  → { currency_pair: “BTC_USDT” }
   Step 2: cex_spot_get_spot_tickers     → { currency_pair: “BTC_USDT” }
   Step 3: cex_spot_get_spot_candlesticks → { currency_pair: “BTC_USDT”, interval: “1d”, limit: 30 }
   ```
5. **Handle errors** — If an MCP call fails or returns empty data:
   - **Symbol not found:** Ask the user to confirm the trading pair.
   - **Order book < 5 levels:** Note limited data; proceed with available depth and flag low confidence.
   - **Futures endpoint unavailable:** Fall back to spot-only analysis and disclose the limitation.
   - **All endpoints unavailable:** Return framework-level reasoning only and mark as data-unavailable.
6. **Apply judgment** — Use the case’s thresholds and flags (from the routing table and `references/scenarios.md`) to produce the assessment.
7. **Output report** — Use the case’s Report Template from `references/scenarios.md`. Always end with a disclaimer: analysis is data-based, not investment advice.
8. **Suggest next steps** — Offer related analyses (e.g. “For basis analysis, ask ‘What is the basis for BTC?’”).

---

## Important Notes

- All analysis is read-only — no trading operations are performed.
- Gate MCP must be configured (use `gate-mcp-installer` skill if needed).
- Full MCP call sequences, parameter details, and output templates for each case are in `references/scenarios.md`; follow them for consistent behavior.
- Degradation and safety rules are in `references/mcp.md`.
