# Changelog

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.4.1-2] - 2026-04-01

### Added

- **README.md**: Human-readable overview (capabilities, routing, architecture), runtime prerequisites for `update-skill` (Bash / PowerShell, sandbox permissions), outbound documentation URLs aligned with **General Rules** / `info-news-runtime-rules.md`, data flow & privacy, age & eligibility, marketplace manifest note, pointer to `references/scenarios.md`.
- **references/scenarios.md**: Verification scenarios (happy path, partial tool failure, cross-skill routing) consistent with routing tables and execution workflow in `SKILL.md`.

### Changed

- **SKILL.md — Safety Rules**: Added items 7–8 only — age & eligibility (18+); data flow (host agent + read-only **Gate-Info** MCP tools listed in `SKILL.md`, plus documented skill-update URLs). No change to sub-scenarios, tool names, or routing semantics.

---

## [2026.4.1-1] - 2026-04-01

### Changed

- **info-news-runtime-rules.md**: Align version-check UX — do not surface technical failure details to end users; forbid auto-download of `update-skill.sh` / `update-skill.ps1` (manual copy from gate/gate-skills allowed); success paths (`update_available` / strict exit 3) still require per-skill confirmation before `apply`.
- **SKILL.md — Trigger update**: Document ClawHub packages may omit `update-skill.ps1`; agent rules for Bash vs PowerShell vs WSL/Git Bash vs silent skip; use the same shell family for Steps 1–2; do not run `apply` / `revoke-pending` when Step 1 is skipped; dual-arg `DEST` / `name` order with script auto-swap when only one path contains `SKILL.md`.
- **scripts/update-skill.sh**, **scripts/update-skill.ps1**: Strict `check` (`GATE_SKILL_CHECK_STRICT=1`, exit 3, `GATE_SKILL_CONFIRM_TOKEN`, `revoke-pending`); expanded default install-root resolution (Cursor, Codex, OpenClaw, `.agents`, Antigravity).

---

## [2026.3.30-6] - 2026-03-30

### Changed

- **SKILL.md**: Frontmatter `description` capped at ≤500 characters for gate-skill-cr Step 6.6; full `info_platformmetrics_*` enumeration remains in SKILL body; `version` → `2026.3.30-6`.

---

## [2026.3.30-5] - 2026-03-30

### Changed

- **SKILL.md**: Semantically tightened frontmatter `description` (clearer intent → triggers → route → tools); `version` → `2026.3.30-5`.

---

## [2026.3.30-4] - 2026-03-30

### Changed

- **SKILL.md**: Restored full frontmatter `description` per **PD / product** requirements (complete triggers, tool list, routing). This exceeds gate-skill-cr Step 6.6 (500 characters) by intentional exception for merge review; `version` → `2026.3.30-4`.

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

- Skill: DeFi ecosystem analysis. Triggers: TVL rankings, single-protocol deep-dive, yield/APY, stablecoins, bridges, exchange reserves, liquidation heatmap. Seven sub-scenarios (A–G) with MCP tool tables; progressive loading for bridges and stablecoins; routing to `gate-info-coinanalysis` / `gate-info-marketoverview`; cross-skill routing, error handling, safety rules.
- SKILL.md: General Rules and MCP block aligned with `gate-info-addresstracker` / `gate-news-briefing`.
- MCP tools (scenario-dependent): info_platformmetrics_get_defi_overview, info_platformmetrics_search_platforms, info_platformmetrics_get_platform_info, info_platformmetrics_get_platform_history, info_platformmetrics_get_yield_pools, info_platformmetrics_get_stablecoin_info, info_platformmetrics_get_bridge_metrics, info_platformmetrics_get_exchange_reserves, info_platformmetrics_get_liquidation_heatmap, info_coin_get_coin_info.

### Audit

- Read-only; no trading or order execution.
