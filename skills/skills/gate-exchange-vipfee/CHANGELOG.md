# Changelog

## [2026.3.11-2] - 2026-03-11

### Added
- `API Behavior Notes` section in Domain Knowledge: account-level pricing, settle parameter scope, invalid currency_pair handling

### Changed
- Step 3: clarified `currency_pair` parameter description (fee rates are account-level, not pair-specific)

## [2026.3.11-1] - 2026-03-11

### Added
- Initial version with VIP tier query via `cex_account_get_account_detail`
- Trading fee rate query (spot and futures) via `cex_wallet_get_wallet_fee`
- Support for combined VIP + fee queries
- Standard architecture with complete Workflow, Judgment Logic Summary, and Report Template
