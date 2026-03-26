# Changelog

## [2026.3.17-4] - 2026-03-17

### Fixed

- Corrected order fields in `order-management.md` based on API response verification:
  - `amount` → `currency_amount` (token quantity field)
  - `fee` → `gas_fee` + `transaction_fee` (two separate fee fields)
  - `fail_reason` → `failed_reason` (correct spelling)
  - Removed `finish_time` (field does not exist in API response)
- Reverted tool name back to `cex_alpha_list_alpha_orders` (plural) based on actual MCP tool file verification (Lark doc was incorrect)
- Clarified `gas_mode="speed"` as default in quote workflow for both buy and sell operations

### Added

- Added "Resolve Currency Symbol" step in `trading-buy.md` and `trading-sell.md` to handle fuzzy token name matching:
  - Try exact match first, then fuzzy search if no result
  - Present candidate list for user selection when multiple tokens match
  - Inform user when no matching token is found
- Added Scenario 14 "Batch Sell All Holdings" in `trading-sell.md` to handle selling all tokens in the account:
  - List all sellable holdings and ask for confirmation first
  - Process tokens one by one sequentially (NOT all at once)
  - Confirm each individual token sale before executing
  - Present summary after all tokens are processed

## [2026.3.17-3] - 2026-03-17

### Fixed

- Corrected all field names to match official Gate Alpha API documentation (snake_case):
  - `market-viewing.md`: `marketCap` → `market_cap`
  - `token-discovery.md`: `amountPrecision` → `amount_precision`
  - `account-holdings.md`: `tokenAddress` → `token_address`
- Corrected tool name: `cex_alpha_list_alpha_orders` → `cex_alpha_list_alpha_order` (per Lark doc binding)
- Rewrote `SKILL.md` API Field Naming Conventions section with complete field list per endpoint

## [2026.3.17-2] - 2026-03-17

### Fixed

- Fixed field name mismatches between documentation and actual API responses:
  - `market-viewing.md`: Changed `change_percentage` → `change`, `quote_volume` → `volume`, removed `high_24h`/`low_24h`/`base_volume`, added `marketCap`
  - `token-discovery.md`: Changed `price_precision` → `precision`, `amount_precision` → `amountPrecision`, `trade_status` → `status`, added `name` field
  - `account-holdings.md`: Changed `address` → `tokenAddress`
  - `trading-buy.md` / `trading-sell.md`: Added note that API returns `gasMode` as `"1"`/`"2"` instead of `"speed"`/`"custom"`
- Added note about chain name case inconsistency (`SOLANA` vs `solana`) between different endpoints
- Added note about empty query results returning `[{}, {}]` instead of `[]`
- Updated `SKILL.md` Domain Knowledge section with API field naming conventions

## [2026.3.17-1] - 2026-03-17

### Added

- Added `references/trading-buy.md` covering 3 scenarios (Cases 8-10): market buy, custom slippage buy, buy and track result.
- Added `references/trading-sell.md` covering 3 scenarios (Cases 11-13): full position sell, partial sell, sell and track result.
- Added `references/account-book.md` covering 2 scenarios (Cases 16-17): recent transaction history, specific time-range history.
- Added `references/order-management.md` covering 4 scenarios (Cases 18-21): check order status, historical buy orders, historical sell orders, time-range order search.

### Changed

- Updated `SKILL.md`: expanded from 3 modules to 7 modules, added 5 new MCP tools (quote, place_order, get_order, list_orders, account_book), added trading domain knowledge, expanded error handling and safety rules.
- Updated `README.md` with new architecture, tools, and usage examples.

## [2026.3.13-1] - 2026-03-13

### Added

- Initialized `gate-exchange-alpha` skill with routing architecture.
- Added `SKILL.md` with routing rules, MCP tool mapping, domain knowledge, and error handling.
- Added `references/token-discovery.md` covering 5 scenarios (Cases 1-5): browse currencies, filter by chain, filter by launch platform, look up by contract address, view token details.
- Added `references/market-viewing.md` covering 2 scenarios (Cases 6-7): view all market tickers, view specific token price.
- Added `references/account-holdings.md` covering 2 scenarios (Cases 14-15): view holdings, calculate portfolio market value.
- Added `README.md` with overview, architecture, and usage examples.
