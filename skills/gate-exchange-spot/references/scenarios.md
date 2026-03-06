# Scenarios

This document defines behavior-oriented scenario templates for all 25 spot cases.

## Global Execution Gate (Mandatory)

For every scenario that includes `create_spot_order`:
- Build and present an Order Draft first
- Require explicit confirmation from the immediately previous user turn
- Treat confirmation as single-use
- Re-confirm whenever parameters or intent change
- For multi-leg flows, confirm each leg separately

If confirmation is missing/ambiguous/stale, do not execute any trading call.

## I. Buy and Account Queries (1-8)

### Scenario 1: Market Buy by Quote Amount
**Context**: User wants to buy a fixed USDT value of a coin at market price.
**Prompt Examples**:
- "Buy 100U of BTC."
- "I want to buy 100 USDT of BTC now."
**Expected Behavior**:
1. Call `get_spot_accounts` to verify quote balance.
2. Build Order Draft with market buy semantics (`amount` = USDT quote amount).
3. Wait for explicit confirmation, then call `create_spot_order`.
4. Return execution outcome and post-trade key fields.
**Unexpected Behavior**:
1. Directly returns "Order placed" with an order id before any `Confirm order`.
2. Sends `amount=0.001 BTC` for market buy request "buy 100U", causing wrong notional.
3. Reports filled quantity but omits average fill price and fee impact.

### Scenario 2: Limit Buy at Target Price
**Context**: User wants to buy at a specified limit price.
**Prompt Examples**:
- "Buy 100U BTC at 60000."
- "Place a limit buy for BTC at 60000."
**Expected Behavior**:
1. Call `get_spot_accounts` for affordability.
2. Build a limit-buy Order Draft with target price.
3. Execute only after confirmation via `create_spot_order`.
4. Explain open-order status if not immediately filled.
**Unexpected Behavior**:
1. Converts to market order and executes immediately even though user asked for limit price.
2. Returns "open order created" without checking whether quote balance can support order value.
3. Uses wrong price precision and returns exchange error without a user-readable fix suggestion.

### Scenario 3: Buy with All USDT
**Context**: User wants to convert full USDT balance into a target coin.
**Prompt Examples**:
- "Use all my USDT to buy ETH."
- "All-in USDT into ETH."
**Expected Behavior**:
1. Call `get_spot_accounts` and compute available USDT.
2. Build Order Draft with full-amount basis and risk note.
3. Execute after confirmation with `create_spot_order`.
4. Report remaining balance after trade.
**Unexpected Behavior**:
1. Uses total balance instead of available balance, leading to `BALANCE_NOT_ENOUGH` at execution.
2. Places full-size order without draft/confirmation despite all-in risk.
3. Returns no residual balance summary, so user cannot verify remaining funds.

### Scenario 4: Tradability and Unit-Cost Check
**Context**: User wants a buy readiness check before placing any order.
**Prompt Examples**:
- "Can BTC be traded now? How much for one BTC?"
- "Check ETH tradability and current unit price."
**Expected Behavior**:
1. Call `get_currency` for currency status.
2. Call `get_currency_pair` for constraints.
3. Call `get_spot_tickers` for current price.
4. Return structured check result without trading.
**Unexpected Behavior**:
1. Places an order in what should be a read-only "can I trade?" request.
2. Ignores disabled/suspended trading status and answers "tradable" incorrectly.
3. Returns only ticker price, missing min amount/precision constraints.

### Scenario 5: Total Account Valuation
**Context**: User wants total account value in USDT terms.
**Prompt Examples**:
- "How much is my account worth now?"
- "Give me my total USDT-equivalent value."
**Expected Behavior**:
1. Call `get_spot_accounts` for holdings.
2. Call `get_spot_tickers` for conversion prices.
3. Aggregate value into USDT and return breakdown + total.
**Unexpected Behavior**:
1. Excludes low-liquidity or non-USDT assets from total, materially understating account value.
2. Uses stale or mismatched pair prices, producing unrealistic valuation output.
3. Triggers trade-related tools in a portfolio-report-only task.

