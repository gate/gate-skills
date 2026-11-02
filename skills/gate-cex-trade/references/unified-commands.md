# Unified trading account settings

## Scope and source

Read unified account mode, collateral eligibility, discount tiers and portfolio risk for the selected account before any configuration write. Mode and collateral changes can affect all positions; do not perform them implicitly to enable one trade. STP groups are trading protection administration and require the actual managing role. The risk calculator simulates a portfolio; it does not open positions. Trading loan actions are owned by margin-commands.md. Fund transfers are owned by gate-cex-assets.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `account.detail` | `gate-cli cex account detail` | read |
| `account.stp.add-users` | `gate-cli cex account stp add-users` | write |
| `account.stp.create` | `gate-cli cex account stp create` | write |
| `account.stp.list` | `gate-cli cex account stp list` | read |
| `account.stp.remove-user` | `gate-cli cex account stp remove-user` | write |
| `account.stp.users` | `gate-cli cex account stp users` | read |
| `unified.account.currencies` | `gate-cli cex unified account currencies` | read |
| `unified.account.get` | `gate-cli cex unified account get` | read |
| `unified.config.collateral` | `gate-cli cex unified config collateral` | write |
| `unified.config.discount-tiers` | `gate-cli cex unified config discount-tiers` | read |
| `unified.config.leverage-config` | `gate-cli cex unified config leverage-config` | read |
| `unified.config.leverage-get` | `gate-cli cex unified config leverage-get` | read |
| `unified.config.leverage-set` | `gate-cli cex unified config leverage-set` | write |
| `unified.config.loan-tiers` | `gate-cli cex unified config loan-tiers` | read |
| `unified.mode.get` | `gate-cli cex unified mode get` | read |
| `unified.mode.set` | `gate-cli cex unified mode set` | write |
| `unified.query.borrowable` | `gate-cli cex unified query borrowable` | read |
| `unified.query.borrowable-list` | `gate-cli cex unified query borrowable-list` | read |
| `unified.query.estimate-rate` | `gate-cli cex unified query estimate-rate` | read |
| `unified.query.transferable` | `gate-cli cex unified query transferable` | read |
| `unified.query.transferables` | `gate-cli cex unified query transferables` | read |
| `unified.risk.calculate` | `gate-cli cex unified risk calculate` | read |
| `unified.risk.units` | `gate-cli cex unified risk units` | read |
| `unified.config.delta-neutral-get` | `gate-cli cex unified config delta-neutral-get` | read |
| `unified.config.delta-neutral-set` | `gate-cli cex unified config delta-neutral-set` | write |
| `unified.config.leverage-set-all` | `gate-cli cex unified config leverage-set-all` | write |
| `unified.loan.quick-estimate` | `gate-cli cex unified loan quick-estimate` | read |
| `unified.loan.quick-repay` | `gate-cli cex unified loan quick-repay` | write |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="account.detail"></a>
### `gate-cli cex account detail`

Operation ID: `account.detail`. Effect: **read**.

Get account detail

```text
gate-cli cex account detail
```

API: `GET /api/v4/account/detail` (private).

