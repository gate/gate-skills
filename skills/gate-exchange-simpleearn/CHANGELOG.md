# Changelog

## [2026.3.18-5] - 2026-03-18

### Changed

- **Flexible (Uni) display**: User-facing output must omit all time-related fields from `gate-cli` responses; chart/history summarized without timestamps (SKILL.md, README.md, `earn-uni-gate-cli-tools.md`, `scenarios.md`).

## [2026.3.18-4] - 2026-03-18

### Fixed

- **skill-validator**: Frontmatter `description` now includes required phrases `Use this skill whenever` and `Trigger phrases include`.
- **`gate-cli` alignment**: Replaced non-existent `gate-cli cex earn uni currencies` with `gate-cli cex earn uni rate` + `gate-cli cex earn uni currency` (SKILL, README, `references/earn-uni-gate-cli-tools.md`).
- **scenarios.md**: Fixed-term Scenario 7 field order (Context → Prompt Examples → Expected Behavior).

## [2026.3.18-3] - 2026-03-18

### Added

- **`gate-cli`-only reference docs**: `references/earn-uni-gate-cli-tools.md` (flexible Uni tools, arguments, response fields) and `references/fixed-earn-gate-cli-tools.md` (fixed-term tools, arguments, output table formats). No REST paths or methods.

### Changed

- **SKILL.md**, **README.md**, **scenarios.md**: All tool and scenario references now point to the `gate-cli`-only docs instead of API/mapping docs. Removed REST Method/Path columns from scenario tables; descriptions are `gate-cli`-tool only.

## [2026.3.18-2] - 2026-03-18

### Changed

- **English-only references**: Replaced Chinese OpenAPI dump in `references/fixed-earn-api.md` with a concise English REST reference. Normalized punctuation in `references/fixed-earn-gate-cli-tools.md` and `references/scenarios.md` (fixed-term bullets).
- **SKILL.md**: Frontmatter `description` now includes required phrases per skill-validator (`Use this skill whenever`, `Trigger phrases include`).

## [2026.3.18-1] - 2026-03-18

### Changed

- Reconciled the skill docs to cover both flexible (Uni) and fixed-term Simple Earn workflows. Updated `SKILL.md`, `README.md`, and routing/reference guidance so the package no longer claims fixed-term is unsupported.

## [2026.3.16-1] - 2026-03-16

### Changed

- **Subscribe/redeem enabled**: Allow `gate-cli cex earn uni lend` for subscribe (lend) and redeem with user confirmation. Updated SKILL.md, README.md, references/scenarios.md, references/earn-uni-api.md.
- **Change min rate enabled**: Allow `gate-cli cex earn uni change` with user confirmation. Updated SKILL.md, README.md, references/scenarios.md, references/earn-uni-api.md.

## [2026.3.12-2] - 2026-03-12

### Changed

- **Subscribe and redeem API calls disabled**: This skill must not call `gate-cli cex earn uni lend` for subscribe (type: lend) or redeem (type: redeem). When the user requests subscribe, redeem, or one-click subscribe top APY, reply only "Simple Earn subscribe and redeem are currently not supported"; do not show draft or call `gate-cli`. Updated SKILL.md, scenarios.md, earn-uni-api.md, README.md.
- **English-only docs**: All skill docs (SKILL.md, README.md, CHANGELOG.md, references) converted to English per project validation (skill-validator).

## [2026.3.11-6] - 2026-03-11

### Added

- `gate-cli` command names unified to `cex_earn_*` (e.g. `gate-cli cex earn uni currencies`, `gate-cli cex earn uni lend`, `gate-cli cex earn uni lends`). Synced SKILL.md, README.md, references/scenarios.md.

### Audit

- Write operations (subscribe/redeem) require user confirmation before submit; no auto-submit.
