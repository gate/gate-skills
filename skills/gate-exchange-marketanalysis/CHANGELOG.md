# Changelog

All notable changes to the gate-exchange-marketanalysis skill are documented here.

Format: date-based versioning (`YYYY.M.DD`). Each release includes a sequential suffix: `YYYY.M.DD-1`, `YYYY.M.DD-2`, etc.

---

## [2026.3.7-1] - 2026-03-07

### Scope

Case 8 adds **slippage simulation**: market-order fill vs order book, slippage reported as deviation from best ask (points and %). Spot and futures supported via same MCP call order as other cases. **Requires both currency pair and quote amount** from the user; no defaults — when either is missing, prompt the user instead of running the simulation.

### Added

- **Case 8: Slippage simulation** — market-order slippage vs best ask
  - Trigger: e.g. "slippage simulation", "market buy $10K, how much slippage?", "ADA_USDT slippage simulation"
  - **Spot:** `list_order_book` → `list_tickers`; **Futures:** `list_futures_order_book` → `list_futures_tickers`
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

- Case 8 uses Gate MCP only (list_order_book / list_futures_order_book, list_tickers / list_futures_tickers)
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

