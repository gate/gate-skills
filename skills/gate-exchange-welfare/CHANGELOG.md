# Changelog

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.4.10-1] - 2026-04-10

### Changed

- Rewrote the SKILL frontmatter description to the standardized organization template with explicit `Use this skill whenever` and `Trigger phrases include` phrasing.
- Confirmed SKILL.md uses compliant Gate branding links and removed dependence on non-compliant `gate.io` wording in this skill bundle.
- Renamed `## Execution Workflow` to `## Execution` in `SKILL.md`.
- Renamed `## Exception Handling` to `## Error Handling` in `SKILL.md`.
- Renamed `references/gate-cli.md` sections to validator-aligned headings: `## Workflow`, `## Report Template`, and `## Error Handling`.
- Normalized `references/scenarios.md` to validator-required field names and added `**Context**:` to every scenario.
- No welfare business logic changes.

---

## [2026.4.3-1] - 2026-04-03

### Changed

- Added packaged `metadata.openclaw` credential declarations for ClawHub review consistency.
- Moved the mandatory runtime-rules reference into this skill bundle for publish-time auditability.
- Preserved the welfare phase-2 execution workflow introduced in `2026.4.2-1`.

---

## [2026.4.2-1] - 2026-04-02

### Updated

- Aligned the skill with the latest welfare Ex-Skill phase-2 requirement and the latest welfare OpenAPI surface.
- Expanded documented command coverage from 2 tools to 4 tools:
  - `gate-cli cex welfare identity`
  - `gate-cli cex welfare beginner-tasks`
  - `cex_welfare_claim_task` (no `gate-cli` mapping; see `gate-cli/cmd/cex/MCP_LEGACY_TOOL_RESOLUTION.md` §二)
  - `cex_welfare_claim_reward` (no `gate-cli` mapping; see `gate-cli/cmd/cex/MCP_LEGACY_TOOL_RESOLUTION.md` §二)
- Added new supported newcomer flows:
  - Claim a single task
  - Claim all currently claimable newcomer rewards
  - Complete-task guidance for KYC, first deposit, and first trade
- Updated newcomer task status handling from the old two-state simplification to the current phase-2 mapping:
  - `0` unclaimed
  - `1` claimed / in progress
  - `2` completed, reward claimable
  - `3` reward distributing
  - `4` completed / settled
  - `5` expired
- Added handling notes for dynamic download tasks (`task_type=23`, `status=0`) and M-select-N reward tasks (`has_m_n_task=true`).
- Replaced the outdated read-only positioning with the current query + write scope for task claim and reward claim.
- Updated the first-trade follow-up route to `gate-exchange-trading`.

### Files Updated

- `SKILL.md`
- `README.md`
- `references/gate-cli.md`
- `references/scenarios.md`
- `references/gate-cli-data-usage.md`
- `CHANGELOG.md`

---

## [2026.3.23-1] - 2026-03-23

### Changed

- Aligned documentation wording for ClawHub review.
- No execution workflow or business logic changes.

---

## [2026.3.19-4] - 2026-03-19

### Updated

- Updated Documented `gate-cli` calls: Replaced placeholders `XXX` with actual `gate-cli` command names
  - `gate-cli cex welfare identity`: Check user eligibility for new user benefits, return specific error codes
  - `gate-cli cex welfare beginner-tasks`: Get beginner guidance task list
- Enhanced error code handling logic: Added specific handling for all user types (error codes 1001-1008)
- Updated scenarios.md: Added complete test scenarios for various user types
- Optimized workflow description: Branch judgment based on actual API return codes

### Files Updated

- README.md: Updated tool descriptions and parameter explanations
- SKILL.md: Enhanced Documented `gate-cli` calls and error handling logic
- references/scenarios.md: Updated test scenarios, added new error code scenarios
- CHANGELOG.md: Added this update record

---

## [2026.3.19-3] - 2026-03-19

### Fixed

- SKILL.md Routing Rules: Added wiki Case2 original trigger phrase "how to claim new user rewards" to line 2.
- SKILL.md Step 1: Removed "(registration time, whether completed any trades, etc.)" — this description was self-inferred, wiki did not define new/existing user determination criteria.
- SKILL.md Safety Rule 4: Changed disclaimer text from "subject to actual receipt, final interpretation rights belong to Gate" to wiki-specified "Non-agent, non-institutional users and users with normal account status can complete tasks and claim rewards", consistent with response template.
- SKILL.md: Restored "Cross-Skill Integration" section (accidentally deleted when removing "Scope Description" last time).

---

## [2026.3.19-2] - 2026-03-19

### Removed

- SKILL.md: Removed "Scope Description (version 3/19)" descriptions of future version planned scenarios (claim individual tasks, complete individual tasks, claim task rewards), aligned with latest wiki documentation — these sub-scenarios have been removed from requirements document and are no longer kept as planned items.
- README.md: Removed "Currently Not Supported" list from Scope, corresponding to above.

---

## [2026.3.19-1] - 2026-03-19

### Added

- Skill: Welfare center new user task entry (version 3/19). Trigger phrases: what welfare, how to claim rewards, new user benefits, new user tasks, what welfare, new user benefits.
- SKILL.md: New/existing user determination process (Step 1 → branching); Case 1 existing user guidance (output Web/App redirect links); Case 2 new user task list (task title / subtitle / rewards / action buttons); response templates (with examples); exception handling (timeout, empty list, not logged in); Cross-Skill integration (deposit / spot trading / KYC / asset query); scope description (version 3/19 boundaries); Safety Rules.
- README.md, CHANGELOG.md, references/scenarios.md.
- Documented `gate-cli` calls used `XXX` placeholders, replaced with actual tool names in version 2026.3.19-4.

### Audit

- Read-only operations, does not execute task claiming or reward distribution.
- New/existing user identity determination is a prerequisite step, must not show new user task list to existing users.
- Must include disclaimer when displaying reward content: subject to actual receipt, final interpretation rights belong to Gate.

---

## [2026.3.18-6] - 2026-03-18

### Language Update

- **CONVERTED TO ENGLISH**: Updated all documentation and templates to English
  - Converted all response templates from Chinese to English
  - Updated all safety rules and instructions to English
  - Maintained emoji usage for visual clarity
  - Updated disclaimer text to English while preserving meaning
- Enhanced version description to reflect English-only documentation

### Files Updated

- SKILL.md: All templates and instructions converted to English
- references/scenarios.md: All examples converted to English  
- references/gate-cli-data-usage.md: Complete English documentation
- CHANGELOG.md: Updated with English language change record

---

## [2026.3.18-5] - 2026-03-18

### Critical Security Fix

- **FIXED MAJOR ISSUE**: Removed all hardcoded fake reward information from templates and examples
  - Removed fake examples like "10 points", "5 USDT trial voucher", "20 USDT bonus" from response templates
  - Added strict requirement to use only real `gate-cli` data from `gate-cli cex welfare beginner-tasks`
  - Enhanced Safety Rules with explicit prohibition against fabricated task information
- Updated response templates to use real `gate-cli` data fields: `task_name`, `task_desc`, `reward_num`, `reward_unit`, `status`
- Added detailed data mapping rules for proper `gate-cli` data extraction
- Enhanced disclaimer text to emphasize official website/App as final authority
- **LANGUAGE UPDATE**: Converted all templates and documentation to English for consistency

### Files Updated

- SKILL.md: Enhanced safety rules, updated templates, added data mapping instructions
- references/scenarios.md: Replaced fake examples with `gate-cli` data requirements  
- CHANGELOG.md: Added this critical security fix record
