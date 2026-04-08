# Changelog

## [2026.4.8-1] - 2026-04-08

### Changed
- Excluded non-runtime documentation from the published bundle to reduce ClawHub scan noise.
- No MCP workflow or business logic changes.

## [2026.4.3-1] - 2026-04-03

### Changed
- Added packaged `metadata.openclaw` credential declarations for ClawHub review consistency.
- Moved the mandatory runtime-rules reference into this skill bundle for publish-time auditability.
- No MCP workflow or business logic changes.

## [2026.3.23-1] - 2026-03-23

### Changed
- Aligned documentation wording for ClawHub review.
- No MCP workflow or business logic changes.

## [2026.3.13-1] - 2026-03-13

### Added
- Initial version of gate-exchange-coupon skill
- Routing architecture with two sub-modules: list-coupons and coupon-detail
- Scenario 1: List all available coupons with grouped summary output
- Scenario 2: Query coupons by specific type, show all coupon fields
- Scenario 3: View full coupon details including all attribute fields from extra blocks
- Scenario 4: Read coupon usage rules (rule_new field from detail API)
- Scenario 5: Trace coupon acquisition source (COUPON_VOUCHER_SOURCE from extra block)
- Domain knowledge: coupon type reference, status reference, MCP tool mapping, API parameter tables
- Error handling for common scenarios (not found, invalid type, empty result, ambiguous input)
- Safety rules: read-only operations, no credential handling
