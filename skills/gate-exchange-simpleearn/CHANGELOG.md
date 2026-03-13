# Changelog

## [2026.3.12-2] - 2026-03-12

### Changed

- **Subscribe and redeem API calls disabled**: This skill must not call `cex_earn_create_uni_lend` for subscribe (type: lend) or redeem (type: redeem). When the user requests subscribe, redeem, or one-click subscribe top APY, reply only "Simple Earn subscribe and redeem are currently not supported"; do not show draft or call MCP. Updated SKILL.md, scenarios.md, earn-uni-api.md, README.md.
- **English-only docs**: All skill docs (SKILL.md, README.md, CHANGELOG.md, references) converted to English per project validation (skill-validator).

## [2026.3.11-6] - 2026-03-11

### Added

- MCP tool names unified to `cex_earn_*` (e.g. `cex_earn_list_uni_currencies`, `cex_earn_create_uni_lend`, `cex_earn_list_user_uni_lends`). Synced SKILL.md, README.md, references/scenarios.md.

### Audit

- Write operations (subscribe/redeem) require user confirmation before submit; no auto-submit.
