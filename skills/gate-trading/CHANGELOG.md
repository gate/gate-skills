# Changelog

All notable changes to the Gate Trading Intelligence skill are documented here.

Format: date-based versioning (`YYYY.M.DD`). Each release includes a sequential suffix: `YYYY.M.DD-1`, `YYYY.M.DD-2`, etc.

---

## [2026.3.5-1] - 2026-03-05

### Added
- Initial release (merged from `basis-monitor`, `funding-rate-arbitrage`, and `liquidation-monitor`)
- Routing-based SKILL.md with progressive document loading
- **Basis Monitor module** (`references/basis-monitor.md`):
  - Spot vs futures basis calculation and monitoring
  - Single-coin deep basis analysis with premium index history
  - Multi-coin basis scan with Top-N ranking
  - Basis deviation analysis (Z-Score) and trend detection
  - Signal generation (positive basis widening, negative basis widening, basis mean reversion, extreme basis deviation, basis flip)
- **Funding Rate Arbitrage module** (`references/funding-rate-arbitrage.md`):
  - Full-market funding rate arbitrage opportunity scanning
  - Multi-step filtering pipeline (volume → rate → basis → depth)
  - Annualized return estimation with composite scoring
  - Directional arbitrage guidance (forward arbitrage / reverse arbitrage)
- **Liquidation Monitor module** (`references/liquidation-monitor.md`):
  - Real-time liquidation event monitoring
  - Abnormal liquidation spike detection (3x daily average threshold)
  - Directional squeeze analysis (long/short squeeze with 80% threshold)
  - Pin-bar / wick event detection with price recovery analysis
- Cross-module synergy and suggestion system

### Audit
- ✅ No external scripts or dependencies
- ✅ Uses Gate MCP tools only
- ✅ No credential handling
- ✅ Read-only data analysis, no trading operations
