---
name: gate-market
version: "2026.3.5-1"
updated: "2026-03-05"
description: Analyze cryptocurrency market data on Gate.io, including single-coin deep analysis and multi-coin screening/ranking. Use this skill whenever the user asks about a coin's price, trend, liquidity, market analysis, or wants to filter/rank coins by conditions. Trigger phrases include "analyze XXX", "how is XXX", "deep analysis of XXX", "help me find", "which coins are up", "screen coins", "volume ranking", "is XXX worth buying", "check XXX", "find the top gainers", "coins with highest volume", "analyze", "screen", "filter coins", "top coins", or any request involving market data inquiry, coin evaluation, coin screening, or multi-coin comparison.
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
| Analyze a specific coin | analyze XX, how is XX, deep dive XX, is XX worth buying, check XX, analyze XX | Read `references/coin-deep-analysis.md`, follow its workflow |
| Screen / filter / rank coins | find, screen, rank, top gainers, highest volume, which coins, filter, rank, top, screen | Read `references/multi-coin-screener.md`, follow its workflow |
| Screen then analyze | find XX first then analyze, which is better among these coins | Execute screener first, then deep analysis on selected coins |
| Compare specific coins | compare XX and YY, compare XX vs YY | Read `references/coin-deep-analysis.md`, run for each coin, present side-by-side |

## Execution

1. **Match user intent** to the routing table above
2. **Read the corresponding document** from `references/` directory
3. **Follow the Workflow** defined in that document exactly
4. **Output the report** using that document's Report Template
5. **Suggest related actions** after completing:
   - After screening → "For a deeper dive into one coin, say 'analyze XXX in detail'"
   - After deep analysis → "To scan more similar coins, say 'help me find ...'"

## Cross-Module Synergy

- After multi-coin screening, suggest using coin deep analysis for top results
- After coin deep analysis, suggest screening for similar coins if relevant
- When user intent spans both (e.g., "find the top-gaining coin then analyze #1 in detail"), execute sequentially

## Important Notes

- All analysis is read-only — no trading operations are performed
- Gate MCP must be configured (use `gate-mcp-installer` skill if needed)
- Reports default to English
- Always include a disclaimer: analysis is data-based, not investment advice
