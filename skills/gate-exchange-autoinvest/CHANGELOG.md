# Changelog

## [2026.4.2-3] - 2026-04-02

### Added

- **gate-exchange-autoinvest** skill for Gate Exchange Earn DCA: eleven earn auto-invest `gate-cli` commands plus supporting `gate-cli cex spot account get` and `gate-cli cex earn uni lends`; documentation uses `gate-cli` command names only (no REST paths in skill text).
- **references/scenarios.md** (16-scenario index), **references/autoinvest-plans.md**, and **references/autoinvest-compliance.md** with workflows, prompt examples, response templates, and compliance-facing rules.
- **SKILL.md** as router: feature modules, `gate-cli` commands, routing, execution, domain knowledge, safety (mandatory confirmation, stale Action Draft invalidation, **default: no write without confirmation** for gate-skill-cr 12.4, add-position call exactly once), error handling, judgment summary, and report templates.
- **Business rules**: USDT/BTC investment currency; `plan_period_day` by `plan_period_type`; multi-target limits (≤10 targets, ≥10% per coin); min/max from `gate-cli`; on-the-hour UTC `plan_period_hour`; `fund_flow` mapping (Simple Earn vs spot).
- **Operational alignment**: link to **exchange-runtime-rules.md**; parameter hygiene when the `gate-cli` schema requires a value with no default; **README** architecture and file map.

### Changed

- Renamed skill and directory from **gate-exchange-auto-invest** to **gate-exchange-autoinvest** for naming convention compliance.
- **Stop plan** behavior: `gate-cli cex earn auto-invest stop` must not run in the same assistant turn as the first Action Draft—wait for the user’s **next** message with explicit confirmation (aligned across SKILL and reference scenarios).
- **Compliance and copy**: removed KYC-specific auto-invest wording; use **Gate** branding and English product naming (e.g. Simple Earn); frontmatter description includes required trigger phrasing.
- **Structure and CR hygiene**: routing chapters extracted for visibility; **## `gate-cli` commands** section title and H1 aligned with skill id; historical ref splits/inlines (scenario index vs SKILL, removal of separate API/`gate-cli`-tools/query ref files as the skill evolved).
