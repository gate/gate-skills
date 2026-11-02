# Withdrawals

## Scope and source

Before a withdrawal, establish the exact destination, network, tag/memo, currency, amount, fee interpretation, recipient/account context and authority. Read chain/withdraw-status and saved destination information where available. Create, cancel and push-order are writes. Follow existing official KYC/AML, sanctions and applicable transfer-information requirements; there is no invented Travel Rule bypass or address-book editor here. Query withdrawal records and status after submission. A cancelled request or accepted withdrawal is not proof of chain settlement.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `wallet.deposit.withdrawals` | `gate-cli cex wallet deposit withdrawals` | read |
| `wallet.market.withdraw-status` | `gate-cli cex wallet market withdraw-status` | read |
| `withdrawal.cancel` | `gate-cli cex withdrawal cancel` | write |
| `withdrawal.create` | `gate-cli cex withdrawal create` | write |
| `withdrawal.push-order` | `gate-cli cex withdrawal push-order` | write |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="wallet.deposit.withdrawals"></a>
### `gate-cli cex wallet deposit withdrawals`

Operation ID: `wallet.deposit.withdrawals`. Effect: **read**.

List withdrawal records

```text
gate-cli cex wallet deposit withdrawals [flags]
```

API: `GET /api/v4/wallet/withdrawals` (private).

Returns: [][WithdrawalRecord](models/withdrawals.md#model-withdrawalrecord).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency name |
| `--from` | `int64` | No | `0` | Start Unix timestamp |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--offset` | `int32` | No | `0` | Number of records to skip |
| `--to` | `int64` | No | `0` | End Unix timestamp |

<a id="wallet.market.withdraw-status"></a>
### `gate-cli cex wallet market withdraw-status`

Operation ID: `wallet.market.withdraw-status`. Effect: **read**.

List withdrawal status for currencies

```text
gate-cli cex wallet market withdraw-status [flags]
```

API: `GET /api/v4/wallet/withdraw_status` (private).

Returns: [][WithdrawStatus](models/withdrawals.md#model-withdrawstatus).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Filter by currency name |

<a id="withdrawal.cancel"></a>
### `gate-cli cex withdrawal cancel`

Operation ID: `withdrawal.cancel`. Effect: **write**.

Cancel a pending withdrawal

```text
gate-cli cex withdrawal cancel [flags]
```

API: `DELETE /api/v4/withdrawals/{withdrawal_id}` (private).

Returns: [WithdrawalsDel](models/withdrawals.md#model-withdrawalsdel).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `string` | Yes | Unset | Withdrawal ID (required) |

<a id="withdrawal.create"></a>
### `gate-cli cex withdrawal create`

Operation ID: `withdrawal.create`. Effect: **write**.

Create a new withdrawal

```text
gate-cli cex withdrawal create [flags]
```

API: `POST /api/v4/withdrawals` (private).

Returns: [LedgerRecord](models/withdrawals.md#model-ledgerrecord).

API request model(s), assembled by the command: [LedgerRecord](models/withdrawals.md#model-ledgerrecord). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--address` | `string` | Yes | Unset | Withdrawal address (required) |
| `--amount` | `string` | Yes | Unset | Withdrawal amount (required) |
| `--chain` | `string` | No | Unset | Chain name |
| `--currency` | `string` | Yes | Unset | Currency name (required) |
| `--memo` | `string` | No | Unset | Memo/tag for the withdrawal |

<a id="withdrawal.push-order"></a>
### `gate-cli cex withdrawal push-order`

Operation ID: `withdrawal.push-order`. Effect: **write**.

UID transfer between main spot accounts

```text
gate-cli cex withdrawal push-order [flags]
```

API: `POST /api/v4/withdrawals/push` (private).

Returns: [UidPushWithdrawalResp](models/withdrawals.md#model-uidpushwithdrawalresp).

API request model(s), assembled by the command: [UidPushWithdrawal](models/withdrawals.md#model-uidpushwithdrawal). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--amount` | `string` | Yes | Unset | Transfer amount (required) |
| `--currency` | `string` | Yes | Unset | Currency name (required) |
| `--receive-uid` | `int64` | Yes | `0` | Recipient UID (required) |

<a id="cli-agent-index"></a>

## Verification and recovery

Use `wallet.deposit.withdrawals` and relevant status reads to check the exact withdrawal/internal push reference. A transaction ID is not the same as final chain confirmation.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex wallet deposit withdrawals  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex withdrawal cancel --id <id> --format json
```
