# Changelog

All notable changes to the gate-exchange-marketanalysis skill are documented here.

Format: date-based versioning (`YYYY.M.DD`). Each release includes a sequential suffix: `YYYY.M.DD-1`, `YYYY.M.DD-2`, etc.

---

## [2026.3.7-3] - 2026-03-07

### Fixed

- **Scenario 1.3** — Replaced abbreviated "order_book → candlesticks → tickers" with exact MCP tool names: `get_spot_order_book` → `get_spot_candlesticks` → `get_spot_tickers`.
- **Case 2 MCP Call Spec table** — Added backticks and "(futures)" label for `get_futures_tickers`, `get_futures_candlesticks`, `get_futures_order_book` for consistency.
- **MCP tool names reference** — Added explicit Gate MCP tool name list at top of `references/scenarios.md` (get_spot_*, get_futures_*, list_futures_funding_rate / list_futures_liq_orders / list_futures_premium_index).

---

## [2026.3.7-2] - 2026-03-07

### Fixed

- **Spot MCP tool names** — Align with Gate MCP (gate-exchange-spot): `list_order_book` → `get_spot_order_book`, `list_candlesticks` → `get_spot_candlesticks`, `list_tickers` → `get_spot_tickers`, `list_trades` → `get_spot_trades`. Updated in `references/scenarios.md`, SKILL.md, README.md, and CHANGELOG.
- **Futures market-data tool names** — Align with `get_*` pattern: `list_futures_order_book` → `get_futures_order_book`, `list_futures_tickers` → `get_futures_tickers`, `list_futures_candlesticks` → `get_futures_candlesticks`, `list_futures_trades` → `get_futures_trades`. `list_futures_funding_rate`, `list_futures_liq_orders`, `list_futures_premium_index` unchanged (list semantics).

---

## [2026.3.7-1] - 2026-03-07

### Scope

Case 8 adds **slippage simulation**: market-order fill vs order book, slippage reported as deviation from best ask (points and %). Spot and futures supported via same MCP call order as other cases. **Requires both currency pair and quote amount** from the user; no defaults — when either is missing, prompt the user instead of running the simulation.

### Added

- **Case 8: Slippage simulation** — market-order slippage vs best ask
  - Trigger: e.g. "slippage simulation", "market buy $10K, how much slippage?", "ADA_USDT slippage simulation"
  - **Spot:** `get_spot_order_book` → `get_spot_tickers`; **Futures:** `get_futures_order_book` → `get_futures_tickers`
  - Logic: walk ask ladder for quote amount Q; volume-weighted avg price; slippage = avg price − ask1 (points and %)
  - Output: simulation inputs, fill summary, slippage vs best ask, conclusion
- Scenario 8.1: spot slippage simulation (e.g. ADA_USDT / ETH market buy $10K)
- Scenario 8.2: futures slippage simulation (perpetual/contract market long)
- Scenario 8.3: missing pair or amount — prompt user (do not call MCP; ask for pair and/or quote amount; do not default to $10K)

### Changed

- **Pure English** — all Chinese trigger phrases and report templates in SKILL.md and `references/scenarios.md` replaced with English (e.g. "Slippage Simulation", "Best ask", "points", "Conclusion")
- **Versioning** — version and `updated` follow current date (`YYYY.M.DD` or `YYYY.M.DD-1`)
- **Case 8 required inputs** — currency pair and quote amount both required; if either missing, prompt user (no default pair, no default amount e.g. $10K). SKILL.md Execution step 3 and Domain Knowledge (Case 8) updated accordingly.

### Audit

- Case 8 uses Gate MCP only (get_spot_order_book / get_futures_order_book, get_spot_tickers / get_futures_tickers)
- No MCP calls when pair or amount is missing; user is prompted first
- Analysis is read-only; no trading operations

---

## [2026.3.5-1] - 2026-03-05

### Scope

This skill supports **market tape analysis only** (read-only): liquidity, momentum, liquidation, funding arbitrage, basis, manipulation risk, order book explainer. No trading operations.

### Added
- Initial release (market tape analysis, seven scenarios)
- Routing-based SKILL.md with document loading from `references/scenarios.md`
- **Seven analysis modules:** Liquidity, Momentum, Liquidation monitoring, Funding arbitrage, Basis, Manipulation risk, Order book explainer
- Smart spot/futures market detection (perpetual/contract keywords)
- MCP call order and Report Template defined in `references/scenarios.md`
- Domain knowledge and safety rules

### Audit

- Uses Gate MCP tools only; all analysis is read-only
- No trading operations or credential handling in this skill

