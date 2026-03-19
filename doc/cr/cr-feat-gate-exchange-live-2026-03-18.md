# Branch Review Report

**Branch:** feat/gate-exchange-live
**Base:** master
**Files changed:** 4 (all new)
**Review date:** 2026-03-18

---

## Summary

| Category | Errors | Warnings | Info |
|----------|--------|----------|------|
| Language quality | 0 | 1 | 0 |
| Markdown syntax | 0 | 0 | 0 |
| Skill naming | 0 | 0 | 0 |
| Directory completeness | 0 | 0 | 0 |
| SKILL.md format | 0 | 1 | 1 |
| Brand compliance | 1 | 0 | 0 |
| SKILL.md content quality | 0 | 1 | 0 |
| Shared rules reference | 0 | 0 | 1 |
| CHANGELOG format | 0 | 0 | 0 |
| References integrity | 0 | 0 | 0 |
| Trading safety rules | 0 | 0 | 0 |
| **Total** | **1** | **3** | **2** |

### Verdict: FAIL

> 1 error must be resolved before merge.

---

## Findings

### Brand compliance

| # | File | Line | Severity | Description | Suggestion |
|---|------|------|----------|-------------|------------|
| 1 | README.md | 5 | Error | **`Gate.io` used in non-URL context.** Text reads "…live streams and replays on Gate.io by business type…". Per brand guidelines, `Gate.io` as a brand name (not as a URL) should be replaced with `Gate` or `Gate.com`. Note: the `https://www.gate.io/live/…` URLs in SKILL.md (L68-69), README.md (L19), and scenarios.md (L18) are acceptable per Step 7.2 (URL exception). | Change README.md L5 from `"…on Gate.io by…"` to `"…on Gate by…"` or `"…on Gate.com by…"`. |

### Language quality

| # | File | Line | Severity | Description | Suggestion |
|---|------|------|----------|-------------|------------|
| 1 | SKILL.md | 5 | Warning | **Chinese–English mix in `description` field.** The frontmatter description contains Chinese trigger phrases: `"最热直播"`, `"行情分析直播间"`, `"给我5个SOL相关直播"`. While this may be intentional to support bilingual trigger matching, it creates a mixed-language description. | If bilingual triggers are intentional, add a brief note (e.g. `"Supports CN/EN triggers."`). Otherwise, use English-only trigger phrases in the frontmatter description and move Chinese examples to `references/scenarios.md`. |

### SKILL.md format

| # | File | Line | Severity | Description | Suggestion |
|---|------|------|----------|-------------|------------|
| 1 | SKILL.md | 6-8 | Warning | **Non-standard `metadata` block in frontmatter.** The frontmatter contains `metadata.owner_team` and `metadata.domain` fields which are not part of the standard required fields (`name`, `version`, `updated`, `description`). These do not cause an error but are non-standard. | If team ownership metadata is desired, consider standardizing across all skills or documenting the convention. No action strictly required. |
| 2 | SKILL.md | 11 | Info | **H1 heading differs from skill name.** H1 is `# Gate Info Liveroom Location — Live & Replay Listing` while name is `gate-info-liveroomlocation`. The heading includes a descriptive subtitle with em dash. Per Step 6.5, the heading should "match or relate to the skill name" — this qualifies as "related". Acceptable. | No action required. |

### SKILL.md content quality

| # | File | Line | Severity | Description | Suggestion |
|---|------|------|----------|-------------|------------|
| 1 | SKILL.md | — | Warning | **No MCP tool mapping table.** This skill uses a direct HTTP API (`GET /live/gate_ai/tag_coin_live_replay`) instead of MCP tools. The SKILL.md correctly documents the API endpoint but does not have an MCP Tool Mapping section. Per Step 8.1, skills that call MCP tools should have a tool inventory — this skill is exempt since it uses HTTP directly. However, it would benefit from explicitly noting the MCP tool name if one exists (e.g. `cex_square_list_live_replay`), or confirming "No MCP tool — direct HTTP only." | Add a brief note: `## MCP Tool Mapping` → `This skill uses HTTP API directly. MCP tool: cex_square_list_live_replay (if available).` This helps future maintainers understand MCP availability. |

