# Gate Options Close Position — Scenarios & Prompt Examples

Gate options close-position scenarios and expected behavior.

## API semantics

- **Full close**: `create_options_order`(contract, **close=true**, **size=0**, price, tif). Market = price `"0"`, tif `"ioc"`.
- **Partial close** (e.g. close half): `create_options_order`(contract, **reduce_only=true**, size = −N for long / +N for short, price, tif). Use market or limit as appropriate. Size must be integer; respect `order_size_min` from `get_options_contract`.

## Scenario 1: Close all (one contract or one position)

**Context**: User wants to fully close a specific option position (by contract / strike / expiry).

**Prompt Examples**:
- "Market close my BTC call, expiry 03/18, strike 70000"
- "Close my ETH put at market, expiry 03/20, strike 3000"
- "Full close my SOL call position"

**Expected Behavior**:
1. Call `list_options_positions`(underlying) to get positions; match by contract (or expiration + strike + call/put).
2. Show position and confirm: "Confirm close this position?"
3. After confirm, call `create_options_order`(contract, close=true, size=0, price="0", tif="ioc") for market, or with limit price and tif="gtc" for limit.
4. Output close result.

**Response Template**:
```
Close order submitted! As requested, you have closed your {long/short} position on {underlying} at {market/limit price}.
```

---

## Scenario 2: Partial close (specified size or close half)

**Context**: User wants to close part of the position.

**Prompt Examples**:
- "Close half of my ETH put at market, expiry 03/20, strike 3000"
- "Reduce 2 contracts of my BTC call, strike 70000"
- "Close half of my option position"

**Expected Behavior**:
1. Call `list_options_positions`(underlying) to get position size and side.
2. Compute close size: for "close half", close_size = floor(position_size / 2); for "reduce N", close_size = N. For long: submit size = −close_size; for short: size = +close_size.
3. Confirm: contract, close size, market vs limit.
4. After confirm, call `create_options_order`(contract, reduce_only=true, size=..., price, tif).
5. Output result.

**Response Template**:
```
Close order submitted! As requested, you have closed {size} of your {long/short} position on {underlying} at {market/limit price}.
```

---

## Scenario 3: Close all positions (one-click) or by condition

**Context**: User wants to close all option positions, or all profitable / all losing beyond a threshold.

**Prompt Examples**:
- "Market close all my option positions"
- "Close all profitable option positions"
- "Market close all options with loss over 50%"

**Expected Behavior**:
1. Call `list_options_positions`(underlying) or without filter to get all positions.
2. Filter by condition if needed (e.g. by PnL: profitable, or loss &gt; 50%).
3. Show list and confirm: "Confirm close all [filtered] positions?"
4. After confirm, for each position: full close with `create_options_order`(contract, close=true, size=0, ...). Or batch if API supports.
5. Output summary (e.g. "Closed N positions.").

**Response Template**:
```
Close order submitted! You have closed all {specified} positions. Total {N} position(s) closed.
```

---

## Scenario 4: Limit close at price

**Context**: User wants to close when price reaches a level (e.g. "when price hits 60000").

**Prompt Examples**:
- "Close all BTC call long when price hits 60000"
- "Limit close my ETH put at 0.05"

**Expected Behavior**:
1. Resolve position and contract.
2. Place limit close order: `create_options_order`(contract, close=true, size=0, price="60000" or "0.05", tif="gtc") or reduce_only with limit price as appropriate.
3. Confirm and submit.
4. Output: "Limit close order placed at {price}. Order will fill when market reaches that price."

---

## Notes

- "Close all profitable" / "close all loss &gt; 50%": filter positions by PnL from position data, then submit close orders for each (or batch if supported).
- When user says "close the one at 70k strike, expiry MM/DD" with no order/position list shown, list positions first, then match by strike/expiry or ask user to confirm which position.
