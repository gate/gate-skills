---
name: gate-info-coincompare-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for multi-coin comparison: coin resolution, market snapshots, technical signals, rankings, and comparative output synthesis."
---

# Gate Info CoinCompare MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Multi-coin side-by-side comparison
- Ranking, market, and technical comparison synthesis

Out of scope:
- Single-coin deep analysis -> `gate-info-coinanalysis`
- Risk-only analysis -> `gate-info-riskcheck`

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate-Info tools availability.
2. Probe with `info_coin_search_coins`.

Fallback:
- If batch snapshot unavailable, fall back to per-coin snapshots.

## 3. Authentication

- API key not required.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

| Tool | Role |
|---|---|
| `info_coin_search_coins` | coin identity disambiguation |
| `info_coin_get_coin_info` | fundamentals per coin |
| `info_coin_get_coin_rankings` | ranking context |
| `info_marketsnapshot_batch_market_snapshot` | batch market snapshot (preferred) |
| `info_marketsnapshot_get_market_snapshot` | per-coin fallback snapshot |
| `info_markettrend_get_technical_analysis` | technical indicators/signals |

## 6. Execution SOP (Non-Skippable)

1. Resolve all target coin symbols first.
2. Collect market data in batch (fallback to per-coin if needed).
3. Collect technical/fundamental context per coin.
4. Build normalized comparison table + concise conclusion.

## 7. Output Templates

```markdown
## Multi-Coin Comparison
| Coin | Price/Change | Ranking | Technical Bias | Notes |
|---|---:|---:|---|---|
| {coin_a} | {market_a} | {rank_a} | {tech_a} | {note_a} |
| {coin_b} | {market_b} | {rank_b} | {tech_b} | {note_b} |

### Summary
- Relative Strength: {summary}
- Relative Risk: {summary}
```

## 8. Safety and Degradation Rules

1. Use consistent time windows across compared coins.
2. If one coin data is missing, mark as unavailable and avoid false ranking.
3. Separate factual metrics from interpretation.
4. Avoid deterministic return predictions.
5. Clearly report when fallback from batch to per-coin snapshot is used.
