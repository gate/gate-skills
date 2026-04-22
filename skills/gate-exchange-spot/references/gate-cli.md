---
name: gate-exchange-spot-gate-cli
version: "2026.4.17-2"
updated: "2026-04-17"
description: "gate-cli execution specification for Gate spot trading: order placement, trigger orders, query, amend/cancel, verification, and safety gates (aligned with gate-cli/cmd/cex/GATE_EXCHANGE_SKILLS_MCP_TO_GATE_CLI.md)."
---

# Gate Spot execution specification (`gate-cli`)

> Authoritative execution specification for `gate-cli cex`. `SKILL.md` handles intent routing; this file defines `gate-cli` contracts, pre-checks, and safety gates.

## 1. Scope and Trigger Boundaries

In scope:
- Spot buy/sell (market/limit)
- Trigger/conditional spot orders
- Spot order query, amend, cancel
- Balance/fill verification and fee estimation

Out of scope / route elsewhere:
- Futures intent -> `gate-cli cex futures`
- DEX swap intent -> `gate-dex-trade`
- Pure market analysis without trading action -> `gate-exchange-marketanalysis` or info skills

## 2. `gate-cli` availability and fallback

Detection:
1. The **`gate-cli`** binary must be installed and runnable (see `SKILL.md` → Skill Dependencies and `setup.sh` if needed).
2. Confirm the host can run the documented read path: `gate-cli cex spot market tickers` (writes only after the confirmation gate in §6).

Fallback:
- `gate-cli` missing: install per `SKILL.md` (`./setup.sh` after the `[ -x …/gate-cli ]` pre-check); then retry reads only until credentials are valid.
- Auth failure: follow runtime auth recovery and stop writes.
- API or endpoint degradation: downgrade to read-only draft/estimation mode.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- Configure credentials with **`gate-cli config init`** (interactive prompt for API key and secret, profiles, and defaults per [gate-cli](https://github.com/gate/gate-cli) docs). Alternatively use env vars / flags supported by `gate-cli` (`GATE_API_KEY`, `GATE_API_SECRET`, `--api-key`, `--api-secret`) without pasting secrets into chat.
- API key required for private endpoints.
- Minimal permissions: Spot:Write, Wallet:Read.
- On auth errors (`401`, permission denied): do not retry writes blindly; switch to guidance mode.

## 4. Optional resources

No bundled auxiliary resources are required for this skill.

## 5. Command specification (`gate-cli`)

### 5.1 Read commands

| Command | Required inputs | Key return fields | Common errors |
|---|---|---|---|
| `gate-cli cex spot account get` | optional `currency` | available/locked balances | auth, currency invalid |
| `gate-cli cex spot market currency` | `currency` | chain/tradability metadata | currency not found |
| `gate-cli cex spot market pair` | `currency_pair` | min size, precision, tradable status | pair invalid |
| `gate-cli cex spot market tickers` | optional pair | last, ask, bid, 24h stats | market unavailable |
| `gate-cli cex spot market orderbook` | `currency_pair` | asks/bids depth | depth unavailable |
| `gate-cli cex spot market candlesticks` | pair + interval | candles OHLCV | interval invalid |
| `gate-cli cex spot order list` | pair + status | open/finished orders | status filter mismatch |
| `gate-cli cex spot price-trigger get` | `order_id` | trigger detail/status | id not found |
| `gate-cli cex spot price-trigger list` | status/filter | trigger order list | empty result |
| `gate-cli cex spot order my-trades` | pair/time/order_id | fill list, fee, side | empty fills |
| `gate-cli cex spot account book` | filters/time | account ledger | range too large |
| `gate-cli cex spot account batch-fee` | `currency_pairs` | maker/taker fee rates | pair unsupported |
| `gate-cli cex wallet market trade-fee` | optional pair | account fee config | auth |

### 5.2 Write commands

| Command | Required inputs | Key return fields | Common errors |
|---|---|---|---|
| `gate-cli cex spot order buy` / `gate-cli cex spot order sell` | pair, side, amount, type | order id, status | min amount, precision, balance |
| `gate-cli cex spot order batch-create` | orders[] | per-order result | partial failures |
| `gate-cli cex spot price-trigger create` | trigger+put+market | trigger order id | trigger schema mismatch |
| `gate-cli cex spot order cancel` | `pair` and either `--id` (single order) or `--all` (all open on that pair) | cancel status / summary | already closed, none open |
| `gate-cli cex spot order batch-cancel` | pair, order_ids | batch cancel result | id mismatch |
| `gate-cli cex spot price-trigger cancel` | order_id | cancel status | already triggered |
| `gate-cli cex spot price-trigger cancel-all` | status/market/account | cancel summary | none open |
| `gate-cli cex spot order amend` | order_id + price/amount | amended order | non-open order |
| `gate-cli cex spot order batch-amend` | orders[] | batch amend result | invalid amend set |

## 6. Execution SOP (Non-Skippable)

### 6.1 Universal pre-check
1. Normalize pair format to `BASE_QUOTE`.
2. Validate tradability + min amount/precision.
3. Validate available balance (quote for market-buy, base for sell).

### 6.2 Mandatory confirmation gate for writes
Before any write (mutating `gate-cli` invocation), show an order draft with:
- pair, side, type
- amount meaning
- price basis (limit/market/trigger)
- estimated fill/cost and major risk

Only execute after explicit user confirmation in immediate previous turn.

### 6.3 Place/amend/cancel flow
1. Pre-check + draft
2. Confirm
3. Execute write
4. Verify using read commands: `gate-cli cex spot order list`, `gate-cli cex spot order my-trades`, and/or `gate-cli cex spot price-trigger get` as appropriate.

### 6.4 Multi-leg flow
For chained actions (sell->buy, buy->place TP-like trigger), require confirmation per leg.

## 7. Output Templates

```markdown
## Spot Order Draft
- Pair: {currency_pair}
- Side/Type: {side} {type}
- Amount: {amount} ({amount_semantics})
- Price: {price_or_market_basis}
- Estimated: {est_cost_or_receive}
- Risk: {risk_note}
Reply "Confirm order" to execute.
```

```markdown
## Spot Execution Result
- Status: {success_or_failed}
- Order ID: {order_id}
- Filled: {filled_amount}
- Avg Price: {avg_price}
- Fee: {fee}
- Next Check: {verification_hint}
```

## 8. Safety and Degradation Rules

1. Never place spot write orders without explicit final confirmation.
2. If pre-check fails (min amount, precision, balance), return blocking reason and suggested corrected input.
3. For trigger orders, echo trigger rule and trigger price before execution.
4. On API or command errors, preserve raw reason and do not fabricate success.
5. If auth is invalid, stop writes and route to `gate-cli config init` / credential recovery.
