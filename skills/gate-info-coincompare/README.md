# gate-info-coincompare

## Overview

An AI Agent skill that **compares multiple coins** side-by-side. **Spec (preferred)**: `info_marketsnapshot_batch_market_snapshot` + `info_coin_search_coins`. **Fallback**: per-coin `info_coin_get_coin_info` + `info_marketsnapshot_get_market_snapshot` (same timeframe/source for fair comparison). Read-only.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Multi-coin comparison** | Price, change, market cap/FDV, relative strength | "Compare BTC, ETH, SOL" / "Compare SOL and AVAX" |
| **Spec vs fallback** | Prefer batch + search_coins; fallback: two tools per coin, same timeframe/source | Per SKILL.md Workflow |
| **5-section report** | Key Metrics table, Fundamentals table, Technical (optional), Comparative Summary, Dimension-by-Dimension Winners; Risk Warnings; "Data unavailable" when unavailable | Per SKILL.md Report Template |

### Routing

| User intent | Action |
|-------------|--------|
| Multi-coin comparison | Execute this skill |
| Single-coin | Ask for at least one more coin or route to `gate-info-coinanalysis` |
| Market overview | Route to `gate-info-marketoverview` |
| Price only (one coin) | Call `info_marketsnapshot_get_market_snapshot` directly |

### Architecture

- **Input**: User message with two or more coin symbols.
- **Tools**: **Preferred**: `info_marketsnapshot_batch_market_snapshot`, `info_coin_search_coins`. **Fallback**: for each coin `info_coin_get_coin_info` + `info_marketsnapshot_get_market_snapshot` (same timeframe/source).
- **Output**: 5-section report (Key Metrics, Fundamentals, Technical optional, Comparative Summary, Dimension-by-Dimension Winners) + Risk Warnings. **Decision Logic** (performance divergence, FDV/circulating ratio, volume, RSI, cross-sector), **Error Handling** (one coin → ask or route; coin not found; timeout), **Safety** (no recommendation, no investment advice) — see SKILL.md.
