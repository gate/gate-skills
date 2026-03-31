# Changelog

## [2026.3.30-1] - 2026-03-30

### Added

- **Partner data aggregated API**: `GET /rebate/partner/data/aggregated` — server-side totals for rebate amount, trade volume, net fee, customer count, and optional `trading_user_count` (only when `business_type=0`). Query params: `start_date`, `end_date` (UTC+8 `yyyy-mm-dd hh:ii:ss`, optional; default last 7 days), `business_type` (0–8).
- **MCP Dependencies**: `cex_rebate_get_partner_agent_data_aggregated` under Query Operations.
- **Workflow / Judgment Logic**: query type `aggregated_summary`; route summary-style intents to the aggregated endpoint.
- **Usage Scenarios**: Case 6 — Aggregated Data Summary (triggers: aggregated data, total summary, overall statistics, summary report); affiliate application guidance renumbered to Case 7.
- **API Parameter Reference**: `data/aggregated` schema and business type enum.
- **Validation**: golden query for aggregated summary.

### Changed

- **SKILL.md** frontmatter: version `2026.3.30-1`; `description` includes **Use this skill whenever** and aggregated-summary **Trigger phrases**; API key link uses `gate.com`.
- **Available APIs** table: row for `GET /rebate/partner/data/aggregated` with optional UTC+8 dates and default last 7 days.
- **Step 3**: call `cex_rebate_get_partner_agent_data_aggregated` when MCP is configured; branch for aggregated summary queries.
- **README.md**: `### Core Capabilities` under **Overview** (skill-validator); REST note mentions `GET /rebate/partner/data/aggregated`.
- **references/scenarios.md**: Scenario 13 — aggregated summary query.
- **MCP tool name**: aggregated summary tool documented as `cex_rebate_get_partner_agent_data_aggregated` (replaces `cex_rebate_partner_data_aggregated`).
- **SKILL.md**: **Rebate / commission intent routing** — summary intents (e.g. 'my rebate', 'query my rebate') → aggregated; record/history/list intents → `commission_history`; new `commission_records` query type and golden queries; Case 3 / Case 6 triggers updated.
- **references/scenarios.md**: Scenario 13 prompt examples expanded; Scenario 14 — commission / rebate records.
- **SKILL.md** / **README.md** / **scenarios.md**: `cex_rebate_get_partner_agent_data_aggregated` supports **up to 180 days in one call**; **no** multi-request splitting for aggregated when range ≤180 days (list APIs still use 30-day segments).
- **SKILL.md** / **README.md**: Re-emphasize **`transaction_history` / `commission_history` hard 30-day max per request**; new **CRITICAL** subsection and API reference constraints; distinct from aggregated 180-day rule.
- **references/scenarios.md**: Scenario 13 — explicit **single aggregated call** for ranges ≤180 days; Scenario 14 — explicit **no >30-day** single `commission_history` request.
- **SKILL.md**: **Workflow** steps 1–6 aligned with skill-validator block pattern (`Call ... with:` + `Key data to extract:`); Step 3 lists each MCP tool and parameters.

## [2026.3.25-1] - 2026-03-25

### Changed

- **SKILL.md**: Shortened frontmatter `description`; moved UTC+8 / time-window rules into **Important Notice → Query time and timezone (UTC+8)**; **Safety Rules** now references that section instead of duplicating conversion details.

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