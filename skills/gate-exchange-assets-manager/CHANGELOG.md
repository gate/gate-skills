# Changelog

## [2026.3.24-6] - 2026-03-24

### Changed

- **SKILL.md**: Documented that `cex_unified_get_unified_estimate_rate` returns **hourly** estimated unified-account borrow rates (per-currency string decimals; not annualized APR/APY). Added Domain Knowledge subsection, tool-inventory clarification, Common Misconceptions row, Action Draft / high-risk grading wording, and report template line for interest rate.

## [2026.3.24-5] - 2026-03-24

### Changed

- Renamed skill directory and `name` frontmatter from **`gate-exchange-asset-manager`** to **`gate-exchange-assets-manager`** (per request; naming-rule waivers as documented for this skill).

## [2026.3.24-4] - 2026-03-24

### Changed

- Renamed skill directory and `name` frontmatter from `gate-exchange-assetriskmanager` to **`gate-exchange-asset-manager`** (per product naming; template hyphen rules waived).
- Display titles updated to **Gate Account and Asset Manager** where applicable.

## [2026.3.24-3] - 2026-03-24

### Changed

- **General Rules**: Canonical block (STOP, tool-call guard, `exchange-runtime-rules.md` link) per gate-skill-cr; L2 intro paragraphs moved above `## General Rules`.
- **S4 Affiliate / rebate**: Documented that `cex_rebate_user_info` may be empty while `cex_rebate_partner_commissions_history` still supports reporting; `commissionAsset` (USDT, POINT), optional source dimensions (FUTURES, SPOT, TradFi, ALPHA); pagination and sum-by-asset rules for USDT/POINT totals; no fabricated lifetime totals; official totals via App/Web partner or rebate center; optional rebate-only follow-up pagination without mixing earn/staking.
- **Report template**, **Edge Case** table, **Common Misconceptions**, **Sub-Modules** and tool inventory for `cex_rebate_user_info` aligned with the above.
- **references/scenarios.md**: Expanded Scenario 7 and Scenario 12; added Scenario 16 (rebate totals with empty user_info and pagination).

## [2026.3.24-2] - 2026-03-24

### Added

- Documented **G. Write operation confirmation mechanism and safety rules**: strong confirmation · Action Draft, with **medium** vs **high** risk grading.
- Medium-risk writes (`set_unified_mode`, `set_user_leverage_currency_setting`, `set_unified_collateral`): single confirmation + risk note; **mode switch must disclose irreversibility**.
- High-risk write (`create_unified_loan`): Action Draft must include **amount, currency, interest rate** before user confirmation.
- Split write report templates in `SKILL.md` for medium-risk settings vs high-risk lending.
- Extended `references/scenarios.md` global gate and Scenario 9 to reference the grading table.

## [2026.3.24-1] - 2026-03-24

### Added

- Initialized the `gate-exchange-asset-manager` L2 skill directory (initial name `gate-exchange-assetriskmanager`) with full documentation structure.
- Added `SKILL.md` with 5-dimension signal overlay routing system (S1 Assets, S2 Risk, S3 Earn, S4 Affiliate, S5 Write Operations).
- Covers 58 deduplicated MCP tool calls (54 read + 4 write) across 7 L1 skills.
- Added 15 behaviour-oriented scenarios in `references/scenarios.md` covering asset panorama, margin risk, earn snapshots, affiliate queries, and write operations.
- Implemented mandatory Action Draft and user confirmation guardrails for all 4 write tools.
- Added external routing rules for out-of-scope intents (trading, research, earn product selection, sub-accounts).
- Added risk disclaimers for trading, leveraged products, and AI-generated output.
