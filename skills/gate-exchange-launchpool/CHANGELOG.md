# Changelog

All notable changes to the Gate Exchange LaunchPool skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [2026.3.18-2] - 2026-03-18

### Changed
- Removed `start_timest`/`end_timest` (activity time) from project list display — these are now internal-only fields
- Kept `days` (staking period) in project list display
- Added `(UTC)` suffix to `create_timest` and `reward_timest` in pledge/reward records display
- Simplified SKILL.md timestamp formatting section to only cover record timestamps
- Removed `Staking Period` line from stake preview template (stake-redeem.md)

## [2026.3.18-1] - 2026-03-18

### Changed
- Added complete API response field documentation from OpenAPI spec for all 5 endpoints
- Added `project_state` field (1=In progress, 2=Warming up, 3=Ended) to project list response
- Added timestamp formatting rule: all timestamps must be displayed as `YYYY-MM-DD HH:MM:SS (UTC)`
- Added API error label mapping (INVALID_PARAM_VALUE, INVALID_CREDENTIALS, INSUFFICIENT_BALANCE, PROJECT_NOT_FOUND)
- Fixed field names to match actual API: `rate_year`, `already_buy_total_amount`, `personal_max_amount`/`personal_min_amount`, `transaction_config`
- Documented time parameter format difference: pledge records uses string `YYYY-MM-DD HH:MM:SS`, reward records uses integer timestamps
- Documented `coin` parameter meaning difference: pledge records filters by staking coin, reward records filters by reward coin
- Added redeem response schema: `{success: boolean}`
- Added create order response schema: `{flow_id: integer}`

## [2026.3.17-1] - 2026-03-17

### Added
- Initial release of Gate Exchange LaunchPool skill
- Browse LaunchPool projects with filtering (status, APR, staking coin, pool type)
- Stake tokens to LaunchPool projects with Preview-Confirm flow
- Redeem staked assets with Preview-Confirm flow
- Query pledge records (staking/redemption history) by time and coin
- Query airdrop reward records by time and coin
- Compliance error handling for region restrictions
- 16 scenarios across 3 sub-modules
- Support for 5 MCP tools from gate-dev and g-d-x services
