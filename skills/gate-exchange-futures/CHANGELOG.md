# Changelog

All notable changes to the Gate Futures Trading skill are documented here.

Format: date-based versioning (`YYYY.M.DD`). Each release includes a sequential suffix: `YYYY.M.DD-1`, `YYYY.M.DD-2`, etc.

---

## [2026.3.17-1] - 2026-03-17

### Changed

- **tp-sl.md**: Reformatted 7 scenarios to standard format (Context / Prompt Examples / Expected Behavior / Response Template); added `## Report Template`; renamed `## Step-by-step workflow` to `## Workflow`; added `Key data to extract` to all workflow steps
- **conditional.md**: Reformatted 5 scenarios to standard format; added `## Report Template`; renamed `## Step-by-step workflow` to `## Workflow`; added `Key data to extract` to all workflow steps
- **manage.md**: Reformatted 5 scenarios to standard format; added `## Workflow` (top-level) with `Key data to extract`; added `## Report Template` (list / cancel / amend templates)
- **SKILL.md**: Updated description to include "Use this skill whenever" and "Trigger phrases include"; added `## Domain Knowledge`
- **README.md**: Renamed `## Routing` to `## Architecture` with routing-architecture description

### Fixed

- **conditional.md**: Corrected MCP tool names `get_futures_contract` → `cex_fx_get_fx_contract`, `list_futures_order_book` → `cex_fx_get_fx_order_book`

---

## [2026.3.13-1] - 2026-03-13

### Merged from gate-futures-price-order

- **TP/SL** — `references/tp-sl.md`: set take-profit or stop-loss on an existing position; auto-selects trigger rule based on position side; supports full close and partial reduce-only; market or limit execution
- **Conditional Open** — `references/conditional.md`: open a new position when price reaches a level; full unit conversion (contracts, USDT cost, USDT value, base amount); supports breakout and dip-buy patterns; market or limit execution
- **Manage Triggers** — `references/manage.md`: list open/finished triggered orders, get order detail, cancel single order, cancel all orders, amend trigger price / execution price / size
- Added Modules E / F / G to `SKILL.md` routing and execution workflow
- Added **Order ID precision** rule (64-bit integer → always pass as string)
- Merged error table entries from gate-futures-price-order
- Removed gate-futures-price-order as a standalone skill

---

## [2026.3.5-1] - 2026-03-05

### Scope

This skill supports **four operations only**: open position, close position, cancel order, amend order. No market monitoring or arbitrage modules.

### Added

- **Open** — `references/open-position.md`: limit/market open long/short, U/contract conversion, cross/isolated mode, pre-order confirmation with leverage display
- **Close** — `references/close-position.md`: full close, partial close, reverse position
- **Cancel** — `references/cancel-order.md`: cancel single or batch orders
- **Amend** — `references/amend-order.md`: amend order price or size
- Routing-based SKILL.md with intent → reference mapping

### Audit

- Uses Gate MCP tools only
- Open/close/cancel/amend require user confirmation before execution where applicable
- No credential handling in this skill
