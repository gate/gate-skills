# Gate Futures Open Position — Scenarios & Prompt Examples

Gate futures open-position scenarios and expected behavior.

## Unit Conversion

When the user does not specify size in **contracts**, convert to **contracts** before placing the order.

There are **two distinct intents** when user specifies USDT:

| User phrase | Intent | Type |
|-------------|--------|------|
| "spend 100U long" / "invest 100 USDT long" | **USDT cost** — 100 USDT is the margin cost | Cost-based |
| "long 100U worth" / "open 100 USDT value position" | **USDT value** — 100 USDT is the notional value | Value-based |
| "long 0.1 BTC" | **Base amount** — direct base conversion | Base |

### Data sources

- `cex_fx_get_fx_contract(settle, contract)` → `quanto_multiplier`, `order_size_min`
- `cex_fx_get_fx_order_book(settle, contract, limit=1)` → `asks[0].p` (best ask), `bids[0].p` (best bid)
- Position query → current leverage for the contract+side (**use this leverage in USDT cost formulas; do not change or override it unless the user explicitly specified a different leverage**)

### USDT Cost → contracts (margin-based)

The user specifies how much margin (USDT) to invest. The formula accounts for fees and leverage.

| Direction | Formula | `order_price` |
|-----------|---------|---------------|
| **Open long** | `contracts = cost / (0.0015 + 1/leverage) / quanto_multiplier / order_price` | Limit: specified price; Market: best ask |
| **Open short** | `contracts = cost / (0.0015 + 1.00075/leverage) / quanto_multiplier / max(order_price, best_bid)` | Limit: specified price; Market: best bid |
| **Close long** | `contracts = cost / (0.0015 + 1.00075/leverage) / quanto_multiplier / max(order_price, best_bid)` | Limit: specified price; Market: best bid. Use the **long position's leverage**. |
| **Close short** | `contracts = cost / (0.0015 + 1/leverage) / quanto_multiplier / order_price` | Limit: specified price; Market: best ask. Use the **short position's leverage**. |

### USDT Value → contracts (notional-based)

The user specifies the notional value of the position in USDT.

| Direction | Formula | `price` |
|-----------|---------|---------|
| **Buy / Open long / Close short** | `contracts = usdt_value / price / quanto_multiplier` | Limit: specified price; Market: best ask |
| **Sell / Open short / Close long** | `contracts = usdt_value / max(best_bid, order_price) / quanto_multiplier` | Limit: max(specified price, best bid); Market: best bid |

### Base amount → contracts

| User unit | Formula |
|-----------|---------|
| **Base (e.g. BTC, ETH)** | `contracts = base_amount / quanto_multiplier` |

### Precision

- Resulting contracts must satisfy `order_size_min` and size precision from the contract; if below minimum, prompt the user.
- Always **floor** (truncate) the result to an integer (contracts are whole numbers).

## Position and leverage query (dual vs single mode)

**Tool `get_position` does not exist.** Use the following by account mode (from **`cex_fx_get_fx_accounts(settle)`** → **`position_mode`** or **`in_dual_mode`**):

- **Dual mode** (`position_mode === "dual"` or `in_dual_mode === true`): use **`cex_fx_list_fx_positions(settle, holding=true)`** or **`cex_fx_get_fx_dual_position(settle, contract)`** for position/leverage. Do **not** use `cex_fx_get_fx_position` in dual mode (API returns an array and causes parse error).
- **Single mode**: use **`cex_fx_get_fx_position(settle, contract)`** for position/leverage.

Same rule for **margin mode** (`pos_margin_mode`): get it from the position returned by the above query.

## Pre-Order Confirmation

**Before opening**, show the **final order summary** and only call `cex_fx_create_fx_order` after user confirmation.

- **Leverage**: Query current leverage for **contract + side** via the **position query** above (dual: `cex_fx_list_fx_positions` or `cex_fx_get_fx_dual_position`; single: `cex_fx_get_fx_position`).
- **Summary**: Contract, side (long/short), size (contracts), price (limit or “market”), margin mode (cross/isolated), **leverage**, estimated margin and liquidation price; for market orders also mention slippage risk. **Do not** add text about mark price, limit protection, or suggesting to adjust price.
- **Confirmation**: *“Please confirm the above and reply ‘confirm’ to place the order.”* Only after the user confirms (e.g. “confirm”, “yes”, “place”) execute the order.

## Margin Mode Switch API (cex_fx_update_fx_dual_position_cross_mode)

