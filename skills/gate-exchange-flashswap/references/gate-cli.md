---
name: gate-exchange-flashswap-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for Flash Swap: pair capability query, quote preview, one-to-one and multi-currency order placement, and order tracking."
---

# Gate FlashSwap MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Supported pair query
- Swap preview/quote query
- Flash swap order placement (single and multi-currency forms)
- Order/history/detail query

Out of scope:
- Spot orderbook trading
- DEX on-chain swaps

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify Gate `gate-cli` supports `gate-cli cex flash-swap preview-v1` and `gate-cli cex flash-swap create-v1`.
2. Probe with pair list endpoint.

Fallback:
- If write endpoints unavailable, downgrade to query/preview only.
- If MCP/auth fails, return setup/auth guidance.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required for user order operations.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

### 5.1 Read commands

- `gate-cli cex flash-swap pairs`
- `gate-cli cex flash-swap preview-v1`
- `gate-cli cex flash-swap preview-one-to-many`
- `gate-cli cex flash-swap preview-many-to-one`
- `gate-cli cex flash-swap orders`
- `gate-cli cex flash-swap order`

### 5.2 Write commandss

- `gate-cli cex flash-swap create-v1`
- `gate-cli cex flash-swap create-one-to-many`
- `gate-cli cex flash-swap create-many-to-one`

## 6. Execution SOP (Non-Skippable)

1. Confirm swap intent and form (1:1 / 1:many / many:1).
2. Validate pair support and amount bounds.
3. Call corresponding preview endpoint first.
4. Present **Swap Draft** with expected exchange amounts and limits.
5. Require explicit confirmation before create endpoint.
6. Execute order and verify status with order query tool.

## 7. Output Templates

```markdown
## FlashSwap Draft
- Mode: {one_to_one_or_multi}
- Sell: {asset_and_amount}
- Buy: {asset_and_amount}
- Quote Summary: {preview_result}
- Risk: quote may change before execution.
Reply "Confirm swap" to execute.
```

```markdown
## FlashSwap Result
- Status: {success_or_failed}
- Order ID: {order_id}
- Filled: {filled_summary}
- Notes: {error_or_followup}
```

## 8. Safety and Degradation Rules

1. Always preview before create.
2. Never execute create endpoints without explicit immediate confirmation.
3. If preview/create mismatch occurs, re-preview and re-confirm.
4. Keep unsupported pairs and limit violations explicit.
5. Preserve API failures and avoid fabricated execution outcomes.