Returns: [AccountDetail](models/unified.md#model-accountdetail).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="account.stp.add-users"></a>
### `gate-cli cex account stp add-users`

Operation ID: `account.stp.add-users`. Effect: **write**.

Add users to an STP group

```text
gate-cli cex account stp add-users [flags]
```

API: `POST /api/v4/account/stp_groups/{stp_id}/users` (private).

Returns: [][StpGroupUser](models/unified.md#model-stpgroupuser).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | STP group ID (required) |
| `--user-ids` | `string` | Yes | Unset | Comma-separated user IDs to add (required) |

<a id="account.stp.create"></a>
### `gate-cli cex account stp create`

Operation ID: `account.stp.create`. Effect: **write**.

Create an STP group

```text
gate-cli cex account stp create [flags]
```

API: `POST /api/v4/account/stp_groups` (private).

Returns: [StpGroup](models/unified.md#model-stpgroup).

API request model(s), assembled by the command: [StpGroup](models/unified.md#model-stpgroup). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--name` | `string` | Yes | Unset | Group name (required) |

<a id="account.stp.list"></a>
### `gate-cli cex account stp list`

Operation ID: `account.stp.list`. Effect: **read**.

List STP groups

```text
gate-cli cex account stp list [flags]
```

API: `GET /api/v4/account/stp_groups` (private).

Returns: [][StpGroup](models/unified.md#model-stpgroup).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--name` | `string` | No | Unset | Filter by group name |

<a id="account.stp.remove-user"></a>
### `gate-cli cex account stp remove-user`

Operation ID: `account.stp.remove-user`. Effect: **write**.

Remove a user from an STP group

```text
gate-cli cex account stp remove-user [flags]
```

API: `DELETE /api/v4/account/stp_groups/{stp_id}/users` (private).

Returns: [][StpGroupUser](models/unified.md#model-stpgroupuser).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | STP group ID (required) |
| `--user-id` | `int64` | Yes | `0` | User ID to remove (required) |

<a id="account.stp.users"></a>
### `gate-cli cex account stp users`

Operation ID: `account.stp.users`. Effect: **read**.

List users in an STP group

```text
gate-cli cex account stp users [flags]
```

API: `GET /api/v4/account/stp_groups/{stp_id}/users` (private).

Returns: [][StpGroupUser](models/unified.md#model-stpgroupuser).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `int64` | Yes | `0` | STP group ID (required) |

<a id="unified.account.currencies"></a>
### `gate-cli cex unified account currencies`

Operation ID: `unified.account.currencies`. Effect: **read**.

List loan currencies supported by unified account

```text
gate-cli cex unified account currencies
```

API: `GET /api/v4/unified/currencies` (public).

Returns: [][UnifiedCurrency](models/unified.md#model-unifiedcurrency).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="unified.account.get"></a>
### `gate-cli cex unified account get`

Operation ID: `unified.account.get`. Effect: **read**.

Get unified account balances

```text
gate-cli cex unified account get [flags]
```

API: `GET /api/v4/unified/accounts` (private).

Returns: [UnifiedAccount](models/unified.md#model-unifiedaccount).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |

<a id="unified.config.collateral"></a>
### `gate-cli cex unified config collateral`

Operation ID: `unified.config.collateral`. Effect: **write**.

Set collateral mode for unified account

```text
gate-cli cex unified config collateral [flags]
```

API: `POST /api/v4/unified/collateral_currencies` (private).

Returns: [UnifiedCollateralRes](models/unified.md#model-unifiedcollateralres).

API request model(s), assembled by the command: [UnifiedCollateralReq](models/unified.md#model-unifiedcollateralreq). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--disable` | `string` | No | Unset | Comma-separated currencies to disable as collateral |
| `--enable` | `string` | No | Unset | Comma-separated currencies to enable as collateral |
| `--type` | `int32` | Yes | `0` | Collateral type: 0=all, 1=custom (required) |

<a id="unified.config.discount-tiers"></a>
### `gate-cli cex unified config discount-tiers`

Operation ID: `unified.config.discount-tiers`. Effect: **read**.

List currency discount tiers (public, no auth)

```text
gate-cli cex unified config discount-tiers
```

API: `GET /api/v4/unified/currency_discount_tiers` (public).

Returns: [][UnifiedDiscount](models/unified.md#model-unifieddiscount).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="unified.config.leverage-config"></a>
### `gate-cli cex unified config leverage-config`

Operation ID: `unified.config.leverage-config`. Effect: **read**.

Get leverage config for a currency

```text
gate-cli cex unified config leverage-config [flags]
```

API: `GET /api/v4/unified/leverage/user_currency_config` (private).

Returns: [UnifiedLeverageConfig](models/unified.md#model-unifiedleverageconfig).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | Yes | Unset | Currency name (required) |

<a id="unified.config.leverage-get"></a>
### `gate-cli cex unified config leverage-get`

Operation ID: `unified.config.leverage-get`. Effect: **read**.

Get leverage setting for currencies

```text
gate-cli cex unified config leverage-get [flags]
```

API: `GET /api/v4/unified/leverage/user_currency_setting` (private).

Returns: [][UnifiedLeverageSetting](models/unified.md#model-unifiedleveragesetting).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |

<a id="unified.config.leverage-set"></a>
### `gate-cli cex unified config leverage-set`

Operation ID: `unified.config.leverage-set`. Effect: **write**.

Set leverage for a currency

```text
gate-cli cex unified config leverage-set [flags]
```

API: `POST /api/v4/unified/leverage/user_currency_setting` (private).

Returns: { `status`: `"ok"`, `currency`: `string`, `leverage`: `string` }.

API request model(s), assembled by the command: [UnifiedLeverageSetting](models/unified.md#model-unifiedleveragesetting). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | Yes | Unset | Currency name (required) |
| `--leverage` | `string` | Yes | Unset | Leverage multiplier (required) |

<a id="unified.config.loan-tiers"></a>
### `gate-cli cex unified config loan-tiers`

Operation ID: `unified.config.loan-tiers`. Effect: **read**.

List loan margin tiers (public, no auth)

```text
gate-cli cex unified config loan-tiers
```

API: `GET /api/v4/unified/loan_margin_tiers` (public).

Returns: [][UnifiedMarginTiers](models/unified.md#model-unifiedmargintiers).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="unified.mode.get"></a>
### `gate-cli cex unified mode get`

Operation ID: `unified.mode.get`. Effect: **read**.

Get current unified account mode

```text
gate-cli cex unified mode get
```

API: `GET /api/v4/unified/unified_mode` (private).

Returns: [UnifiedModeSet](models/unified.md#model-unifiedmodeset).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="unified.mode.set"></a>
### `gate-cli cex unified mode set`

Operation ID: `unified.mode.set`. Effect: **write**.

Set unified account mode

```text
gate-cli cex unified mode set [flags]
```

API: `PUT /api/v4/unified/unified_mode` (private).

Returns: { `status`: `"ok"`, `mode`: `string` }.

API request model(s), assembled by the command: [UnifiedModeSet](models/unified.md#model-unifiedmodeset). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--mode` | `string` | Yes | Unset | Account mode: classic, multi_currency, portfolio, single_currency (required) |

<a id="unified.query.borrowable"></a>
### `gate-cli cex unified query borrowable`

Operation ID: `unified.query.borrowable`. Effect: **read**.

Get max borrowable amount for a currency

```text
gate-cli cex unified query borrowable [flags]
```

API: `GET /api/v4/unified/borrowable` (private).

Returns: [UnifiedBorrowable](models/unified.md#model-unifiedborrowable).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | Yes | Unset | Currency name (required) |

<a id="unified.query.borrowable-list"></a>
### `gate-cli cex unified query borrowable-list`

Operation ID: `unified.query.borrowable-list`. Effect: **read**.

Batch query max borrowable amounts

```text
gate-cli cex unified query borrowable-list [flags]
```

API: `GET /api/v4/unified/batch_borrowable` (private).

Returns: [][UnifiedBorrowable](models/unified.md#model-unifiedborrowable).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currencies` | `string` | Yes | Unset | Comma-separated currency names, max 10 (required) |

<a id="unified.query.estimate-rate"></a>
### `gate-cli cex unified query estimate-rate`

Operation ID: `unified.query.estimate-rate`. Effect: **read**.

Query estimated interest rate for currencies

```text
gate-cli cex unified query estimate-rate [flags]
```

API: `GET /api/v4/unified/estimate_rate` (private).

Returns: `map[string]string`.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currencies` | `string` | Yes | Unset | Comma-separated currency names, max 10 (required) |

<a id="unified.query.transferable"></a>
### `gate-cli cex unified query transferable`

Operation ID: `unified.query.transferable`. Effect: **read**.

Get max transferable amount for a currency

```text
gate-cli cex unified query transferable [flags]
```

API: `GET /api/v4/unified/transferable` (private).

Returns: [UnifiedTransferable](models/unified.md#model-unifiedtransferable).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | Yes | Unset | Currency name (required) |

<a id="unified.query.transferables"></a>
### `gate-cli cex unified query transferables`

Operation ID: `unified.query.transferables`. Effect: **read**.

Batch query max transferable amounts

```text
gate-cli cex unified query transferables [flags]
```

API: `GET /api/v4/unified/transferables` (private).

Returns: [][TransferablesResult](models/unified.md#model-transferablesresult).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currencies` | `string` | Yes | Unset | Comma-separated currency names, max 100 (required) |

<a id="unified.risk.calculate"></a>
### `gate-cli cex unified risk calculate`

Operation ID: `unified.risk.calculate`. Effect: **read**.

CLI handler notes: Calculate portfolio margin. Provide JSON input via --input flag.
Example: gate-cli cex unified risk calculate --input '{"spot_balances":[...]}'

Calculate portfolio margin from JSON input (via stdin or --input)

```text
gate-cli cex unified risk calculate [flags]
```

API: `POST /api/v4/unified/portfolio_calculator` (public).

Returns: [UnifiedPortfolioOutput](models/unified.md#model-unifiedportfoliooutput).

API request model(s), assembled by the command: [UnifiedPortfolioInput](models/unified.md#model-unifiedportfolioinput). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--input` | `string` | Yes | Unset | Portfolio input as JSON string (required) |

<a id="unified.risk.units"></a>
### `gate-cli cex unified risk units`

Operation ID: `unified.risk.units`. Effect: **read**.

Get risk units for unified account

```text
gate-cli cex unified risk units
```

API: `GET /api/v4/unified/risk_units` (private).

Returns: [UnifiedRiskUnits](models/unified.md#model-unifiedriskunits).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

## Verification and recovery

Re-read `unified.mode.get`, account/config reads and the exact STP group as appropriate. The selected position/account state must match the requested change, including existing collateral and protections.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

Trading loans are defined in [margin actions](margin-commands.md).

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex account detail  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex account stp add-users --id <id> --user-ids <user-ids> --format json
```

<a id="unified.config.delta-neutral-get"></a>
### `gate-cli cex unified config delta-neutral-get`

Operation ID: `unified.config.delta-neutral-get`. Effect: **read**.

Get Delta-neutral strategy mode

```text
gate-cli cex unified config delta-neutral-get [flags]
```

API: `GET /api/v4/unified/delta_neutral` (private).

Returns: [DeltaNeutralEnabled](models/unified.md#model-deltaneutralenabled).

No local parameters.

<a id="unified.config.delta-neutral-set"></a>
### `gate-cli cex unified config delta-neutral-set`

Operation ID: `unified.config.delta-neutral-set`. Effect: **write**.

Enable or disable Delta-neutral strategy mode

```text
gate-cli cex unified config delta-neutral-set [flags]
```

API: `POST /api/v4/unified/delta_neutral` (private).

Returns: [DeltaNeutralEnabled](models/unified.md#model-deltaneutralenabled).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--enabled` | `bool` | Yes | `false` | Explicit true or false |

<a id="unified.config.leverage-set-all"></a>
### `gate-cli cex unified config leverage-set-all`

Operation ID: `unified.config.leverage-set-all`. Effect: **write**.

Set the account leverage; currency limits may cap the requested value

```text
gate-cli cex unified config leverage-set-all [flags]
```

API: `POST /api/v4/unified/leverage/user_setting` (private).

Returns: [][LeverageFailedCurrencies](models/unified.md#model-leveragefailedcurrencies).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--leverage` | `string` | Yes | Unset | Positive leverage multiplier as a decimal string |

<a id="unified.loan.quick-estimate"></a>
### `gate-cli cex unified loan quick-estimate`

Operation ID: `unified.loan.quick-estimate`. Effect: **read**.

Estimate quick repayment

```text
gate-cli cex unified loan quick-estimate [flags]
```

API: `GET /api/v4/unified/estimated_quick_repayment` (private).

Returns: [QuickEstimatedRepayment](models/unified.md#model-quickestimatedrepayment).

No local parameters.

<a id="unified.loan.quick-repay"></a>
### `gate-cli cex unified loan quick-repay`

Operation ID: `unified.loan.quick-repay`. Effect: **write**.

Repay liabilities using selected available currencies

```text
gate-cli cex unified loan quick-repay [flags]
```

API: `POST /api/v4/unified/quick_repayment` (private).

Returns: [QuickRepaymentResponse](models/unified.md#model-quickrepaymentresponse).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--available-currencies` | `stringSlice` | Yes | `[]` | Comma-separated repayment currencies |
| `--debt-currencies` | `stringSlice` | Yes | `[]` | Comma-separated liability currencies |

<a id="unified-quick-repayment"></a>
## Quick repayment and Delta-neutral settings

`unified.config.delta-neutral-get` reads the account's Delta-neutral strategy mode;
`delta-neutral-set --enabled=true|false` changes it. An explicit false disables the
mode; omitting the flag does not request a default change. Verify using the get
action. This account setting is separate from creating a continuing trading bot.

Quick repayment is for unified cross-currency margin or portfolio margin modes.
Read `unified.loan.quick-estimate` and the current debt/balances before
`quick-repay`. Its two required comma-separated lists select liability currencies
and the currencies to repay with; each list has 1–100 nonempty, unique identifiers.
They are currency selections, not amounts. The CLI has no repayment amount or
maximum-spend flag: stop if the user's amount cap cannot be enforced by the trusted
execution boundary. Do not infer authority to consume available assets from a
request to inspect or estimate debt.

The response contains an order ID, repaid amounts, liabilities left and funding
amounts used. Re-read debt/balances and reconcile those exact fields; acceptance
or a reduced debt is not proof that all selected debt was repaid. Do not replay an
uncertain repayment or silently add a different funding currency.

<a id="unified-leverage-partial-failure"></a>
## Set leverage across borrowed currencies

`unified.config.leverage-set-all` uses a positive decimal-string leverage value.
It affects all borrowed-currency settings, not one currency. A currency limit can
cap the requested value; outstanding loans can prevent a change. Read settings
first and obtain authority for the entire affected set; use the existing
per-currency action when only one currency is authorized.

The API's response is a **failure list**: empty `[]` means no reported currency
failure. A nonempty list returns a failed CLI exit with currency/reason details;
other currencies may already have changed and are not rolled back. Null or
malformed failure-list responses also fail. Inspect current leverage settings
before any next action. Do not retry the entire write or infer rollback from its
nonzero exit. Report confirmed successes, failures and any unresolved settings.
