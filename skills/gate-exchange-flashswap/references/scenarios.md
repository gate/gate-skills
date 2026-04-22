# Flash Swap Scenarios

## Scenario 1: Query Supported Pairs and Swap Limits

**Context**: The user wants to explore which currency pairs are available for flash swap, or check the minimum/maximum amounts for a specific currency.

**Prompt Examples**:
- "Show me all flash swap supported pairs"
- "Can I flash swap BTC for USDT? What are the limits?"
- "What is the minimum amount to flash swap ETH?"
- "List flash swap pairs for SOL"

**Expected Behavior**:
1. Identify intent as "list_pairs"
2. Call `gate-cli cex flash-swap pairs` with optional currency filter
3. If no filter and result is large, summarize total count and show a sample of 20 pairs
4. If filtered by currency, show all matching pairs with min/max amounts
5. Present results in a formatted table

## Scenario 2: Query Flash Swap Order History and Details

**Context**: The user wants to review their flash swap transaction records or look up a specific order by ID.

**Prompt Examples**:
- "Show me my recent flash swap orders"
- "Query my successful flash swap orders"
- "Check flash swap order 122136 details"
- "Show me failed flash swap orders"

**Expected Behavior**:
1. Identify intent as "list_orders" or "get_order"
2. For order list: validate status if provided (only 1 or 2), call `gate-cli cex flash-swap orders` with filters
3. For single order: extract order_id, call `gate-cli cex flash-swap order`
4. Present results in a formatted table or detail view
5. If order not found (404), inform the user and suggest checking the ID

**Unexpected Behavior**:
- If the user provides an invalid status value, inform them only 1 (success) and 2 (failed) are accepted
- If order_id is not provided for a detail query, prompt the user or suggest using the order list first

## Scenario 3: One-to-One Flash Swap

**Context**: The user wants to convert one cryptocurrency to another, for example selling 1 BTC for USDT. The full flow requires previewing the quote first, then confirming and creating the order.

**Prompt Examples**:
- "Sell 1 BTC for USDT"
- "I want to swap 100 USDT to ETH"
- "Convert 0.5 ETH to BTC"
- "Flash swap 1000 USDT for SOL"

**Expected Behavior**:
1. Identify intent as "one_to_one" with sell_asset, buy_asset, and sell_amount or buy_amount
2. Call `gate-cli cex flash-swap preview-v1` with the extracted parameters
3. Present the preview to the user showing quote_id, exchange rate, amounts, and valid_timestamp
4. Wait for user confirmation
5. Call `gate-cli cex flash-swap create-v1` with the quote_id and amounts from the preview
6. Present the created order with order ID, status, and executed rate

**Unexpected Behavior**:
- If the preview returns an error, inform the user and suggest adjusting the amount or trying a different pair
- If the create returns code 1052 (quote expired), re-run the preview and try again

## Scenario 4: One-to-Many Flash Swap

**Context**: The user wants to use a single currency (typically USDT) to buy multiple target cryptocurrencies in one operation. Each target has its own amount.

**Prompt Examples**:
- "Buy 1u BTC, 2u ETH, 3u SOL, 4u DOGE, 5u PEPE"
- "Use USDT to buy 10u worth of BTC and 20u worth of ETH"
- "Flash swap USDT into BTC, ETH, SOL"

**Expected Behavior**:
1. Identify intent as "one_to_many" with sell_asset (e.g. USDT) and a list of buy targets with amounts
2. Call `gate-cli cex flash-swap preview-one-to-many` with params array
3. Present the full preview table showing each target's quote_id, amounts, rate, and error status
4. Highlight any items that failed to get a quote (error.code != 0)
5. Wait for user confirmation
6. Call `gate-cli cex flash-swap create-one-to-many` with only the successful items (exclude failed ones)
7. Present the order results showing order IDs, status, and any per-item errors

**Unexpected Behavior**:
- If some items fail in preview, warn the user and offer to proceed with only the successful items
- If create returns per-item errors (400001/400007), report which items failed

## Scenario 5: Flash Swap Quote Preview