**Switch margin mode only when the user explicitly requests it**: switch to isolated only when user asks for isolated (e.g. "isolated"); switch to cross only when user asks for cross (e.g. "cross"). **If the user does not specify margin mode, do not switch — place the order in the current margin mode.**

When switching cross/isolated margin, call MCP **`cex_fx_update_fx_dual_position_cross_mode`** with **`settle`**, **`contract`**, **`mode`**:

- **`mode`**: `"CROSS"` = cross margin, `"ISOLATED"` = isolated margin (required; do not use a `cross` boolean).
- **`settle`**: Settlement currency, e.g. `"usdt"`.
- **`contract`**: Contract name, e.g. `"BTC_USDT"`.

Example: cross `cex_fx_update_fx_dual_position_cross_mode(settle="usdt", contract="BTC_USDT", mode="CROSS")`; isolated `cex_fx_update_fx_dual_position_cross_mode(settle="usdt", contract="BTC_USDT", mode="ISOLATED")`.

## Leverage Before Order

If the **user specifies leverage** and it **differs from current** for that contract/side, **first** set leverage, **then** call `cex_fx_create_fx_order`. Use **`cex_fx_update_fx_dual_position_leverage(settle, contract, leverage)`** in dual mode; **`cex_fx_update_fx_position_leverage(settle, contract, leverage)`** in single mode. Do not use `cex_fx_update_fx_position_leverage` in dual mode (API returns array and causes parse error). *Note:* In dual mode, `cex_fx_update_fx_dual_position_leverage` may return an MCP parse error (e.g. "expected record, received array") even when leverage was set successfully; if the call was made, proceed to place the order.

**If the user does not specify leverage, do not change it.** Use the current leverage from the position query for all calculations (including the USDT cost formula). Do not default to any standard leverage value (e.g. 10x). This is especially important when the user already has a position — changing leverage without explicit request would alter the existing position's risk parameters.

## Margin Mode vs Position Mode

**Switch to isolated only when the user explicitly requests isolated; switch to cross only when the user explicitly requests cross.** If the user does not specify margin mode, **do not switch — place the order in the current margin mode.**

When **target margin mode** is explicitly requested and **differs from** the **current margin mode** of the existing position for that contract, check **position mode** first:

- **Position mode**: Call MCP **`cex_fx_get_fx_accounts(settle)`**. From **`position_mode`**: `single` = single position mode, `dual` = dual (hedge) position mode.
- **Margin mode**: From **position** — use the **position query** per dual/single mode above and read `pos_margin_mode` (cross/isolated).

**Branch logic** (target margin mode ≠ current position margin mode and contract already has a position):

| position_mode | Position mode | Behavior | Prompt |
|---------------|---------------|----------|--------|
| `single` | Single position | Do not interrupt | Prompt: "You already have a {currency} position; switching margin mode will apply to this position too. Continue?" (e.g. currency from contract: BTC_USDT → BTC). After user confirms, switch and continue opening. |
| `dual` | Dual position | **Interrupt** | Prompt: "Please close the position first, then open a new one." Do not switch margin mode or place the order. |

## Scenario 1: Limit order open long (cross margin)

**Context**: User wants to open long on BTC_USDT at a limit price, cross margin.

**Prompt Examples**:
- "Open long 1 contract BTC_USDT at 65000"
- "BTC_USDT perpetual, cross margin, long 1 contract at 65000"
- "limit buy 1 BTC_USDT futures at 65000"

**Expected Behavior**:
1. Fetch contract via `cex_fx_get_fx_contract(settle="usdt", contract="BTC_USDT")`
2. Switch to cross via `cex_fx_update_fx_dual_position_cross_mode(settle="usdt", contract="BTC_USDT", mode="CROSS")`
3. Query leverage via **position query** (dual: `cex_fx_list_fx_positions` or `cex_fx_get_fx_dual_position`; single: `cex_fx_get_fx_position`) for contract + long side
4. **Show final order summary** (contract, side, size, price, mode, **leverage**, estimated liq/margin), ask user to confirm
5. After confirm, place order via `cex_fx_create_fx_order(settle="usdt", contract="BTC_USDT", size="1", price="65000", tif="gtc")`
6. Verify position via **position query** (dual: `cex_fx_list_fx_positions(holding=true)` or `cex_fx_get_fx_dual_position`; single: `cex_fx_get_fx_position`)
7. Output open result

**Response Template**:
```
Order placed.

Order ID: 123456789
Contract: BTC_USDT
Side: long (buy)
Size: 1 contract
Price: 65000 USDT
Status: open (resting)
Mode: cross
Leverage: 10x (from position query)
```

