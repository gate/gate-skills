# Changelog

## [2026.4.6-1] - 2026-04-06

- Excluded non-runtime documentation files from the published bundle so ClawHub review matches Phase 1 same-UID transfer scope.
- Removed the remaining SKILL.md pointer to future sub-account scenarios from the published execution path.
- No execution workflow or business logic changes.

## [2026.4.3-1] - 2026-04-03

- Added packaged `metadata.openclaw` credential declarations for ClawHub review consistency.
- Moved the mandatory runtime-rules reference into this skill bundle for publish-time auditability.
- No execution workflow or business logic changes.

## [2026.3.23-1] - 2026-03-23

- Aligned documentation wording for ClawHub review.
- No execution workflow or business logic changes.

## [2026.3.11-1] - 2026-03-11

- Initialized the `gate-exchange-transfer` skill directory and documentation structure.
- Added `SKILL.md`, covering 8 transfer scenarios (main account, sub-account, status query).
- Added `references/scenarios.md`, with per-case examples for inputs, API calls, and confirmation flow.
- Mandatory balance verification and user confirmation before any transfer execution.
*** Add File: /Users/gaixg/gate/gate-github-skills/skills/gate-exchange-transfer/.clawhubignore
README.md
CHANGELOG.md
references/scenarios.md
