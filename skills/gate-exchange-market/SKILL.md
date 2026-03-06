---
name: Gate-Exchange-Market
version: "2026.3.5-6"
updated: "2026-03-05"
description: "The market analysis function of Gate Exchange — liquidity, momentum, liquidation, funding arbitrage, basis, manipulation risk, order book explainer. Use when the user asks about liquidity, depth, slippage, buy/sell pressure, liquidation, funding rate arbitrage, basis/premium, manipulation risk, or order book explanation. Trigger phrases: liquidity, depth, slippage, momentum, buy/sell pressure, liquidation, squeeze, funding rate, arbitrage, basis, premium, manipulation, order book, spread, or equivalent in other languages."
---

# Gate-Exchange-Market

Market tape analysis covering seven scenarios: liquidity, momentum, liquidation monitoring, funding arbitrage, basis monitoring, manipulation risk, and order book explanation. This skill provides structured market insights by orchestrating Gate MCP tools; call order and judgment logic are defined in `references/scenarios.md`.

## Sub-Modules

| Module | Purpose | Document |
|--------|---------|----------|
| **Liquidity** | Order book depth, 24h vs 30d volume, slippage | `references/scenarios.md` (Case 1) |
| **Momentum** | Buy vs sell share, funding rate, order book balance | `references/scenarios.md` (Case 2) |
| **Liquidation** | 1h liq vs baseline, squeeze, wicks | `references/scenarios.md` (Case 3) |
| **Funding arbitrage** | Rate + volume screen, spot–futures spread | `references/scenarios.md` (Case 4) |
| **Basis** | Spot–futures price, premium index | `references/scenarios.md` (Case 5) |
| **Manipulation risk** | Depth/volume ratio, large orders | `references/scenarios.md` (Case 6) |
| **Order book explainer** | Bids/asks, spread, depth | `references/scenarios.md` (Case 7) |

## Routing Rules

Determine which module (case) to run based on user intent:

| User Intent | Keywords | Action |
|-------------|----------------------|--------|
| Liquidity / depth | 流动性, 深度, 滑点, liquidity, depth, slippage | Read `references/scenarios.md` Case 1, follow MCP order (futures APIs if perpetual/contract) |
| Momentum | 多头空头, 动能, 可持续, buy vs sell, momentum | Read Case 2, follow MCP order |
| Liquidation | 爆仓, 清洗, 插针, liquidation, squeeze | Read Case 3 (futures only) |
| Funding arbitrage | 套利, 费率异常, arbitrage, funding rate | Read Case 4 |
| Basis | 基差, 期现价差, basis, premium | Read Case 5 |
| Manipulation risk | 深度和成交比, 容易操控吗, manipulation | Read Case 6 (spot or futures per keywords) |
| Order book explainer | 解释订单簿, 盘口, order book, spread | Read Case 7 |

## Execution

1. **Match user intent** to the routing table above
2. **Read** the corresponding case in `references/scenarios.md`
3. **Call Gate MCP** in the exact order defined for that case
4. **Apply judgment logic** from scenarios (thresholds, flags, ratings)
5. **Output the report** using that case’s Report Template
6. **Suggest related actions** (e.g. “如需基差可问‘XXX 基差怎么样’”)

## Domain Knowledge (short)

- **Spot vs futures**: Keywords “perpetual”, “contract”, “future”, “perp” → use futures MCP APIs; “spot” or unspecified → spot.
- **Liquidity (Case 1)**: Depth &lt; 10 levels → low liquidity; 24h volume &lt; 30-day avg → cold pair; slippage = 2×(ask1−bid1)/(bid1+ask1) &gt; 0.5% → high slippage risk.
- **Momentum (Case 2)**: Buy share &gt; 70% → buy-side strong; 24h volume &gt; 30-day avg → active; funding rate sign → long/short bias; order book top 10 for bid/ask balance.
- **Liquidation (Case 3)**: 1h liq &gt; 3× daily avg → anomaly; one-sided liq &gt; 80% → long/short squeeze; price recovered → wick/spike.
- **Arbitrage (Case 4)**: |rate| &gt; 0.05% and 24h vol &gt; $10M → candidate; spot–futures spread &gt; 0.2% → bonus; thin depth → exclude.
- **Basis (Case 5)**: Current basis vs history; basis widening/narrowing for sentiment.
- **Manipulation (Case 6)**: Top-10 depth total / 24h volume &lt; 0.5% → "thin depth"; 24h trades have consecutive same-direction large orders → "possible manipulation / 可能有主力在控盘". Use spot tools by default; use futures order_book → futures_tickers → futures_trades when user says perpetual/contract.
- **Order book (Case 7)**: Show bids/asks example, explain spread with last price, depth and volatility.

## Important Notes

- All analysis is read-only — no trading operations are performed
- Gate MCP must be configured (use `gate-mcp-installer` skill if needed)
- MCP call order and output format are defined in `references/scenarios.md`; follow them for consistent behavior
- Reports default to Chinese with English technical terms retained
- Always include a disclaimer: analysis is data-based, not investment advice