**Context**: The user wants to check the current exchange rate and estimated amount before committing to a swap. They want to see the quote first and evaluate whether the price is acceptable.

**Prompt Examples**:
- "I want to swap 0.1 BTC for USDT, how much can I get? Is the price good?"
- "Preview selling 500 USDT for ETH"
- "What is the current flash swap rate for BTC to USDT?"
- "How much GT can I get for 100 USDT right now?"

**Expected Behavior**:
1. Identify intent as "one_to_one"
2. Call `gate-cli cex flash-swap preview-v1` with sell_asset, buy_asset, and sell_amount
3. Present the quote_id, exchange rate (price), estimated buy_amount, and quote validity period
4. Inform the user of the quote details and ask if they want to proceed
5. Do NOT auto-create the order — wait for explicit user confirmation

## Scenario 6: Confirm Preview and Execute Order

**Context**: The user has already seen a preview result (with a quote_id) and now wants to confirm and execute the swap based on that specific quote.

**Prompt Examples**:
- "The price looks good, go ahead and execute the swap with that quote"
- "Confirm the swap based on the preview just now (quote ID: MP-bfae76af)"
- "Yes, proceed with the flash swap"
- "Execute the order using the preview result"

**Expected Behavior**:
1. Retrieve the quote_id and associated parameters from the most recent preview result
2. Call `gate-cli cex flash-swap create-v1` with the stored quote_id, sell_asset, sell_amount, buy_asset, buy_amount
3. Check the response: if `status == 1`, inform user the swap succeeded with the final order ID and buy_amount
4. If `status == 2`, inform user the swap failed and suggest retrying
5. If code 1052 (quote expired), automatically re-preview and ask user to confirm again

## Scenario 7: One-Click Flash Swap (Preview + Create)

**Context**: The user wants to complete a flash swap immediately without a separate confirmation step. The system should automatically preview and create in one seamless flow.

**Prompt Examples**:
- "Directly swap 100 USDT to GT for me"
- "One-click convert 0.5 ETH to USDT"
- "Just flash swap 1000 USDT for BTC right now"
- "Quick swap 50 SOL to USDT, no need to confirm"

**Expected Behavior**:
1. Identify intent as "one_to_one_auto" (user explicitly says "directly" / "one-click" / "just do it")
2. Call `gate-cli cex flash-swap preview-v1` to get the latest quote
3. Immediately call `gate-cli cex flash-swap create-v1` with the returned quote_id and amounts — no separate confirmation
4. Present the final order result: order ID, status, sell/buy amounts, and rate
5. If the order fails, inform the user and suggest retrying

## Scenario 8: Swap Amount Validation Check

**Context**: The user requests a flash swap with an extremely small amount that may be below the minimum allowed. The system should validate the amount before calling the preview API.

**Prompt Examples**:
- "Flash swap 0.0000001 BTC for USDT"
- "Swap 0.001 USDT for BTC"
- "Convert a tiny amount of DOGE to USDT"

**Expected Behavior**:
1. Extract sell_asset, buy_asset, and sell_amount from the request
2. Call `gate-cli cex flash-swap pairs` with the sell currency to get the sell_min_amount
3. Compare the user's sell_amount against sell_min_amount
4. If below minimum: inform the user "The amount is too small. Minimum for selling {currency} is {sell_min_amount}." Do NOT call the preview API
5. If within range: proceed normally to preview

**Unexpected Behavior**:
- If the currency pair is not found, inform the user this pair is not supported for flash swap

## Scenario 9: Flash Swap Order Result Verification

**Context**: The user just completed a flash swap and wants to verify whether it succeeded and check the actual amounts received.

**Prompt Examples**:
- "Did my last flash swap go through? How much did I actually get?"
- "Check if my swap succeeded"
- "What is the status of my most recent flash swap order?"
- "I just swapped BTC for USDT, was it successful?"

**Expected Behavior**:
1. Identify intent as "verify_order"
2. If the order_id is known from the recent create response, call `gate-cli cex flash-swap order` with that ID
3. If no order_id is available, call `gate-cli cex flash-swap orders` with `reverse=true` and `limit=1` to get the most recent order
4. Check the `status` field: if `1`, confirm success and show the final buy_amount received
5. If `status == 2`, inform the user it failed and suggest re-previewing with adjusted parameters

