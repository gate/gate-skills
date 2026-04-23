# Asset Allocation Optimization Scenarios

## Scenario 1: List Eligible Spot Assets for Optimization

**Context**: The user wants to know which spot holdings can participate in asset allocation optimization, or to inspect approximate valuations before choosing a strategy.

**Prompt Examples**:
- "Which coins in my spot account can I use for asset allocation optimization?"
- "List assets eligible for allocation optimization on Gate"
- "What can I rebalance with the allocation optimization product?"

**Expected Behavior**:
1. Classify goal as list-only or precursor to a later preview
2. Call `gate-cli cex assetswap assets` per MCP parameter documentation
3. Summarize count and key fields returned by the API (symbols, available balances, valuation if present)
4. Offer next steps: load config, evaluate, or preview once the user selects assets and strategy

## Scenario 2: Load Strategy and Limits

**Context**: The user needs allowed strategies, target assets, TopN options, or min/max limits before building a preview.

**Prompt Examples**:
- "What allocation optimization strategies does Gate support?"
- "Show asset allocation optimization configuration"
- "What targets can I pick for conservative vs market-cap strategy?"

**Expected Behavior**:
1. Call `gate-cli cex assetswap config`
2. Present allowed strategies and parameters using API field names and values
3. Guide the user to choose parameters compatible with the next preview call

## Scenario 3: Optional Evaluation Before Preview

**Context**: The user wants a quick estimate without committing to a full preview, or is iterating on strategy parameters.

**Prompt Examples**:
- "Estimate how much USDT I would get if I optimized these alts conservatively"
- "Rough valuation for allocation optimization with Top 5 market cap strategy"

**Expected Behavior**:
1. Ensure Case 1 and Case 2 data are sufficient to build the evaluate payload
2. Call `gate-cli cex assetswap evaluate` with API-compliant body
3. Present evaluation output and caveats (estimates, not final execution)
4. Offer to proceed to preview (Case 3b) when the user is ready

## Scenario 4: Preview Optimization Order

**Context**: The user has chosen assets and strategy parameters and should see estimated execution and risk hints before placing an order.

**Prompt Examples**:
- "Preview asset allocation optimization selling DOGE, SHIB, PEPE into Top 5 market cap"
- "Show me the allocation optimization preview for conservative USDT target"
- "Preview rebalancing my selected alts into BTC only"

**Expected Behavior**:
1. Complete Case 1 and Case 2 as needed
2. Call `gate-cli cex assetswap order preview` with a valid payload
3. Show preview results clearly and ask for explicit confirmation before any create call
4. If preview indicates expiry or validation failure, explain and retry preview after user adjusts inputs

## Scenario 5: Create Order After Confirmed Preview

**Context**: The user explicitly confirmed the preview output and wants to submit the optimization.

**Prompt Examples**:
- "I confirm the preview — place the allocation optimization order"
- "Submit the portfolio optimization now"
- "Execute the asset allocation with the parameters we just previewed"

**Expected Behavior**:
1. Verify preview succeeded and user confirmation is explicit
2. Call `gate-cli cex assetswap order create` with required fields including any preview-bound tokens from the preview response
3. Return order id and status from the API
4. Suggest querying order detail if the user wants child-order progress

## Scenario 6: Query Recent Allocation Optimization History

**Context**: The user wants a paginated list of past asset allocation optimization orders.

**Prompt Examples**:
- "Show my recent allocation optimization orders"
- "List asset allocation optimization history for the last month"
- "Do I have any pending portfolio optimization orders?"

**Expected Behavior**:
1. Call `gate-cli cex assetswap order list` with pagination parameters per API
2. Present a concise table: order id, status, time, summary fields returned by API
3. Offer detail lookup for a specific id

## Scenario 7: Query Single Allocation Optimization Order

**Context**: The user asks for progress or outcome of one optimization, including child orders.

**Prompt Examples**:
- "What is the status of allocation optimization order {id}?"
- "Did my portfolio optimization complete?"
- "Show child orders for my last asset allocation run"

**Expected Behavior**:
1. Extract order id from the user or from a prior list result
2. Call `gate-cli cex assetswap order get`
3. Present aggregate status and relevant child-order information from the response
4. If not found, state clearly and suggest checking the id or list endpoint

## Scenario 8: Conservative Risk-Off Posture

**Context**: The user wants to move diversified spot alts into a single stablecoin for a defensive posture.

**Prompt Examples**:
- "Market is too volatile — consolidate my small caps to USDT via allocation optimization"
- "Risk off: optimize holdings to stablecoin using conservative strategy"

**Expected Behavior**:
1. Confirm intent is asset allocation optimization, not a single manual spot sell
2. Run Case 1 and Case 2; align strategy with conservative targets from config
3. Run Case 3b preview; require confirmation before Case 4
4. Use compliance-safe wording: no guaranteed PnL; final balances per exchange records

## Scenario 9: Conviction or Single-Asset Target

**Context**: The user wants to rotate selected assets into BTC, ETH, GT, or similar conviction target.

**Prompt Examples**:
- "Reallocate my listed alts into BTC using asset allocation optimization"
- "Optimize my spot bag toward ETH with the faith-style strategy"

**Expected Behavior**:
1. Map user language to strategy parameters from `gate-cli cex assetswap config`
2. Follow Case 1 → 2 → 3b → 4 with explicit preview confirmation
3. Avoid promising VIP or volume outcomes

## Scenario 10: Market-Cap-Weighted Basket

**Context**: The user wants Top N large-cap exposure rather than a single ticker.

**Prompt Examples**:
- "Rebalance to Top 5 market cap coins using allocation optimization"
- "Turn my shitcoins into a large-cap basket via portfolio optimization"

**Expected Behavior**:
1. Resolve TopN and allowed basket from config
2. Execute preview with correct parameters; emphasize index-like behavior is API-defined
3. Create only after user confirms preview
