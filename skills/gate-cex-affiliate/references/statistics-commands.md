# Affiliate statistics and transactions

## Scope and source

Separate transaction notional, net fees, rebates and number of clients/traders. Use bounded windows and preserve the documented timezone: partner agent-data uses UTC+8 date strings, while timestamp flags follow their own units. Do not aggregate unlike currencies without an explicit rate/time basis. A reported statistic is not a payout instruction.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `rebate.agency.transactions` | `gate-cli cex rebate agency transactions` | read |
| `rebate.broker.transactions` | `gate-cli cex rebate broker transactions` | read |
| `rebate.partner.agent-data` | `gate-cli cex rebate partner agent-data` | read |
| `rebate.partner.transactions` | `gate-cli cex rebate partner transactions` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="rebate.agency.transactions"></a>
### `gate-cli cex rebate agency transactions`

Operation ID: `rebate.agency.transactions`. Effect: **read**.

Agency obtains transaction history of recommended users

```text
gate-cli cex rebate agency transactions [flags]
```

API: `GET /api/v4/rebate/agency/transaction_history` (private).

Returns: [][AgencyTransactionHistory](models/statistics.md#model-agencytransactionhistory).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--from` | `int64` | No | `0` | Start timestamp |
| `--limit` | `int32` | No | `0` | Max records |
| `--offset` | `int32` | No | `0` | List offset |
| `--pair` | `string` | No | Unset | Currency pair filter |
| `--to` | `int64` | No | `0` | End timestamp |
| `--user-id` | `int64` | No | `0` | User ID filter |

<a id="rebate.broker.transactions"></a>
### `gate-cli cex rebate broker transactions`

Operation ID: `rebate.broker.transactions`. Effect: **read**.

Broker obtains user trading history

```text
gate-cli cex rebate broker transactions [flags]
```

API: `GET /api/v4/rebate/broker/transaction_history` (private).

Returns: [][BrokerTransactionHistory](models/statistics.md#model-brokertransactionhistory).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--from` | `int64` | No | `0` | Start timestamp |
| `--limit` | `int32` | No | `0` | Max records |
| `--offset` | `int32` | No | `0` | List offset |
| `--to` | `int64` | No | `0` | End timestamp |
| `--user-id` | `int64` | No | `0` | User ID filter |

<a id="rebate.partner.agent-data"></a>
### `gate-cli cex rebate partner agent-data`

Operation ID: `rebate.partner.agent-data`. Effect: **read**.

Aggregated partner agent statistics

```text
gate-cli cex rebate partner agent-data [flags]
```

API: `GET /api/v4/rebate/partner/data/aggregated` (private).

Returns: [PartnerDataAggregatedResponse](models/statistics.md#model-partnerdataaggregatedresponse).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--business-type` | `int32` | No | `0` | Business type: 0=All, 1=Spot, 2=Futures, 3=Alpha, etc. |
| `--end-date` | `string` | No | Unset | End date (yyyy-mm-dd hh:ii:ss, UTC+8) |
| `--start-date` | `string` | No | Unset | Start date (yyyy-mm-dd hh:ii:ss, UTC+8) |

<a id="rebate.partner.transactions"></a>
### `gate-cli cex rebate partner transactions`

Operation ID: `rebate.partner.transactions`. Effect: **read**.

Partner obtains transaction history of recommended users

```text
gate-cli cex rebate partner transactions [flags]
```

API: `GET /api/v4/rebate/partner/transaction_history` (private).

Returns: [PartnerTransactionHistory](models/statistics.md#model-partnertransactionhistory).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--from` | `int64` | No | `0` | Start timestamp |
| `--limit` | `int32` | No | `0` | Max records |
| `--offset` | `int32` | No | `0` | List offset |
| `--pair` | `string` | No | Unset | Currency pair filter |
| `--to` | `int64` | No | `0` | End timestamp |
| `--user-id` | `int64` | No | `0` | User ID filter |

## Verification and recovery

Keep query window, timezone, currency and metric definitions attached to aggregates. An empty result is not proof that the user has no customers or unpaid rebates.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex rebate agency transactions  --format json
```
