# Changelog

## [2026.3.11-5] - 2026-03-11

### Added
- ORDER_NOT_FOUND (404) error handling for non-existent order_id in Step 5 and Error Handling table
- API response field name mapping table (camelCase to snake_case) in Domain Knowledge
- Large result set handling guidance in Step 2 (34,000+ rows: summarize, sample 20, suggest filter)
- Timestamp format definition (`YYYY-MM-DD HH:mm:ss UTC`) in Report Template section

### Fixed
- Changed `order_id` type from integer to string to match API response schema
- Added data type note for `order_id` in Domain Knowledge

## [2026.3.11-4] - 2026-03-11

### Added
- `## Quick Start` section with 3 common query examples
- `## Trigger Conditions` section as independent trigger definition
- Fallback behavior for limit check when currency is not specified (prompt user)
- Pre-validation for `status` parameter (only 1 or 2 accepted, reject before API call)
- Two new error handling entries: "Currency not specified for limit check" and "Invalid status value"
- Two new judgment logic entries for edge case coverage

## [2026.3.11-3] - 2026-03-11

### Added
- New intent "check_limits" for validating currency support and querying min/max swap amounts
- New report template "Flash Swap Currency Limit Report" with sell/buy min/max columns
- Scenario 2 (currency limit validation) in scenarios.md
- Error handling for unsupported currency case

### Changed
- Expanded intent classification from 3 to 4 types (list_pairs, check_limits, list_orders, get_order)
- Updated Workflow from 5 to 6 steps to accommodate limit checking
- Restructured scenarios.md from 3 to 4 scenarios matching new case coverage
- Updated Judgment Logic Summary with limit-related conditions
- Enhanced Domain Knowledge with sell/buy min/max amount concepts

## [2026.3.11-2] - 2026-03-11

### Changed
- Converted all documentation to English

## [2026.3.11-1] - 2026-03-11

### Added
- Initial release
- Support querying flash swap currency pair list (`cex_fc_list_fc_currency_pairs`) with optional currency filter
- Support querying flash swap order history (`cex_fc_list_fc_orders`) with status, currency, and pagination filters
- Support querying single flash swap order details (`cex_fc_get_fc_order`)
- Includes error handling and safety rules
- Provides 3 scenario examples covering all query functions
