# Changelog

## [2026.4.17-3] - 2026-04-17

- **Skill Dependencies:** `gate-cli` only; if missing, run `setup.sh` before any invocations; removed **Required gate-cli**.
- **Authentication:** document **`gate-cli config init`**; **Installation Check** now **Required: gate-cli**.
- Renamed **`references/gate-cli.md`** → **`references/gate-cli.md`**; `SKILL.md` and runtime rules updated accordingly.

## [2026.4.17-2] - 2026-04-17

- Added `setup.sh` for GateClaw/OpenClaw: installs `gate-cli` to `$HOME/.openclaw/skills/bin/gate-cli` (default **build** from [gate/gate-cli](https://github.com/gate/gate-cli); optional **release** tarball path aligned with upstream `install.sh`).
## [2026.4.17-1] - 2026-04-17

- Aligned `SKILL.md`, `references/gate-cli.md`, and `references/gate-runtime-rules.md`: `gate-cli` as the documented command contract, mapping truth source `gate-cli/cmd/cex/GATE_EXCHANGE_SKILLS_MCP_TO_GATE_CLI.md`, OpenClaw-friendly single-line `metadata`, and removal of duplicate `gate-cli cex spot order cancel` listings.
- Clarified cancel-all behavior (`order cancel` with `--all` per pair), fixed TP/SL safety wording to match price-trigger flows, and replaced stale `gate-cli` method names in verification steps with `gate-cli` read commands.

## [2026.4.3-1] - 2026-04-03

- Added ClawHub-compatible `metadata.openclaw` runtime credential declarations in `SKILL.md`.
- Replaced the package-external runtime-rules reference with a bundled `references/gate-runtime-rules.md` file so the published skill remains fully auditable.
- No execution workflow or business logic changes.

## [2026.3.23-1] - 2026-03-23

- Aligned documentation wording for ClawHub review.
- No execution workflow or business logic changes.

## [2026.3.12-1] - 2026-03-12

- Added 5 trigger-order and TP/SL automation scenarios (`Scenario 32-36`) in `references/scenarios.md`:
 - Conditional trigger buy placement from live ticker with computed trigger threshold
 - Dual TP/SL trigger placement after holdings validation
 - Single trigger order progress query (distance to trigger)
 - Batch cancellation for filtered BTC buy trigger orders
 - Single trigger order verification and cancellation by id
- Updated `SKILL.md` routing map from 31 to 36 cases and added trigger-order tool mapping:
 - `gate-cli cex spot price-trigger create`
 - `gate-cli cex spot price-trigger list`
 - `gate-cli cex spot price-trigger get`
 - `gate-cli cex spot price-trigger cancel`
 - `gate-cli cex spot price-trigger cancel-all`
- Updated confirmation/safety rules in `SKILL.md` to include trigger-order placement and TP/SL-style execution flows.
- Updated `README.md` capability list to include the new 5 trigger-order cases.

## [2026.3.10-1] - 2026-03-10

- Added new advanced scenario capability for batch order amendment (`Case 31` / `Scenario 31`):
 - Query open orders by pair (BTC buy orders)
 - Select up to 5 unfilled candidate orders
 - Compute +1% repricing per order
 - Require user verification, then execute one-shot batch amend via `gate-cli cex spot order batch-amend`
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