---

## Scenario 2: Market order open short isolated 10x

**Context**: User wants to open short at market, isolated margin, 10x leverage.

**Prompt Examples**:
- "Market short 2 contracts ETH_USDT, isolated 10x"
- "ETH_USDT isolated 10x, market short 2"
- "market sell 2 ETH_USDT futures with 10x leverage"

**Expected Behavior**:
1. Fetch contract via `cex_fx_get_fx_contract(settle="usdt", contract="ETH_USDT")`
2. Switch to isolated via `cex_fx_update_fx_dual_position_cross_mode(settle="usdt", contract="ETH_USDT", mode="ISOLATED")`
3. Set leverage via **`cex_fx_update_fx_dual_position_leverage`** (dual) or **`cex_fx_update_fx_position_leverage`** (single): `(settle="usdt", contract="ETH_USDT", leverage="10")`
4. **Show final order summary** (contract, side, size, market, mode, leverage, estimated liq/margin), ask user to confirm
5. After confirm, place market order via `cex_fx_create_fx_order(settle="usdt", contract="ETH_USDT", size="-2", price="0", tif="ioc")`
6. Verify position via **position query** (dual: `cex_fx_list_fx_positions(holding=true)` or `cex_fx_get_fx_dual_position`; single: `cex_fx_get_fx_position`)
7. Output fill and position info

**Response Template**:
```
Market short filled.

Order ID: 123456790
Contract: ETH_USDT
Side: short (sell)
Size: 2 contracts
Avg fill: 3500.50 USDT
Status: finished
Mode: isolated 10x

Current position:
- Size: -2 contracts
- Entry: 3500.50
- Liq price: 3850.00
```

---

## Scenario 3: FOK order (fill or kill)

**Context**: User wants FOK so the order either fills completely or is cancelled.

**Prompt Examples**:
- "FOK limit buy 1 BTC_USDT at 65000"
- "BTC_USDT FOK, long 1 at 65000"
- "fill or kill buy 1 BTC_USDT at 65000"

**Expected Behavior**:
1. Fetch contract via `cex_fx_get_fx_contract(settle="usdt", contract="BTC_USDT")`
2. Place FOK via `cex_fx_create_fx_order(settle="usdt", contract="BTC_USDT", size="1", price="65000", tif="fok")`
3. If depth insufficient, return ORDER_FOK error
4. If success, output full fill result

**Error Case Response**:
```
FOK order did not fill.

Reason: Insufficient depth to fill entirely.
Suggestions:
1. Reduce size
2. Adjust price
3. Use GTC or IOC instead
```

---

## Scenario 4: Price outside limit protection

**Context**: User’s price is too far from market and hits exchange limit protection.

**Prompt Examples**:
- "BTC_USDT long at 100000" (market ~65000)

**Expected Behavior**:
1. Do **not** pre-compute valid range from contract `order_price_deviate` (actual limit depends on risk_limit_tier and may differ).
2. Place order; if API returns **PRICE_TOO_DEVIATED**, extract the **valid price range from the error message** and show it to the user.
3. Suggest user adjust price within that range.

**Response Template** (after receiving PRICE_TOO_DEVIATED):
```
Order failed: price outside limit protection.

Your price: 100000 USDT
Valid range (from exchange): [min] - [max] USDT

Suggestion: Adjust price within the range above.
```

---

## Scenario 5: Insufficient balance

**Context**: Account margin is insufficient for the requested position.

**Prompt Examples**:
- "Open long 100 contracts BTC_USDT" (insufficient balance)

**Expected Behavior**:
1. Fetch contract via `cex_fx_get_fx_contract(settle="usdt", contract="BTC_USDT")`
2. Place order → receive BALANCE_NOT_ENOUGH
3. Output balance warning and suggestions

**Response Template**:
```
Order failed: insufficient margin.

Required margin: 6500 USDT
Available: 1000 USDT

Suggestions:
1. Reduce size
2. Add USDT
3. Increase leverage (e.g. from 10x to 20x)
```

---

## Scenario 6: Mode switch failed (position not empty)

**Context**: User tries to switch cross/isolated while having an open position; switch is rejected.

**Prompt Examples**:
- "Switch to cross" (currently isolated with position)
- "Cross margin long BTC_USDT" (currently isolated with position)

