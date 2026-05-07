# Gate Bot Scenarios

Scenario coverage for the routing-style `gate-exchange-bot` skill.

## Scenario 1: Recommend a Strategy for a Specific Market

**Context**: The user wants a bot strategy recommendation but has not yet chosen a full manual configuration.

**Prompt Examples**:
- "Recommend a BTC strategy."
- "What bot should I use for ETH?"
- "Give me a spot grid recommendation for BTC."

**Expected Behavior**:
1. Route the request to `gate-cli cex bot strategy recommend`.
2. Determine whether the request maps to `top1`, `bundle`, `filter`, or `refresh`.
3. Ask for the target coin only if the market is still missing and recommendation quality depends on it.
4. Return recommendation results without performing any create action.

## Scenario 2: Create a Manual Spot Grid

**Context**: The user wants to create a spot grid with explicit manual parameters.

**Prompt Examples**:
- "Create a BTC spot grid from 60000 to 72000 with 50 grids and 1000 USDT."
- "Use arithmetic mode and create this BTC spot grid."

**Expected Behavior**:
1. Route the request to `references/create-spot-grid.md`.
2. Check whether market, amount, range, grid count, and mode are all present.
3. Ask only for missing business inputs; do not guess them.
4. Present an Action Draft with normalized ratio values if any exist.
5. Execute `gate-cli cex bot spot-grid create` only after explicit confirmation.

## Scenario 3: Create a Manual Martingale with Stop-Loss Intent

**Context**: The user wants a martingale strategy and also expresses stop-loss intent.

**Prompt Examples**:
- "Create a spot martingale for BTC with 2% deviation and 1.5% take profit, and stop loss at 5%."
- "Create a spot martingale and use 78000 as the stop-loss price."

**Expected Behavior**:
1. Route the request to the correct martingale reference file based on spot vs contract.
2. If the request is for spot martingale, enforce `stop_loss_per_cycle` semantics rather than accepting a fixed stop-loss price.
3. Ask for the missing stop-loss ratio if the user provided only a fixed price for spot martingale.
4. Present a confirmation summary with readable percentages and normalized decimal payload values.
5. Execute the create command only after explicit confirmation.

## Scenario 4: List and Inspect Running Strategies

**Context**: The user wants to understand which bot strategies are currently running and optionally inspect one of them.

**Prompt Examples**:
- "What bots do I have running?"
- "Show my running BTC bot strategies."
- "Show me the detail for strategy 123456."

**Expected Behavior**:
1. Use `gate-cli cex bot portfolio running` for list requests.
2. Use `gate-cli cex bot portfolio detail` only when `strategy_id` and `strategy_type` are both known.
3. Do not guess a detail target from a non-unique list result.
4. Keep these flows read-only.

## Scenario 5: Stop a Single Running Strategy

**Context**: The user wants to stop a specific running bot.

**Prompt Examples**:
- "Stop that BTC grid bot."
- "Stop strategy 123456."
- "Stop the ETH martingale."

**Expected Behavior**:
1. If the target strategy is ambiguous, first list matching running strategies.
2. Resolve one exact strategy before preparing the stop action.
3. Present a strategy-type-specific risk and settlement summary.
4. Require explicit confirmation in the immediately following turn.
5. Execute `gate-cli cex bot portfolio stop` for one strategy only.
