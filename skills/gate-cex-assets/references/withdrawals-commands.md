# Withdrawal Queries and UID Transfers

## Scope and source

Read withdrawal records and currency withdrawal status for the requested account/currency and bounded time window. UID transfers move funds between main spot accounts; establish the recipient UID, currency, exact amount, fee interpretation, recipient/account context and authority before submitting once. Follow existing official KYC/AML, sanctions and applicable transfer-information requirements; there is no invented Travel Rule bypass or address-book editor here. An accepted transfer is not proof of receipt. On-chain withdrawal submission and cancellation are unavailable through this skill.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `wallet.deposit.withdrawals` | `gate-cli cex wallet deposit withdrawals` | read |
| `wallet.market.withdraw-status` | `gate-cli cex wallet market withdraw-status` | read |
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
gate-cli cex withdrawal push-order --receive-uid <receive-uid> --currency <currency> --amount <amount> --format json
```
