---
name: gate-exchange-marketanalysis
version: "2026.3.5-1"
updated: "2026-03-05"
description: "The market analysis function of Gate Exchange — liquidity, momentum, liquidation, funding arbitrage, basis, manipulation risk, order book explainer. Use when the user asks about liquidity, depth, slippage, buy/sell pressure, liquidation, funding rate arbitrage, basis/premium, manipulation risk, or order book explanation. Trigger phrases: liquidity, depth, slippage, momentum, buy/sell pressure, liquidation, squeeze, funding rate, arbitrage, basis, premium, manipulation, order book, spread, or equivalent in other languages."
---

# gate-exchange-marketanalysis

Market tape analysis covering seven scenarios: liquidity, momentum, liquidation monitoring, funding arbitrage, basis monitoring, manipulation risk, and order book explanation. This skill provides structured market insights by orchestrating Gate MCP tools; call order and judgment logic are defined in `references/scenarios.md`.

---

## Sub-Modules

| Module | Purpose | Document |
|--------|---------|----------|
| **Liquidity** | Order book depth, 24h vs 30d volume, slippage | `references/scenarios.md` (Case 1) |
| **Momentum** | Buy vs sell share, funding rate | `references/scenarios.md` (Case 2) |
| **Liquidation** | 1h liq vs baseline, squeeze, wicks | `references/scenarios.md` (Case 3) |
| **Funding arbitrage** | Rate + volume screen, spot–futures spread | `references/scenarios.md` (Case 4) |
| **Basis** | Spot–futures price, premium index | `references/scenarios.md` (Case 5) |
| **Manipulation risk** | Depth/volume ratio, large orders | `references/scenarios.md` (Case 6) |
| **Order book explainer** | Bids/asks, spread, depth | `references/scenarios.md` (Case 7) |

---

## Routing Rules

Determine which module (case) to run based on user intent:

| User Intent | Keywords | Action |
|-------------|----------|--------|
| Liquidity / depth | liquidity, depth, slippage | Read Case 1, follow MCP order (use futures APIs if perpetual/contract) |
| Momentum | buy vs sell, momentum | Read Case 2, follow MCP order |
| Liquidation | liquidation, squeeze | Read Case 3 (futures only) |
| Funding arbitrage | arbitrage, funding rate | Read Case 4 |
| Basis | basis, premium | Read Case 5 |
| Manipulation risk | manipulation, depth vs volume | Read Case 6 (spot or futures per keywords) |
| Order book explainer | order book, spread | Read Case 7 |

---

## Execution

1. **Match user intent** to the routing table above and determine case (1–7) and market type (spot/futures).
2. **Read** the corresponding case in `references/scenarios.md` for MCP call order and required fields.
3. **Call Gate MCP** in the exact order defined for that case.
4. **Apply judgment logic** from scenarios (thresholds, flags, ratings).
5. **Output the report** using that case’s Report Template.
6. **Suggest related actions** (e.g. “For basis, ask ‘What is the basis for XXX?’”).

---

## Domain Knowledge (short)

- **Spot vs futures:** Keywords “perpetual”, “contract”, “future”, “perp” → use futures MCP APIs; “spot” or unspecified → spot.
- **Liquidity (Case 1):** Depth &lt; 10 levels → low liquidity; 24h volume &lt; 30-day avg → cold pair; slippage = 2×(ask1−bid1)/(bid1+ask1) &gt; 0.5% → high slippage risk.
- **Momentum (Case 2):** Buy share &gt; 70% → buy-side strong; 24h volume &gt; 30-day avg → active; funding rate sign + order book top 10 for bias.
- **Liquidation (Case 3):** 1h liq &gt; 3× daily avg → anomaly; one-sided liq &gt; 80% → long/short squeeze; price recovered → wick/spike.
- **Arbitrage (Case 4):** |rate| &gt; 0.05% and 24h vol &gt; $10M → candidate; spot–futures spread &gt; 0.2% → bonus; thin depth → exclude.
- **Basis (Case 5):** Current basis vs history; basis widening/narrowing for sentiment.
- **Manipulation (Case 6):** Top-10 depth total / 24h volume &lt; 0.5% → thin depth; consecutive same-direction large orders → possible manipulation. Use spot by default; use futures when user says perpetual/contract.
- **Order book (Case 7):** Show bids/asks example, explain spread with last price, depth and volatility.

---

## Important Notes

- All analysis is read-only — no trading operations are performed.
- Gate MCP must be configured (use `gate-mcp-installer` skill if needed).
- MCP call order and output format are in `references/scenarios.md`; follow them for consistent behavior.
- Always include a disclaimer: analysis is data-based, not investment advice.
