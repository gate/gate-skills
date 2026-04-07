# Gate Options Place Order — Scenarios & Unit Conversion

Gate options place-order scenarios and expected behavior. The API accepts **size in contracts** only; when the user specifies base notional or USDT, convert to contracts before placing the order.

## Contract name format

Options contract name format: `{underlying}-{expiration}-{strike}-{C|P}` (e.g. `BTC_USDT-20210916-50000-C`). Resolve user input (underlying, expiration, strike, call/put) to this exact string via `list_options_contracts` or `get_options_contract`. C = call, P = put.

## Unit Conversion

When the user does not specify size in **contracts**, convert to **contracts** before placing the order.

There are **two distinct intents** when user specifies amount:

| User phrase | Intent | Type |
|-------------|--------|------|
| "1 contract", "buy 3 contracts" | **Contracts** — size in contracts | Contracts |
| "0.1 BTC call", "1 BTC put", "1 ETH call" | **Base notional** — notional in underlying | Base |
| "1000U", "spend 500 USDT", "half of account" | **Quote (USDT)** — premium / cost in USDT | Quote |

**Default**: When user says "X BTC" or "X ETH" (or other base) without the word "contract(s)", treat as **base notional** and convert to contracts. Use explicit "X contracts" for contract count.

### Data sources

- `get_options_contract(contract)` → `multiplier` (face value of one contract in underlying units), `order_size_min`, `order_price_round`
- `list_options_order_book(contract)` → best ask / best bid for price per contract
- `list_options_tickers`(underlying or contract) → index price (for "strike at current price"), or mid for price_per_contract
- `list_options_account` → available balance in USDT (for "half of account" or quote-based size)

### Base notional → contracts

The user specifies notional in the underlying (e.g. 1 BTC, 0.1 ETH).

| Formula | Notes |
|---------|-------|
| **contracts = base_amount / multiplier** | Floor to integer. multiplier from `get_options_contract`. |

Example: multiplier = 0.1, user says "1 BTC call" (1 BTC notional) → contracts = 1 / 0.1 = 10. User says "0.1 BTC call" → 0.1 / 0.1 = 1 contract.

### Quote (USDT) → contracts

The user specifies premium or cost in USDT.

| Formula | Notes |
|---------|-------|
| **contracts = usdt_amount / price_per_contract** | Floor to integer. price_per_contract from order book (e.g. best ask for buy, best bid for sell) or ticker. |

For "half of account": get available balance from `list_options_account`, then usdt_amount = half of that, then contracts as above.

### Precision

- Resulting contracts must satisfy `order_size_min` from the contract; if below minimum, prompt the user.
- Always **floor** (truncate) the result to an integer (contracts are whole numbers).
- Price must be rounded to `order_price_round` from `get_options_contract`.

## "Strike at current price" resolution

When user says "strike at current price" or "ATM": get underlying index/spot price from `list_options_tickers`(underlying) or underlying ticker, then from `list_options_contracts` pick the strike closest to that price (or list and let user choose if ambiguous).

## Pre-Order Confirmation

**Before placing**, show the **final order summary** and only call `create_options_order` after user confirmation.

- **Summary**: Contract, side (buy/sell), size in **contracts** (and optionally equivalent base notional or USDT when converted), price (limit or "market"), strike, expiration, call/put.
- **Confirmation**: *"Please confirm the above and reply 'confirm' to place the order."* Only after the user confirms (e.g. "confirm", "yes", "place") execute the order.

---

## Scenario 1: Market or limit place order

**Context**: User wants to buy or sell options at market or limit price.

**Prompt Examples**:
- "Market buy 1 BTC call, strike at current price, expire in one week"
- "Sell 1000U of weekly BTC call at 70k strike"
- "Open long 1 SOL weekly option at market"
- "Use half of account to buy BTC call expiring in 3 days"
- "Buy 2 contracts of BTC put, strike 65000, one week expiry"

**Expected Behavior**:
1. Resolve underlying, expiration, strike, call/put → exact contract name via `list_options_contracts` or `get_options_contract`.
2. Resolve size to contracts (see Unit Conversion above): contracts / base notional / quote.
3. Get `order_size_min`, `order_price_round` from `get_options_contract`; enforce precision.
4. For limit/market: use order book or ticker for "current price" strike or price_per_contract as needed.
5. Show final order summary and ask user to confirm.
6. After confirm, call `create_options_order`(contract, size, price). Market: price `"0"`, tif `"ioc"` per API.
7. Output using response template.

**Response Template**:
```
Order submitted! You have placed a {buy/sell} order on {underlying} at {market/limit price}, strike {xxx}, expiration {xxx}, option type {call/put}, size {xxx} contracts.
```
When size was converted from base or USDT, add e.g. " (equiv. 1 BTC notional)" or " (equiv. 500 USDT)".

---

## Scenario 2: Mark IV place order

**Context**: User wants to place order by implied volatility (mark IV).

**Prompt Examples**:
- "Mark IV order: buy 1 BTC call, strike at current price, one week expiry"
- "Sell 1000U weekly BTC call at 70k strike, mark IV"
- "Open long 1 SOL weekly option, mark IV"
- "Use half of account to buy BTC 3-day call, mark IV"

**Expected Behavior**:
1. Same as Scenario 1 for resolving contract and size (unit conversion).
2. If backend supports **IV-based order**: use the appropriate parameter (e.g. order by IV / mark IV) in `create_options_order` or equivalent API.
3. Otherwise: resolve mark IV to a limit price via backend (e.g. IV-to-price endpoint or `orders/price_from_iv`) then call `create_options_order` with that price.
4. Confirm with user: contract, side, size, "mark IV" (and resolved price if shown).
5. After confirm, call create order (with IV or derived price).
6. Output using same response template as Scenario 1; use "size {xxx} contracts" and optionally show equivalent when size was converted.
