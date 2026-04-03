# Changelog

## [2026.3.31-2] - 2026-03-31

### Added

- **Atomic Tool Call Chains** section in `SKILL.md`: all **21** scenarios from the L2 HTML spec (#1–#8 base, #9–#13 extended, #14–#21 dust/small/split) with **P1 parallel**, **serial →**, **P0**, **Confirm**, and **(W)** notation; marked **mandatory** when the user story maps to a row.

### Changed

- **Workflow** Step 1: require matching atomic chains before generic signal fallback.

## [2026.3.31-1] - 2026-03-31

### Added

- Initial **gate-exchange-flashswap-assistant** L2 skill derived from the Flash Swap Assistant L2 Tool Calls spec (fc + spot balance + dust-to-GT), with thirteen-tool allowlist, signal routing S1–S7, Action Draft confirmation, `references/scenarios.md`, and English-only skill-facing prose aligned with gate-skill-cr and skill-validator-v2.
