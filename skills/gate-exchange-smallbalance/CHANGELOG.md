# Changelog

## [2026.3.20-1] - 2026-03-20

### Added
- Gate Exchange Small Balance Skill (dust to GT): list eligible dust, convert to GT, view conversion history
- Interactive conversion flow with currency validation and explicit user confirmation
- `gate-cli` commands: `gate-cli cex wallet balance small`, `gate-cli cex wallet balance convert-small`, `gate-cli cex wallet balance small-history`
- Domain knowledge, error handling, and safety rules (confirm-before-convert, no fabricated results)
- Standard architecture with `references/scenarios.md` and README