### Scenario 6: Cancel All Open Orders Then Recheck Balance
**Context**: User wants all open orders canceled and updated balances.
**Prompt Examples**:
- "Cancel all unfilled orders and show my balance."
- "Clear open orders first."
**Expected Behavior**:
1. Call `cancel_all_spot_orders`.
2. Call `get_spot_accounts` for post-cancel balances.
3. Return cancellation and balance summary.
**Unexpected Behavior**:
1. Cancels only one pair's orders but reports "all orders canceled."
2. Fails to show which order ids were canceled vs already filled.
3. Skips post-cancel balance refresh, so refund state is unknown.

### Scenario 7: Sell Full Dust Position
**Context**: User wants to sell all holdings of a coin into USDT.
**Prompt Examples**:
- "Sell all my DOGE to USDT."
- "Convert my DOGE position to USDT."
**Expected Behavior**:
1. Call `get_spot_accounts` for available coin amount.
2. Call `get_currency_pair` for min-size/precision checks.
3. Build draft and execute `create_spot_order` after confirmation.
4. If below minimum, return constraint warning and no trade.
**Unexpected Behavior**:
1. Submits size below `min_base_amount`, then surfaces raw API error only.
2. Rounds amount with wrong precision and creates unexpected partial leftover balance.
3. Executes sell without showing user that dust remains unsellable.

### Scenario 8: Balance and Minimum-Amount Buy Check
**Context**: User asks to buy only if both balance and minimum amount conditions are satisfied.
**Prompt Examples**:
- "I want to buy 5U ETH; if possible, place it."
- "Check if I can buy 5 USDT of ETH, then buy."
**Expected Behavior**:
1. Call `get_spot_accounts` for available quote balance.
2. Call `get_currency_pair` for `min_quote_amount`.
3. If both checks pass, build draft and execute after confirmation via `create_spot_order`.
4. If failed, explain which condition failed and required top-up.
**Unexpected Behavior**:
1. Places order even when 5U is below `min_quote_amount` or available quote balance.
2. Returns generic "cannot trade" without showing minimum threshold and shortfall.
3. Fails to provide top-up guidance (how much additional USDT is needed).

## II. Smart Monitoring and Trading (9-16)

### Scenario 9: Buy 2% Lower
**Context**: User wants a discounted-entry limit buy based on current price.
**Prompt Examples**:
- "Buy 50U BTC when it is 2% lower than now."
**Expected Behavior**:
1. Call `get_spot_tickers` and compute target = current * 0.98.
2. Build limit-order draft with computed price.
3. Execute after confirmation via `create_spot_order`.
**Unexpected Behavior**:
1. Uses an outdated last price and computes wrong -2% target.
2. Submits market order instead of computed limit order.
3. Places order without showing target price formula in draft.

### Scenario 10: Sell at Current + 500
**Context**: User wants a profit-taking limit sell at fixed offset.
**Prompt Examples**:
- "If BTC rises by 500, sell my holdings."
**Expected Behavior**:
1. Call `get_spot_tickers`, compute target sell price.
2. Draft sell parameters and risk note.
3. Execute after confirmation with `create_spot_order`.
**Unexpected Behavior**:
1. Sells immediately at market instead of placing current+500 limit sell.
2. Calculates offset from wrong reference price (for example 24h open, not current).
3. Omits size source (available holdings) and causes insufficient-balance failure.

### Scenario 11: Buy Near 24h Low
**Context**: User wants to buy only when price is near daily low.
**Prompt Examples**:
- "If ETH is near today's low, buy."
**Expected Behavior**:
1. Call `get_spot_tickers` and compare current vs 24h low.
2. If condition met, build draft then execute after confirmation.
3. If not met, return no-trade decision with gap details.
**Unexpected Behavior**:
1. Buys even though current price is clearly above user's "near low" threshold.
2. Returns binary yes/no without reporting current price, 24h low, and distance.
3. Treats "near" as exact equality only, causing unrealistic non-execution.

### Scenario 12: Sell on 5% Drop Request
**Context**: User wants downside-exit style execution using a computed target.
**Prompt Examples**:
- "Sell if BTC drops 5%."
**Expected Behavior**:
1. Call `get_spot_tickers`, compute drop target.
2. Build limit-sell draft at computed level.
3. Execute only after confirmation.
**Unexpected Behavior**:
1. Claims native TP/SL trigger support and submits unsupported order semantics.
2. Executes sell without confirmation under "risk-control urgency" wording.
3. Computes 5% drop from wrong anchor (entry price vs current price) without disclosure.