**Expected Behavior**:
1. Call `cex_fx_update_fx_dual_position_cross_mode(settle="usdt", contract="BTC_USDT", mode="CROSS")`
2. Receive POSITION_HOLDING (or similar; API returns this for mode switch with position)
3. Query position via **position query** (dual: `cex_fx_list_fx_positions` or `cex_fx_get_fx_dual_position`; single: `cex_fx_get_fx_position`)
4. Output failure and current position

**Response Template**:
```
Mode switch failed: position not empty.

Current position: BTC_USDT long 5 contracts
Current mode: isolated 10x

Suggestion: Close the position first, then switch margin mode.
```

---

## Scenario 6b: Dual position — switch margin mode (interrupt)

**Context**: User wants to open in a different margin mode than current position, and account is **dual position** mode.

**Expected Behavior**:
1. During open flow, detect target margin mode ≠ current `pos_margin_mode` and contract has a position.
2. Call `cex_fx_get_fx_accounts(settle="usdt")`; if `position_mode === "dual"`.
3. **Interrupt**: do not call `cex_fx_update_fx_dual_position_cross_mode`, do not place order.
4. Output: *"Please close the position first, then open a new one."*

**Response Template**:
```
In dual position mode you cannot switch this contract’s margin mode while a position exists.

Please close the position first, then open a new one.
```

---

## Scenario 6c: Single position — switch margin mode (confirm then continue)

**Context**: User wants to open in a different margin mode; account is **single position** mode.

**Expected Behavior**:
1. Detect target margin mode ≠ current `pos_margin_mode` and contract has a position.
2. Call `cex_fx_get_fx_accounts(settle="usdt")`; if `position_mode === "single"`.
3. **Do not interrupt**. Prompt: *"You already have a {currency} position; switching margin mode will apply to this position too. Continue?"* (e.g. BTC_USDT → "You already have a BTC position...").
4. After user confirms, call `cex_fx_update_fx_dual_position_cross_mode(settle, contract, mode="ISOLATED" or "CROSS")`, then continue leverage and place order.

**Response Template** (before confirm):
```
You already have a BTC position; switching margin mode will apply to this position too. Continue?
```

---

## Scenario 7: POC (Post Only) order

**Context**: User wants to post as Maker only; if the order would take liquidity it should be cancelled.

**Prompt Examples**:
- "POC limit buy 1 BTC_USDT at 64000"
- "Maker only, BTC_USDT long 1 at 64000"
- "post only buy 1 BTC_USDT at 64000"

**Expected Behavior**:
1. Fetch contract via `cex_fx_get_fx_contract(settle="usdt", contract="BTC_USDT")`
2. Place POC via `cex_fx_create_fx_order(settle="usdt", contract="BTC_USDT", size="1", price="64000", tif="poc")`
3. If order would immediately match, return ORDER_POC (or similar)
4. If resting as Maker, output success

**Response Template**:
```
Order placed (Post Only).

Order ID: 123456791
Contract: BTC_USDT
Side: long (buy)
Size: 1 contract
Price: 64000 USDT
Status: open
Role: Maker

Note: This order will only fill as Maker (maker fee).
```

---

## Scenario 8: Top gainer/loser order (ticker-based)

**Context**: User wants to open a position on the contract with the highest 24h gain or loss. The system discovers the contract automatically via `cex_fx_get_fx_tickers`.

**Trigger phrases**:
- "top gainer long 10U"
- "top loser short 5U"
- "long 10U on today's biggest gainer"
- "short 5U on the 24h biggest loser"

**Expected Behavior**:
1. Call `cex_fx_get_fx_tickers(settle="usdt")` to get all USDT-settled futures tickers.
2. Sort by `changePercentage`:
   - **Top gainer**: sort descending, pick the contract with the highest positive `changePercentage`.
   - **Top loser**: sort ascending, pick the contract with the most negative `changePercentage`.
3. With the identified contract (e.g. `PEPE_USDT`), call `cex_fx_get_fx_contract(settle="usdt", contract="PEPE_USDT")` for `mark_price`, `quanto_multiplier`, `order_size_min`.
4. Convert USDT notional to contracts: `contracts = u ÷ mark_price ÷ quanto_multiplier` (or `u × leverage ÷ mark_price ÷ quanto_multiplier` if leverage specified). Round to meet `order_size_min`.
5. **Show discovery result and order summary**, ask user to confirm:
   - Which contract was identified, 24h change percentage
   - Order details: contract, side, size (contracts + USDT equivalent), market/limit, mode, leverage
   - Risk warning for volatile coins
