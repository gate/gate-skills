# Changelog — gate-news-briefing

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.3.25-1] - 2026-03-25

### Added

- **Runtime rules**: SKILL.md references shared `info-news-runtime-rules.md` with `gate-runtime-rules.md`; **Trigger update** (check / confirm / apply) and **Routing Rules** aligned to the gate-info / gate-news rollout.
- **Update scripts**: `scripts/update-skill.sh`, `scripts/update-skill.ps1` (same pilot implementation as sibling Info/News skills).

---

## [2026.3.12-1] - 2026-03-12

### Added

- Skill: News briefing. Trigger: "What happened recently", "Today's hot topics". MCP tools (order): news_feed_search_news, news_feed_get_social_sentiment, news_events_get_latest_events (3 in parallel).
- SKILL.md: Routing, 3-tool parallel table, 3-section Report Template (strong constraint), Decision Logic, Error Handling, Cross-Skill, Safety. Aligned with docs/SKILL_SPEC_TABLE.md, docs/PD_VS_SKILLS_OPTIMIZATION_SUMMARY.md.
- README.md, references/scenarios.md.

### Audit

- Read-only; no trading or order execution.
