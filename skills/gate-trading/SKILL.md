---
name: gate-trading
version: "2026.3.5-1"
updated: "2026-03-05"
description: Monitor trading opportunities and risks in Gate.io derivatives markets, including basis/premium analysis, funding rate arbitrage scanning, and liquidation anomaly detection. Use this skill whenever the user asks about arbitrage, funding rate, basis, premium, spot-futures spread, liquidation, forced closure, or trading signals. Trigger phrases include "arbitrage opportunities", "abnormal funding rate", "funding rate arbitrage", "basis", "spot-futures spread", "basis monitoring", "futures premium", "futures discount", "liquidation", "liquidation", "forced liquidation", "liquidation monitoring", "which coins had the most liquidations", "arbitrage", "funding rate", "basis", "premium", "liquidation", "squeeze", or any request involving derivatives trading analysis, risk monitoring, or opportunity scanning.
---

# Gate Trading Intelligence

Derivatives market monitoring and trading opportunity detection covering three analysis dimensions: basis/premium analysis, funding rate arbitrage scanning, and liquidation anomaly detection. This skill provides comprehensive derivatives market insights to support trading decisions.

## Sub-Modules

| Module | Purpose | Document |
|--------|---------|----------|
| **Basis Monitor** | Spot-futures basis analysis, premium tracking, arbitrage signals | `references/basis-monitor.md` |
| **Funding Rate Arbitrage** | Full-market funding rate scan, arbitrage opportunity ranking | `references/funding-rate-arbitrage.md` |
| **Liquidation Monitor** | Liquidation spike detection, directional squeeze, pin-bar events | `references/liquidation-monitor.md` |

## Routing Rules

Determine which sub-module to load based on the user's intent:

| User Intent | Keywords | Action |
|-------------|----------|--------|
| Basis / premium / spot-futures spread | basis, spot-futures spread, premium, discount, premium, basis, spread | Read `references/basis-monitor.md`, follow its workflow |
| Funding rate / arbitrage scanning | funding rate, arbitrage, abnormal funding rate, funding arbitrage | Read `references/funding-rate-arbitrage.md`, follow its workflow |
| Liquidation / forced closure / squeeze | liquidation, liquidation, forced liquidation, liquidation, squeeze, wick event | Read `references/liquidation-monitor.md`, follow its workflow |
| General derivatives overview | how is the derivatives market, derivatives, derivatives, trading opportunities | Load all three, produce combined summary |
| Multi-dimension query | basis and liquidation, funding rate and basis | Load and execute requested modules sequentially |

## Execution

1. **Match user intent** to the routing table above
2. **Read the corresponding document** from `references/` directory
3. **Follow the Workflow** defined in that document exactly
4. **Output the report** using that document's Report Template
5. **Suggest related checks** after completing (see Cross-Module Synergy below)

## Cross-Module Synergy

When analyzing one dimension, suggest related checks from other modules:

- **After basis analysis**: If basis rate > 0.3%, suggest checking funding rate for confirmation → "You can also check funding conditions by saying 'run a funding-rate arbitrage scan'"
- **After funding rate scan**: Mention basis spread context for top candidates → "For basis details of a coin, say 'how is XX basis?'"
- **After liquidation analysis**: Suggest checking basis + funding rate for sentiment context → "To understand market sentiment, check basis and funding rate."
- **Cross-skill reference**: For deeper coin analysis, suggest using `gate-market` skill → "For deep single-coin analysis, say 'analyze XXX in detail'."

## Important Notes

- All analysis is read-only — no trading operations are performed
- Gate MCP must be configured (use `gate-mcp-installer` skill if needed)
- Reports default to English
- Always include a disclaimer: analysis is data-based, not investment advice
- Derivatives data may not be available for all coins — handle gracefully
