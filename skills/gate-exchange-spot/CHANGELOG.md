# Changelog

## 2026.3.10-1 (2026-03-10)

- Added new advanced scenario capability for batch order amendment (`Case 31` / `Scenario 31`):
  - Query open orders by pair (BTC buy orders)
  - Select up to 5 unfilled candidate orders
  - Compute +1% repricing per order
  - Require user verification, then execute one-shot batch amend via `cex_spot_amend_spot_batch_orders`
- Updated `SKILL.md` routing/map to expand from 30 to 31 cases and include batch amend tool mapping.
- Updated `references/scenarios.md` from 30 to 31 scenarios with full template coverage for the new batch-amend case.
- Updated `README.md` advanced utility summary to include batch amend support.

## 2026.3.9-1 (2026-03-09)

- Expanded `references/scenarios.md` with 5 new advanced capability cases (`Scenario 26-30`):
  - Order filtering + precise batch cancellation by selected order ids
  - Market slippage simulation from order-book depth
  - One-click multi-asset batch buy placement
  - Multi-pair trading fee comparison
  - Account-book flow query + current balance reconciliation

## 2026.3.5-1 (2026-03-05)

- Initialized the `gate-exchange-spot` skill directory and documentation structure.
- Added `SKILL.md`, covering 25 spot trading and account operation scenarios.
- Added `references/scenarios.md`, with per-case examples for inputs, API calls, and decision logic.
