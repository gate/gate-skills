# Permission boundaries

## Scope and source

Use account keys only for the current HMAC key and redact sensitive fields. It does not establish user authorization or institution representation. Subaccount key permission/IP changes use the canonical api-keys-commands.md actions; do not maintain a second implementation. No separate business-activation or managed-custody entitlement endpoint is established by this baseline. Stop if required role, scope or account qualification cannot be verified.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `account.keys` | `gate-cli cex account keys` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="account.keys"></a>
### `gate-cli cex account keys`

Operation ID: `account.keys`. Effect: **read**.

Get API key information for the current key

```text
gate-cli cex account keys
```

API: `GET /api/v4/account/main_keys` (private).

Returns: [AccountKeyInfo](models/permissions.md#model-accountkeyinfo).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

## Verification and recovery

Check the effective current key and actual service permission result; do not broaden credentials after denial. Route mutations to api-keys-commands.md.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

Key permission/IP mutations are defined in [API key actions](api-keys-commands.md).

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex account keys  --format json
```
