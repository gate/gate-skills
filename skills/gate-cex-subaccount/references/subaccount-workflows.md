# Subaccount Administration Workflows

## Inspect, create or change account state

Use [accounts](accounts-commands.md). Establish trusted parent/managing HMAC identity and target authority; Agentic OAuth cannot administer subaccounts. Read the requested account and state. Create/lock/unlock only within the explicit grant and re-read that user-id afterward. Password entry or other secret handling outside the approved local flow requires a user handoff. Do not transfer funds as an implicit provisioning step.

## Maintain key permissions or IP restrictions

Read [permissions](permissions-commands.md) and the canonical [key actions](api-keys-commands.md). Inspect redacted current settings, request the minimal intended change and preserve unrelated permissions/IP restrictions. Execute only through a trusted local secret-safe provisioning flow; if command output would expose a secret to model/tool logs, hand off to the user. Re-read redacted state and distinguish local storage from remote creation/revocation. Never test a key with an order or withdrawal.

## Fund a subaccount

Delegate the explicit transfer to `gate-cex-assets`, carrying only target UID, source/destination, currency, amount and remaining grant. If that skill is not installed, explain the handoff without implementing its command here.

## Shared stopping rules

Read [preflight](../../_shared/cex/preflight.md), [safety](../../_shared/cex/safety.md) and [execution](../../_shared/cex/execution-cli.md). Keep the same selected account context, credentials, origin and grant throughout. Stop before a step outside verified authority, on changed material terms, or on an ambiguous write. Do not replay earlier steps or automatically compensate. A cross-skill task transfers only the required account/environment, object reference, exact amount/unit, completed state and remaining authority; never credentials.
