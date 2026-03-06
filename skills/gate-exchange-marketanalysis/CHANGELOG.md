# Changelog

All notable changes to the gate-exchange-MarketAnalysis skill are documented here.

Format: date-based versioning (`YYYY.M.DD`). Each release includes a sequential suffix: `YYYY.M.DD-1`, `YYYY.M.DD-2`, etc.

---

## [2026.3.5-8] - 2026-03-05

### Changed
- **English-only documentation:** Removed all Chinese content from SKILL.md, README.md, CHANGELOG.md, and references/scenarios.md. Documentation is now full English.

---

## [2026.3.5-1] - 2026-03-05

### Added
- Initial release (market tape analysis, seven scenarios)
- Routing-based SKILL.md with document loading from `references/scenarios.md`
- **Seven analysis modules:** Liquidity, Momentum, Liquidation monitoring, Funding arbitrage, Basis, Manipulation risk, Order book explainer
- Smart spot/futures market detection (perpetual/contract keywords)
- MCP call order and Report Template defined in `references/scenarios.md`
- Domain knowledge and safety rules
