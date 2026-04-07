# Changelog

## [2026.4.3-1] - 2026-04-03

- Added ClawHub-compatible `metadata.openclaw` runtime credential declarations in `SKILL.md`.
- Replaced the package-external runtime-rules reference with a bundled `references/gate-runtime-rules.md` file so the published skill remains fully auditable.
- No MCP workflow or business logic changes.

## [2026.3.23-1] - 2026-03-23

- Aligned documentation wording for ClawHub review.
- No MCP workflow or business logic changes.

## [2026.3.12-1] - 2026-03-12

- Added 5 trigger-order and TP/SL automation scenarios (`Scenario 32-36`) in `references/scenarios.md`:
    - Conditional trigger buy placement from live ticker with computed trigger threshold
    - Dual TP/SL trigger placement after holdings validation
    - Single trigger order progress query (distance to trigger)
    - Batch cancellation for filtered BTC buy trigger orders
    - Single trigger order verification and cancellation by id
- Updated `SKILL.md` routing map from 31 to 36 cases and added trigger-order tool mapping:
    - `cex_spot_create_spot_price_triggered_order`
    - `cex_spot_list_spot_price_triggered_orders`
    - `cex_spot_get_spot_price_triggered_order`
    - `cex_spot_cancel_spot_price_triggered_order`
    - `cex_spot_cancel_spot_price_triggered_order_list`
- Updated confirmation/safety rules in `SKILL.md` to include trigger-order placement and TP/SL-style execution flows.
- Updated `README.md` capability list to include the new 5 trigger-order cases.

## [2026.3.10-1] - 2026-03-10

- Added new advanced scenario capability for batch order amendment (`Case 31` / `Scenario 31`):
    - Query open orders by pair (BTC buy orders)
    - Select up to 5 unfilled candidate orders
    - Compute +1% repricing per order
    - Require user verification, then execute one-shot batch amend via `cex_spot_amend_spot_batch_orders`
- Updated `SKILL.md` routing/map to expand from 30 to 31 cases and include batch amend tool mapping.
- Updated `references/scenarios.md` from 30 to 31 scenarios with full template coverage for the new batch-amend case.
- Updated `README.md` advanced utility summary to include batch amend support.

## [2026.3.9-1] - 2026-03-09

- Expanded `references/scenarios.md` with 5 new advanced capability cases (`Scenario 26-30`):
    - Order filtering + precise batch cancellation by selected order ids
    - Market slippage simulation from order-book depth
    - One-click multi-asset batch buy placement
    - Multi-pair trading fee comparison
    - Account-book flow query + current balance reconciliation

## [2026.3.5-1] - 2026-03-05

- Initialized the `gate-exchange-spot` skill directory and documentation structure.
- Added `SKILL.md`, covering 25 spot trading and account operation scenarios.
- Added `references/scenarios.md`, with per-case examples for inputs, API calls, and decision logic.
