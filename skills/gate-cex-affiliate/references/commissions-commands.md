# Affiliate commissions

## Scope and source

Select the actual partner, broker or agency role and bounded currency/user/time filters. Distinguish earned, pending, paid and reversed commissions where the response supports them. Do not label trading volume as income or promise future commissions. Restrict subordinate information to the authorized relationship and minimize exported records.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `rebate.agency.commissions` | `gate-cli cex rebate agency commissions` | read |
| `rebate.broker.commissions` | `gate-cli cex rebate broker commissions` | read |
| `rebate.partner.commissions` | `gate-cli cex rebate partner commissions` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="rebate.agency.commissions"></a>
### `gate-cli cex rebate agency commissions`

Operation ID: `rebate.agency.commissions`. Effect: **read**.

Agency obtains rebate history of recommended users

```text
gate-cli cex rebate agency commissions [flags]
```

API: `GET /api/v4/rebate/agency/commission_history` (private).

Returns: [][AgencyCommissionHistory](models/commissions.md#model-agencycommissionhistory).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--commission-type` | `int32` | No | `0` | Type: 1=Direct, 2=Indirect, 3=Self |
| `--currency` | `string` | No | Unset | Currency filter |
| `--from` | `int64` | No | `0` | Start timestamp |
| `--limit` | `int32` | No | `0` | Max records |
| `--offset` | `int32` | No | `0` | List offset |
| `--to` | `int64` | No | `0` | End timestamp |
| `--user-id` | `int64` | No | `0` | User ID filter |

<a id="rebate.broker.commissions"></a>
### `gate-cli cex rebate broker commissions`

Operation ID: `rebate.broker.commissions`. Effect: **read**.

Broker obtains user rebate records

```text
gate-cli cex rebate broker commissions [flags]
```

API: `GET /api/v4/rebate/broker/commission_history` (private).

Returns: [][BrokerCommission](models/commissions.md#model-brokercommission).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--from` | `int64` | No | `0` | Start timestamp |
| `--limit` | `int32` | No | `0` | Max records |
| `--offset` | `int32` | No | `0` | List offset |
| `--to` | `int64` | No | `0` | End timestamp |
| `--user-id` | `int64` | No | `0` | User ID filter |

<a id="rebate.partner.commissions"></a>
### `gate-cli cex rebate partner commissions`

Operation ID: `rebate.partner.commissions`. Effect: **read**.

Partner obtains rebate records of recommended users

```text
gate-cli cex rebate partner commissions [flags]
```

API: `GET /api/v4/rebate/partner/commission_history` (private).

Returns: [PartnerCommissionHistory](models/commissions.md#model-partnercommissionhistory).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Currency filter |
| `--from` | `int64` | No | `0` | Start timestamp |
| `--limit` | `int32` | No | `0` | Max records |
| `--offset` | `int32` | No | `0` | List offset |
| `--to` | `int64` | No | `0` | End timestamp |
| `--user-id` | `int64` | No | `0` | User ID filter |

## Verification and recovery

Preserve currency, time range, role and payout/status meaning from returned records. Do not sum unconverted currencies or treat pending rebates as settled income.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex rebate agency commissions  --format json
```
