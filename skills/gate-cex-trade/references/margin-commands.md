# Spot margin and trading loans

## Scope and source

Distinguish isolated margin, cross margin and unified borrowing. Read the account mode, loan currency, available collateral, interest and liquidation exposure. Borrow/repay, leverage and auto-repay changes require explicit authority. Margin orders use the canonical [spot account selection](spot-commands.md#spot-account-selection) and [attached protection](spot-commands.md#spot-attached-protection) rules. Buy/sell expose account and automatic borrow/repay flags with product-specific constraints; do not invent a separate margin-order endpoint. Do not infer native linked orders or automatic borrowing from a buy request. Independent multi-collateral loans belong to gate-cex-earn.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `margin.account.book` | `gate-cli cex margin account book` | read |
| `margin.account.funding` | `gate-cli cex margin account funding` | read |
| `margin.account.list` | `gate-cli cex margin account list` | read |
| `margin.account.transferable` | `gate-cli cex margin account transferable` | read |
| `margin.account.user-info` | `gate-cli cex margin account user-info` | read |
| `margin.auto-repay.get` | `gate-cli cex margin auto-repay get` | read |
| `margin.auto-repay.set` | `gate-cli cex margin auto-repay set` | write |
| `margin.cross.loans` | `gate-cli cex margin cross loans` | read |
| `margin.cross.repayments` | `gate-cli cex margin cross repayments` | read |
| `margin.leverage.set` | `gate-cli cex margin leverage set` | write |
| `margin.tier.market` | `gate-cli cex margin tier market` | read |
| `margin.tier.user` | `gate-cli cex margin tier user` | read |
| `margin.uni.borrowable` | `gate-cli cex margin uni borrowable` | read |
| `margin.uni.estimate-rate` | `gate-cli cex margin uni estimate-rate` | read |
| `margin.uni.interest-records` | `gate-cli cex margin uni interest-records` | read |
| `margin.uni.lend` | `gate-cli cex margin uni lend` | write |
| `margin.uni.loan-records` | `gate-cli cex margin uni loan-records` | read |
| `margin.uni.loans` | `gate-cli cex margin uni loans` | read |
| `margin.uni.pair` | `gate-cli cex margin uni pair` | read |
| `margin.uni.pairs` | `gate-cli cex margin uni pairs` | read |
| `spot.order.cross-liquidate` | `gate-cli cex spot order cross-liquidate` | write |
| `unified.loan.create` | `gate-cli cex unified loan create` | write |
| `unified.loan.history-rate` | `gate-cli cex unified loan history-rate` | read |
| `unified.loan.interest` | `gate-cli cex unified loan interest` | read |
| `unified.loan.list` | `gate-cli cex unified loan list` | read |
| `unified.loan.records` | `gate-cli cex unified loan records` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="margin.account.book"></a>
### `gate-cli cex margin account book`

Operation ID: `margin.account.book`. Effect: **read**.

List margin account book records

```text
gate-cli cex margin account book [flags]
```

API: `GET /api/v4/margin/account_book` (private).

Returns: [][MarginAccountBook](models/margin.md#model-marginaccountbook).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |
| `--from` | `int64` | No | `0` | Start Unix timestamp |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--page` | `int32` | No | `0` | Page number |
| `--pair` | `string` | No | Unset | Filter by currency pair |
| `--to` | `int64` | No | `0` | End Unix timestamp |
| `--type` | `string` | No | Unset | Filter by type |

<a id="margin.account.funding"></a>
### `gate-cli cex margin account funding`

Operation ID: `margin.account.funding`. Effect: **read**.

List funding accounts

```text
gate-cli cex margin account funding [flags]
```

API: `GET /api/v4/margin/funding_accounts` (private).

Returns: [][FundingAccount](models/margin.md#model-fundingaccount).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |

<a id="margin.account.list"></a>
### `gate-cli cex margin account list`

Operation ID: `margin.account.list`. Effect: **read**.

List margin accounts

```text
gate-cli cex margin account list [flags]
```

API: `GET /api/v4/margin/accounts` (private).

Returns: [][MarginAccount](models/margin.md#model-marginaccount).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--pair` | `string` | No | Unset | Filter by currency pair |

<a id="margin.account.transferable"></a>
### `gate-cli cex margin account transferable`

Operation ID: `margin.account.transferable`. Effect: **read**.

Get maximum transferable amount for isolated margin

```text
gate-cli cex margin account transferable [flags]
```

API: `GET /api/v4/margin/transferable` (private).

Returns: [MarginTransferable](models/margin.md#model-margintransferable).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | Yes | Unset | Currency name (required) |
| `--pair` | `string` | No | Unset | Currency pair |

<a id="margin.account.user-info"></a>
### `gate-cli cex margin account user-info`

Operation ID: `margin.account.user-info`. Effect: **read**.

List user's isolated margin accounts

```text
gate-cli cex margin account user-info [flags]
```

API: `GET /api/v4/margin/user/account` (private).

Returns: [][MarginAccount](models/margin.md#model-marginaccount).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--pair` | `string` | No | Unset | Filter by currency pair |

<a id="margin.auto-repay.get"></a>
### `gate-cli cex margin auto-repay get`

Operation ID: `margin.auto-repay.get`. Effect: **read**.

Get current auto-repay status

```text
gate-cli cex margin auto-repay get
```

API: `GET /api/v4/margin/auto_repay` (private).

Returns: [AutoRepaySetting](models/margin.md#model-autorepaysetting).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="margin.auto-repay.set"></a>
### `gate-cli cex margin auto-repay set`

Operation ID: `margin.auto-repay.set`. Effect: **write**.

Enable or disable auto-repay

```text
gate-cli cex margin auto-repay set [flags]
```

API: `POST /api/v4/margin/auto_repay` (private).

Returns: [AutoRepaySetting](models/margin.md#model-autorepaysetting).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--status` | `string` | Yes | Unset | Auto-repay status: on or off (required) |

<a id="margin.cross.loans"></a>
### `gate-cli cex margin cross loans`

Operation ID: `margin.cross.loans`. Effect: **read**.

List cross margin loans

```text
gate-cli cex margin cross loans [flags]
```

API: `GET /api/v4/margin/cross/loans` (private).

Returns: [][CrossMarginLoan](models/margin.md#model-crossmarginloan).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--offset` | `int32` | No | `0` | Record offset for pagination |
| `--status` | `int32` | No | `2` | Loan status (default 2: borrowed) |

<a id="margin.cross.repayments"></a>
### `gate-cli cex margin cross repayments`

Operation ID: `margin.cross.repayments`. Effect: **read**.

List cross margin repayments

```text
gate-cli cex margin cross repayments [flags]
```

API: `GET /api/v4/margin/cross/repayments` (private).

Returns: [][CrossMarginRepayment](models/margin.md#model-crossmarginrepayment).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--offset` | `int32` | No | `0` | Record offset for pagination |

<a id="margin.leverage.set"></a>
### `gate-cli cex margin leverage set`

Operation ID: `margin.leverage.set`. Effect: **write**.

Set user market leverage

```text
gate-cli cex margin leverage set [flags]
```

API: `POST /api/v4/margin/leverage/user_market_setting` (private).

Returns: { `message`: `"leverage set successfully"`, `currency_pair`: `string`, `leverage`: `string` }.

API request model(s), assembled by the command: [MarginMarketLeverage](models/margin.md#model-marginmarketleverage). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--leverage` | `string` | Yes | Unset | Leverage value (required) |
| `--pair` | `string` | Yes | Unset | Currency pair (required) |

<a id="margin.tier.market"></a>
### `gate-cli cex margin tier market`

Operation ID: `margin.tier.market`. Effect: **read**.

Get market margin leverage tier (public)

```text
gate-cli cex margin tier market [flags]
```

API: `GET /api/v4/margin/loan_margin_tiers` (public).

Returns: [][MarginLeverageTier](models/margin.md#model-marginleveragetier).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--pair` | `string` | Yes | Unset | Currency pair (required) |

<a id="margin.tier.user"></a>
### `gate-cli cex margin tier user`

Operation ID: `margin.tier.user`. Effect: **read**.

Get user margin leverage tier

```text
gate-cli cex margin tier user [flags]
```

API: `GET /api/v4/margin/user/loan_margin_tiers` (private).

Returns: [][MarginLeverageTier](models/margin.md#model-marginleveragetier).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--pair` | `string` | Yes | Unset | Currency pair (required) |

<a id="margin.uni.borrowable"></a>
### `gate-cli cex margin uni borrowable`

Operation ID: `margin.uni.borrowable`. Effect: **read**.

Get maximum borrowable amount

```text
gate-cli cex margin uni borrowable [flags]
```

API: `GET /api/v4/margin/uni/borrowable` (private).

Returns: [MaxUniBorrowable](models/margin.md#model-maxuniborrowable).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | Yes | Unset | Currency name (required) |
| `--pair` | `string` | Yes | Unset | Currency pair (required) |

<a id="margin.uni.estimate-rate"></a>
### `gate-cli cex margin uni estimate-rate`

Operation ID: `margin.uni.estimate-rate`. Effect: **read**.

Get estimated interest rates

```text
gate-cli cex margin uni estimate-rate [flags]
```

API: `GET /api/v4/margin/uni/estimate_rate` (private).

Returns: `map[string]string`.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currencies` | `string` | Yes | Unset | Comma-separated currency list, e.g. BTC,ETH (required) |

<a id="margin.uni.interest-records"></a>
### `gate-cli cex margin uni interest-records`

Operation ID: `margin.uni.interest-records`. Effect: **read**.

List uni loan interest records

```text
gate-cli cex margin uni interest-records [flags]
```

API: `GET /api/v4/margin/uni/interest_records` (private).

Returns: [][UniLoanInterestRecord](models/margin.md#model-uniloaninterestrecord).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |
| `--from` | `int64` | No | `0` | Start Unix timestamp |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--page` | `int32` | No | `0` | Page number |
| `--pair` | `string` | No | Unset | Filter by currency pair |
| `--to` | `int64` | No | `0` | End Unix timestamp |

<a id="margin.uni.lend"></a>
### `gate-cli cex margin uni lend`

Operation ID: `margin.uni.lend`. Effect: **write**.

Create a uni loan (borrow)

```text
gate-cli cex margin uni lend [flags]
```

API: `POST /api/v4/margin/uni/loans` (private).

Returns: { `message`: `"loan created successfully"`, `currency`: `string`, `amount`: `string`, `currency_pair`: `string` }.

API request model(s), assembled by the command: [CreateUniLoan](models/margin.md#model-createuniloan). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--amount` | `string` | Yes | Unset | Borrow amount (required) |
| `--currency` | `string` | Yes | Unset | Currency to borrow (required) |
| `--pair` | `string` | Yes | Unset | Currency pair (required) |
| `--type` | `string` | No | `margin` | Loan type (default: margin) |

<a id="margin.uni.loan-records"></a>
### `gate-cli cex margin uni loan-records`

Operation ID: `margin.uni.loan-records`. Effect: **read**.

List uni loan records

```text
gate-cli cex margin uni loan-records [flags]
```

API: `GET /api/v4/margin/uni/loan_records` (private).

Returns: [][UniLoanRecord](models/margin.md#model-uniloanrecord).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--page` | `int32` | No | `0` | Page number |
| `--pair` | `string` | No | Unset | Filter by currency pair |
| `--type` | `string` | No | Unset | Filter by type: borrow or repay |

<a id="margin.uni.loans"></a>
### `gate-cli cex margin uni loans`

Operation ID: `margin.uni.loans`. Effect: **read**.

List uni loans

```text
gate-cli cex margin uni loans [flags]
```

API: `GET /api/v4/margin/uni/loans` (private).

Returns: [][UniLoan](models/margin.md#model-uniloan).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--page` | `int32` | No | `0` | Page number |
| `--pair` | `string` | No | Unset | Filter by currency pair |

<a id="margin.uni.pair"></a>
### `gate-cli cex margin uni pair`

Operation ID: `margin.uni.pair`. Effect: **read**.

Get uni currency pair detail (public)

```text
gate-cli cex margin uni pair [flags]
```

API: `GET /api/v4/margin/uni/currency_pairs/{currency_pair}` (public).

Returns: [UniCurrencyPair](models/margin.md#model-unicurrencypair).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--pair` | `string` | Yes | Unset | Currency pair, e.g. BTC_USDT (required) |

<a id="margin.uni.pairs"></a>
### `gate-cli cex margin uni pairs`

Operation ID: `margin.uni.pairs`. Effect: **read**.

List all uni currency pairs (public)

```text
gate-cli cex margin uni pairs
```

API: `GET /api/v4/margin/uni/currency_pairs` (public).

Returns: [][UniCurrencyPair](models/margin.md#model-unicurrencypair).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="spot.order.cross-liquidate"></a>
### `gate-cli cex spot order cross-liquidate`

Operation ID: `spot.order.cross-liquidate`. Effect: **write**.

Create a cross margin liquidation order

```text
gate-cli cex spot order cross-liquidate [flags]
```

API: `POST /api/v4/spot/cross_liquidate_orders` (private).

Returns: [Order](models/margin.md#model-order).

API request model(s), assembled by the command: [LiquidateOrder](models/margin.md#model-liquidateorder). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--amount` | `string` | Yes | Unset | Trade amount (required) |
| `--pair` | `string` | Yes | Unset | Currency pair (required) |
| `--price` | `string` | Yes | Unset | Order price (required) |

<a id="unified.loan.create"></a>
### `gate-cli cex unified loan create`

Operation ID: `unified.loan.create`. Effect: **write**.

Borrow or repay in unified account

```text
gate-cli cex unified loan create [flags]
```

API: `POST /api/v4/unified/loans` (private).

Returns: [UnifiedLoanResult](models/margin.md#model-unifiedloanresult).

API request model(s), assembled by the command: [UnifiedLoan](models/margin.md#model-unifiedloan). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--amount` | `string` | Yes | Unset | Amount (required) |
| `--currency` | `string` | Yes | Unset | Currency to borrow/repay (required) |
| `--type` | `string` | No | `borrow` | Operation type: borrow, repay |

<a id="unified.loan.history-rate"></a>
### `gate-cli cex unified loan history-rate`

Operation ID: `unified.loan.history-rate`. Effect: **read**.

Get historical lending rates for a currency

```text
gate-cli cex unified loan history-rate [flags]
```

API: `GET /api/v4/unified/history_loan_rate` (public).

Returns: [UnifiedHistoryLoanRate](models/margin.md#model-unifiedhistoryloanrate).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | Yes | Unset | Currency name (required) |
| `--limit` | `int32` | No | `0` | Max records to return |
| `--page` | `int32` | No | `0` | Page number |
| `--tier` | `string` | No | Unset | VIP tier for floating rate |

<a id="unified.loan.interest"></a>
### `gate-cli cex unified loan interest`

Operation ID: `unified.loan.interest`. Effect: **read**.

List loan interest records

```text
gate-cli cex unified loan interest [flags]
```

API: `GET /api/v4/unified/interest_records` (private).

Returns: [][UniLoanInterestRecord](models/margin.md#model-uniloaninterestrecord).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |
| `--from` | `int64` | No | `0` | Start Unix timestamp |
| `--limit` | `int32` | No | `0` | Max records to return |
| `--page` | `int32` | No | `0` | Page number |
| `--to` | `int64` | No | `0` | End Unix timestamp |
| `--type` | `string` | No | Unset | Filter by type |

<a id="unified.loan.list"></a>
### `gate-cli cex unified loan list`

Operation ID: `unified.loan.list`. Effect: **read**.

List current unified loans

```text
gate-cli cex unified loan list [flags]
```

API: `GET /api/v4/unified/loans` (private).

Returns: [][UniLoan](models/margin.md#model-uniloan).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |
| `--limit` | `int32` | No | `0` | Max records to return |
| `--page` | `int32` | No | `0` | Page number |
| `--type` | `string` | No | Unset | Filter by type: platform, margin |

<a id="unified.loan.records"></a>
### `gate-cli cex unified loan records`

Operation ID: `unified.loan.records`. Effect: **read**.

List loan records

```text
gate-cli cex unified loan records [flags]
```

API: `GET /api/v4/unified/loan_records` (private).

Returns: [][UnifiedLoanRecord](models/margin.md#model-unifiedloanrecord).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |
| `--limit` | `int32` | No | `0` | Max records to return |
| `--page` | `int32` | No | `0` | Page number |
| `--type` | `string` | No | Unset | Filter by type: borrow, repay |

## Verification and recovery

Use `margin.uni.loans`/`margin.uni.loan-records`, cross loans/repayments or `unified.loan.list`/records for the actual loan family; verify debt and interest. Verify margin orders through the spot contract. Do not confuse an accepted repay with zero remaining debt.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

Spot margin order parameters are defined in [spot actions](spot-commands.md).

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex margin account book  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex margin auto-repay set --status <status> --format json
```
