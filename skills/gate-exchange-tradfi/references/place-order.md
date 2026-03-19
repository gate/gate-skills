# Gate TradFi Place Order

Place a new TradFi order. **Before placing an order, call `cex_tradfi_query_symbol_detail`** with the symbol to get the trading pair configuration; if the symbol is not found, do not place the order. **`cex_tradfi_create_tradfi_order` supports setting take-profit and stop-loss price** (optional, per MCP). Use only MCP-documented tool names and parameters.

## MCP tools and parameters

| Tool | Purpose | Parameters (declare per MCP) |
| -----| --------| -----------------------------|
| `cex_tradfi_query_symbol_detail` | Get symbol config (required before place order) | Pass symbol (trading pair). Returns config including `leverages`, `min_order_volume`, `step_order_volume`. If no result or error, symbol may not exist — do not place order. |
| `cex_tradfi_create_tradfi_order` | Place new order | Required/optional from MCP. Typical: symbol, side, size (volume), price (limit) or market flag. **Optional: take-profit price, stop-loss price**, leverage. Do not pass parameters not documented in the MCP. |

### Symbol config validation (from `cex_tradfi_query_symbol_detail`)

- **Pre-order requirement**: Before calling `cex_tradfi_create_tradfi_order`, call **`cex_tradfi_query_symbol_detail`** with the symbol. If the query returns no data or an error, **do not place the order** — the symbol may not exist; inform the user.
- **If symbol config is found**, use the response to validate:
  - **`leverages`** (array): Supported leverage values. Leverage is optional; if the user specifies leverage, it **must** be one of the values in `leverages`. Do not pass a leverage value not in this array.
  - **`min_order_volume`**: Minimum order volume. Order size **must be greater than or equal to** `min_order_volume`.
  - **`step_order_volume`**: Minimum order size step. Order size **must be an integer multiple of** `step_order_volume` (e.g. valid sizes: step_order_volume, 2×step_order_volume, …; and size ≥ min_order_volume).
- **Missing required param**: Ask the user (e.g. symbol, side, size, or price for limit orders).

## Pre-execution confirmation

Before calling `cex_tradfi_create_tradfi_order`: **output all parameters** that will be sent (e.g. symbol, side, size, price or market, and **take-profit / stop-loss** if set). Ask the user to confirm (e.g. "Confirm: place order symbol=EURUSD, side=buy, size=0.1, price=1.0500, take-profit 1.08, stop-loss 1.03. Reply yes to execute."). Do **not** call the tool until the user explicitly confirms.

---

## Workflow

1. Parse user intent: symbol, side, size, price (or market), **take-profit / stop-loss price** and **leverage** (optional) if the user specifies them.
2. If symbol/side/size missing or invalid, ask user. For limit orders, price is required unless MCP supports market orders with a different convention.
3. **Required before place order**: Call **`cex_tradfi_query_symbol_detail`** with the symbol (trading pair). If the call returns no data or an error, **do not place the order** — tell the user the symbol may not exist.
4. **If symbol detail is returned**: From the response get `leverages`, `min_order_volume`, `step_order_volume`. Validate: (a) Order size **≥** `min_order_volume`; (b) Order size is an **integer multiple of** `step_order_volume`; (c) If leverage is provided, it **must** be in the `leverages` array. If validation fails, ask the user to correct size or leverage.
5. Build parameter set using **only MCP-documented parameters** (include take-profit, stop-loss, leverage when requested and valid).
6. **Output the full parameter set to the user and ask for confirmation.** Do not call the place-order tool until user confirms.
7. After confirmation, call `cex_tradfi_create_tradfi_order` with the confirmed parameters.
8. In the response: **explain the parameters that were used** and the outcome (order id, status, or error). Use the Report Template below.

## Report Template

After execution, include:

- **Parameters used**: Table or list of what was sent (symbol, side, size, price/market, **take-profit, stop-loss** if set, and any other params).
- **Result**: Order id and status (e.g. open, filled) or error code/message. If error, restate the sent parameters and suggest correction.

**Important**: The `id` and `log_id` returned by `cex_tradfi_create_tradfi_order` **must not be used** as the order id for the cancel (`cex_tradfi_delete_order`) or amend (`cex_tradfi_update_order`) APIs. For cancel or amend, the order id **must** come from **`cex_tradfi_query_order_list`** (the order list query). If the user wants to cancel or amend an order they just created, call `cex_tradfi_query_order_list` first and use the order id from that response.

---

## Scenario 1: Limit order

**Context**: User wants to place a limit order with symbol, side, size, and price.

**Prompt Examples**:
- "Place order buy EURUSD 0.1 at 1.0500"
- "Sell XAUUSD 0.01 at 2650"
- "Open long EURUSD size 0.1 limit 1.05"

**Expected Behavior**:
1. Extract symbol, side, size, price. Call `cex_tradfi_query_symbol_detail(symbol)`; if no result, do not place order and inform user.
2. From symbol detail validate size ≥ min_order_volume, size is integer multiple of step_order_volume; if leverage given, it must be in leverages array.
3. Output parameters for user confirmation. Wait for confirmation.
4. Call `cex_tradfi_create_tradfi_order` with only MCP-documented parameters.
5. Respond with parameters used and result (order id, status or error).

**Response Template**:
```
Parameters sent:
| Symbol | Side | Size | Price |
| EURUSD | buy | 0.1 | 1.0500 |

Result: Order created. Order ID: … Status: open.
```

---

## Scenario 2: Market order (if supported by MCP)

**Context**: User wants to place a market order. Only include if the MCP documents a market-order parameter or equivalent.

**Prompt Examples**:
- "Market buy EURUSD 0.1"
- "Sell XAUUSD 0.01 market"

**Expected Behavior**:
1. Extract symbol, side, size. Call `cex_tradfi_query_symbol_detail(symbol)`; if no result, do not place order.
2. Validate size and optional leverage from symbol detail (min_order_volume, step_order_volume, leverages). Use MCP-documented way to indicate market.
3. Output parameters for user confirmation. Wait for confirmation.
4. Call `cex_tradfi_create_tradfi_order`.
5. Respond with parameters used and result.

---

## Scenario 3: Place order with take-profit and/or stop-loss

**Context**: User wants to place an order and set take-profit and/or stop-loss price at creation. **`cex_tradfi_create_tradfi_order` supports this.**

**Prompt Examples**:
- "Buy EURUSD 0.1 at 1.05, take-profit 1.08, stop-loss 1.03"
- "Place order sell XAUUSD 0.01 at 2650 with stop-loss 2640"
- "Open long EURUSD 0.1 limit 1.05, take-profit 1.08"

**Expected Behavior**:
1. Extract symbol, side, size, price (or market), take-profit/stop-loss if given. Call `cex_tradfi_query_symbol_detail(symbol)`; if no result, do not place order.
2. Validate size (min_order_volume, step_order_volume) and leverage (leverages array) from symbol detail. Build params per MCP.
3. Output full parameter set for user confirmation.
4. After confirmation, call `cex_tradfi_create_tradfi_order` with the parameters.
5. Respond with parameters used and result.
