# Asset balances and histories

## Scope and source

Read only the requested accounts/currencies and bounded time range. Separate available, locked, borrowed, equity and estimated valuation fields. A total valuation is not withdrawable balance; preserve account and settlement units. Subaccount balance reads need managing authority. Snapshots and API-permission status must not be invented from account labels. Trading, lending, mode changes and fund movements need their owning action contracts.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `wallet.balance.sub` | `gate-cli cex wallet balance sub` | read |
| `wallet.balance.sub-cross-margin` | `gate-cli cex wallet balance sub-cross-margin` | read |
| `wallet.balance.sub-futures` | `gate-cli cex wallet balance sub-futures` | read |
| `wallet.balance.sub-margin` | `gate-cli cex wallet balance sub-margin` | read |
| `wallet.balance.total` | `gate-cli cex wallet balance total` | read |
| `wallet.market.low-cap` | `gate-cli cex wallet market low-cap` | read |
| `wallet.market.trade-fee` | `gate-cli cex wallet market trade-fee` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="wallet.balance.sub"></a>
### `gate-cli cex wallet balance sub`

Operation ID: `wallet.balance.sub`. Effect: **read**.

List sub-account spot balances

```text
gate-cli cex wallet balance sub [flags]
```

API: `GET /api/v4/wallet/sub_account_balances` (private).

Returns: [][SubAccountBalance](models/balances.md#model-subaccountbalance).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--limit` | `int32` | No | `0` | Page size, max 100 (default 100) |
| `--page` | `int32` | No | `0` | Page number (default 1) |
| `--sub-uid` | `string` | No | Unset | Filter by sub-account user IDs (comma-separated) |

<a id="wallet.balance.sub-cross-margin"></a>
### `gate-cli cex wallet balance sub-cross-margin`

Operation ID: `wallet.balance.sub-cross-margin`. Effect: **read**.

List sub-account cross-margin account balances

```text
gate-cli cex wallet balance sub-cross-margin [flags]
```

API: `GET /api/v4/wallet/sub_account_cross_margin_balances` (private).

Returns: [][SubAccountCrossMarginBalance](models/balances.md#model-subaccountcrossmarginbalance).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--sub-uid` | `string` | No | Unset | Filter by sub-account user IDs (comma-separated) |

<a id="wallet.balance.sub-futures"></a>
### `gate-cli cex wallet balance sub-futures`

Operation ID: `wallet.balance.sub-futures`. Effect: **read**.

List sub-account perpetual futures account balances

```text
gate-cli cex wallet balance sub-futures [flags]
```

API: `GET /api/v4/wallet/sub_account_futures_balances` (private).

Returns: [][SubAccountFuturesBalance](models/balances.md#model-subaccountfuturesbalance).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--settle` | `string` | No | Unset | Filter by settlement currency |
| `--sub-uid` | `string` | No | Unset | Filter by sub-account user IDs (comma-separated) |

<a id="wallet.balance.sub-margin"></a>
### `gate-cli cex wallet balance sub-margin`

Operation ID: `wallet.balance.sub-margin`. Effect: **read**.

List sub-account margin account balances

```text
gate-cli cex wallet balance sub-margin [flags]
```

API: `GET /api/v4/wallet/sub_account_margin_balances` (private).

Returns: [][SubAccountMarginBalance](models/balances.md#model-subaccountmarginbalance).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--sub-uid` | `string` | No | Unset | Filter by sub-account user IDs (comma-separated) |

<a id="wallet.balance.total"></a>
### `gate-cli cex wallet balance total`

Operation ID: `wallet.balance.total`. Effect: **read**.

Get total estimated balance across all accounts

```text
gate-cli cex wallet balance total [flags]
```

API: `GET /api/v4/wallet/total_balance` (private).

Returns: [TotalBalance](models/balances.md#model-totalbalance).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Target currency for conversion (BTC, CNY, USD, USDT) |

<a id="wallet.market.low-cap"></a>
### `gate-cli cex wallet market low-cap`

Operation ID: `wallet.market.low-cap`. Effect: **read**.

List currencies available for low-cap exchange

```text
gate-cli cex wallet market low-cap
```

API: `GET /api/v4/wallet/getLowCapExchangeList` (private).

Returns: `[]string`.

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="wallet.market.trade-fee"></a>
### `gate-cli cex wallet market trade-fee`

Operation ID: `wallet.market.trade-fee`. Effect: **read**.

Get personal trading fee rates

```text
gate-cli cex wallet market trade-fee [flags]
```

API: `GET /api/v4/wallet/fee` (private).

Returns: [TradeFee](models/balances.md#model-tradefee).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency-pair` | `string` | No | Unset | Specify currency pair for more accurate fee settings |
| `--settle` | `string` | No | Unset | Specify settlement currency for contract fees |

## Verification and recovery

Check currency and account identifiers and distinguish available funds from aggregate estimates; keep the requested history interval and valuation timestamp.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex wallet balance sub  --format json
```
