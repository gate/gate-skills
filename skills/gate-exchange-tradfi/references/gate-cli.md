---
name: gate-exchange-tradfi-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for TradFi module: symbols, market data, assets, order/position query and order/position mutations."
---

# Gate TradFi MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- TradFi symbols and market data query
- TradFi order/position/assets query
- TradFi order/place/update/cancel and position close/update operations

Out of scope:
- CEX spot/futures/DEX operations

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify `cex_tradfi_*` tools are available.
2. Probe with `gate-cli cex tradfi market symbols` or `gate-cli cex tradfi account assets`.

Fallback:
- If write operations unavailable, switch to read-only TradFi mode.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required.
- Mutation calls require strict auth and explicit confirmation.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

Namespace note:
- `cex_tradfi` is the base namespace prefix used by this module.
- `cex_tradfi_*` endpoints belong to the TradFi module namespace.

### Read tools
- `gate-cli cex tradfi market categories`
- `gate-cli cex tradfi account info`
- `gate-cli cex tradfi market symbols`
- `gate-cli cex tradfi market symbol`
- `gate-cli cex tradfi market ticker`
- `gate-cli cex tradfi market kline`
- `gate-cli cex tradfi order list`
- `gate-cli cex tradfi order history`
- `gate-cli cex tradfi position list`
- `gate-cli cex tradfi position history`
- `gate-cli cex tradfi account assets`

### Write tools
- `gate-cli cex tradfi order create`
- `gate-cli cex tradfi order update`
- `gate-cli cex tradfi order cancel`
- `gate-cli cex tradfi position update`
- `gate-cli cex tradfi position close`

## 6. Execution SOP (Non-Skippable)

1. Classify intent (query vs mutation).
2. For mutations, build action draft including symbol/side/volume/price and risk notes.
3. Require explicit confirmation.
4. Execute mutation call.
5. Verify via order/position query endpoints.

## 7. Output Templates

```markdown
## TradFi Action Draft
- Action: {place_or_update_or_cancel_or_close}
- Symbol: {symbol}
- Parameters: {key_params}
- Risk: market volatility and execution slippage.
Reply "Confirm action" to proceed.
```

```markdown
## TradFi Result
- Status: {success_or_failed}
- Object: {order_or_position_id}
- Updated State: {state_summary}
```

## 8. Safety and Degradation Rules

1. Never execute TradFi mutation calls without explicit immediate confirmation.
2. Keep symbol and volume precision as API expects.
3. If market data is stale/unavailable, warn before mutation.
4. Preserve backend error codes/messages.
5. Degrade to query-only mode when write permissions are missing.
