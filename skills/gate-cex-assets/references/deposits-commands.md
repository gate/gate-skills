# Deposit information and records

## Scope and source

Resolve the coin, supported chain, network status, address and required memo/tag from the response. Do not replace a network or synthesize an address. An address response is not a deposit or proof of ownership of an external wallet. Deposit push-order records may represent internal flows and must retain their documented meaning. Respect minimum amount/confirmations and query a bounded history; crediting depends on the actual backend state.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `wallet.deposit.address` | `gate-cli cex wallet deposit address` | read |
| `wallet.deposit.list` | `gate-cli cex wallet deposit list` | read |
| `wallet.deposit.push-orders` | `gate-cli cex wallet deposit push-orders` | read |
| `wallet.deposit.saved` | `gate-cli cex wallet deposit saved` | read |
| `wallet.market.chains` | `gate-cli cex wallet market chains` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="wallet.deposit.address"></a>
### `gate-cli cex wallet deposit address`

Operation ID: `wallet.deposit.address`. Effect: **read**.

Get deposit address for a currency

```text
gate-cli cex wallet deposit address [flags]
```

API: `GET /api/v4/wallet/deposit_address` (private).

Returns: [DepositAddress](models/deposits.md#model-depositaddress).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | Yes | Unset | Currency name (required) |

<a id="wallet.deposit.list"></a>
### `gate-cli cex wallet deposit list`

Operation ID: `wallet.deposit.list`. Effect: **read**.

List deposit records

```text
gate-cli cex wallet deposit list [flags]
```

API: `GET /api/v4/wallet/deposits` (private).

Returns: [][DepositRecord](models/deposits.md#model-depositrecord).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency name |
| `--from` | `int64` | No | `0` | Start Unix timestamp |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--offset` | `int32` | No | `0` | Number of records to skip |
| `--to` | `int64` | No | `0` | End Unix timestamp |

<a id="wallet.deposit.push-orders"></a>
### `gate-cli cex wallet deposit push-orders`

Operation ID: `wallet.deposit.push-orders`. Effect: **read**.

List UID push orders

```text
gate-cli cex wallet deposit push-orders [flags]
```

API: `GET /api/v4/wallet/push` (private).

Returns: [][UidPushOrder](models/deposits.md#model-uidpushorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--from` | `int32` | No | `0` | Start Unix timestamp |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--offset` | `int32` | No | `0` | Number of records to skip |
| `--to` | `int32` | No | `0` | End Unix timestamp |

<a id="wallet.deposit.saved"></a>
### `gate-cli cex wallet deposit saved`

Operation ID: `wallet.deposit.saved`. Effect: **read**.

List saved withdrawal address whitelist

```text
gate-cli cex wallet deposit saved [flags]
```

API: `GET /api/v4/wallet/saved_address` (private).

Returns: [][SavedAddress](models/deposits.md#model-savedaddress).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--chain` | `string` | No | Unset | Filter by chain name |
| `--currency` | `string` | Yes | Unset | Currency name (required) |
| `--limit` | `int32` | No | `20` | Records per page (1-100) |

<a id="wallet.market.chains"></a>
### `gate-cli cex wallet market chains`

Operation ID: `wallet.market.chains`. Effect: **read**.

List supported chains for a currency (public, no authentication required)

```text
gate-cli cex wallet market chains [flags]
```

API: `GET /api/v4/wallet/currency_chains` (public).

Returns: [][CurrencyChain](models/deposits.md#model-currencychain).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | Yes | Unset | Currency name (required) |

## Verification and recovery

Use `wallet.deposit.list` and the actual deposit transaction/network/status. An address query alone cannot prove a transfer or credit.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex wallet deposit address --currency <currency> --format json
```
