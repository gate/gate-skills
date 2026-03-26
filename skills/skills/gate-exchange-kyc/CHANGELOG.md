# Changelog

## [2026.3.18-2] - 2026-03-18

### Changed

- Simplified skill: single short workflow (provide KYC portal URL + brief steps), reduced judgment logic and report template. Scenarios reduced to 2. README shortened.

## [2026.3.18-1] - 2026-03-18

### Added

- Initial release of gate-exchange-kyc (KYC Portal Skill).
- Workflow: identify intent, determine guidance, provide KYC portal URL, brief instructions, guide user to complete actions.
- Judgment logic for start KYC, learn about KYC, resolve restriction, and out-of-scope (e.g. application status).
- Report template for consistent response format.
- Scope and boundaries: portal link and high-level guidance only; no verification execution, OCR, or application review.
- references/scenarios.md with scenario cases and prompt examples.
