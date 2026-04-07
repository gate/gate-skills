# Gate Options Amend Order — Scenarios & Prompt Examples

Gate options amend-order scenarios and expected behavior. Use MCP `cex_options_amend_options_order` to update open order price or size.

## Scenario 1: Change order price

**Context**: User wants to change the limit price of an open option order.

**Prompt Examples**:
- "Change my BTC call order at 70k strike, expiry 03/18, price to 0.05"
- "Update the limit price of my SOL put order to 0.02"
- "Change price to 0.05 for my BTC call at 70000 strike"

**Expected Behavior**:
1. Call `list_options_orders`(status=open, underlying) to find the order matching strike, expiry, call/put (and side if needed).
2. If multiple match: list them and ask user to choose (e.g. by number or order id).
3. Confirm: current price → new price. New price must respect `order_price_round` from `get_options_contract`.
4. Call `cex_options_amend_options_order`(order_id, contract, price=new_price).
5. Output result.

**Response Template**:
```
Amend confirmed! Your open order on {underlying} has been updated: price is now {new price}. Waiting for fill.
```

---

## Scenario 2: Change order size

**Context**: User wants to change the size of an open option order (e.g. halve it).

**Prompt Examples**:
- "Halve the size of my SOL put at strike 70, expiry 03/20"
- "Halve the size of my SOL call at strike 70, expiry 03/20"
- "Change my order size from 5 to 3 contracts"

**Expected Behavior**:
1. Call `list_options_orders`(status=open, underlying) to find the order.
2. If multiple match: ask user to choose.
3. Confirm: current size → new size. New size must be integer and ≥ `order_size_min` from `get_options_contract`.
4. Call `cex_options_amend_options_order`(order_id, contract, size=new_size).
5. Output result.

**Response Template**:
```
Amend confirmed! Your open order on {underlying} has been updated: size is now {new size}. Waiting for fill.
```

---

## Scenario 3: Change both price and size

**Context**: User wants to change both price and size of an open order.

**Expected Behavior**: Same as above; confirm both new price and new size; call `cex_options_amend_options_order`(order_id, contract, price=new_price, size=new_size); output "price is now {new price}, size is now {new size}."

---

## Notes

- New price/size must respect contract `order_price_round` and `order_size_min` from `get_options_contract`.
- If only price is changed, report "price is now {new price}"; if only size, "size is now {new size}"; if both, include both in the output.
