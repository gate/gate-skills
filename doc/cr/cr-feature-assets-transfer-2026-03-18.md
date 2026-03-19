# Branch Review Report

**Branch:** feature/assets-transfer
**Base:** master
**Files changed:** 4 (all new)
**Review date:** 2026-03-18

---

## Summary

| Category | Errors | Warnings | Info |
|----------|--------|----------|------|
| Language quality | 0 | 0 | 0 |
| Markdown syntax | 0 | 1 | 0 |
| Skill naming | 0 | 0 | 0 |
| Directory completeness | 0 | 0 | 0 |
| SKILL.md format | 0 | 0 | 0 |
| Brand compliance | 0 | 0 | 0 |
| SKILL.md content quality | 0 | 2 | 1 |
| Shared rules reference | 1 | 0 | 0 |
| CHANGELOG format | 0 | 2 | 0 |
| References integrity | 0 | 1 | 0 |
| Trading safety rules | 0 | 1 | 1 |
| **Total** | **1** | **7** | **2** |

### Verdict: FAIL

> 1 error must be resolved before merge.

---

## Findings

### Markdown syntax

| # | File | Line | Severity | Description | Suggestion |
|---|------|------|----------|-------------|------------|
| 1 | references/scenarios.md | 16-18 | Warning | Scenarios 1-8 use `##` headings but some (e.g. "## Scenario 1: Spot to Futures") appear under section headings also at `##` level ("## I. Main Account Transfers (1-4)"), causing sibling-level ambiguity. A strict hierarchy would use `###` for individual scenarios under `##` section headings. | Change individual scenario headings from `##` to `###` (e.g. `### Scenario 1: Spot to Futures`). |

### SKILL.md content quality

| # | File | Line | Severity | Description | Suggestion |
|---|------|------|----------|-------------|------------|
| 1 | SKILL.md | 53-58 | Warning | **MCP tool inventory incomplete.** The Tool Mapping table (line 53-58) only lists the write tool `cex_wallet_create_transfer`. However, the Transfer History Query section (line 319-331) references 5 additional read tools (`cex_spot_list_spot_account_book`, `cex_fx_list_futures_account_book`, `cex_delivery_list_delivery_account_book`, `cex_margin_list_margin_account_book`, `cex_options_list_options_account_book`). The Tool Mapping should list all tools used by the skill. | Add a consolidated Tool Mapping table covering both the write tool and all read/query tools used by the skill. |
| 2 | SKILL.md | 325-329 | Warning | **Incorrect MCP tool names.** Two tools in the Transfer History Query table do not match the actual MCP tool names: `cex_fx_list_futures_account_book` → should be `cex_fx_list_fx_account_book`; `cex_delivery_list_delivery_account_book` → should be `cex_dc_list_dc_account_book`. Per the naming convention, `futures` abbreviates to `fx` and `delivery` abbreviates to `dc`. | Correct to `cex_fx_list_fx_account_book` and `cex_dc_list_dc_account_book`. |
| 3 | SKILL.md | — | Info | **Report template missing.** No explicit report template section defining the standardized output format for Transfer Result Report, Transfer Draft, or error messages. The case sections describe output informally. | Consider adding a "## Report Templates" section with structured template definitions (similar to futures skill's `## Report template`). |

### Shared rules reference

| # | File | Line | Severity | Description | Suggestion |
|---|------|------|----------|-------------|------------|
| 1 | SKILL.md | — | Error | **Missing exchange-runtime-rules.md reference.** This is a `gate-exchange-*` skill but SKILL.md does not contain any reference or link to `exchange-runtime-rules.md`. Without this, the skill will skip shared auto-update check, MCP installation check, and authorization error handling logic. | Add a reference, e.g.: `→ See [exchange-runtime-rules.md](../exchange-runtime-rules.md) for shared runtime rules (auto-update, MCP installation check, auth error handling).` |

### CHANGELOG format

| # | File | Line | Severity | Description | Suggestion |
|---|------|------|----------|-------------|------------|
| 1 | CHANGELOG.md | 3 | Warning | **Version format mismatch.** CHANGELOG heading uses `## 2026.3.11-1 (2026-03-11)` but SKILL.md frontmatter version is `2026.3.16-2`. The latest CHANGELOG version should match the SKILL.md version. | Add a `## 2026.3.16-2 (2026-03-16)` entry to CHANGELOG.md describing Phase 1 refinements, or update SKILL.md version to match the CHANGELOG. |
| 2 | CHANGELOG.md | 5-8 | Warning | **CHANGELOG content describes sub-account scenarios** ("covering 8 transfer scenarios (main account, sub-account, status query)") but SKILL.md Phase 1 explicitly excludes sub-account transfers. The CHANGELOG entry is inconsistent with the actual SKILL.md scope. | Update CHANGELOG entry to accurately reflect Phase 1 scope: internal transfer only (11 cases), no main-sub transfers. |

### References integrity

| # | File | Line | Severity | Description | Suggestion |
|---|------|------|----------|-------------|------------|
| 1 | references/scenarios.md | 81-143 | Warning | **scenarios.md covers sub-account transfers (Scenarios 5-7, 8) but SKILL.md Phase 1 excludes them.** The scenarios file references tools `cex_wallet_create_sub_account_transfer`, `cex_wallet_create_sub_account_to_sub_account_transfer`, `cex_wallet_list_sub_account_balances`, and `cex_wallet_get_transfer_order_status` that are not in SKILL.md's tool mapping or case index. This creates a scope mismatch between SKILL.md and its reference file. | Either: (A) Add a clear "## Phase 2 (Future)" section header in scenarios.md to separate the sub-account scenarios from Phase 1, or (B) remove sub-account scenarios until Phase 2 is active. Also add `get_spot_accounts` / `get_futures_accounts` with correct MCP names to the reference. |

### Trading safety rules

| # | File | Line | Severity | Description | Suggestion |
|---|------|------|----------|-------------|------------|
| 1 | references/scenarios.md | 24, 40, 56, 89 | Warning | **Inconsistent tool names for balance checks in scenarios.md.** Uses `get_spot_accounts` and `get_futures_accounts` (non-MCP names) instead of proper MCP tool names like `cex_spot_get_spot_accounts` and `cex_fx_get_fx_accounts`. The SKILL.md uses correct MCP tool prefixes elsewhere but scenarios.md does not. | Update to correct MCP tool names: `cex_spot_get_spot_accounts`, `cex_fx_get_fx_accounts`. |
| 2 | SKILL.md | — | Info | **Stale confirmation handling mentioned but minimal.** case10 addresses ambiguous/stale confirmations well. No dedicated "staleness invalidation" rule (e.g. "confirmation expires if user sends ≥ N unrelated messages"). Current coverage is adequate for Phase 1. | No action required; consider enhancing in Phase 2. |

---

## Additional Observations (non-scoring)

1. **README.md vs SKILL.md scope mismatch**: README.md (line 5, 10-14) describes "main-to-sub, sub-to-main, sub-to-sub" as core capabilities, but SKILL.md explicitly scopes Phase 1 to internal transfers only. README should align with the current phase scope or clearly label future capabilities.

2. **README.md mentions "Query transfer status"** (line 14) as a core capability, but SKILL.md has no case or tool for status query (this is in scenarios.md as Scenario 8 only). Consider adding a note in README that status query is Phase 2.

3. **SKILL.md quality overall**: Well-structured with clear case index, Transfer Draft mandatory flow, and explicit confirmation rules. The error code table and API reference section are good additions.
