# Changelog

## [2026.3.18-5] - 2026-03-18

### Fixed
- Replaced misleading camelCase-to-snake_case mapping table with accurate per-API field naming notes (P1-1)
- Quote validity now references `valid_timestamp` from response instead of hardcoded "5 minutes" (P1-2)
- Consolidated error codes 4/400001/400007 with clearer descriptions of when each occurs (P1-4)
- Stale confirmation rule now checks `valid_timestamp` instead of assuming fixed duration

## [2026.3.18-4] - 2026-03-18

### Added
- **CRITICAL** error handling for region/compliance restriction (`code: -2`): stop all operations, inform user
- **CRITICAL** error handling for any preview failure (`code != 0`): block create step, report error honestly
- **CRITICAL** safety rule: NEVER fabricate results — no fake order IDs, quote_ids, or success messages when API returns error
- **CRITICAL** safety rule: NEVER proceed after preview failure — if preview returns error, do NOT call create API
- Pre-condition guard on Step 4 (Create): requires `code == 0` from Step 3 (Preview)
- Guard on `one_to_one_auto` flow: if preview fails, stop and report error even in auto mode
- Judgment logic entries for `code -2` and general preview failure

### Fixed
- Security vulnerability: AI could fabricate successful transaction results when API returned errors (e.g. region restriction code -2)

## [2026.3.18-3] - 2026-03-18

### Added
- MCP Tool Inventory table in Domain Knowledge section listing all 9 tools with type and description
- Explicit "No write operations without confirmation" safety rule
- Stale confirmation handling rule (auto re-preview if quote_id > 5 min old)

### Fixed
- Safety Rules contradiction: "Always preview before creating" conflicted with `one_to_one_auto` mode. Clarified that user's explicit "direct/one-click" request serves as pre-authorized confirmation
- Added explicit write-protection statement to Safety Rules

## [2026.3.18-2] - 2026-03-18

### Added
- Pre-validation step: check sell_amount against sell_min_amount before calling preview API (Case 8)
- One-click swap mode: auto preview + create without separate confirmation (Case 7)
- Order result verification: check status after create and via `cex_fc_get_fc_order` (Case 9)
- One-to-many split by ratio: auto-calculate per-target amounts from total + ratio (Case 10)
- One-to-many with buy_amount: specify exact buy quantities, API calculates sell cost (Case 11)
- Many-to-one asset consolidation: query balances, filter by min amounts, preview + create (Case 12)
- Many-to-one preview-only: estimate total without executing (Case 13)
- 9 new scenarios (Cases 5-13) covering quote preview, confirm-and-execute, one-click, amount validation, order verification, ratio split, buy-quantity, asset consolidation, and feasibility preview
- New error handling entries: amount below/above min/max, balance below minimum for consolidation
- New judgment logic entries for all new intent types

### Changed
- Expanded intent classification from 6 to 12 types
- Workflow expanded from 11 to 12 steps (added Step 2: Pre-validate Swap Amount)
- Step numbering shifted: old Steps 2-11 are now Steps 3-12
- Enhanced one-to-many preview step with split and buy_amount modes
- Enhanced many-to-one preview step with consolidation and preview-only modes
- Total scenarios expanded from 5 to 13

## [2026.3.18-1] - 2026-03-18

### Added
- One-to-one flash swap: preview via `cex_fc_preview_fc_order_v1`, create via `cex_fc_create_fc_order_v1`
- One-to-many flash swap: preview via `cex_fc_preview_fc_multi_currency_one_to_many_order`, create via `cex_fc_create_fc_multi_currency_one_to_many_order`
- Many-to-one flash swap: preview via `cex_fc_preview_fc_multi_currency_many_to_one_order`, create via `cex_fc_create_fc_multi_currency_many_to_one_order`
- Quote expiry handling (code 1052) with auto-retry guidance
- Multi-currency failed item exclusion logic (prevent code 4 rejection)
- Safety rule: always preview before creating, never skip confirmation
- Warning for large swap amounts exceeding 10,000 USDT equivalent
- 5 comprehensive scenarios covering all swap modes and query operations

### Changed
- Upgraded from query-only skill to full trading skill with preview-and-create workflow
- Expanded from 3 MCP tools to 9 MCP tools
- Restructured workflow from 6 steps to 11 steps
- Updated all report templates for swap operations

### Removed
- Deprecated `cex_fc_preview_fc_order` (replaced by `cex_fc_preview_fc_order_v1`)
- Deprecated `cex_fc_create_fc_order` (replaced by `cex_fc_create_fc_order_v1`)

## [2026.3.11-5] - 2026-03-11

### Fixed
- Replaced relative path link with inline code format to prevent 404 on Skills Hub

## [2026.3.11-4] - 2026-03-11

### Added
- Quick Start section with common query examples
- Trigger Conditions section
- Fallback behavior for limit check when currency not specified
- Pre-validation for status parameter

## [2026.3.11-3] - 2026-03-11

### Added
- Currency limit validation intent and workflow step
- Flash Swap Currency Limit Report template

## [2026.3.11-2] - 2026-03-11

### Changed
- Converted all documentation to English

## [2026.3.11-1] - 2026-03-11

### Added
- Initial release with query-only functionality
- Support for querying flash swap currency pairs, order history, and single order details
