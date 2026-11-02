# Small-balance conversion

## Scope and source

Read eligible holdings and the actual conversion asset/terms. Confirm the selected currency set and expected spend; listing dust does not authorize converting every asset. convert-small is a write and may have partial outcomes. Query small-history and balances afterward; report fees and received quantity only when supplied.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `wallet.balance.convert-small` | `gate-cli cex wallet balance convert-small` | write |
| `wallet.balance.small` | `gate-cli cex wallet balance small` | read |
| `wallet.balance.small-history` | `gate-cli cex wallet balance small-history` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="wallet.balance.convert-small"></a>
### `gate-cli cex wallet balance convert-small`

Operation ID: `wallet.balance.convert-small`. Effect: **write**.

Convert small balances to GT

```text
gate-cli cex wallet balance convert-small [flags]
```

API: `POST /api/v4/wallet/small_balance` (private).

Returns: Array of objects: `{Status: "success"}`.

API request model(s), assembled by the command: [ConvertSmallBalance](models/small-balance.md#model-convertsmallbalance). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--all` | `bool` | No | `false` | Convert all small balances |
| `--currencies` | `stringSlice` | No | `[]` | Currencies to convert (omit for all) |

<a id="wallet.balance.small"></a>
### `gate-cli cex wallet balance small`

Operation ID: `wallet.balance.small`. Effect: **read**.

List small balances convertible to GT

```text
gate-cli cex wallet balance small
```

API: `GET /api/v4/wallet/small_balance` (private).

Returns: [][SmallBalance](models/small-balance.md#model-smallbalance).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="wallet.balance.small-history"></a>
### `gate-cli cex wallet balance small-history`

Operation ID: `wallet.balance.small-history`. Effect: **read**.

List small balance conversion history

```text
gate-cli cex wallet balance small-history [flags]
```

API: `GET /api/v4/wallet/small_balance_history` (private).

Returns: [][SmallBalanceHistory](models/small-balance.md#model-smallbalancehistory).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--page` | `int32` | No | `0` | Page number |

## Verification and recovery

Use `wallet.balance.small-history` and balances; verify each currency spent and the actual received quantity, preserving partial outcomes.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex wallet balance small  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex wallet balance convert-small  --format json
```
