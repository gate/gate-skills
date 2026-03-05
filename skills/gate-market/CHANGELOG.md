# Changelog

All notable changes to the Gate Market Intelligence skill are documented here.

Format: date-based versioning (`YYYY.M.DD`). Each release includes a sequential suffix: `YYYY.M.DD-1`, `YYYY.M.DD-2`, etc.

---

## [2026.3.5-1] - 2026-03-05

### Added
- Initial release (merged from `coin-deep-analysis` and `multi-coin-screener`)
- Routing-based SKILL.md with progressive document loading
- **Coin Deep Analysis module** (`references/coin-deep-analysis.md`):
  - Comprehensive single-coin analysis with 6-step data pipeline
  - Basic info retrieval (currency details, trading pair config)
  - K-line trend analysis (30-day daily candles) with support/resistance detection
  - Order book depth analysis with bid-ask ratio assessment
  - Recent trade analysis with whale activity detection
  - Funding rate sentiment analysis with crowding detection
  - Volume anomaly detection (3x 7-day average threshold)
  - Three quantitative risk flags (多头拥挤, 卖压较重, 异常放量)
- **Multi-Coin Screener module** (`references/multi-coin-screener.md`):
  - Dynamic multi-criteria coin screening (price change, volume, funding rate, price range, spread)
  - Automatic criteria parsing from natural language queries
  - Spot and futures data cross-referencing
  - Configurable Top-N ranking with customizable sort fields
- Cross-module synergy: screen → analyze pipeline

### Audit
- ✅ No external scripts or dependencies
- ✅ Uses Gate MCP tools only
- ✅ No credential handling
- ✅ Read-only data analysis, no trading operations
