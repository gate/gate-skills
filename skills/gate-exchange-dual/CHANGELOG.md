# Changelog

## [2026.3.18-1] - 2026-03-18

### Changed
- Added new order status `PROCESSING` with display label "In Position"
- Removed Case 16 (KYC Not Met) — this business has no KYC restriction
- Removed all KYC-related logic and references from SKILL.md, subscription.md, and scenarios.md
- Compliance handling now covers Cases 15 (restricted region) and 17 (general compliance failure) only
- Removed timestamp-to-date conversion logic — timestamp fields are not accurately convertible
- All timestamp fields (`delivery_time`, `create_time`, `complete_time`, `delivery_timest`) are now omitted from user-facing output
- Removed Delivery (UTC) column from all report templates
- Removed Delivery Date from order confirmation templates

## [2026.3.17-1] - 2026-03-17

### Changed
- Restored `cex_earn_place_dual_order` to Available MCP Tools — order placement is now supported
- Cases 7-10 (subscription & order placement) now have full workflows via `references/subscription.md`
- Re-created `references/subscription.md` with order placement workflows (Cases 7-10) and compliance handling (Cases 15-17)
- Added Cases 15 (restricted region), 16 (KYC not met), 17 (general compliance failure) to routing rules
- Updated SKILL.md Execution section to include order placement and compliance routing
- Added order placement confirmation safety rule — explicit user confirmation required before calling `cex_earn_place_dual_order`
- Added error handling entries for `cex_earn_place_dual_order` compliance and balance errors
- Updated scenarios.md: Cases 7-10 now have full expected behaviors; added Scenarios 15-17
- Total cases: 13 → 16 (added Cases 15, 16, 17; case numbering skips 2)

## [2026.3.12-1] - 2026-03-12

### Changed
- Cases 7-10 (subscription & order placement) now reply "not supported yet" instead of calling order placement API
- Removed `cex_earn_place_dual_order` from Available MCP Tools (order placement not supported yet)
- Deleted `references/subscription.md` — Cases 7-10 no longer need a workflow, just a fixed reply
- Removed write operation safety rules and place_dual_order error handling entries
- Updated SKILL.md Execution section to include step for Cases 7-10 "not supported yet" reply
- Removed subscription.md links from product-query.md and settlement-assets.md
- Updated SKILL.md description to remove order placement references

## [2026.3.11-4] - 2026-03-11

### Changed
- Reorganized reference docs by functional area instead of API endpoint:
  - `product-query.md` (Cases 1, 3, 4, 5, 6) — product listing, eligibility, simulation, positions, settlement records
  - `subscription.md` (Cases 7, 8, 9, 10) — sell-high/buy-low orders, amount validation
  - `settlement-assets.md` (Cases 11, 12) — settlement result query, asset briefing
- Removed old per-API reference files: dual-investment-plan.md, dual-place-order.md, dual-orders.md, dual-balance.md
- Removed all API URLs from all .md files (endpoint paths, base URLs)
- Removed Method/Endpoint columns from MCP Tools tables
- Updated SKILL.md routing table to reference new functional md files
- Fixed README.md architecture diagram: 14 Cases → 13 Cases

## [2026.3.11-3] - 2026-03-11

### Changed
- Removed Case 2 (Filter by Coin) — merged into Case 3 via `currency` parameter
- Routing rules reduced from 14 to 13 cases (Case numbering preserved, skips 2)
- Simplified Case 1 description to "Browse dual product list"
- Updated Case 3 to use `currency` filter instead of `plan_id`
- Fixed Case 9 logic: amount > min_investment → proceed (was incorrectly `<`)
- Updated scenarios.md from 14 to 13 scenarios
- Updated dual-investment-plan.md: removed Case 2 workflow section

## [2026.3.11-2] - 2026-03-11

### Changed
- Expanded routing rules from 4 to 14 cases based on product requirement document
- Added `currency` parameter support to `cex_earn_list_dual_investment_plans`
- Added settlement simulation workflow (Case 4) with calculation formulas
- Split order placement into separate sell-high (Case 7) and buy-low (Case 8) workflows
- Added insufficient balance handling (Case 9) and minimum amount check (Case 10)
- Added ongoing position summary (Case 5) combining orders + balance
- Added settlement record queries (Cases 6, 11) with outcome interpretation
- Expanded Domain Knowledge with detailed settlement rules, Gate calculation examples, and key terminology
- Added Risk FAQ for currency conversion risk (Case 13) and missed gains (Case 14)
- Expanded scenarios.md from 10 to 14 scenarios matching all documented cases
- Added `status`, `from`, `to`, `investment_type` parameters to orders documentation

## [2026.3.11-1] - 2026-03-11

### Added
- Initial release of gate-exchange-dual skill
- Product discovery: list dual investment plans with APY, exercise price, delivery time
- Order placement: subscribe to dual plans with confirmation flow and settlement scenario explanation
- Order history: review past orders with settlement results and pagination
- Balance query: total holdings and accumulated interest in USDT and BTC

### Audit
- ✅ No internal API keys, domains, or proprietary data exposed
- ✅ All order placement requires explicit user confirmation
- ✅ Settlement scenarios (call/put outcomes) clearly explained before confirmation
- ✅ Risk disclaimers included: not principal-protected, may receive different currency
- ✅ No investment advice or price predictions provided
- ✅ Error messages are user-friendly without internal debug information
