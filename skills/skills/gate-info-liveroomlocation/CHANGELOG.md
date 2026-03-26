# Changelog

## [2026.3.13-1] - 2026-03-13

### Added

- Initial skill: live and replay listing by tag, coin, sort, and limit.
- Single API: `GET /live/gate_ai/tag_coin_live_replay`.
- Workflow: parse intent and map parameters (with defaults) → call API → build list (title + link).
- Judgment logic summary and report template.
- Restricted-region check: do not call API; reply with region-not-available message.
- No follow-up questions for missing parameters; use defaults.

### Audit

- ✅ Naming: gate-info-liveroomlocation (7.3.2). Description reflects Gate Exchange. English only (7.3.3). Directory and four required files per standard.
