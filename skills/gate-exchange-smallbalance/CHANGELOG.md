# Changelog

## [2026.3.20-1] - 2026-03-20

### Added
- Gate Exchange Small Balance Skill (dust to GT): list eligible dust, convert to GT, view conversion history
- Interactive conversion flow with currency validation and explicit user confirmation
- MCP tools: `cex_wallet_list_small_balance`, `cex_wallet_convert_small_balance`, `cex_wallet_list_small_balance_history`
- Domain knowledge, error handling, and safety rules (confirm-before-convert, no fabricated results)
- Standard architecture with `references/scenarios.md` and README