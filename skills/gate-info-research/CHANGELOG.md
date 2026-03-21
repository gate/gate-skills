# Changelog — gate-info-research

---

## [2026.3.20-1] - 2026-03-20 — Initialization

### Added

- **Skill**: Market Research Copilot (L2 composite). Orchestrates 12 read-only MCP tools across Gate-Info (8) and Gate-News (4) for structured market intelligence. Covers: market overview, single-coin deep dive, multi-coin comparison, technical trend, event attribution, risk check, and screening mode.
- **SKILL.md**: 5-dimension signal detection (S1 Market/Macro, S2 Fundamentals, S3 Technicals, S4 News/Sentiment, S5 Security), parallel/serial execution model, 5 report templates (Market Brief, Single-Coin, Multi-Coin, Event Attribution, Risk Check), judgment logic, error handling, cross-skill routing, safety rules. Parameter notes for `source=spot` constraint on `get_kline` and `get_market_snapshot`.
- **README.md**: Overview, 7 core capabilities, routing table, architecture description, MCP service dependencies, signal-to-tool mapping.
- **references/scenarios.md**: 9 scenario definitions covering low/medium/high complexity use cases with tool call chains.

### Audit

- Read-only; all 12 tools are public read, no authentication required. No trading, swaps, staking, or fund-moving operations.
