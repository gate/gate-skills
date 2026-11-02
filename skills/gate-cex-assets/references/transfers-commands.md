# Internal and product transfers

## Scope and source

Specify source/destination accounts from the selected execution context, any required subaccount UID, currency and exact amount. Stock/CFD deposit or withdraw directions move funds between spot and the product, not a blockchain address. Stock transfer requires a stable ref-id; an exact ref-id transaction query is used alone. CFD has no transfer-reference flag, so ambiguous outcomes can require manual reconciliation. Check available/transferable amounts, then query transfer status or product transactions. Never replay an ambiguous transfer or sweep all balances by default.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `stock.account.transactions` | `gate-cli cex stock account transactions` | read |
| `stock.account.transfer` | `gate-cli cex stock account transfer` | write |
| `tradfi.account.transactions` | `gate-cli cex tradfi account transactions` | read |
| `tradfi.account.transfer` | `gate-cli cex tradfi account transfer` | write |
| `wallet.transfer.create` | `gate-cli cex wallet transfer create` | write |
| `wallet.transfer.status` | `gate-cli cex wallet transfer status` | read |
| `wallet.transfer.sub-list` | `gate-cli cex wallet transfer sub-list` | read |
| `wallet.transfer.sub-to-sub` | `gate-cli cex wallet transfer sub-to-sub` | write |
| `wallet.transfer.to-sub` | `gate-cli cex wallet transfer to-sub` | write |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="stock.account.transactions"></a>
### `gate-cli cex stock account transactions`

Operation ID: `stock.account.transactions`. Effect: **read**.

Query stock transaction records

```text
gate-cli cex stock account transactions [flags]
```

API: `GET /api/v4/stock/transactions` (private).

