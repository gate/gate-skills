# Gate Options Cancel Order — Scenarios & Prompt Examples

Gate options cancel-order scenarios and expected behavior.

## API

- **Single cancel**: `cancel_options_order`(order_id). Corresponds to `DELETE /options/orders/{order_id}`.
- **Batch cancel**: `DELETE /options/orders` with optional query params: `underlying`, `contract`, `side` (ask/bid). "One-click cancel" = batch with no params; "cancel all SOL call buy" = underlying=SOL_USDT, side=bid (or equivalent).

## Scenario 1: List orders then choose to cancel (recommended)

**Context**: User wants to cancel but does not know order ID; need to list open orders first.

**Prompt Examples**:
- "Cancel my option order"
- "What open option orders do I have"
- "Show my option orders"
- "Cancel order" (no ID)

**Expected Behavior**:
1. Detect no order_id → query mode.
2. Call `list_options_orders`(status=open, underlying or contract if known).
3. Show order list with numbered options (contract, side, size, price, strike, expiry).
4. Wait for user selection (e.g. "1", "1,2", "all").
5. Confirm scope: "Confirm cancel {selected} order(s)?"
6. Cancel based on selection.

**Response Template** (list phase):
```
You have {N} open option order(s):

| # | Contract   | Side | Size | Price | Strike | Expiry  |
|---|------------|------|------|-------|--------|---------|
| 1 | BTC_USDT-...-70000-C | Buy  | 1    | 0.05  | 70000  | 03/18   |
| 2 | ...        | Sell | 2    | ...   | ...    | ...     |

Which order(s) do you want to cancel?
- Enter number(s), e.g. "1" or "1,2"
- Enter "all" to cancel all
```

---

## Scenario 2: Cancel by strike / expiry / contract

**Context**: User identifies the order by contract details (strike, expiry, call/put) rather than order ID.

**Prompt Examples**:
- "Cancel the BTC call order at 70k strike, expiry 03/18"
- "Cancel all SOL call buy orders"
- "Cancel all SOL put buy orders"
- "Cancel the one at strike 70000, expiry 03/18"

**Expected Behavior**:
1. Call `list_options_orders`(status=open, underlying).
2. Filter by user intent: specific strike/expiry/call-put, or side (buy/sell). If "cancel all SOL call buy", filter by underlying (SOL_USDT), side = bid (buy).
3. Show matching orders and confirm: "Confirm cancel these N order(s)?"
4. For each: `cancel_options_order`(order_id), or use batch cancel if API supports (e.g. by underlying + side).
5. Output result.

**Response Template**:
```
Cancel successful! Your {specified/all} open order(s) have been cancelled. A total of {N} order(s) were cancelled, releasing {xxx} USDT margin.
```
If the API does not return released margin, omit "releasing {xxx} USDT margin" or show "—".

---

## Scenario 3: Cancel all orders (one-click)

**Context**: User wants to cancel all open option orders.

**Prompt Examples**:
- "Cancel all open orders"
- "One-click cancel"
- "Cancel all option orders"
- "All" (after seeing the list)

**Expected Behavior**:
1. Confirm: "Confirm cancel all open option orders?"
2. **Must cover all underlyings before cancel-all**:
   - Call `list_options_underlyings` to get all underlyings (e.g. `BTC_USDT`, `ETH_USDT`, …).
   - For each underlying, call `list_options_orders` with `status=open` and `underlying=<...>` (paginate and/or increase `limit` if supported) to fetch **all** open orders under that underlying.
   - Merge all returned open orders across underlyings.
3. Cancel:
   - If the API supports **batch cancel with no params** ("one-click cancel"), prefer calling batch cancel (no params), or batch cancel scoped to one underlying when appropriate.
   - Otherwise, for each open order, call `cancel_options_order(order_id)`.
4. Output result.

**Response Template**:
```
Cancel successful! All open order(s) have been cancelled. A total of {N} order(s) were cancelled, releasing {xxx} USDT margin.
```

---

## Notes

- If user says "cancel the one at 70k strike, expiry MM/DD" with no list shown, list open orders first, then match by strike/expiry or ask user to confirm which order.
- Some backends may not return all open orders in a single `list_options_orders` call without scoping by `underlying` and/or paginating. For "cancel all", ensure the implementation is **exhaustive** (enumerate underlyings + paginate), unless a no-param batch cancel is available and used.

---

## Scenario 4: Cancel by order_id (single cancel)

**Context**: User provides an explicit order ID and wants to cancel exactly that order.

**Prompt Examples**:
- "Cancel order 1234567890"
- "Revoke option order id=987654321"

**Expected Behavior**:
1. Confirm: "Confirm cancel order {order_id}?"
2. Call `cancel_options_order(order_id)`.
3. Output result.

**Response Template**:
```
Cancel successful! Order {order_id} has been cancelled.
```
