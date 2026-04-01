# Changelog

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.4.1-2] - 2026-04-01

### Fixed

- **SKILL.md — MCP Dependencies**: **Gate-Info** added to **Required MCP Servers** and **Installation Check** alongside Gate-News. The skill already calls `info_marketsnapshot_get_market_snapshot` and `info_onchain_get_token_onchain` (Gate-Info); the document previously listed only Gate-News, which misstated install/runtime dependencies. Resolves QC daily validation item: MCP declaration must match tools in **MCP Tools Used**.

---

## [2026.4.1-1] - 2026-04-01

### Changed

- **info-news-runtime-rules.md**: Align version-check UX — do not surface technical failure details to end users; forbid auto-download of `update-skill.sh` / `update-skill.ps1` (manual copy from gate/gate-skills allowed); success paths (`update_available` / strict exit 3) still require per-skill confirmation before `apply`.
- **SKILL.md — Trigger update**: Document ClawHub packages may omit `update-skill.ps1`; agent rules for Bash vs PowerShell vs WSL/Git Bash vs silent skip; use the same shell family for Steps 1–2; do not run `apply` / `revoke-pending` when Step 1 is skipped; dual-arg `DEST` / `name` order with script auto-swap when only one path contains `SKILL.md`.
- **scripts/update-skill.sh**, **scripts/update-skill.ps1**: Strict `check` (`GATE_SKILL_CHECK_STRICT=1`, exit 3, `GATE_SKILL_CONFIRM_TOKEN`, `revoke-pending`); expanded default install-root resolution (Cursor, Codex, OpenClaw, `.agents`, Antigravity).

---

## [2026.3.25-1] - 2026-03-25

### Added

- **Runtime rules**: SKILL.md references shared `info-news-runtime-rules.md` with `gate-runtime-rules.md`; **Trigger update** (check / confirm / apply) and **Routing Rules** aligned to the gate-info / gate-news rollout.
- **Update scripts**: `scripts/update-skill.sh`, `scripts/update-skill.ps1` (same pilot implementation as sibling Info/News skills).

---

## [2026.3.12-1] - 2026-03-12

### Added

- Skill: Event attribution and explanation. Trigger: why did X pump/dump, what caused this move. Tools: news_events_get_latest_events, info_marketsnapshot_get_market_snapshot, news_events_get_event_detail, info_onchain_get_token_onchain, news_feed_search_news. Multi-step workflow with event-found vs expand-news branch.
- SKILL.md: Workflow (Phase 1 parallel, Step 4a/4b branch), Report Template (attribution + no-event template), Reasoning Logic, Error Handling, Cross-Skill, Safety. Synced from docs/pd-vs-skills/skills/gate-news-eventexplain; tool names in underscore form.
- README.md, references/scenarios.md.

### Audit

- Read-only; no trading or order execution. No definitive causal claims; no follow-on price predictions.
