# Changelog

## [2026.3.27-2] - 2026-03-27

### Fixed

- SKILL.md: H1 aligned with skill id (`gate-exchange-pay — Gate Pay payment`, gate-skill-cr 6.7). Clarified Step 2 vs Step 1 (optional display does not replace payment-intent gate). Added concise **Risk of loss** bullet alongside existing irreversibility and disclaimers.
- `references/scenarios.md`: Scenario 1 **Expected Behavior** now parameterizes `order_id` / `amount` / `currency` across all three prompt shapes; added document-level **Scenario layout** note for **Unexpected Behavior** placement.
- `CHANGELOG.md`: **Compliance** note under `2026.3.26-1` corrected so it no longer implies H1/General Rules adjacency was true before `2026.3.27-1`.

## [2026.3.27-1] - 2026-03-27

### Fixed

- SKILL.md: `## General Rules` now immediately follows the H1 heading; introductory prose moved to `## Scope and audience` (gate-skill-cr Step 9.2).
- `references/scenarios.md`: Prompt Examples use English-only lines; Chinese receipts remain inside fenced code blocks. Context clarifies that live user wording may be non-English (gate-skill-cr Step 2.2–2.5).
- Compliance notes: reworded brand bullet to avoid spelling deprecated brand forms.
- Removed redundant `skills/gate-exchange-pay.zip` (duplicate of the skill directory; lowers bundle noise).
- Added `## Scenarios` pointer to `references/scenarios.md` in SKILL.md.

## [2026.3.26-1] - 2026-03-26

### Added

- Initial release of `gate-exchange-pay` skill for Gate Pay payment execution
- Payment workflow with 4 steps: readiness verification → intent confirmation → optional details display → execution + result output
- Localized receipt generation supporting user's conversation language (English, Chinese, etc.)
- Authorization validation with guidance flow for missing/expired authorization
- Error handling mapping for common payment failures (insufficient balance, expired order, invalid authorization, order not found)
- Domain knowledge section covering Gate Pay overview, authorization requirements, payment flow constraints
- `gate-cli` command integration: `cex_pay_create_ai_order_pay` (no `gate-cli` mapping; see `gate-cli/cmd/cex/MCP_LEGACY_TOOL_RESOLUTION.md` §二) for payment-account debiting
- Judgment logic table for routing decisions (execute, block, inform)
- Report template with success receipt and failure explanation formats
- Data privacy & collection statement compliant with Gate Privacy Policy
- Risk disclaimers: transaction irreversibility, regulatory compliance, merchant responsibility, AI output limitations
- Safety rules: confirmation requirements, authorization guards, duplicate payment prevention
- Security requirements: no data fabrication, input validation, no duplicate charges, no sensitive data exposure
- Standard architecture with complete workflow in single SKILL.md file
- Documentation: README.md with overview, core capabilities, usage examples, and support contact
- Initial scenario templates in `references/scenarios.md` covering happy path, error cases, and edge cases

### Compliance

- ✅ General Rules block includes canonical STOP line, runtime-rules link, and `gate-cli` allowlist wording (H1 adjacency finalized in [2026.3.27-1])
- ✅ References canonical `gate-runtime-rules.md` from gate-skills repository
- ✅ `gate-cli` command allowlist constraint included (only documented tools may be called)
- ✅ Brand compliance: use **Gate** / **Gate.com** naming only (no legacy domain-as-brand spelling)
- ✅ Naming convention: `gate-exchange-pay` matches `gate-{category}-{title}` pattern
- ✅ Required files: SKILL.md, README.md, CHANGELOG.md, references/scenarios.md
- ✅ Description includes "Use this skill whenever" and "Trigger phrases include"
- ✅ Age restriction statement (18+ with full civil capacity)
- ✅ Transaction irreversibility notice in Report Template
