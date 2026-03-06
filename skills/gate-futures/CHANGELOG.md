# Changelog

All notable changes to the Gate.io Futures Trading skill are documented here.

Format: date-based versioning (`YYYY.M.DD`). Each release includes a sequential suffix: `YYYY.M.DD-1`, `YYYY.M.DD-2`, etc.

---

## [2026.3.5-1] - 2026-03-05

### Scope

This skill supports **four operations only**: 开仓 (open position), 平仓 (close position), 撤单 (cancel order), 改单 (amend order). No market monitoring or arbitrage modules.

### Added

- **开仓 (Open)** — `references/open-position.md`: limit/market open long/short, U/张 conversion, cross/isolated mode, pre-order confirmation with leverage display
- **平仓 (Close)** — `references/close-position.md`: full close, partial close, reverse position
- **撤单 (Cancel)** — `references/cancel-order.md`: cancel single or batch orders
- **改单 (Amend)** — `references/amend-order.md`: amend order price or size
- Routing-based SKILL.md with intent → reference mapping

### Audit

- Uses Gate MCP tools only
- Open/close/cancel/amend require user confirmation before execution where applicable
- No credential handling in this skill
