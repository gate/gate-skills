# Scenarios

This document provides standardized test inputs, API call order, and decision logic for all 25 cases.

## I. Buy and Account Queries (1-8)

### Scenario 1: Market Buy
- User Prompt: `I want to buy 100 USDT of BTC. Check if my balance is enough, and if yes, buy at the current price.`
- Tools: `GET /spot/accounts` → `POST /spot/orders`
- Logic: Check available USDT balance; if sufficient, place a market buy order.

### Scenario 2: Buy at Target Price (Limit)
- User Prompt: `Buy 100 USDT of BTC, but place the order at 60000 when BTC drops there.`
- Tools: `GET /spot/accounts` → `POST /spot/orders`
- Logic: If balance is sufficient, create a `type=limit` buy order at 60000.

### Scenario 3: Buy with Full Balance
- User Prompt: `Use all USDT in my account to buy ETH.`
- Tools: `GET /spot/accounts` → `POST /spot/orders`
- Logic: Read all available USDT and buy ETH using an executable order type.

### Scenario 4: Buy Readiness Check
- User Prompt: `I want to buy BTC. Is it tradable right now, and how much does one BTC cost?`
- Tools: `GET /spot/currencies/{currency}` → `GET /spot/currency_pairs/{pair}` → `GET /spot/tickers`
- Logic: Check currency status, minimum trade rules, and return current price for buying 1 unit.

### Scenario 5: Account Asset Summary
- User Prompt: `Show me how much my account is worth in total right now.`
- Tools: `GET /spot/accounts` → `GET /spot/tickers`
- Logic: Convert each coin balance to USDT using latest prices and sum the total.

### Scenario 6: Cancel All Open Orders
- User Prompt: `Cancel all my unfilled orders, then tell me my remaining balance.`
- Tools: `DELETE /spot/orders` → `GET /spot/accounts`
- Logic: Cancel all open orders, then query and return balances.

### Scenario 7: Sell Dust to USDT
- User Prompt: `Sell all my DOGE and convert it to USDT.`
- Tools: `GET /spot/accounts` → `GET /spot/currency_pairs/{pair}` → `POST /spot/orders`
- Logic: Read all available DOGE; sell only if it meets minimum size, otherwise return a clear warning.

### Scenario 8: Minimum Buy Check
- User Prompt: `Can I buy 5 USDT worth of ETH?`
- Tools: `GET /spot/currency_pairs/{pair}` → `POST /spot/orders`
- Logic: Validate `min_quote_amount` first; if below threshold (for example <10U), ask the user to increase amount instead of forcing execution.

## II. Smart Monitoring and Trading (9-16)

### Scenario 9: Buy 2% Lower (Limit Buy)
- User Prompt: `Monitor BTC and buy 50U when it is 2% lower than current price.`
- Tools: `GET /spot/tickers` → `POST /spot/orders`
- Logic: Read current price, compute target `current * 0.98`, then place a limit buy order.

### Scenario 10: Sell at +500 (Limit Sell)
- User Prompt: `If BTC rises by 500, sell all my holdings.`
- Tools: `GET /spot/tickers` → `POST /spot/orders`
- Logic: Set target sell price to `current + 500`, then place limit sell using available holdings.

### Scenario 11: Buy Near Daily Low
- User Prompt: `Is ETH at today's low now? If yes, buy some for me.`
- Tools: `GET /spot/tickers` → `POST /spot/orders`
- Logic: Compare current price with 24h low; execute buy if within threshold, otherwise report the gap.

### Scenario 12: Sell on 5% Drop
- User Prompt: `Watch BTC and sell quickly if it drops by 5%.`
- Tools: `GET /spot/tickers` → `POST /spot/orders`
- Logic: Calculate target drop price as `current * 0.95`, then place a limit sell order.

### Scenario 13: Buy Top Gainer
- User Prompt: `Which coin is up the most right now? Buy 20 USDT of that one.`
- Tools: `GET /spot/tickers` → `POST /spot/orders`
- Logic: Select the tradable pair with highest 24h gain and buy 20U.

