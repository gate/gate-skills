# Gate CEX package runtime rules

Read [preflight](../../_shared/cex/preflight.md), [CLI setup](../../_shared/cex/cli-setup.md), [authentication](../../_shared/cex/cli-auth.md), [execution](../../_shared/cex/execution-cli.md), [safety](../../_shared/cex/safety.md), and [display templates](../../_shared/cex/templates.md) before using this package. These are the shared authority for authentication selection, permissions, deadlines, bounded reads, active authorization and recovery. The product rules below specialize that boundary.

These rules make `gate-cex-trade` usable when a product-specific Gate skill is not installed. A product reference may add a narrower rule, but it may not weaken these requirements.

## Identity and environment

- Use the account, profile, environment, and API base URL already selected by the current execution context. Never infer an account from a symbol or from the last request.
- Keep the product, settlement, account mode, and scope in the execution context for the whole write sequence. A changed context starts a new sequence.
- Treat API v4 as the contract for REST fields and enums. Treat the installed CLI only as an adapter whose exact leaf help and path mapping must be checked before use.

## Authentication and security

- Let the registered CLI resolve credentials under the shared authentication contract. Do not read credentials into the agent or introduce another client. Never request or print API keys, OAuth tokens, signatures, cookies, or authorization headers in chat, logs, reports, or error toasts.
- Verify issuer, audience/resource, environment, account permissions, and product scopes before a write. A read-only credential cannot be upgraded by changing a flag.
- Keep test and production endpoints separate. If the selected endpoint, API path, CLI adapter, or product scope is ambiguous, stop before writing.
- Redact secrets and internal infrastructure details from user-facing output. Report the product operation and compatibility reason, not repository URLs, checkout paths, commit IDs, hostnames, or source provenance.

## Execution and confirmation

- Private reads and every write use registered CLI leaves only. If a necessary command or flag is absent, stop that operation; never substitute HTTP, SDK, an API executor or another product. Only the bounded public market reads and public WS helper in [market rules](market.md) are transport exceptions.
- Use argv without shell interpolation, exact decimal strings, a 30-second deadline per call, at most three bounded read attempts, and at most 10 pages / 1,000 records unless the shared contract imposes a smaller bound. Never automatically retry writes. Inspect per-item failures even with a successful process exit.

- Read the current rules, balance, position, liability, or configuration before a write. Do not use a guessed default for a missing field.
- A confirmation covers the complete displayed operation: account, product, scope, parameters, quote/expiry, declared sequence, and stop condition. Ask once immediately before the first write when that complete operation is ready.
- Keep that confirmation active for unchanged writes in the same execution context. Reads, bounded status polling, reconciliation, and retries of a read must not ask again.
- Ask again only when a parameter, account, scope, sequence step, quote, expiry, or live resource state changes in a way that affects the confirmed operation, safety, or stop condition; when execution is paused and resumed; or when a new write/cleanup action was not included in the confirmed sequence. Expected state transitions inside the declared sequence do not trigger another confirmation. Never blindly retry a write after a timeout.
- For a batch or multi-step flow, show every item and the stop condition in one summary. After a partial failure, confirm only newly proposed steps or changed items.

## Reconciliation

- After every write, query the strongest deterministic key available: order/trigger/conversion ID, loan or liability record, configuration resource, MMP resource, and then the resulting balance or position.
- Separate accepted, open, partially filled, filled, cancelled, failed, pending, and unresolved states. Do not call an accepted request successful until the documented status predicate and post-write resource check pass.
- If the actual SDK request path or fields and the API contract disagree (not merely a diagnostic label), preserve the API contract, record the adapter mismatch internally, and block that write until compatibility is resolved. Never translate an incompatible field or enum silently.

## User-facing output

- Use the user's language for prose and the module's native field names for values. Keep normative metadata keys and values in one language.
- Do not expose internal source, checkout, package, or dependency names. Use the two-line failure toast defined in `workflows.md` and describe the actionable product-level reason.