6. After user confirms, place order via `cex_fx_create_fx_order(settle="usdt", contract=..., size=..., price="0", tif="ioc")` for market order.
7. Verify position and output result.

**Response Template** (discovery + confirmation):
```
Today's top gainer: PEPE_USDT (+45.2% in 24h)

Order summary:
- Contract: PEPE_USDT
- Side: long (buy)
- Size: ~10 USDT (≈ 1234 contracts)
- Type: market
- Mode: cross
- Leverage: 20x

⚠️ Hot coin alert: PEPE_USDT has high volatility. Please manage risk and consider setting a stop-loss.

Reply 'confirm' to place the order.
```

**Response Template** (after fill):
```
Order filled.

Contract: PEPE_USDT (24h top gainer, +45.2%)
Order ID: 123456792
Side: long (buy)
Size: 1234 contracts (~10 USDT)
Avg fill: 0.00001234 USDT
Status: finished
Mode: cross 20x

⚠️ Hot coins are highly volatile — consider setting a stop-loss.
```

**Edge cases**:
- If `changePercentage` is `"0"` for all contracts (e.g. data unavailable), inform user: "24h price change data is currently unavailable. Please specify a contract directly."
- If the top contract has very low liquidity or is not in `trading` status, skip to the next one.
- If user says "top gainer" / "biggest gainer" → top gainer (long by default); "top loser" / "biggest loser" → top loser (user specifies long or short; do not assume).

---

## Scenario 9: Open by USDT cost (margin-based)

**Context**: User specifies how much USDT to **invest as margin**. Contracts are calculated using the cost formula that accounts for fees and leverage.

**Prompt Examples**:
- "spend 100U long BTC_USDT"
- "invest 100 USDT to open long BTC_USDT"
- "spend 500U isolated 10x short ETH_USDT"

**Expected Behavior**:
1. Fetch contract via `cex_fx_get_fx_contract(settle="usdt", contract="BTC_USDT")` for `quanto_multiplier`.
2. Fetch orderbook via `cex_fx_get_fx_order_book(settle="usdt", contract="BTC_USDT", limit=1)` for best ask (`asks[0].p`) and best bid (`bids[0].p`).
3. Get current leverage from position query. **Use this leverage in the formula. Do not change leverage unless the user explicitly requests a different value.**
4. Compute contracts:
   - **Open long**: `contracts = cost / (0.0015 + 1/leverage) / quanto_multiplier / order_price` (`order_price`: limit → specified; market → best ask)
   - **Open short**: `contracts = cost / (0.0015 + 1.00075/leverage) / quanto_multiplier / max(order_price, best_bid)` (`order_price`: limit → specified; market → best bid)
5. Floor to integer. If < `order_size_min`, prompt user.
6. Proceed with open flow; report shows both "~xxx U cost" and "yy contracts".

**Response Template**:
```
Order summary:
- Contract: BTC_USDT
- Side: long (buy)
- Cost: 100 USDT (margin)
- Size: 156 contracts (≈ 1.0 BTC)
- Type: market (best ask: 64,200)
- Mode: cross 10x
- Estimated liq price: ...

Reply 'confirm' to place the order.
```

---

## Scenario 10: Open by USDT value (notional-based)

**Context**: User specifies the **notional value** of the position in USDT.

**Prompt Examples**:
- "long 100U worth of BTC_USDT"
- "open 100 USDT value long BTC_USDT"
- "market short 500 USDT value ETH_USDT"

**Expected Behavior**:
1. Fetch contract via `cex_fx_get_fx_contract(settle="usdt", contract="BTC_USDT")` for `quanto_multiplier`.
2. Fetch orderbook via `cex_fx_get_fx_order_book(settle="usdt", contract="BTC_USDT", limit=1)` for best ask and best bid.
3. Compute contracts:
   - **Buy / open long**: `contracts = usdt_value / price / quanto_multiplier` (`price`: limit → specified; market → best ask)
   - **Sell / open short**: `contracts = usdt_value / max(best_bid, order_price) / quanto_multiplier` (`order_price`: limit → specified; market → best bid)
4. Floor to integer. If < `order_size_min`, prompt user.
5. Proceed with open flow; report shows both "~xxx U value" and "yy contracts".

**Response Template**:
```
Order summary:
- Contract: BTC_USDT
- Side: long (buy)
- Notional: ~100 USDT
- Size: 15 contracts (≈ 0.0015 BTC)
- Type: market (best ask: 64,200)
- Mode: cross 10x

Reply 'confirm' to place the order.
```