### Shared rules reference

| # | File | Line | Severity | Description | Suggestion |
|---|------|------|----------|-------------|------------|
| 1 | SKILL.md | — | Info | **No `exchange-runtime-rules.md` reference.** This is a `gate-info-*` skill (not `gate-exchange-*`), so Step 9 shared rules reference is **not required**. The skill correctly omits it. | No action required. This is a `gate-info-*` product line and is exempt from Step 9. |

---

## Detailed Step-by-Step Analysis

### Step 2 — Language quality: 1 Warning
- All files are primarily English ✓
- No grammar/fluency issues ✓
- Chinese–English mix in SKILL.md frontmatter `description` field (Warning — see findings)
- scenarios.md contains Chinese prompt examples (L9-10, L29-31, L48-50, L70) — these are intentional bilingual trigger examples within the scenarios file, acceptable for a bilingual skill

### Step 3 — Markdown syntax: PASS
- Heading hierarchy correct: `#` → `##` → `###` throughout ✓
- All code blocks properly closed ✓
- All tables formatted correctly ✓
- No broken links ✓
- No trailing whitespace issues ✓

### Step 4 — Skill naming: PASS
- Directory name: `gate-info-liveroomlocation` ✓
- Pattern: `gate-{product-line}-{sub-line}` → `gate-info-liveroomlocation` ✓
- All lowercase ✓
- Prefix `gate-` ✓

### Step 5 — Directory completeness: PASS
- `SKILL.md` ✓
- `CHANGELOG.md` ✓
- `references/scenarios.md` ✓

### Step 6 — SKILL.md format: 1 Warning, 1 Info
- YAML frontmatter with required fields ✓
- `name: gate-info-liveroomlocation` matches directory ✓
- `version: "2026.3.13-1"` follows format ✓
- `description` non-empty (within 500 chars) ✓
- H1 heading present ✓
- Substantive body ✓
- Non-standard `metadata` block (Warning)

### Step 7 — Brand compliance: 1 Error
- README.md L5: `Gate.io` used as brand name (not URL) → **Error**
- SKILL.md L68-69, README.md L19, scenarios.md L18: `https://www.gate.io/…` URLs → acceptable (URL exception)

### Step 8 — Content quality: 1 Warning
- No `cex_` MCP tools used; skill uses HTTP API directly
- Workflow section present (L15-81) ✓
- Judgment logic summary present (L73-81) ✓
- Report template present (L83-86) ✓
- Error/edge case handling: restricted region check, empty list, API error ✓
- MCP tool mapping absent (Warning — recommend noting MCP availability)

### Step 9 — Shared rules reference: N/A (Info)
This is `gate-info-*`, not `gate-exchange-*`. Exempt from Step 9.

### Step 10 — CHANGELOG format: PASS
- Title `# Changelog` ✓
- Version entry `## [2026.3.13-1] - 2026-03-13` ✓
- Version matches SKILL.md frontmatter `2026.3.13-1` ✓
- Content describes additions and includes audit notes ✓
- Reverse chronological (single entry) ✓

### Step 11 — References integrity: PASS
- `references/scenarios.md` exists and referenced from SKILL.md ✓
- No dangling references ✓
- No orphaned files ✓
- scenarios.md has substantive content (5 scenarios) ✓

### Step 12 — Trading safety rules: N/A (PASS)
No write operations. Skill is read-only (HTTP GET only). Exempt.

---

## Overall Assessment

A clean and focused skill with a well-defined single-API workflow. The parameter mapping table, judgment logic summary, and bilingual scenario coverage are strong. The only blocking issue is the brand name `Gate.io` usage in README.md.