## Scenario 10: One-to-Many Split by Ratio

**Context**: The user wants to split a single currency into multiple targets by specifying a ratio or proportion, rather than exact amounts per target.

**Prompt Examples**:
- "Split 1000 USDT: half into BTC, half into ETH"
- "Distribute 500 USDT equally among BTC, ETH, and SOL"
- "Put 60% of my 1000 USDT into BTC and 40% into ETH"
- "Divide 200 USDT evenly between BTC, ETH, SOL, and DOGE"

**Expected Behavior**:
1. Identify intent as "one_to_many_split"
2. Calculate per-target sell_amount based on the user's specified ratio (e.g. 1000 USDT / 2 = 500 each for half-and-half)
3. Call `gate-cli cex flash-swap preview-one-to-many` with the calculated amounts
4. Present the preview showing how much of each target currency the user will receive
5. After user confirmation, call `gate-cli cex flash-swap create-one-to-many`
6. Report the final results: how much BTC and ETH were received

## Scenario 11: One-to-Many with Specified Buy Quantities

**Context**: The user specifies exact buy quantities for each target currency instead of sell amounts. The system needs to calculate the required sell amount (USDT cost) using the buy_amount field.

**Prompt Examples**:
- "Buy 0.1 BTC and 1 ETH using my USDT"
- "I want exactly 10 SOL and 100 DOGE, pay with USDT"
- "Flash swap USDT to get 0.5 BTC and 2 ETH"

**Expected Behavior**:
1. Identify intent as "one_to_many_buy"
2. Call `gate-cli cex flash-swap preview-one-to-many` with `buy_amount` specified for each item (instead of sell_amount)
3. Present the preview showing the required USDT cost per target and the total cost
4. After user confirmation, call `gate-cli cex flash-swap create-one-to-many`
5. Report the final order results

## Scenario 12: Many-to-One Asset Consolidation

**Context**: The user wants to consolidate multiple "small" or "dust" holdings into a single target currency. The system should automatically detect balances and filter out currencies below the minimum swap amount.

**Prompt Examples**:
- "Convert all my BTC, ETH, and DOGE to USDT"
- "Sweep all my small balances into USDT"
- "Cash out all my BTC, ETH, and SOL into USDT"
- "Consolidate my crypto holdings into GT"

**Expected Behavior**:
1. Identify intent as "many_to_one_all"
2. Query the user's spot account balances for the specified currencies
3. Call `gate-cli cex flash-swap pairs` to get sell_min_amount for each currency
4. Filter out currencies whose balance is below sell_min_amount, inform the user which were excluded
5. Call `gate-cli cex flash-swap preview-many-to-one` with the qualifying currencies and their full balances
6. Present the preview showing per-currency conversion amounts and total expected USDT
7. After confirmation, call `gate-cli cex flash-swap create-many-to-one` (excluding any failed preview items)
8. Report total USDT received

**Unexpected Behavior**:
- If all currencies are below minimum, inform the user none qualify for flash swap

## Scenario 13: Many-to-One Preview-Only (Feasibility Check)

**Context**: The user wants to estimate how much target currency they would receive if they converted multiple holdings, but does NOT want to actually execute the swap.

**Prompt Examples**:
- "How much GT can I get if I convert all my BTC and ETH?"
- "Calculate the total USDT I would get from selling 1 BTC and 2 ETH"
- "Preview converting my BTC, ETH, SOL to USDT without actually doing it"
- "What would 0.5 BTC and 3 ETH be worth in USDT right now?"

**Expected Behavior**:
1. Identify intent as "many_to_one_preview"
2. Call `gate-cli cex flash-swap preview-many-to-one` with the specified currencies and amounts
3. Sum up all successful `buy_amount` values to get the total expected target amount
4. Present the per-currency breakdown and the total sum
5. Explicitly state this is a preview only and no order has been placed
6. Ask if the user would like to proceed with the actual swap

**Unexpected Behavior**:
- If some currencies fail to get a quote, show them as failed and calculate the total from successful items only
