# VIP, fees and rate limits

## Scope and source

Read the actual account tier and product/instrument fee schedule. Maker and taker rates, rebates and temporary discounts are distinct. A fee-rate quote is not the final charged fee. Debit-fee enable/disable is a write with a separate grant. Never promise a fee tier, discount, referral return or rate-limit exemption.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `account.debit-fee.get` | `gate-cli cex account debit-fee get` | read |
| `account.debit-fee.set` | `gate-cli cex account debit-fee set` | write |
| `account.rate-limit` | `gate-cli cex account rate-limit` | read |
| `futures.account.fee` | `gate-cli cex futures account fee` | read |
| `spot.account.batch-fee` | `gate-cli cex spot account batch-fee` | read |
| `spot.account.fee` | `gate-cli cex spot account fee` | read |
| `stock.market.fee-rate` | `gate-cli cex stock market fee-rate` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="account.debit-fee.get"></a>
### `gate-cli cex account debit-fee get`

Operation ID: `account.debit-fee.get`. Effect: **read**.

Get debit fee setting

```text
gate-cli cex account debit-fee get
```

API: `GET /api/v4/account/debit_fee` (private).

Returns: [DebitFee](models/vip-fees.md#model-debitfee).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="account.debit-fee.set"></a>
### `gate-cli cex account debit-fee set`

Operation ID: `account.debit-fee.set`. Effect: **write**.

Enable or disable debit fee

```text
gate-cli cex account debit-fee set [flags]
```

API: `POST /api/v4/account/debit_fee` (private).

Returns: Array of objects: `{Enabled: string}`.

API request model(s), assembled by the command: [DebitFee](models/vip-fees.md#model-debitfee). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--enabled` | `string` | Yes | Unset | Enable or disable debit fee: true or false (required) |

<a id="account.rate-limit"></a>
### `gate-cli cex account rate-limit`

Operation ID: `account.rate-limit`. Effect: **read**.

Get account rate limit tiers

```text
gate-cli cex account rate-limit
```

API: `GET /api/v4/account/rate_limit` (private).

Returns: [][AccountRateLimit](models/vip-fees.md#model-accountratelimit).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="futures.account.fee"></a>
### `gate-cli cex futures account fee`

Operation ID: `futures.account.fee`. Effect: **read**.

Get futures trading fee rates

```text
gate-cli cex futures account fee [flags]
```

API: `GET /api/v4/futures/{settle}/fee` (private).

Returns: map[string][FuturesFee](models/vip-fees.md#model-futuresfee).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="spot.account.batch-fee"></a>
### `gate-cli cex spot account batch-fee`

Operation ID: `spot.account.batch-fee`. Effect: **read**.

Get trading fee rates for multiple currency pairs

```text
gate-cli cex spot account batch-fee [flags]
```

API: `GET /api/v4/spot/batch_fee` (private).

Returns: map[string][SpotFee](models/vip-fees.md#model-spotfee).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--pairs` | `string` | Yes | Unset | Comma-separated currency pairs, e.g. BTC_USDT,ETH_USDT (required) |

<a id="spot.account.fee"></a>
### `gate-cli cex spot account fee`

Operation ID: `spot.account.fee`. Effect: **read**.

Get personal trading fee rates

```text
gate-cli cex spot account fee [flags]
```

API: `GET /api/v4/spot/fee` (private).

Returns: [SpotFee](models/vip-fees.md#model-spotfee).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--pair` | `string` | No | Unset | Specify currency pair for more accurate fee settings |

<a id="stock.market.fee-rate"></a>
### `gate-cli cex stock market fee-rate`

Operation ID: `stock.market.fee-rate`. Effect: **read**.

Query fee rates for Japanese and Korean stocks

```text
gate-cli cex stock market fee-rate
```

API: `GET /api/v4/stock/fee-rate` (public).

Returns: [FeeRate](models/vip-fees.md#model-feerate).

Parameters: none beyond shared options and any positional arguments shown in the syntax. This endpoint's documented coverage is Japanese and Korean stock fee rates; do not infer fees for another exchange.

## Verification and recovery

Re-read the relevant fee schedule and, for a setting change, `account.debit-fee.get`. Report the quoted tier/rates separately from actual trade fees.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex account debit-fee get  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex account debit-fee set --enabled <enabled> --format json
```
