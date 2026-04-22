# Gate Options Trading Scenarios

This document summarizes the 5 operation scenarios handled by the `gate-exchange-options` skill, and highlights the shared safety/confirmation rules.

## Case Overview

| Case | Scenario | Routed Reference |
|---|---|---|
| **1** | Place order (market/limit) | `references/place-order.md` |
| **2** | Place order (mark IV) | `references/place-order.md` |
| **3** | Close / reduce position | `references/close-position.md` |
| **4** | Cancel open orders | `references/cancel-order.md` |
| **5** | Amend open orders | `references/amend-order.md` |

## Shared Safety & Confirmation Rules (Global)

1. **Resolve to exact contract first** (before create/cancel/amend):
   - Contract format: `{underlying}-{expiration}-{strike}-{C|P}`
   - Always resolve `underlying / expiration / strike / call|put` to a single contract name before executing.
2. **Precision requirements**:
   - Price must respect `order_price_round` from `get_options_contract`.
   - Size must be an integer and must respect `order_size_min` from `get_options_contract` (floor when converting to contracts).
3. **All order-changing actions require user confirmation**:
   - **Place order**: show the final order summary and ask the user to reply `confirm` (or equivalent confirmation).
   - **Close / cancel / amend** (including single-order cancel): show the exact scope (contract/order_id + side/size/price where applicable) and ask for confirmation *before* calling the MCP tool.

## Cancel-All Key Note (Case 4)

For **“Cancel all / one-click cancel”**, the implementation must be **exhaustive across all underlyings**:

1. Call `list_options_underlyings` to get all underlyings.
2. For each underlying, call `list_options_orders(status=open, underlying=...)` (paginate / increase `limit` as needed) to fetch **all** open orders for that underlying.
3. Merge results and then cancel each order by `cancel_options_order(order_id)`.

If the backend supports **no-parameter batch cancel** (`gate-cli cex options order cancel-all`), that can be used as the preferred alternative; otherwise use the exhaustive fallback path above.

## Single Cancel Key Note (Case 4)

For **single cancel**, the flow is:
1. Identify the target order by `order_id`.
2. Show scope and ask for confirmation.
3. Call `gate-cli cex options order cancel`.

