# Withdrawal Queries

## Scope and source

Read withdrawal records and currency withdrawal status for the requested account/currency and bounded time window. These queries do not initiate a transfer or prove settlement. On-chain withdrawal submission, cancellation and UID Push transfer submission are unavailable through this skill.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `wallet.deposit.withdrawals` | `gate-cli cex wallet deposit withdrawals` | read |
| `wallet.market.withdraw-status` | `gate-cli cex wallet market withdraw-status` | read |

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

<a id="cli-agent-index"></a>

## Verification and recovery

Use `wallet.deposit.withdrawals` and relevant status reads to check the exact withdrawal reference. Use the deposit reference for UID transfer history. A transaction ID is not the same as final chain confirmation.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex wallet deposit withdrawals  --format json
```