### Scenario 13: Buy Top 24h Gainer
**Context**: User wants to rotate into the strongest coin by recent performance.
**Prompt Examples**:
- "Buy 20U of the top gainer now."
**Expected Behavior**:
1. Call `get_spot_tickers` and rank candidates by 24h gain.
2. Build draft for selected pair and amount.
3. Execute after confirmation.
**Unexpected Behavior**:
1. Picks a non-top gainer while saying it is rank #1.
2. Selects an illiquid/suspended pair and fails at order placement.
3. Omits ranking evidence (top candidates and 24h change values).

### Scenario 14: Buy the Bigger Loser (BTC vs ETH)
**Context**: User wants comparative dip-buy between two assets.
**Prompt Examples**:
- "Between BTC and ETH, buy whichever dropped more."
**Expected Behavior**:
1. Call `get_spot_tickers` and compare 24h change.
2. Select the larger loser and show comparison.
3. Draft and execute after confirmation.
**Unexpected Behavior**:
1. Chooses BTC/ETH winner without presenting both percentage changes.
2. Uses absolute price drop rather than percentage decline despite scenario intent.
3. Executes before final confirmation after showing comparison.

### Scenario 15: Buy Then Place +2% Sell
**Context**: User wants a two-leg flow: entry first, then exit order.
**Prompt Examples**:
- "Buy 100U BTC, then place sell at +2%."
**Expected Behavior**:
1. Build and confirm leg-1 draft, execute `create_spot_order` (buy).
2. Build and confirm leg-2 draft from fill reference price.
3. Execute second `create_spot_order` (sell).
**Unexpected Behavior**:
1. Executes buy and sell legs under one confirmation, bypassing per-leg checkpoint.
2. Uses requested +2% on intended price instead of actual fill reference.
3. Creates second leg with wrong quantity (requested amount vs filled amount).

### Scenario 16: Fee-Inclusive Cost Estimate
**Context**: User wants pre-trade cost estimation only.
**Prompt Examples**:
- "If I buy 1000U, what's total including fees?"
**Expected Behavior**:
1. Call `get_wallet_fee` for fee rate.
2. Call `get_spot_tickers` for quote.
3. Return principal + fee estimate; no trade execution.
**Unexpected Behavior**:
1. Places a trade even though user asked only for estimation.
2. Returns "about 1000U" without fee breakdown or fee rate source.
3. Uses maker fee assumption without stating uncertainty for taker execution.

## III. Order Management and Amendment (17-25)

### Scenario 17: Raise Price for Unfilled Buy Order
**Context**: User wants to amend an unfilled buy order to improve fill chance.
**Prompt Examples**:
- "My buy order is unfilled, raise the price a bit."
**Expected Behavior**:
1. Ask user to confirm raise amount or exact target price.
2. Call `list_spot_orders` with `status=open` and filter buy orders.
3. If multiple candidates, ask user to pick exact order (id/row).
4. After confirmation, call `amend_spot_order` and return amended result.
**Unexpected Behavior**:
1. Amends order without confirming raise amount/new target price.
2. Amends the wrong order when multiple open buy orders exist.
3. Returns success without showing old price -> new price delta.

### Scenario 18: Verify Latest Buy Fill and Current Holdings
**Context**: User wants confirmation of executed buy and current total holdings.
**Prompt Examples**:
- "Did my BTC buy fill, and how much BTC do I have now?"
**Expected Behavior**:
1. Call `list_spot_my_trades` to get latest buy fill amount X.
2. Call `get_spot_accounts` to get current holdings Y.
3. Return X and Y clearly.
**Unexpected Behavior**:
1. Uses old trade history entry instead of latest buy fill.
2. Returns fill quantity but not current holding total (or vice versa).
3. Mixes pair/currency units (for example reports USDT where BTC is expected).

