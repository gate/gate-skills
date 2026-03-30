# Changelog — gate-info-macroimpact

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.3.30-6] - 2026-03-30

### Changed

- **SKILL.md**: Frontmatter `description` capped at ≤500 characters for gate-skill-cr Step 6.6; exact macro tool names remain in SKILL body; `version` → `2026.3.30-6`.

---

## [2026.3.30-5] - 2026-03-30

### Changed

- **SKILL.md**: Semantically tightened frontmatter `description` (macro ↔ crypto framing, compact route matrix, full tool list); `version` → `2026.3.30-5`.

---

## [2026.3.30-4] - 2026-03-30

### Changed

- **SKILL.md**: Restored full frontmatter `description` per **PD / product** requirements; retains secondary routes to `gate-news-briefing` and `gate-news-eventexplain`. Exceeds gate-skill-cr Step 6.6 (500 characters) by intentional exception; `version` → `2026.3.30-4`.

---

## [2026.3.30-3] - 2026-03-30

### Changed

- **SKILL.md**: Frontmatter `description` adds secondary routes (gate-news-briefing, gate-news-eventexplain) within 500-char cap; `version` → `2026.3.30-3`.

---

## [2026.3.30-2] - 2026-03-30

### Changed

- **SKILL.md**: Frontmatter `description` shortened to ≤500 characters (gate-skill-cr Step 6.6); `version` → `2026.3.30-2`.

---

## [2026.3.30-1] - 2026-03-30

### Added

- **README.md**, **references/scenarios.md**: overview, capabilities, routing, architecture; scenario prompts aligned with `gate-info-addresstracker`.
- **Update scripts**: `scripts/update-skill.sh`, `scripts/update-skill.ps1` (same pilot implementation as `gate-info-addresstracker`).
- **SKILL.md**: **Per-skill updates** + full **Trigger update (with Execution)** (check / confirm / apply); frontmatter `version` / `updated` set to `2026.3.30-1` / `2026-03-30`.

### Changed

- **SKILL.md**: `### Required MCP Servers` table spacing aligned with `gate-info-addresstracker`.

### Audit

- Read-only; no trading or order execution.

---

## [2026.3.25-1] - 2026-03-25

### Added

- Skill: Macro-economic impact on crypto. Triggers: CPI/Fed/NFP and related vs BTC or broader market. Parallel MCP flow: economic calendar, macro indicator or macro summary (when no specific indicator), news search, market snapshot; decision logic for inflation/employment surprises; report template, routing, error handling, cross-skill routing, safety rules.
- SKILL.md: General Rules and MCP block aligned with `gate-info-addresstracker` / `gate-news-briefing`.
- MCP tools: info_macro_get_economic_calendar, info_macro_get_macro_indicator, info_macro_get_macro_summary, news_feed_search_news, info_marketsnapshot_get_market_snapshot.

### Audit

- Read-only; no trading or order execution.
