# Changelog

## [2026.4.8-1] - 2026-04-08

### Changed

- Added packaged `metadata.openclaw` credential declarations for ClawHub review consistency.
- Moved the mandatory runtime-rules reference into this skill bundle for publish-time auditability.
- Excluded non-runtime documentation from the published bundle.
- No execution workflow or business logic changes.

## [2026.3.25-1] - 2026-03-25

### Changed

- **SKILL.md**: `description` opening clause now highlights **TradFi** alongside other account lines; added `'TradFi'` to trigger phrases for routing alignment.

## [2026.3.12-3] - 2026-03-12

- Translated all Chinese content to English in scenarios.md, SKILL.md, and CHANGELOG.md.

## [2026.3.12-2] - 2026-03-12

- Removed deposit history and withdrawal history from skill scope.
- Removed `gate-cli cex wallet deposit list` and `gate-cli cex wallet deposit withdrawals` from `gate-cli` command mapping.
- Removed Scenario 8 (Deposit History) and Scenario 9 (Withdrawal History) from scenarios.

## [2026.3.12-1] - 2026-03-12

- Replaced REST API endpoints with Gate `gate-cli` command names: `gate-cli cex wallet balance total`, `gate-cli cex spot account get`, `gate-cli cex unified account get`, `gate-cli cex futures account get`, `gate-cli cex delivery account get`, `gate-cli cex options account get`, `gate-cli cex margin account list`, `gate-cli cex tradfi account assets`, `gate-cli cex earn dual balance`/`gate-cli cex earn dual orders`/`cex_earn_list_structured_orders` (no `gate-cli` mapping; see `gate-cli/cmd/cex/MCP_LEGACY_TOOL_RESOLUTION.md` §二), `gate-cli cex spot account book`.
- Added comprehensive cases from asset query skills (external) PDF specification.
- **Case 1**: Total asset query (GET /wallet/total_balance) with account/coin distribution, TradFi/payment isolation.
- **Case 2**: Specific currency query (concurrent multi-account aggregation).
- **Case 3**: Specific account + currency query (spot/unified).
- **Case 4**: Spot account query.
- **Case 5**: Futures account query (USDT/BTC perpetual, delivery, unified handling).
- **Case 6**: Trading account (unified) query with margin_mode branching.
- **Case 7**: Options account query.
- **Case 8**: Finance account query.
- **Case 9**: Alpha account query.
- **Case 12**: Isolated margin account query.
- **Case 15**: TradFi account query (USDx, isolated display).
- Added API mapping table, account name mapping, output templates.
- Added special scenario handling (small assets, unified migration, dust, TradFi, ST/delisted tokens).
- Added acceptance test queries for validation.
- Added recommendation engine (P1–P4) and transfer path restrictions.
- Expanded `references/scenarios.md` with full scenario templates and edge cases.

## [2026.3.11-1] - 2026-03-11

- Initialized the `gate-exchange-assets` skill directory and documentation structure.
- Added `SKILL.md`, covering 9 read-only asset and balance query scenarios.
- Added `references/scenarios.md`, with per-case examples for inputs, API calls, and decision logic.
- Read-only skill: total balance, spot balance, account valuation, account book.
