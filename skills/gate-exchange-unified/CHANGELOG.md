# Changelog

## [2026.4.3-1] - 2026-04-03

- Added packaged `metadata.openclaw` credential declarations for ClawHub review consistency.
- Moved the mandatory runtime-rules reference into this skill bundle for publish-time auditability.
- No execution workflow or business logic changes.

## [2026.3.23-1] - 2026-03-23

- Aligned documentation wording for ClawHub review.
- No execution workflow or business logic changes.

## [2026.3.13-1] - 2026-03-13

- Initialized the `gate-exchange-unified` skill directory documentation structure.
- Added `SKILL.md`, covering 18 unified account scenarios across account overview, borrowing, repayment, transferability, leverage, and collateral configuration.
- Added `references/scenarios.md`, with per-scenario prompt templates, expected behavior, and unexpected behavior checks.
- Added mandatory mutation-confirmation guardrails for borrow/repay, mode switching, leverage updates, and collateral updates.
