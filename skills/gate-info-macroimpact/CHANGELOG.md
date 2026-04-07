# Changelog

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.4.6-1] - 2026-04-06

### Changed

- Packaged required runtime-rule references inside this skill so `SKILL.md` no longer points outside the published bundle.
- Removed repository-only maintenance guidance and update-flow references from the published skill instructions.
- Excluded `README.md`, `CHANGELOG.md`, and `references/scenarios.md` from the published bundle to reduce non-runtime audit noise.
- No MCP workflow or business logic changes.

---

## [2026.4.3-1] - 2026-04-03

### Changed

- Added `.clawhubignore` so repository-only maintenance scripts are excluded from published skill bundles.
- Clarified in `SKILL.md` that local maintenance steps apply only to the repository copy.
- No MCP workflow or business logic changes.

---

## [2026.4.1-2] - 2026-04-01

### Added

- **README.md**: Human-readable overview (capabilities, routing, architecture), runtime prerequisites for `update-skill` (Bash / PowerShell, sandbox permissions), outbound documentation URLs aligned with **General Rules** / `info-news-runtime-rules.md`, data flow & privacy, age & eligibility, marketplace manifest note, pointer to `references/scenarios.md`.
- **references/scenarios.md**: Verification scenarios (happy path, partial tool failure, cross-skill routing) consistent with routing tables and execution workflow in `SKILL.md`.

### Changed

- **SKILL.md — Safety Rules**: Added items 7–8 only — age & eligibility (18+); data flow (host agent + read-only **Gate-Info** and **Gate-News** MCP tools listed in `SKILL.md`, plus documented skill-update URLs). No change to sub-scenarios, tool names, or routing semantics.

---

## [2026.4.1-1] - 2026-04-01

### Changed

- **info-news-runtime-rules.md**: Align version-check UX — do not surface technical failure details to end users; forbid auto-download of `update-skill.sh` / `update-skill.ps1` (manual copy from gate/gate-skills allowed); success paths (`update_available` / strict exit 3) still require per-skill confirmation before `apply`.
- **SKILL.md — Trigger update**: Document ClawHub packages may omit `update-skill.ps1`; agent rules for Bash vs PowerShell vs WSL/Git Bash vs silent skip; use the same shell family for Steps 1–2; do not run `apply` / `revoke-pending` when Step 1 is skipped; dual-arg `DEST` / `name` order with script auto-swap when only one path contains `SKILL.md`.
- **scripts/update-skill.sh**, **scripts/update-skill.ps1**: Strict `check` (`GATE_SKILL_CHECK_STRICT=1`, exit 3, `GATE_SKILL_CONFIRM_TOKEN`, `revoke-pending`); expanded default install-root resolution (Cursor, Codex, OpenClaw, `.agents`, Antigravity).

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
