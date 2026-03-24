# Changelog

## [2026.3.24-1] - 2026-03-24

### Added
- `README.md`: Overview, core capabilities, MCP tool table, architecture layout, authentication note.

### Changed
- `SKILL.md`: General Rules — MCP tool allowlist bullet (aligned with `gate-exchange-crossex` template).

## [2026.3.18-2] - 2026-03-18

### Added
- **Domain Knowledge** section: Partner/affiliate, commission, trading volume and net fees, subordinates, eligibility, application status.
- **Safety Rules** section: No future timestamps, user_id usage, data scope, aggregation, sub-accounts.

### Changed
- **MCP Dependencies**: Expanded with full tool table; document Call `tool_name` pattern; list `cex_rebate_get_partner_eligibility` and `cex_rebate_get_partner_application_recent`.
- **Step 3 (Call Partner APIs)**: Added paragraph to call MCP tools by name when MCP is configured, fallback to API paths when not.

## [2026.3.18-1] - 2026-03-18

### Added
- Partner eligibility API: `GET /rebate/partner/eligibility` — check if user is eligible to apply for partner (returns eligible, block_reasons, block_reason_codes)
- Partner recent application API: `GET /rebate/partner/applications/recent` — get user's recent partner application record (last 30 days, includes audit_status, apply_msg)
- New query types: application_eligibility, application_status in Workflow and Judgment Logic
- Case 6 extended with eligibility response template and application status template
- API Parameter Reference for eligibility and applications/recent
- Trigger phrases: "can I apply", "am I eligible", "my application status", "recent application", "partner application status"

### Changed
- Application guidance (Case 6) now supports calling eligibility and/or applications/recent when user asks "can I apply?" or "my application status?"
- Scenario 9 Expected Behavior: optionally call eligibility before guiding
- New Scenario 10: Eligibility Check (call eligibility API, return block_reasons if not eligible)
- New Scenario 11: Application Status Query (call applications/recent, show audit_status and apply_msg)
- Previous Scenario 10 (Invalid Query Handling) renumbered to Scenario 12

## [2026.3.12-2] - 2026-03-12

### Changed
- Restructured SKILL.md to follow standard template format
- Added formal Workflow section with 6 defined steps
- Added Judgment Logic Summary table with 14 conditions
- Added standardized Report Template
- Updated README.md with Architecture section
- Reformatted scenarios.md to standard Scenario format

### Improved
- Better alignment with skill-validator requirements
- Clearer separation of workflow steps and data extraction
- More structured documentation organization

## [2026.3.12-1] - 2026-03-12

### Added
- Initial release of Gate Exchange Affiliate skill
- Support for partner transaction history queries
- Support for partner commission history queries
- Support for partner subordinate list queries
- Automatic handling of >30 day queries (up to 180 days)
- Comprehensive error handling and user guidance
- Affiliate program application instructions

### Features
- Query commission amount, trading volume, net fees, customer count, and trading users
- Time-range specific queries with automatic request splitting
- User-specific contribution analysis
- Team performance report generation
- Multi-language trigger phrase support (internally handled in English)

### Technical
- Uses Partner APIs only (Agency APIs deprecated)
- Implements pagination for large result sets
- Handles Unix timestamp conversion
- Provides detailed API parameter documentation