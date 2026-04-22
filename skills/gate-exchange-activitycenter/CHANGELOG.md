# Changelog

All notable changes to this skill will be documented in this file.

## [2026.4.3-1] - 2026-04-03

### Changed
- Added packaged `metadata.openclaw` credential declarations for ClawHub review consistency.
- Moved the mandatory runtime-rules reference into this skill bundle for publish-time auditability.
- No execution workflow or business logic changes.

## [2026.3.23-1] - 2026-03-23

### Changed
- Aligned runtime-rule references and documentation wording for ClawHub review.
- No execution workflow or business logic changes.

## [2026.3.19-18] - 2026-03-19

### Added
- Added language conversion rule for Scenario 1.4: non-English keywords must be translated to English before API call

## [2026.3.19-17] - 2026-03-19

### Changed
- Fixed heading hierarchy: H1 now appears before H2 General Rules
- Fixed General Rules reference: now points to local `gate-runtime-rules.md` instead of `scenarios.md`
- Translated all Chinese content to English (trigger examples, error messages, labels)
- Expanded Error Handling table with 401/400/429/500/Network error scenarios
- Fixed link placeholder format: `[{activity_title}]({processed_url})`

## [2026.3.19-16] - 2026-03-19

### Changed
- Added mandatory response template enforcement rule
- Restructured Response Templates section with detailed compliance rules
- Added Template Compliance Rules with REQUIRED/FORBIDDEN specifications
- Added explicit response structure examples for all scenarios
- Added My Activities Template (Scenario 2) with required structure

## [2026.3.19-1] - 2026-03-19

### Added
- Initial release of gate-exchange-activitycenter skill
- Scenario 1: Activity Recommendation (hot, type-based, scenario-based, search by name)
- Scenario 2: My Activities entry
- Response templates for all scenarios
- Error handling and safety rules
- Support for 3 `gate-cli` commands: `gate-cli cex activity types`, `gate-cli cex activity list`, `gate-cli cex activity get-entry`
- Fixed page_size=3 for all activity list queries
- Case-insensitive type matching
