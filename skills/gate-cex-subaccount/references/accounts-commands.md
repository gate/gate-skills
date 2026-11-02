# Subaccount administration

## Scope and source

Require a managing HMAC API key with the actual parent role and explicit target authority. Agentic OAuth blocks subaccount/key management routes. Distinguish list/get/create/lock/unlock and unified-mode reads. Lock/unlock affect availability and are not a permission test. Do not pass a password through process arguments or model/tool logs; if provisioning needs a new password, hand off local secret entry. Fund transfers belong to gate-cex-assets.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `sub-account.create` | `gate-cli cex sub-account create` | write |
| `sub-account.get` | `gate-cli cex sub-account get` | read |
| `sub-account.list` | `gate-cli cex sub-account list` | read |
| `sub-account.lock` | `gate-cli cex sub-account lock` | write |
| `sub-account.unified-mode` | `gate-cli cex sub-account unified-mode` | read |
| `sub-account.unlock` | `gate-cli cex sub-account unlock` | write |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="sub-account.create"></a>
### `gate-cli cex sub-account create`

Operation ID: `sub-account.create`. Effect: **write**.

Create a new sub-account

```text
gate-cli cex sub-account create [flags]
```

API: `POST /api/v4/sub_accounts` (private).

Returns: [SubAccount](models/accounts.md#model-subaccount).

API request model(s), assembled by the command: [SubAccount](models/accounts.md#model-subaccount). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--email` | `string` | No | Unset | Email (default: same as main account) |
| `--login-name` | `string` | Yes | Unset | Login name (required) |
| `--password` | `string` | No | Unset | Password (default: same as main account) |
| `--remark` | `string` | No | Unset | Remark |

<a id="sub-account.get"></a>
### `gate-cli cex sub-account get`

Operation ID: `sub-account.get`. Effect: **read**.

Get sub-account details

```text
gate-cli cex sub-account get [flags]
```

API: `GET /api/v4/sub_accounts/{user_id}` (private).

Returns: [SubAccount](models/accounts.md#model-subaccount).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--user-id` | `int64` | Yes | `0` | Sub-account user ID (required) |

<a id="sub-account.list"></a>
### `gate-cli cex sub-account list`

Operation ID: `sub-account.list`. Effect: **read**.

List sub-accounts

```text
gate-cli cex sub-account list [flags]
```

API: `GET /api/v4/sub_accounts` (private).

Returns: [][SubAccount](models/accounts.md#model-subaccount).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--type` | `string` | No | Unset | Sub-account type: 0=all, 1=regular (default: regular only) |

<a id="sub-account.lock"></a>
### `gate-cli cex sub-account lock`

Operation ID: `sub-account.lock`. Effect: **write**.

Lock a sub-account

```text
gate-cli cex sub-account lock [flags]
```

API: `POST /api/v4/sub_accounts/{user_id}/lock` (private).

Returns: { `user_id`: `int64`, `action`: `"locked"` }.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--user-id` | `int64` | Yes | `0` | Sub-account user ID (required) |

<a id="sub-account.unified-mode"></a>
### `gate-cli cex sub-account unified-mode`

Operation ID: `sub-account.unified-mode`. Effect: **read**.

List sub-account unified mode

```text
gate-cli cex sub-account unified-mode
```

API: `GET /api/v4/sub_accounts/unified_mode` (private).

Returns: [][SubUserMode](models/accounts.md#model-subusermode).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="sub-account.unlock"></a>
### `gate-cli cex sub-account unlock`

Operation ID: `sub-account.unlock`. Effect: **write**.

Unlock a sub-account

```text
gate-cli cex sub-account unlock [flags]
```

API: `POST /api/v4/sub_accounts/{user_id}/unlock` (private).

Returns: { `user_id`: `int64`, `action`: `"unlocked"` }.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--user-id` | `int64` | Yes | `0` | Sub-account user ID (required) |

## Verification and recovery

Use `sub-account.get`/list for the exact target user-id, plus unified-mode only when relevant. Do not test key permissions by creating a trading order.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex sub-account get --user-id <user-id> --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex sub-account create --login-name <login-name> --format json
```