### Scenario 14: Buy the Bigger Loser
- User Prompt: `Between BTC and ETH, which dropped more today? Buy the one that dropped more.`
- Tools: `GET /spot/tickers` → `POST /spot/orders`
- Logic: Compare 24h performance for BTC and ETH, then buy the one with the larger decline.

### Scenario 15: Buy Then Auto-Place Sell
- User Prompt: `Buy 100U of BTC, then immediately place a sell order 2% above the buy price.`
- Tools: `POST /spot/orders` → `POST /spot/orders`
- Logic: Place buy first, then place limit sell at +2% of the fill reference price.

### Scenario 16: Fee-Inclusive Cost Estimation
- User Prompt: `I want to buy 1000U of a coin. How much will it cost in total including fees?`
- Tools: `GET /wallet/fee` → `GET /spot/tickers`
- Logic: Estimate total cost (principal + fee) from fee tier and current quote, then return final amount.

## III. Order Management and Amendment (17-25)

### Scenario 17: Raise Price if Unfilled
- User Prompt: `My buy order is still unfilled. Help me raise the price a bit.`
- Tools: `GET /spot/open_orders` → `PATCH /spot/orders`
- Logic: Find target open buy order and increase limit price to improve fill probability.

### Scenario 18: Verify Fill and Holdings
- User Prompt: `Did my BTC buy just succeed? How much was credited, and how much BTC do I hold in total now?`
- Tools: `GET /spot/my_trades` → `GET /spot/accounts`
- Logic: Read latest buy fill quantity X, then read total holdings Y, and return both.

### Scenario 19: Cancel if Not Filled
- User Prompt: `Check my ETH buy order. If it is not filled, cancel it and confirm whether the funds returned.`
- Tools: `GET /spot/open_orders` → `DELETE /spot/orders` → `GET /spot/accounts`
- Logic: If order is still open, cancel it, then check USDT balance and confirm refund.

### Scenario 20: Rebuy at Last Fill Price
- User Prompt: `I liked the last BTC buy price. If I have enough balance now, buy another 100 USDT at that same price.`
- Tools: `GET /spot/my_trades` → `GET /spot/accounts` → `POST /spot/orders`
- Logic: Read last fill price, check if balance covers 100U, then place limit buy at that price.

### Scenario 21: Break-even Sell Check
- User Prompt: `Check my ETH cost basis. If selling now would not lose money, sell all of it.`
- Tools: `GET /spot/my_trades` → `GET /spot/tickers` → `POST /spot/orders`
- Logic: Compute average historical buy cost; if current price is above cost basis, execute full sell.

### Scenario 22: Asset Swap
- User Prompt: `I want to swap all my DOGE into BTC. Check if it is worth at least 10 USDT; if yes, do it.`
- Tools: `GET /spot/accounts` → `GET /spot/tickers` → `POST /spot/orders`(sell) → `POST /spot/orders`(buy)
- Logic: Estimate total DOGE value first; only if >=10U, execute "sell DOGE then buy BTC."

### Scenario 23: Buy If Price Is Favorable
- User Prompt: `Is BTC cheaper than 60000 now? If yes, buy 50 USDT and tell me my balance after.`
- Tools: `GET /spot/tickers` → `POST /spot/orders` → `GET /spot/accounts`
- Logic: Buy only when `current price < 60000`; then return updated balances.

### Scenario 24: Buy on Trend Condition
- User Prompt: `Check whether BTC has been rising over recent hours. If yes, buy 100 USDT.`
- Tools: `GET /spot/candlesticks` → `POST /spot/orders`
- Logic: Fetch last 4 hourly candles; if at least 3 are bullish, treat as uptrend and buy.

### Scenario 25: Fast Execution Order
- User Prompt: `Show me where bids are for ETH right now. I also want to buy 50 USDT; place it for fastest execution.`
- Tools: `GET /spot/order_book` → `POST /spot/orders`
- Logic: Read best opposite-book price (`ask1`) and place a limit buy at that level to improve execution speed.
