# Changelog

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.4.7-1] - 2026-04-07

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

- **SKILL.md — Safety Rules**: Added items 7–8 only — age & eligibility (18+); data flow (host agent + read-only **Gate-Info** MCP tools listed in `SKILL.md`, plus documented skill-update URLs). No change to sub-scenarios, tool names, or routing semantics.

---

## [2026.4.1-1] - 2026-04-01

### Changed

- **info-news-runtime-rules.md**: Align version-check UX — do not surface technical failure details to end users; forbid auto-download of `update-skill.sh` / `update-skill.ps1` (manual copy from gate/gate-skills allowed); success paths (`update_available` / strict exit 3) still require per-skill confirmation before `apply`.
- **SKILL.md — Trigger update**: Document ClawHub packages may omit `update-skill.ps1`; agent rules for Bash vs PowerShell vs WSL/Git Bash vs silent skip; use the same shell family for Steps 1–2; do not run `apply` / `revoke-pending` when Step 1 is skipped; dual-arg `DEST` / `name` order with script auto-swap when only one path contains `SKILL.md`.
- **scripts/update-skill.sh**, **scripts/update-skill.ps1**: Strict `check` (`GATE_SKILL_CHECK_STRICT=1`, exit 3, `GATE_SKILL_CONFIRM_TOKEN`, `revoke-pending`); expanded default install-root resolution (Cursor, Codex, OpenClaw, `.agents`, Antigravity).

---

## [2026.3.30-5] - 2026-03-30

### Changed

- **SKILL.md**: Semantically tightened frontmatter `description` (scopes + Smart Money caveat without contradicting availability); `version` → `2026.3.30-5`.

---

## [2026.3.30-4] - 2026-03-30

### Changed

- **SKILL.md**: Restored full frontmatter `description` per **PD / product** requirements. Exceeds gate-skill-cr Step 6.6 (500 characters) by intentional exception; `version` → `2026.3.30-4`.

---

## [2026.3.30-2] - 2026-03-30

### Changed

- **SKILL.md**: Frontmatter `description` shortened to ≤500 characters (gate-skill-cr Step 6.6); `version` → `2026.3.30-2`.

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

- Skill: Token-level on-chain analysis (holders, activity, large transfers) plus coin info; **Known Limitations** documents no Smart Money / entity profile in this version. Routing to `gate-info-addresstracker` for address queries; scopes `holders` / `activity` / `transfers`; decision logic, report template, error handling, cross-skill routing, safety rules.
- SKILL.md: General Rules and MCP block aligned with `gate-info-addresstracker` / `gate-news-briefing`.
- MCP tools: info_onchain_get_token_onchain, info_coin_get_coin_info.

### Audit

- Read-only; no trading or order execution.
