---
name: gate-market
version: "2026.3.5-1"
updated: "2026-03-05"
description: Analyze cryptocurrency market data on Gate.io, including single-coin deep analysis and multi-coin screening/ranking. Use this skill whenever the user asks about a coin's price, trend, liquidity, market analysis, or wants to filter/rank coins by conditions. Trigger phrases include "分析 XXX", "XXX 怎么样", "XXX 深度分析", "帮我找出", "哪些币涨了", "筛选币种", "成交量排名", "XXX 值得买吗", "看看 XXX", "找出涨幅最大的", "成交量最高的币", "analyze", "screen", "filter coins", "top coins", or any request involving market data inquiry, coin evaluation, coin screening, or multi-coin comparison.
---

# Gate Market Intelligence

Market data analysis covering two modes: single-coin deep dive and multi-coin screening. This skill provides comprehensive market insights by orchestrating Gate MCP tools to retrieve, analyze, and present cryptocurrency market data.

## Sub-Modules

| Module | Purpose | Document |
|--------|---------|----------|
| **Coin Deep Analysis** | Comprehensive single-coin analysis covering trend, liquidity, sentiment, and risk | `references/coin-deep-analysis.md` |
| **Multi-Coin Screener** | Screen and filter coins across the entire market by user-defined criteria | `references/multi-coin-screener.md` |

## Routing Rules

Determine which sub-module to load based on the user's intent:

| User Intent | Keywords | Action |
|-------------|----------|--------|
| Analyze a specific coin | 分析XX, XX怎么样, XX深度, XX值得买吗, 看看XX, analyze XX | Read `references/coin-deep-analysis.md`, follow its workflow |
| Screen / filter / rank coins | 找出, 筛选, 排名, 涨幅最大, 成交量最高, 哪些币, filter, rank, top, screen | Read `references/multi-coin-screener.md`, follow its workflow |
| Screen then analyze | 先找出XX再分析, 这些币里哪个好 | Execute screener first, then deep analysis on selected coins |
| Compare specific coins | 对比XX和YY, compare XX vs YY | Read `references/coin-deep-analysis.md`, run for each coin, present side-by-side |

## Execution

1. **Match user intent** to the routing table above
2. **Read the corresponding document** from `references/` directory
3. **Follow the Workflow** defined in that document exactly
4. **Output the report** using that document's Report Template
5. **Suggest related actions** after completing:
   - After screening → "如需深入分析某个币，可以说'帮我分析一下 XXX'"
   - After deep analysis → "如需扫描更多类似币种，可以说'帮我找出...'"

## Cross-Module Synergy

- After multi-coin screening, suggest using coin deep analysis for top results
- After coin deep analysis, suggest screening for similar coins if relevant
- When user intent spans both (e.g., "找出涨幅最大的币然后详细分析第一名"), execute sequentially

## Important Notes

- All analysis is read-only — no trading operations are performed
- Gate MCP must be configured (use `gate-mcp-installer` skill if needed)
- Reports default to Chinese with English technical terms retained
- Always include a disclaimer: analysis is data-based, not investment advice