### Scenario 19: Cancel If Still Unfilled and Verify Refund
**Context**: User wants conditional cancellation and post-cancel balance verification.
**Prompt Examples**:
- "If my ETH buy is still open, cancel it and check refund."
**Expected Behavior**:
1. Call `list_spot_orders` (`status=open`) for target order.
2. If open, call `cancel_spot_order`.
3. Call `get_spot_accounts` to verify returned quote funds.
**Unexpected Behavior**:
1. Attempts to cancel already filled/canceled order without clear handling path.
2. Reports "refund completed" without checking updated quote balance.
3. Fails to identify target order among multiple open ETH buys.

### Scenario 20: Rebuy at Last Fill Price
**Context**: User wants another buy using previous execution price.
**Prompt Examples**:
- "If balance allows, buy 100U BTC at my last buy price."
**Expected Behavior**:
1. Call `list_spot_my_trades` for last fill price.
2. Call `get_spot_accounts` for affordability.
3. Draft limit-buy and execute after confirmation via `create_spot_order`.
**Unexpected Behavior**:
1. Uses current ticker price instead of last fill price for rebuy.
2. Skips balance check and hits insufficient funds after confirmation.
3. Places market order when scenario requires price reuse via limit order.

### Scenario 21: Break-even Exit
**Context**: User wants to sell only if current price is above cost basis.
**Prompt Examples**:
- "If I can exit ETH without loss, sell all."
**Expected Behavior**:
1. Call `list_spot_my_trades` to compute cost basis.
2. Call `get_spot_tickers` for current price.
3. If condition met, draft sell and execute after confirmation.
4. If not met, return no-trade rationale.
**Unexpected Behavior**:
1. Sells even when current price is below computed cost basis.
2. Computes cost basis from one trade only, ignoring partial fills/history.
3. Omits fee-adjusted break-even explanation, misleading "no-loss" decision.

### Scenario 22: Full Asset Swap (DOGE -> BTC)
**Context**: User wants a two-leg conversion only above minimum value threshold.
**Prompt Examples**:
- "Swap all DOGE to BTC if worth at least 10U."
**Expected Behavior**:
1. Call `get_spot_accounts` and `get_spot_tickers` to estimate DOGE value.
2. If >= 10U, confirm and execute leg-1 sell via `create_spot_order`.
3. Build, confirm, and execute leg-2 buy via `create_spot_order`.
**Unexpected Behavior**:
1. Executes swap when DOGE valuation is below 10U threshold.
2. Runs both legs without independent confirmation checkpoints.
3. Proceeds with buy leg before confirming sell leg completion amount.

### Scenario 23: Buy Only If Below Price Threshold
**Context**: User wants conditional buy and post-trade balance report.
**Prompt Examples**:
- "If BTC < 60000, buy 50U and show balance."
**Expected Behavior**:
1. Call `get_spot_tickers` and evaluate condition.
2. If met, draft + confirm + execute `create_spot_order`.
3. Call `get_spot_accounts` and return updated balance.
**Unexpected Behavior**:
1. Buys despite current price not below 60000.
2. Uses delayed ticker snapshot and mis-evaluates condition.
3. Skips post-trade account refresh and returns stale balance.

### Scenario 24: Buy on Short-Term Uptrend
**Context**: User wants trend-filtered execution using recent candlesticks.
**Prompt Examples**:
- "If BTC has been rising for recent hours, buy 100U."
**Expected Behavior**:
1. Call `get_spot_candlesticks` for recent 4 hourly candles.
2. Check whether at least 3 of 4 are bullish.
3. If met, draft + confirm + execute `create_spot_order`.
**Unexpected Behavior**:
1. Buys without fetching/validating the last 4 hourly candles.
2. Miscounts bullish candles (for example includes incomplete current candle incorrectly).
3. Executes on sideways/downtrend while labeling it "uptrend confirmed."

### Scenario 25: Fast Execution Limit Buy from Order Book
**Context**: User wants fastest practical limit execution using book top.
**Prompt Examples**:
- "Check ETH book and place fastest 50U buy."
**Expected Behavior**:
1. Call `get_spot_order_book` and read best opposite price (`ask1`).
2. Build limit-buy draft at execution-oriented price.
3. Execute after confirmation via `create_spot_order`.
**Unexpected Behavior**:
1. Uses bid price instead of ask-side top for fast buy placement.
2. Ignores depth/size mismatch and proposes unrealistic instant fill.
3. Omits risk note about slippage or partial fill at chosen limit price.
