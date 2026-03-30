# Changelog — gate-news-communityscan

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.3.30-5] - 2026-03-30

### Changed

- **SKILL.md**: Semantically aligned frontmatter `description` with the other three skills (X-first scope, UGC caveat, tools); `version` → `2026.3.30-5`.

---

## [2026.3.30-1] - 2026-03-30

### Added

- **README.md**, **references/scenarios.md**: overview, capabilities, routing, architecture; scenario prompts aligned with `gate-info-addresstracker`.
- **Update scripts**: `scripts/update-skill.sh`, `scripts/update-skill.ps1` (same pilot implementation as `gate-info-addresstracker`).
- **SKILL.md**: **Per-skill updates** + full **Trigger update (with Execution)** (check / confirm / apply); **Known Limitations** remains before **MCP Dependencies**; frontmatter `version` / `updated` set to `2026.3.30-1` / `2026-03-30`.

### Changed

- **SKILL.md**: `### Required MCP Servers` table spacing aligned with `gate-info-addresstracker`.

### Audit

- Read-only; no trading or order execution.

---

## [2026.3.25-1] - 2026-03-25

### Added

- Skill: Community sentiment scan with **X/Twitter** focus. Parallel MCP: news_feed_search_x, news_feed_get_social_sentiment; **Known Limitations** for deferred UGC (Reddit/Discord/Telegram). Report template, decision logic, routing, error handling, cross-skill routing, safety rules.
- SKILL.md: General Rules and MCP block aligned with `gate-info-addresstracker` / `gate-news-briefing`.
- MCP tools: news_feed_search_x, news_feed_get_social_sentiment.

### Audit

- Read-only; no trading or order execution.
