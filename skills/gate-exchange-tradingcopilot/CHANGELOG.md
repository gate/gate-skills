# Changelog

## [2026.3.28-14] - 2026-03-28

### Fixed

- **Language policy**: Removed CJK from skill-facing prose in `SKILL.md`, `README.md`, and `references/scenarios.md` (gate-skill-cr / skill-validator English-only policy).
- **Repository completeness**: Added **`CHANGELOG.md`** (required alongside `SKILL.md` and `README.md`).

## [2026.3.28-13] - 2026-03-28

### Changed

- Aligned scenarios **7**, **14**, **20** and **signal detection** with **Trading Copilot L2 Tool Calls** HTML spec in repository `docs/` (L2 Tool Calls full copy): futures orders/entrustments query; unified-account repay-only path; mandatory two-step confirmation for scenario 20.
- **MCP Dependencies**: added **`cex_unified_list_unified_loan_records`** for unified loan repayment reads.
