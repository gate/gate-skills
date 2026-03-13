# Flash Swap Query Scenarios

## Scenario 1: Query Supported Flash Swap Currency Pairs

**Context**: The user wants to explore which currency pairs are available for flash swap on Gate, in order to find possible exchange paths before making a swap.

**Prompt Examples**:
- "I want to swap some coins, show me what flash swap pairs are available"
- "List all flash swap currency pairs"
- "What coins can I exchange via flash swap"
- "Show me flash swap supported pairs"

**Expected Behavior**:
1. Identify intent as "list_pairs"
2. Call `cex_fc_list_fc_currency_pairs` without any filter to get the full list
3. Parse the returned currency pair list
4. Present results in a formatted table showing pair name, sell currency, and buy currency
5. Show total count of available pairs to give the user an overview

## Scenario 2: Validate Currency Support and Check Swap Limits

**Context**: The user wants to check whether a specific currency (e.g. BTC) supports flash swap, and if so, what the minimum and maximum swap amounts are for that currency.

**Prompt Examples**:
- "I want to swap BTC for USDT, what is the minimum and maximum amount"
- "Can I flash swap ETH? What are the limits"
- "Check if SOL supports flash swap and show the amount range"
- "What is the max amount I can flash swap for DOGE"

**Expected Behavior**:
1. Identify intent as "check_limits"
2. Extract the target currency from the user request (e.g. "BTC")
3. Call `cex_fc_list_fc_currency_pairs` with `currency` filter set to the target currency
4. If results are returned, parse the pairs and extract `sellMinAmount`, `sellMaxAmount`, `buyMinAmount`, `buyMaxAmount` for each pair
5. Present results in a formatted table showing the pair, sell/buy limits
6. If no results are returned, inform the user that the specified currency does not support flash swap

**Unexpected Behavior**:
- If the user does not specify a currency, prompt them to provide one

## Scenario 3: Query Flash Swap Order History

**Context**: The user wants to review their recent flash swap transaction records to check whether the swaps were successful or failed, and see the details of each transaction.

**Prompt Examples**:
- "Show me my recent flash swap records and check if they all succeeded"
- "Query my flash swap order history"
- "Show successful flash swap records"
- "Check my flash swap orders where I sold BTC"
- "Query failed flash swap orders"

**Expected Behavior**:
1. Identify intent as "list_orders"
2. Extract filter conditions from user request: status (1=success, 2=failed), sell_currency, buy_currency
3. Call `cex_fc_list_fc_orders` with the extracted parameters
4. Parse the returned order list including order ID, currencies, amounts, exchange rate, status, and timestamps
5. Present results in a formatted table with all order details, clearly indicating success or failure for each order
6. Show total record count

## Scenario 4: Track Specific Flash Swap Order Details

**Context**: The user has a specific flash swap order ID and wants to look up the full details of that order, including completion status, exchange rate, and transaction amounts.

**Prompt Examples**:
- "Check the details of flash swap order 54646"
- "What is the status of flash swap order 120841"
- "Look up flash swap order number 67890"
- "Show me the details of my flash swap order 12345"

**Expected Behavior**:
1. Identify intent as "get_order"
2. Extract `order_id` from user request
3. Call `cex_fc_get_fc_order` with the extracted `order_id`
4. Parse the returned order details including creation time, completion status, sell/buy currencies, amounts, and exchange rate
5. Present results in a detailed key-value format showing all order fields

**Unexpected Behavior**:
- If user does not provide an order ID, prompt them to provide one or suggest using the order list query (Scenario 3) first
