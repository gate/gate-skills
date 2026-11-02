# CEX Preflight

Use this contract before the first CEX operation in a task. This is a workflow, not a new CLI command: `gate-cli preflight` checks Info/News readiness and does not verify CEX identity or trading permissions.

1. Resolve the existing CLI binary and its version. A trusted existing binary reporting `dev` is allowed; do not stop, require an upgrade, or replace it solely because of that version label. Read [setup](cli-setup.md) only if installation or an approved upgrade is needed. Check the exact required leaf's `--help` and required parameter variants; a version string alone does not prove support. For advanced algorithms, account selection, protection or closing, verify the specific leaf and flags rather than only the parent group.
2. Confirm the approved API origin and product. Public market reads may proceed without private authentication or account checks.
3. For private actions, follow [authentication](cli-auth.md). Use the account, credentials and API environment already selected by the authenticated execution context. A separate account-detail query or UID verification is not a prerequisite for a private read or write. Resolve a known account or environment conflict before execution; never forge a UID header or switch credentials to bypass a denial.
4. Check the exact operation's schema, grant/key permissions, account mode, and product eligibility. Use bounded reads only; never place/cancel an order or transfer funds to test permission.
5. Apply [authorization and safety](safety.md). Existing scoped authorization may be reused only while the selected account context, scope, amount limits, and expiry remain verifiable.
6. Follow the selected product reference using the [execution rules](execution-cli.md). Record unverified prerequisites rather than inventing support or silently broadening permissions.

Keep a minimal task record: binary/version/provenance, API origin, effective auth mode, selected account/profile, required actions, confirmed capabilities, unresolved permissions, and authorization reference. Do not store credentials in this record.

Recheck affected prerequisites after credential, account, endpoint, binary, scope, schema, or authorization changes. Do not reuse stale account or authorization context across such changes.

On a denial, explain the actual missing prerequisite. Authentication, user authorization, product eligibility, and service restrictions are separate checks. Never switch accounts, endpoints, or transports to bypass a denial.

## Capability and scope boundaries

Use official [Gate CLI](https://github.com/gate/gate-cli) releases. Documentation coverage and installed-release availability are separate: verify the requested command, parameters and authentication method before execution. If any are unavailable, stop the affected task; do not obtain an internal branch or private artifact.

Alpha belongs to `gate-cex-trade`. P2P, CrossEx, welfare, activity-center, coupon-management and Exchange Announcement operations are outside these six skills, even if the installed CLI or existing scope exposes them. Do not invoke them, install an older build or switch execution channels to bypass this boundary.

This boundary does not remove supported coupon fields within an earn product. Independent News capabilities and ordinary Gate APIs are separate services, not business execution fallbacks. Existing orders/positions are not automatically cancelled or closed by this scope restriction.
