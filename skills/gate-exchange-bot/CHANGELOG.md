# Changelog

## [2026.5.6-5] - 2026-05-06

### Changed

- Added literal `## Execution`, `## Domain Knowledge`, and `## Error Handling` sections to satisfy routing-skill validator requirements.
- Added `## Workflow` and `## Report Template` sections to all non-scenario reference documents.
- Added a `gate-cli` to bot capability mapping table for clearer MCP-backed command traceability.

## [2026.5.6-4] - 2026-05-06

### Changed

- Reworked `SKILL.md` structure to align with General Rules placement and canonical tool-allowlist wording.
- Removed Skills Hub-breaking relative Markdown links from root skill documentation.
- Added explicit safety, privacy, installation dependency, and confirmation sections.
- Added `references/scenarios.md` for routing-skill scenario coverage.
- Expanded `README.md` with Architecture, runtime dependency, privacy, compliance, and support sections.
- Normalized changelog heading format.

## [2026.5.6-3] - 2026-05-06

### Changed

- Rewrote `gate-exchange-bot` authoring content in English to match the style of other exchange skills.
- Replaced mixed-language bot reference documents with English `gate-cli`-style workflow specifications.

## [2026.5.6-2] - 2026-05-06

### Changed

- Converted `gate-exchange-bot` from MCP-only wording to standard `gate-cli` exchange skill style.
- Added `openclaw` metadata, `gate-cli` dependency declaration, install guidance, and `setup.sh`.
- Added `references/gate-cli.md` as the authoritative execution contract.
- Rewrote root `SKILL.md` and `README.md` around `gate-cli cex bot ...` commands.
- Updated module reference documents to use `gate-cli` bot command names.

## [2026.5.6-1] - 2026-05-06

### Added

- Reorganized `gate-exchange-bot` into a single-entry skill layout aligned with other top-level Gate skills.
- Moved bot workflow documents into a root `references/` directory.
- Added root `SKILL.md`, `README.md`, and `CHANGELOG.md`.
