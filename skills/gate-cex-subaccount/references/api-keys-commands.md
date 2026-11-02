# Subaccount API keys

## Scope and source

Require trusted parent/subaccount authority and explicit intended permissions/IP restrictions. Agentic OAuth cannot administer keys. Key creation/get/list may expose secret fields: execute only through an approved local secret sink that keeps them out of model, tool and audit logs; otherwise hand off provisioning to the user. Do not pass secret values in command arguments. Key identifiers needed to address an existing key are distinct from its secret. Verify intended permissions and IP restrictions through a redacted result, without printing credentials.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `sub-account.key.create` | `gate-cli cex sub-account key create` | write |
| `sub-account.key.delete` | `gate-cli cex sub-account key delete` | write |
| `sub-account.key.get` | `gate-cli cex sub-account key get` | read |
| `sub-account.key.list` | `gate-cli cex sub-account key list` | read |
| `sub-account.key.update` | `gate-cli cex sub-account key update` | write |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="sub-account.key.create"></a>
### `gate-cli cex sub-account key create`

Operation ID: `sub-account.key.create`. Effect: **write**.

Create a new API key for a sub-account

```text
gate-cli cex sub-account key create [flags]
```

API: `POST /api/v4/sub_accounts/{user_id}/keys` (private).

Returns: [SubAccountKey](models/api-keys.md#model-subaccountkey).

API request model(s), assembled by the command: [SubAccountKey](models/api-keys.md#model-subaccountkey). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--ip-whitelist` | `stringSlice` | No | `[]` | IP whitelist |
| `--mode` | `int32` | No | `1` | Mode: 1=classic, 2=portfolio |
| `--name` | `string` | No | Unset | API key name |
| `--perms` | `stringSlice` | No | `[]` | Permissions, e.g. spot,futures,wallet |
| `--user-id` | `int64` | Yes | `0` | Sub-account user ID (required) |

<a id="sub-account.key.delete"></a>
### `gate-cli cex sub-account key delete`

Operation ID: `sub-account.key.delete`. Effect: **write**.

Delete a sub-account API key

```text
gate-cli cex sub-account key delete [flags]
```

API: `DELETE /api/v4/sub_accounts/{user_id}/keys/{key}` (private).

Returns: { `user_id`: `int32`, `api_key`: `string`, `action`: `"deleted"` }.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--api-key` | `string` | Yes | Unset | API key (required) |
| `--user-id` | `int32` | Yes | `0` | Sub-account user ID (required) |

<a id="sub-account.key.get"></a>
### `gate-cli cex sub-account key get`

Operation ID: `sub-account.key.get`. Effect: **read**.

Get a specific API key of a sub-account

```text
gate-cli cex sub-account key get [flags]
```

API: `GET /api/v4/sub_accounts/{user_id}/keys/{key}` (private).

Returns: [SubAccountKey](models/api-keys.md#model-subaccountkey).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--api-key` | `string` | Yes | Unset | API key (required) |
| `--user-id` | `int32` | Yes | `0` | Sub-account user ID (required) |

<a id="sub-account.key.list"></a>
### `gate-cli cex sub-account key list`

Operation ID: `sub-account.key.list`. Effect: **read**.

List all API keys of a sub-account

```text
gate-cli cex sub-account key list [flags]
```

API: `GET /api/v4/sub_accounts/{user_id}/keys` (private).

Returns: [][SubAccountKey](models/api-keys.md#model-subaccountkey).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--user-id` | `int32` | Yes | `0` | Sub-account user ID (required) |

<a id="sub-account.key.update"></a>
### `gate-cli cex sub-account key update`

Operation ID: `sub-account.key.update`. Effect: **write**.

Update a sub-account API key

```text
gate-cli cex sub-account key update [flags]
```

API: `PUT /api/v4/sub_accounts/{user_id}/keys/{key}` (private).

Returns: { `user_id`: `int32`, `api_key`: `string`, `action`: `"updated"` }.

API request model(s), assembled by the command: [SubAccountKey](models/api-keys.md#model-subaccountkey). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--api-key` | `string` | Yes | Unset | API key (required) |
| `--ip-whitelist` | `stringSlice` | No | `[]` | IP whitelist |
| `--name` | `string` | No | Unset | API key name |
| `--perms` | `stringSlice` | No | `[]` | Permissions, e.g. spot,futures,wallet |
| `--user-id` | `int32` | Yes | `0` | Sub-account user ID (required) |

## Verification and recovery

Use redacted `sub-account.key.get`/list through the approved secret-safe local flow. Confirm permission and IP restrictions without exposing key material. A deletion requires both local handling and server result evidence.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex sub-account key get --api-key <api-key> --user-id <user-id> --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex sub-account key create --user-id <user-id> --format json
```
