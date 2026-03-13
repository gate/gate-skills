# Gate CrossEx Order Management - Scenarios and Prompt Examples

Gate CrossEx order query scenarios.

## Workflow

### Step 1: Identify the target order set

Call `cex_crossex_list_crossex_open_orders` with:
- `symbol`: optional filter when the user provides a symbol
- `exchange_type`: optional filter when the user provides an exchange scope

Key data to extract:
- matching open orders
- order ids
- order side and type

### Step 2: Query a specific order

Call `cex_crossex_get_crossex_order` with:
- `order_id`: the order to inspect

Key data to extract:
- current order status
- current price
- current quantity

## Report Template

Use the scenario-specific templates below. The minimum response should include:

```text
Order Management Summary
- Operation: {operation}
- Order ID: {order_id}
- Symbol: {symbol}
- Price: {price}
- Quantity: {qty}
- Status: {status}
```

## API Call Parameters

### Order Operation Types

```
{ACTION} : {ORDER_ID} / {SYMBOL}
```

**Examples**:
- `QUERY : 123456789` - Query order

### Order Query Parameters

| Parameter | Description |
|-----------|-------------|
| `order_id` | Order ID |
| `symbol` | Trading pair (optional) |
| `status` | Order status (optional) |
| `limit` | Return quantity (optional) |


### Data Sources

- **Order Query**: Call `cex_crossex_get_crossex_order` → Order details
- **Current Open Orders**: Call `cex_crossex_list_crossex_open_orders` → All open orders
- **Order History**: Call `cex_crossex_list_crossex_history_orders` → Historical orders

### Error Handling

| Error Code | Handling |
|-----------|----------|
| `ORDER_NOT_FOUND` | Order doesn't exist or already cancelled, query order history |

---

## Scenario 1: Query All Open Orders

**Context**: User wants to view all current open orders.

**Prompt Examples**:
- "Query all open orders"
- "Show my orders"
- "What are my current open orders"
- "list orders"

**Expected Behavior**:
1. Call `cex_crossex_list_crossex_open_orders` to query all open orders
2. Display order list (including order ID, trading pair, direction, quantity, price)

**Report Template**:
```
Current Open Orders:

| Order ID | Trading Pair | Direction | Quantity | Price | Time |
|----------|--------------|-----------|----------|--------|------|
| 123456789 | GATE_SPOT_BTC_USDT | Buy | 0.001 | 50000 | 10:30:25 |
| 123456790 | GATE_FUTURE_ETH_USDT | Long | 1 | 3000 | 10:35:12 |
| 123456791 | GATE_MARGIN_XRP_USDT | Short | 10 | 1.00 | 11:02:45 |

Total: 3 open orders
```

---

## Scenario 2: Query Order Details

**Context**: User wants to view detailed information for a specific order.

**Prompt Examples**:
- "Query order 123456789"
- "Order details 123456789"
- "My order 123456789 status"

**Expected Behavior**:
1. Call `cex_crossex_get_crossex_order` to query order details
2. Display complete order information

**Report Template**:
```
Order Details:

Order ID: 123456789
Trading Pair: GATE_SPOT_BTC_USDT
Direction: Buy (BUY)
Type: Limit (GTC)
Quantity: 0.001 BTC
Price: 50000 USDT
Filled: 0 BTC
Remaining: 0.001 BTC
Status: Open
Create Time: 10:30:25
Update Time: 10:30:25
```

---

## Scenario 3: Query Order History

**Context**: User wants to view historical order records.

**Prompt Examples**:
- "Query order history"
- "Show historical orders"
- "Past orders"
- "order history"

**Expected Behavior**:
1. Call `cex_crossex_list_crossex_history_orders` to query order history
2. Parameters: `limit` (max 100), `page`, `from` (start timestamp), `to` (end timestamp)
3. Display recent order records

**Report Template**:
```
Order History (Recent 10):

| Order ID | Trading Pair | Direction | Type | Quantity | Price | Status | Time |
|----------|--------------|-----------|------|----------|--------|--------|------|
| 123456788 | GATE_SPOT_BTC_USDT | Buy | Market | 0.0019 | 52631.58 | Filled | 10:25:10 |
| 123456787 | GATE_FUTURE_ETH_USDT | Long | Limit | 1 | 3000 | Cancelled | 10:20:05 |
| 123456786 | GATE_MARGIN_XRP_USDT | Short | Market | 50 | 1.02 | Filled | 10:15:30 |

Total: 3 records
```