Returns: [TransactionList2](models/transfers.md#model-transactionlist2).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--begin` | `int64` | No | `0` | Begin Unix seconds |
| `--end` | `int64` | No | `0` | End Unix seconds |
| `--page` | `int32` | No | `1` | Page number |
| `--page-size` | `int32` | No | `10` | Page size (1-500) |
| `--ref-id` | `string` | No | Unset | Query an exact business reference |
| `--type` | `string` | No | Unset | Transaction type |

<a id="stock.account.transfer"></a>
### `gate-cli cex stock account transfer`

Operation ID: `stock.account.transfer`. Effect: **write**.

Transfer once using a caller-supplied idempotency reference

```text
gate-cli cex stock account transfer [flags]
```

API: `POST /api/v4/stock/transactions` (private).

Returns: [CreateTransaction2](models/transfers.md#model-createtransaction2).

API request model(s), assembled by the command: [TradFiSpotTransactionRequest](models/transfers.md#model-tradfispottransactionrequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--asset` | `string` | No | `USDT` | Asset: USDT |
| `--change` | `string` | Yes | Unset | change (required) |
| `--ref-id` | `string` | Yes | Unset | ref-id (required) |
| `--type` | `string` | Yes | Unset | type (required) |

<a id="tradfi.account.transactions"></a>
### `gate-cli cex tradfi account transactions`

Operation ID: `tradfi.account.transactions`. Effect: **read**.

List TradFi account transactions

```text
gate-cli cex tradfi account transactions [flags]
```

API: `GET /api/v4/tradfi/transactions` (private).

Returns: [TransactionList](models/transfers.md#model-transactionlist).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--begin` | `int64` | No | `0` | Begin timestamp (Unix seconds) |
| `--end` | `int64` | No | `0` | End timestamp (Unix seconds) |
| `--page` | `int32` | No | `1` | Page number |
| `--page-size` | `int32` | No | `20` | Number of records per page |
| `--type` | `string` | No | Unset | Transaction type filter |

<a id="tradfi.account.transfer"></a>
### `gate-cli cex tradfi account transfer`

Operation ID: `tradfi.account.transfer`. Effect: **write**.

Transfer funds into or out of the TradFi account

```text
gate-cli cex tradfi account transfer [flags]
```

API: `POST /api/v4/tradfi/transactions` (private).

Returns: [CreateTransaction](models/transfers.md#model-createtransaction).

API request model(s), assembled by the command: [TradFiTransactionRequest](models/transfers.md#model-tradfitransactionrequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--asset` | `string` | No | `USDT` | Asset type, e.g. USDT |
| `--change` | `string` | Yes | Unset | Amount to transfer (required) |
| `--type` | `string` | Yes | Unset | Transaction type: deposit (transfer in) or withdraw (transfer out) (required) |

<a id="wallet.transfer.create"></a>
### `gate-cli cex wallet transfer create`

Operation ID: `wallet.transfer.create`. Effect: **write**.

Transfer between accounts

```text
gate-cli cex wallet transfer create [flags]
```

API: `POST /api/v4/wallet/transfers` (private).

Returns: [TransactionId](models/transfers.md#model-transactionid).

API request model(s), assembled by the command: [Transfer](models/transfers.md#model-transfer). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--amount` | `string` | Yes | Unset | Transfer amount (required) |
| `--currency` | `string` | Yes | Unset | Currency name (required) |
| `--currency-pair` | `string` | Conditional | Unset | Margin trading pair (required for margin accounts) |
| `--from` | `string` | Yes | Unset | Source account type (required) |
| `--to` | `string` | Yes | Unset | Destination account type (required) |

<a id="wallet.transfer.status"></a>
### `gate-cli cex wallet transfer status`

Operation ID: `wallet.transfer.status`. Effect: **read**.

Query main-sub account transfer status

```text
gate-cli cex wallet transfer status [flags]
```

API: `GET /api/v4/wallet/order_status` (private).

Returns: [TransferOrderStatus](models/transfers.md#model-transferorderstatus).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--client-order-id` | `string` | No | Unset | Client-defined transfer order ID |
| `--tx-id` | `string` | No | Unset | Transaction ID returned from transfer |

<a id="wallet.transfer.sub-list"></a>
### `gate-cli cex wallet transfer sub-list`

Operation ID: `wallet.transfer.sub-list`. Effect: **read**.

List transfer records between main and sub accounts

```text
gate-cli cex wallet transfer sub-list [flags]
```

API: `GET /api/v4/wallet/sub_account_transfers` (private).

Returns: [][SubAccountTransferRecordItem](models/transfers.md#model-subaccounttransferrecorditem).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--from` | `int64` | No | `0` | Start Unix timestamp |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--offset` | `int32` | No | `0` | Number of records to skip |
| `--sub-uid` | `string` | No | Unset | Filter by sub-account user ID |
| `--to` | `int64` | No | `0` | End Unix timestamp |

<a id="wallet.transfer.sub-to-sub"></a>
### `gate-cli cex wallet transfer sub-to-sub`

Operation ID: `wallet.transfer.sub-to-sub`. Effect: **write**.

Transfer between sub accounts

```text
gate-cli cex wallet transfer sub-to-sub [flags]
```

API: `POST /api/v4/wallet/sub_account_to_sub_account` (private).

Returns: [TransactionId](models/transfers.md#model-transactionid).

API request model(s), assembled by the command: [SubAccountToSubAccount](models/transfers.md#model-subaccounttosubaccount). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--amount` | `string` | Yes | Unset | Transfer amount (required) |
| `--currency` | `string` | Yes | Unset | Currency name (required) |
| `--from-type` | `string` | Yes | Unset | Source sub-account type (required) |
| `--from-uid` | `string` | Yes | Unset | Source sub-account user ID (required) |
| `--to-type` | `string` | Yes | Unset | Destination sub-account type (required) |
| `--to-uid` | `string` | Yes | Unset | Destination sub-account user ID (required) |

<a id="wallet.transfer.to-sub"></a>
### `gate-cli cex wallet transfer to-sub`

Operation ID: `wallet.transfer.to-sub`. Effect: **write**.

Transfer between main and sub accounts

```text
gate-cli cex wallet transfer to-sub [flags]
```

API: `POST /api/v4/wallet/sub_account_transfers` (private).

Returns: [TransactionId](models/transfers.md#model-transactionid).

API request model(s), assembled by the command: [SubAccountTransfer](models/transfers.md#model-subaccounttransfer). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--amount` | `string` | Yes | Unset | Transfer amount (required) |
| `--currency` | `string` | Yes | Unset | Currency name (required) |
| `--direction` | `string` | Yes | Unset | Transfer direction: to or from (required) |
| `--sub-account` | `string` | Yes | Unset | Sub-account user ID (required) |
| `--sub-account-type` | `string` | No | Unset | Sub-account trading account type |

## Verification and recovery

Use `wallet.transfer.status` for the returned transfer ID or product transactions for the exact known reference. Stock ref-id must be used alone in its transaction query. If a CFD transfer has no uniquely reconcilable reference, report unknown rather than matching a similar recent amount.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex stock account transactions  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex stock account transfer --change <change> --ref-id <ref-id> --type <type> --format json
```
