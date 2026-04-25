# Changelog — gate-news-intel

## 2026.4.20-2

- SKILL.md: added a News-intel-specific follow-up routing table in `## Cross-skill routing + Safety rules` so the three delegate targets (`gate-info-research`, `gate-info-web3`, `gate-info-risk`) are surfaced next to the report-completion stage, mirroring the other three primary skills. Fixes the asymmetry that caused `scripts/test-cross-skill-routing.py` to flag three WARNs (CSR section had no target skill references).
- No playbook execution-path changes; version bumped only to keep SKILL.md ↔ playbook `version` / `updated` consistent per CLAUDE.md rule 2.

## 2026.4.20-1

- Initial primary skill: brief, event explain, exchange listings, community intel (UGC + X + sentiment), intel + market/coin context, market-wide web + overview.
- Documented `cli_future_shortcut` for unshipped `news +*` and `info +*` aggregates.
- Five-section report template per `需求文档.md` §5.6.
