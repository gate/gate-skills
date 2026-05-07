# Gate Bot Portfolio Stop — `gate-cli cex bot portfolio stop`

Single-strategy stop contract.

## Scope

This command performs the final stop action for one exact strategy. Risk explanation, settlement explanation, and user confirmation are handled at the skill layer before execution.

## Required Payload

```json
{
  "body": "{\"strategy_id\":\"123456\",\"strategy_type\":\"spot_grid\"}"
}
```

### Required fields

- `strategy_id`
- `strategy_type`

## When To Use

Only use this command when all three conditions are true:

- the user wants to stop exactly one strategy
- the specific strategy has already been identified
- the user has explicitly confirmed the stop action

## When Not To Use

- the user only wants a running list
- the user only wants detail
- the request is ambiguous, such as "stop all", "stop the losing ones", or "stop the bad bots"
- the user has not confirmed yet

For ambiguous stop requests, the required flow is:

1. call `gate-cli cex bot portfolio running`
2. present candidates
3. ask the user to choose one exact strategy
4. present a stop summary and confirmation
5. call `gate-cli cex bot portfolio stop` for that one target only

## Pre-Stop Risk Summary

### Spot grid / infinite grid / spot martingale

Explain at least:

- current holdings may be sold at market, or kept only if the upstream product rule explicitly says so
- funds return to the relevant trading or spot account
- open orders are cancelled
- the strategy cannot be resumed after stop

### Futures grid / contract martingale

Explain at least:

- positions may be closed at market
- margin or remaining funds return to the relevant contract or trading account
- open orders are cancelled
- slippage may cause actual exit values to differ from displayed P&L
- the strategy cannot be resumed after stop

### Margin grid

Explain at least:

- borrowed assets must be repaid and interest settled
- remaining funds return to the relevant trading or spot account
- open orders are cancelled
- the strategy cannot be resumed after stop

## Success and Failure

Success requires body `code = 200`.

Typical success fields:

- `data.strategy_id`
- `data.strategy_type`
- `data.status`
- `data.result_message`

Typical failures:

- invalid request body
- invalid `strategy_id`
- invalid `strategy_type`
- invalid user

## Guardrails

- Never stop without explicit confirmation.
- Never map a bulk-stop request into one or more hidden stop calls.
- Never skip the strategy-type-specific settlement and risk explanation.

## Workflow

1. Resolve a single exact target strategy.
2. If needed, list running strategies first and let the user choose one.
3. Present the strategy-type-specific stop risk summary.
4. Require explicit confirmation.
5. Execute the stop command for one strategy only.

## Report Template

```markdown
## Stop Action Draft
- Strategy ID: {strategy_id}
- Strategy Type: {strategy_type}
- Risk Summary: {risk_summary}
- Confirmation Required: yes
```
