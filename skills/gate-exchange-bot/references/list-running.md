# Gate Bot Portfolio Running — `gate-cli cex bot portfolio running`

Running-strategy list query contract.

## Scope

Use this command to list the user's currently running AIHub strategies.

## Query Parameters

| Parameter | Required | Notes |
|---|---|---|
| `strategy_type` | No | Filter by strategy type |
| `market` | No | Filter by market |
| `page` | No | Default `1` |
| `page_size` | No | Default `20`, maximum `50` |

## When To Use

- "What bots are currently running?"
- "Show my running BTC strategies"
- "List only spot grid bots"

## When Not To Use

- The user already chose one concrete strategy and wants detail
- The user wants to stop a specific strategy
- The user wants bulk stop

## Success and Failure

Success requires:

- HTTP `200`
- body `code = 200`

Read mainly:

- `data.items`
- `data.page`
- `data.page_size`
- `data.total`

## Guardrails

- Do not treat this as a bulk-stop command.
- Do not exceed `page_size=50`.
- If the user later wants to stop one of the returned items, move into the stop workflow and confirm a single concrete target.

## Workflow

1. Confirm that the user wants a running-strategy list rather than detail or stop.
2. Apply optional filters for strategy type, market, page, or page size.
3. Execute the running-list command.
4. Return the items and explain next-step options if needed.

## Report Template

```markdown
## Running Strategy List
- Filters: {filter_summary}
- Page: {page}
- Page Size: {page_size}
- Total: {total}
- Items: {items_summary}
```
