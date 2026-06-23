# Changelog — gate-info-research

**Note**: Dates follow the same `YYYY.M.D-N` format the legacy `gate-info-business-skills` project uses. Bump `version` + `updated` in `SKILL.md` frontmatter and in [playbooks/gate-info-research.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-research.yaml) together when this file receives a new entry.

---

## [2026.6.22-1] - 2026-06-22 — market_overview shortcut keeps ranking boards

- `market_overview.shortcut`: `replaces_command_ids` now lists ONLY `market_overview`; ranking boards (`popular_board`, `gainers_board`, `losers_board`) moved to `post_shortcut_optional_ids` so they still run after `+market-overview` (no data loss; +3 ranking calls). Updated `synthesis_note`/`notes` and `_shared/cli-version-routing.md` mapping.

## [2026.6.12-8] - 2026-06-12 — +brief shortcut time-range arg_enums

- `research_plus_news.additional_shortcut`: `arg_enums.time-range: [1h, 24h, 7d]`; clamp note for 30d partial.

## [2026.6.12-7] - 2026-06-12 — Shortcut skip union + research_plus_news branch

- Step 2: global `skip_ids` union across shortcut blocks (incl. parent `news_addons`); §2.F explicit shortcut vs legacy branches.
- `market_overview` synthesis_note: top-level JSON fields (not `.data.*`).

## [2026.6.12-6] - 2026-06-12 — Orchestration contract (args_when, symbols_csv)

- `multi_coin` shortcut uses `{symbols_csv}`; slot_registry documents comma-join vs repeatable legacy `--symbols`.
- Step 2 shortcut routing references machine `when` predicates and block order in `_shared/cli-version-routing.md`.

## [2026.6.12-5] - 2026-06-12 — Fix +coin-compare field mapping

- `compare_matrix` (not `comparison_matrix`) in `_shared/cli-version-routing.md`; row shape + `dropped_symbols` documented.

## [2026.6.12-4] - 2026-06-12 — Align info/news JSON contract with gate-cli 0.7.6

- Document actual stdout/stderr shape in `_shared/cli-version-routing.md` (payload root on success; stderr `error` on failure; not `{ status, data, meta }`).
- Step 2 fallback: exit code + stderr, not stdout `status != "success"`.
- `cli-reference.md`, `preflight.md`, `gate-cli-commands-summary.md` cross-links.

## [2026.6.12-3] - 2026-06-12 — CLI enum sync (0.7.6)

- `get-coin-rankings` `arg_enums`: add `market_pulse_hot`.

## [2026.6.12-2] - 2026-06-12 — Shortcut review fixes

- `research_plus_news`: `inherits_shortcuts_from: single_coin`; `market_overview` synthesis_note for missing boards on shortcut path.
- Field mapping corrections in `cli-version-routing.md`.

## [2026.6.12-1] - 2026-06-12 — gate-cli v0.7.6 shortcut routing

### Added

- Playbook `shortcut` blocks for `single_coin`, `market_overview`, `multi_coin`, `trend`; `additional_shortcut` for `research_plus_news`.
- Shared [skills/_shared/cli-version-routing.md](../_shared/cli-version-routing.md): `shortcuts_enabled` when `cli_version >= 0.7.6`.

### Changed

- Step 0.5 version gate; Step 2 prefers aggregates, legacy `commands` fallback on failure or `< 0.7.6`.
- `cli_baseline` → v0.7.6 shortcuts opt-in; legacy v0.5.2 retained in `commands`.

---

## [2026.4.18-1] - 2026-04-18 — Initial release

### Added

- **Skill**: Research-oriented primary skill covering single-coin analysis, market overview, multi-coin comparison, trend / technical analysis, macro impact, and research-plus-news synthesis. Consolidates the legacy `gate-info-coinanalysis`, `gate-info-marketoverview`, `gate-info-coincompare`, `gate-info-trendanalysis`, `gate-info-macroimpact` into one unified 6-section report.
- **SKILL.md**: Steps 0-3 + cross-skill routing; references shared modules under [skills/_shared/](https://github.com/gate/gate-skills/tree/master/skills/_shared) for preflight, routing, report style.
- **Playbook**: [playbooks/gate-info-research.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-research.yaml) — six playbooks (`single_coin`, `market_overview`, `multi_coin`, `trend`, `macro`, `research_plus_news`) with real `gate-cli v0.5.2` lower-level commands.
- **References**: [references/scenarios.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-research/references/scenarios.md), [references/cli-reference.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-research/references/cli-reference.md), [references/troubleshooting.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-research/references/troubleshooting.md).
- **Scripts**: `scripts/update-skill.sh`, `scripts/update-skill.ps1` — mirror of the legacy Trigger-update flow.

### CLI baseline

- Aligned to `gate-cli v0.5.2` as of `gate-cli info list` / `gate-cli news list`.
- No aggregate shortcuts (`info +coin-overview`, `news +brief`, ...) are assumed; every command referenced is verified present.

### Audit

- Read-only; no trade execution.
- No investment advice emitted; strongest phrasing is `偏强 / 偏弱 / 需继续观察`.
