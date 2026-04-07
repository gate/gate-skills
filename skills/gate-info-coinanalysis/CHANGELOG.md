# Changelog

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.4.6-1] - 2026-04-06

### Changed

- Packaged required runtime-rule references inside this skill so `SKILL.md` no longer points outside the published bundle.
- Removed repository-only maintenance guidance from `SKILL.md`.
- Excluded `README.md`, `CHANGELOG.md`, and `references/scenarios.md` from the published bundle to reduce non-runtime audit noise.
- No MCP workflow or business logic changes.

---

## [2026.4.3-1] - 2026-04-03

### Changed

- Added `.clawhubignore` so repository-only maintenance scripts are excluded from published skill bundles.
- Clarified in `SKILL.md` that local maintenance steps apply only to the repository copy.
- No MCP workflow or business logic changes.

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

## [2026.3.12-2] - 2026-03-12 — Initialization

### Added

- **Skill**: Coin comprehensive analysis. Trigger: single-coin analysis (e.g. "Analyze SOL", "How is BTC"). Tools: `info_coin_get_coin_info`, `info_marketsnapshot_get_market_snapshot`, `info_markettrend_get_technical_analysis`, `news_feed_search_news`, `news_feed_get_social_sentiment` (optional when no news MCP). Tool count: 5.
- **SKILL.md**: Workflow (5 tools in parallel + LLM aggregation), Decision Logic (RSI / volume / funding / fear_greed / unlock), Report Template (5 sections), Routing, Error Handling, Cross-Skill, Safety. Aligned with `docs/pd-vs-skills` and `docs/PD_VS_SKILLS_OPTIMIZATION_SUMMARY.md`.
- **README.md**, **references/scenarios.md**.

### Changed

- **info_marketsnapshot_get_market_snapshot**: Parameters use `timeframe="1d"` and `source="spot"` (aligned with PD; same as gate-info-coincompare and gate-news-listing).

### Audit

- Read-only; no trading or order execution.
