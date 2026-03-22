# Changelog

All notable changes to the **gate-info-research** (Market Research Copilot) skill are documented here.

---

## [2026.3.22-2] - 2026-03-22

### Changed

- **SKILL.md**: Step 2 signal table and **Signal Routing Examples** are **English-only** (no embedded non-English trigger lists); routing remains **intent-based** for user queries in any language.
- **references/scenarios.md**: All **Prompt Examples** and maintainer notes translated to English; Scenario 7 expected-behavior steps use English only.

---

## [2026.3.22-1] - 2026-03-22

### Added

- **SKILL.md**: Bilingual **Trigger Keywords** (English and Simplified Chinese) for S1–S5; expanded **Screening mode** cues in both languages (e.g. screen, rank, screening, leaderboard, highest-potential picks); **Signal Routing Examples** table extended with paired English and Chinese examples (daily brief, top-gainer screen, DeFi leader, long-hold compare, sentiment rebound, etc.).
- **references/scenarios.md**: One **Simplified-Chinese prompt example** per scenario; Scenario 7 adds **HTML #2** line (top 5 gainers + potential deep-dive); Context / Expected Behavior updated for screening (rank by 24h gain vs oversold/RSI paths).
- **README.md**: **Support** section (support@gate.com, business@gate.com, Help Center, GitHub Issues).
- **Safety Rules** (#9–#10): Age restriction (18+); data-flow declaration (Gate MCP → Gate API only, no third-party user-data transfer).

### Changed

- **SKILL.md**: `references/scenarios.md` cross-link under **Workflow**; user-facing output rules tightened (no internal tool or field names in reports); frontmatter description trimmed / neutral wording for multi-dimensional queries.

---

## [2026.3.20-1] - 2026-03-20 — Initialization

### Added

- **Skill**: Market Research Copilot (L2 composite). Orchestrates 12 read-only MCP tools across Gate-Info (8) and Gate-News (4) for structured market intelligence. Covers: market overview, single-coin deep dive, multi-coin comparison, technical trend, event attribution, risk check, and screening mode.
- **SKILL.md**: 5-dimension signal detection (S1 Market/Macro, S2 Fundamentals, S3 Technicals, S4 News/Sentiment, S5 Security), parallel/serial execution model, 5 report templates (Market Brief, Single-Coin, Multi-Coin, Event Attribution, Risk Check), judgment logic, error handling, cross-skill routing, safety rules. Parameter notes for `source=spot` constraint on `get_kline` and `get_market_snapshot`.
- **README.md**: Overview, 7 core capabilities, routing table, architecture description, MCP service dependencies, signal-to-tool mapping.
- **references/scenarios.md**: 9 scenario definitions covering low/medium/high complexity use cases with tool call chains.

### Audit

- Read-only; all 12 tools are public read, no authentication required. No trading, swaps, staking, or fund-moving operations.
