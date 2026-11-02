# CLI Authentication and Identity

Public reads do not require credentials. For private actions, use the effective credentials, API origin, and selected account context for the operation.

User-facing authentication guidance must stay semantic: state that sign-in or the
required authorization is needed, in progress, or complete. Do not render profile
names, environment-variable assignments, API origins, OAuth issuers/scopes,
authorization URLs, callback codes, tokens, or internal test configuration unless
the user explicitly requests authorized technical diagnostics. These values may be
used locally for execution but are never routine answer content.

## API key

Reuse the intended existing key or let the user enter it locally through the interactive wizard:

```bash
# Configure credentials locally; never ask the user to paste keys into chat.
gate-cli config init
```

API credential flags override environment values, which override profile values. `GATE_BASE_URL` overrides the profile API origin. When both key and secret resolve, HMAC takes precedence over OAuth. OAuth login does not change that precedence.

Use the intended existing profile with `--profile` where applicable, and account for credential precedence: environment credentials can override that profile. Do not pass secrets in process arguments, dump environment/configuration files, or use `--show-secrets` for diagnostics. Do not silently remove another credential source to change authentication mode.

Configuration is stored at `~/.gate-cli/config.yaml`. Treat it as a local secret-bearing file; do not read or publish its contents for diagnostics.

| Existing input | Purpose |
|---|---|
| `GATE_API_KEY` / `GATE_API_SECRET` | API credentials; override profile values |
| `GATE_BASE_URL` | API origin; overrides the profile origin |
| `--profile` | Selects API configuration; does not select an OAuth UID/resource |

`config init` also changes `default_profile` to the selected profile. Use the wizard only for an authorized setup change; keep the existing profile for diagnostics. Do not assume that a help label saying public overrides the documented access contract: product references mark protected actions as private even where CLI help is stale. Backend eligibility remains authoritative.

## OAuth, when supported

First check the official installation's CEX help for an auth group and its login/status/refresh/logout commands. Continue below only when those commands and the required scope/resource flow exist. Some public releases do not provide them. If OAuth is required but unavailable, stop and report that limitation; do not install an internal build or silently substitute an API key. Use the API-key flow only when independently authorized.


```bash
# Inspect local OAuth state before initiating a browser login.
gate-cli cex auth status
```

`authenticated` means locally unexpired; a protected read must still verify access. `expired (refreshable)` permits refresh on the next protected call. Missing credentials or non-refreshable expiry require a browser login with the required scope set:

```bash
# Example for a workflow that reads balances and places spot orders; consent is still required.
gate-cli cex auth login --scope base,spot_trade
```

For `--manual`, use a trusted local terminal: start the login, open the shown official authorization URL in the browser, complete consent, then enter the returned authorization code in that terminal. Never paste the code or callback URL into chat or logs. Cancel with Ctrl+C if the wrong identity/resource is selected or consent cannot finish. Allow a bounded human-interaction window agreed with the user; the normal 30-second business-command deadline does not cover browser consent.

Use `--manual` only for this local handoff. Reauthorization or `--force` must be intentional. Login accepts a subset of `base spot_trade futures_trade earn cfd stock`; omitting `--scope` requests all six. `base` includes asset operations and is not read-only. The final consent result and service authorization remain authoritative.

Scope families for selecting the minimum consent set:

| Scope | Typical purpose |
|---|---|
| `base` | Applicable account reads and permitted asset/account operations; includes writes |
| `spot_trade` | Supported spot and margin trading operations |
| `futures_trade` | Supported perpetual, delivery and options operations |
| `earn` | Supported earn and borrowing operations |
| `cfd` | Private CFD reads, orders, positions and funding |
| `stock` | Private stock reads, orders, positions and funding |

A workflow can need several scopes for its requested operations. The gateway's current exact-route grant, role and product checks remain authoritative. These families do not promise bot access, institutional rights or permission to administer keys/subaccounts. Request only the scopes needed for independently supported routes; stop on an unresolved route grant rather than silently requesting all scopes.

`gate-cli cex auth refresh` explicitly refreshes once; normal protected calls can refresh when needed. `gate-cli cex auth logout` clears local OAuth credentials and attempts remote revocation; do not claim remote revocation without evidence. Auth commands return human-readable text even with `--format json`; successful status exit alone does not prove login.

For a CLI that supports this Agentic flow, verify the advertised official issuer `https://www.gate.com/.well-known/oauth-authorization-server` and a resource bound to the selected APIv4 origin, normally `https://api.gateio.ws/api/v4`. Do not reuse tokens for another resource or invent an issuer override. Browser consent selects or creates an Agentic subaccount.

## Account context

Use the account, profile and environment already selected by the authenticated execution context. Do not require a separate account-detail query, UID lookup or successful identity response before a private read or write. An unavailable account-detail endpoint or a missing returned UID does not by itself block an otherwise authorized operation.

Query account details only when the requested task needs account information or an authorized diagnostic needs it. Keep authentication, route permissions and user authority checks for the requested operation; its actual denial remains a failure. Resolve a known account-context conflict before writing, and do not broaden scopes, change credentials or query API-key management to work around a denial. `key.mode` does not establish institution authority or every product's account mode.

Agentic authorization blocks API-key and subaccount-management routes even when CLI commands exist. Institutional actions also need trusted role/representation evidence; authentication alone does not establish that authority.
