---
name: gate-market-tape
version: "2026.3.5-3"
updated: "2026-03-05"
description: "Gate.io market tape intelligence — liquidity, momentum, liquidation, funding arbitrage, basis, manipulation risk, order book explainer. Use when the user asks about liquidity, depth, slippage, buy/sell pressure, liquidation, funding rate arbitrage, basis/premium, manipulation risk, or order book explanation. Trigger phrases: liquidity, depth, slippage, momentum, buy/sell pressure, liquidation, squeeze, funding rate, arbitrage, basis, premium, manipulation, order book, spread, or equivalent in other languages."
---

# Gate Market Tape Intelligence

Market tape analysis across seven scenarios: liquidity, momentum, liquidation monitoring, funding arbitrage, basis monitoring, manipulation risk, and order book explanation. This skill routes user intent to the correct case, then follows the MCP call order and judgment logic defined in `references/scenarios.md`.

## Sub-Modules (Cases)

| Case | Scenario | Document / Reference |
|------|----------|----------------------|
| 1 | Liquidity analysis | `references/scenarios.md` — MCP: list_order_book → list_candlesticks → list_tickers (use futures APIs when user says perpetual/contract) |
| 2 | Momentum (buy vs sell) | list_trades → list_tickers → list_candlesticks → list_order_book → list_futures_funding_rate |
| 3 | Liquidation monitoring | list_futures_liq_orders → list_futures_candlesticks → list_futures_tickers |
| 4 | Funding rate arbitrage | list_futures_tickers → list_futures_funding_rate → list_tickers → list_order_book |
| 5 | Basis (spot vs futures) | list_tickers → list_futures_tickers → list_futures_premium_index |
| 6 | Manipulation risk | list_order_book → list_tickers → list_trades (use list_futures_order_book → list_futures_tickers → list_futures_trades when user says perpetual/contract) |
| 7 | Order book explainer | list_order_book(limit=10) → list_tickers |

## Routing Rules

Determine which case to run from user intent and keywords:

| User intent | Keywords (EN / 中文) | Action |
|-------------|----------------------|--------|
| Liquidity / depth | liquidity, depth, slippage / 流动性, 深度, 滑点 | Case 1 — follow scenarios.md MCP order; if user says perpetual/contract, use futures APIs |
| Momentum | buy vs sell, momentum, sustainable / 多头空头, 动能, 可持续 | Case 2 — trades → tickers → candlesticks → order_book → funding_rate |
| Liquidation | liquidation, squeeze, which coins / 爆仓, 清洗, 插针 | Case 3 — liq_orders → candlesticks → tickers (futures only) |
| Funding arbitrage | arbitrage, funding rate, rate anomaly / 套利, 费率异常 | Case 4 — futures_tickers → funding_rate → spot tickers → order_book |
| Basis | basis, premium, spot-futures spread / 基差, 期现价差 | Case 5 — spot tickers → futures_tickers → premium_index |
| Manipulation risk | manipulation, depth vs volume, "easy to manipulate?" / 深度和成交比怎么样, 容易操控吗 | Case 6 — order_book → tickers → trades (futures APIs when user says perpetual/contract) |
| Order book explainer | explain order book, spread / 解释订单簿, 盘口 | Case 7 — order_book(limit=10) → tickers |

Key to extract: case number (1–7), market type (spot/futures), symbol or pair.

## Domain Knowledge (short)

- **Spot vs futures**: Keywords “perpetual”, “contract”, “future”, “perp” → use futures MCP APIs; “spot” or unspecified → spot.
- **Liquidity (Case 1)**: Depth &lt; 10 levels → low liquidity; 24h volume &lt; 30-day avg → cold pair; slippage = 2×(ask1−bid1)/(bid1+ask1) &gt; 0.5% → high slippage risk.
- **Momentum (Case 2)**: Buy share &gt; 70% → buy-side strong; 24h volume &gt; 30-day avg → active; funding rate sign → long/short bias; order book top 10 for bid/ask balance.
- **Liquidation (Case 3)**: 1h liq &gt; 3× daily avg → anomaly; one-sided liq &gt; 80% → long/short squeeze; price recovered → wick/spike.
- **Arbitrage (Case 4)**: |rate| &gt; 0.05% and 24h vol &gt; $10M → candidate; spot–futures spread &gt; 0.2% → bonus; thin depth → exclude.
- **Basis (Case 5)**: Current basis vs history; basis widening/narrowing for sentiment.
- **Manipulation (Case 6)**: Top-10 depth total / 24h volume &lt; 0.5% → "thin depth"; 24h trades have consecutive same-direction large orders → "possible manipulation / 可能有主力在控盘". Use spot tools by default; use futures order_book → futures_tickers → futures_trades when user says perpetual/contract.
- **Order book (Case 7)**: Show bids/asks example, explain spread with last price, depth and volatility.

## Execution

1. **Match user intent** to the routing table and determine case (1–7) and market (spot/futures).
2. **Read** `references/scenarios.md` for that case’s **MCP call order**, parameters, and required fields.
3. **Call Gate MCP** in the exact order given in scenarios (e.g. list_order_book → list_candlesticks → list_tickers for Case 1).
4. **Apply judgment logic** from scenarios (thresholds, flags, ratings).
5. **Output the report** using the Report Template for that case in scenarios.md (core metrics table, conclusion, recommendation).
6. **Suggest related actions** where useful (e.g. “For basis view, ask ‘What is the basis for ETH?’” or “For liquidation view, ask ‘Recent liquidations?’”).

## Report Templates

Report structure per case is defined in `references/scenarios.md` (Case 1: core metrics + liquidity rating; Case 2: buy/sell share + momentum + sustainability; Case 3: liquidation overview + anomaly table; Case 4: arbitrage table + strategy; Case 5: basis table + trend; Case 6: depth table + large orders + risk; Case 7: order book tutorial + live example + spread). Use those templates so output is consistent with the skill.

## Error Handling

| Error | Cause | Action |
|-------|--------|--------|
| MCP timeout / no response | Gate MCP not configured or network | Prompt user to check MCP config; suggest gate-mcp-installer |
| No data for pair | New or illiquid pair | State insufficient data; skip or partial report |
| Contract not found | Spot-only pair for futures ask | Explain no futures data; offer spot-only analysis |
| API timeout | High load | Retry or reduce limit |

## Important Notes

- All analysis is read-only — no trading operations.
- Gate MCP must be configured (use `gate-mcp-installer` if needed).
- MCP call order and output format are defined in `references/scenarios.md`; follow them for consistent behavior.
- Always include a short disclaimer: analysis is data-based, not investment advice.
