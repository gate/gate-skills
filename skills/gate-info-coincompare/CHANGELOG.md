# Changelog — gate-info-coincompare

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.3.12-1] - 2026-03-12

### Added

- Skill: Coin comparison. Trigger: multi-coin comparison (e.g. "Compare BTC, ETH, SOL"). MCP tools: info_marketsnapshot_batch_market_snapshot, info_coin_search_coins (spec first, fallback per coin). Tool count: 2.
- SKILL.md: Routing, Workflow tool table (spec + fallback), 4-section Report Template, Decision Logic, Error Handling, Cross-Skill, Safety. Aligned with docs/SKILL_SPEC_TABLE.md, docs/PD_VS_SKILLS_OPTIMIZATION_SUMMARY.md.
- README.md, references/scenarios.md.

### Audit

- Read-only; no trading or order execution.
