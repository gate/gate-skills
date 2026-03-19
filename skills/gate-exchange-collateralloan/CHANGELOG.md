# Changelog

## [2026.3.18-3] - 2026-03-18

### Changed

- **Order list/detail — no time in user replies**: When showing loan orders or order detail, **never** include any time/date/timestamp/maturity fields or relative-time paraphrases; allowed: order_id, status, amounts, collateral, LTV, fixed term as **7d/30d** label only. If the user asks for dates, direct them to Gate app/web—do not echo API times. Updated SKILL.md, `mcl-mcp-tools.md`, **scenarios.md**.

## [2026.3.18-2] - 2026-03-18

### Changed

- **Order list/detail presentation**: Default user-facing summary **hides time fields** (borrow_time, maturity, timestamps); show only order_id, status, amounts, LTV unless the user asks for dates/times. Updated SKILL.md, `mcl-mcp-tools.md`, **scenarios.md** (new Scenario 6).

## [2026.3.18-1] - 2026-03-18

### Changed

- **MCP-only reference**: Removed REST/API mapping doc. Added **`references/mcl-mcp-tools.md`** (MCP tool arguments and JSON payloads only). Deleted **`references/mcl-api.md`**.
- **SKILL.md / README / scenarios**: All pointers updated to `mcl-mcp-tools.md`; removed Method/Path columns. Aligned tool names with Gate MCP: **`cex_mcl_repay_multi_collateral_loan`**, **`order`** / **`repay_loan`** / **`collateral_adjust`** JSON parameters; list orders uses **`order_type`** / **`sort`** per MCP (not REST-only `status`).
- **Frontmatter**: `description` includes **Use this skill whenever** and **Trigger phrases include** (skill-validator).

## [2026.3.16-1] - 2026-03-16

### Changed

- Added **Workflow**, **Judgment Logic Summary**, and **Report Template** sections to SKILL.md to satisfy validator requirements.
- Added tester-friendly Scenario blocks (User Prompt + Tools) in references/scenarios.md.

---

## [2026.3.12-3] - 2026-03-12

### Fixed

- **Fixed loan 400 errors**: Fixed-term orders require **fixed_rate**; missing it can cause 400. Updates:
  - **mcl-api.md** §2: fixed_type required for fixed loans; fixed_rate conditionally required when order_type is fixed; must use rate_7d/rate_30d from fix_rate API.
  - **scenarios.md** Scenario 2: call `cex_mcl_get_multi_collateral_fix_rate` first, use rate_7d (7D) or rate_30d (30D) for fixed_rate; if fix_rate fails or currency not supported, stop and show an error message (no submit).
  - **SKILL.md**: Fixed loan flow requires fixed_rate; Domain Knowledge and Error Handling updated accordingly.

---

## [2026.3.12-2] - 2026-03-12

### Changed

- **Format aligned with gate-exchange-simpleearn**: SKILL.md restructured with Prerequisites, MCP Tools, Routing Rules, Execution, Domain Knowledge, Safety Rules, Error Handling, and Prompt Examples reference.
- README.md: Overview, Core Capabilities, Architecture, MCP Tools, Quick Start, Safety & Compliance, Related skills.
- references/scenarios.md: Intro mapping table; per-scenario Context / Prompt Examples / Expected Behavior / API & MCP table; auth failure note at end.

### Audit

- ✅ All write operations (create order, repay, add/redeem collateral) require user confirmation before submit.
- ✅ Auth failure: do not expose credentials; prompt to configure Gate CEX API Key with multi-collateral loan permission.

---

## [2026.3.11-1] - 2026-03-11

### Added

- Initial **gate-exchange-collateralloan** skill (multi-collateral loan phase 1).
- Five cases: create current loan, create fixed loan, repay, add collateral, redeem collateral; based on REST API `/loan/multi_collateral/orders`, `repay`, `mortgage`. **No MCP yet**; workflow and cases reserved for MCP mapping; keep confirmation gates and output templates.
- API reference: [Gate API v4 Multi-Collateral Loan](https://www.gate.com/docs/developers/apiv4/zh_CN/#multi-collateral-loan). API section and scenarios marked as “reserved for MCP mapping”.
- Added `SKILL.md`, `README.md`, `references/scenarios.md` (four-file layout). All write operations require user confirmation; success/failure output templates in scenarios.

### Changed

- Skill content language switched to English (SKILL, README, CHANGELOG, scenarios).

### Audit

- ✅ All create-order, repay, add/redeem collateral are write operations; must show draft and get explicit user confirmation before calling.
- ✅ On auth failure, do not expose credentials; only prompt to set API Key or MCP.
