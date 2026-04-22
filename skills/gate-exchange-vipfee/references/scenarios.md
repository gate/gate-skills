# Scenarios

## Scenario 1: Query VIP Tier

**Context**: User wants to check their current Gate VIP level.

**Prompt Examples**:
- "What is my VIP level?"
- "Check my VIP tier"
- "Show me my current VIP level"
- "Which VIP tier am I on?"

**Expected Behavior**:
1. Identify query type as "vip"
2. Call `gate-cli cex account detail` to retrieve account profile
3. Extract VIP level from the response
4. Return VIP tier in the Report Template format

## Scenario 2: Query Trading Fee Rates

**Context**: User wants to know their current spot and futures trading fee rates.

**Prompt Examples**:
- "What are my trading fees?"
- "Check my fee rates"
- "Show me the spot and futures fees"
- "What are my maker and taker fees?"

**Expected Behavior**:
1. Identify query type as "fee"
2. Call `gate-cli cex wallet market trade-fee` to retrieve fee rate data
3. Extract spot maker/taker fee and futures maker/taker fee
4. Return fee rates in the Report Template format with spot and futures categories

## Scenario 3: Query Both VIP Tier and Fee Rates

**Context**: User wants to know both their VIP level and trading fee rates in a single query.

**Prompt Examples**:
- "Check my VIP level and trading fees"
- "What is my VIP tier and fee rate?"
- "Show me my VIP level and trading fees"
- "Show my account tier and fee info"

**Expected Behavior**:
1. Identify query type as "combined"
2. Call `gate-cli cex account detail` to retrieve VIP tier
3. Call `gate-cli cex wallet market trade-fee` to retrieve fee rates
4. Return combined result with both VIP tier and fee rate sections

## Scenario 4: Query Fee for Specific Trading Pair

**Context**: User wants to check the fee rate for a specific trading pair.

**Prompt Examples**:
- "What is the fee for BTC_USDT?"
- "Check the fee rate for ETH_USDT"
- "Show me the trading fee for BTC_USDT"

**Expected Behavior**:
1. Identify query type as "fee" with `currency_pair` parameter
2. Call `gate-cli cex wallet market trade-fee` with `currency_pair` set to the specified pair
3. Extract fee rates for the specified pair
4. Return fee rates in the Report Template format

## Scenario 5: Query Futures Fee by Settlement Currency

**Context**: User specifically asks about futures/contract fee rates for a particular settlement currency.

**Prompt Examples**:
- "What are my USDT-settled futures fees?"
- "Check the BTC-settled contract fees"
- "Show me the futures fees for USDT settlement"

**Expected Behavior**:
1. Identify query type as "fee" with `settle` parameter
2. Call `gate-cli cex wallet market trade-fee` with `settle` set to the specified currency (BTC / USDT / USD)
3. Extract futures maker/taker fee rates
4. Return futures fee rates in the Report Template format
