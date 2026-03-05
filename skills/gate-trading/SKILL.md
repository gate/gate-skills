---
name: gate-trading
version: "2026.3.5-1"
updated: "2026-03-05"
description: Monitor trading opportunities and risks in Gate.io derivatives markets, including basis/premium analysis, funding rate arbitrage scanning, and liquidation anomaly detection. Use this skill whenever the user asks about arbitrage, funding rate, basis, premium, spot-futures spread, liquidation, forced closure, or trading signals. Trigger phrases include "套利机会", "费率异常", "资金费率套利", "基差", "期现价差", "基差监控", "合约溢价", "合约折价", "爆仓", "清算", "强平", "爆仓监控", "哪些币爆得多", "arbitrage", "funding rate", "basis", "premium", "liquidation", "squeeze", or any request involving derivatives trading analysis, risk monitoring, or opportunity scanning.
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
| Basis / premium / spot-futures spread | 基差, 期现价差, 溢价, 折价, premium, basis, spread | Read `references/basis-monitor.md`, follow its workflow |
| Funding rate / arbitrage scanning | 费率, 套利, funding rate, arbitrage, 费率异常, 费率套利 | Read `references/funding-rate-arbitrage.md`, follow its workflow |
| Liquidation / forced closure / squeeze | 爆仓, 清算, 强平, liquidation, squeeze, 插针 | Read `references/liquidation-monitor.md`, follow its workflow |
| General derivatives overview | 合约市场怎么样, 衍生品, derivatives, 交易机会 | Load all three, produce combined summary |
| Multi-dimension query | 基差和爆仓, 费率和基差 | Load and execute requested modules sequentially |

## Execution

1. **Match user intent** to the routing table above
2. **Read the corresponding document** from `references/` directory
3. **Follow the Workflow** defined in that document exactly
4. **Output the report** using that document's Report Template
5. **Suggest related checks** after completing (see Cross-Module Synergy below)

## Cross-Module Synergy

When analyzing one dimension, suggest related checks from other modules:

- **After basis analysis**: If basis rate > 0.3%, suggest checking funding rate for confirmation → "也可以看看费率情况，说'资金费率套利扫描'"
- **After funding rate scan**: Mention basis spread context for top candidates → "要看某个币的基差详情，可以说'XX 基差怎么样'"
- **After liquidation analysis**: Suggest checking basis + funding rate for sentiment context → "想了解市场情绪，可以看看基差和费率"
- **Cross-skill reference**: For deeper coin analysis, suggest using `gate-market` skill → "如需单币深度分析，可以说'帮我分析一下 XXX'"

## Important Notes

- All analysis is read-only — no trading operations are performed
- Gate MCP must be configured (use `gate-mcp-installer` skill if needed)
- Reports default to Chinese with English technical terms retained
- Always include a disclaimer: analysis is data-based, not investment advice
- Derivatives data may not be available for all coins — handle gracefully
