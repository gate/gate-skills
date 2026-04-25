# Changelog — gate-info-research

**Note**: Dates follow the same `YYYY.M.D-N` format the legacy `gate-info-business-skills` project uses. Bump `version` + `updated` in `SKILL.md` frontmatter and in [playbooks/gate-info-research.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-research.yaml) together when this file receives a new entry.

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
