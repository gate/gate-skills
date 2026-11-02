# Fixture Isolation and Authorization Contract

This is the single policy for legacy skill-tester fixture setup, execution,
verification and cleanup. The six gate-cex-* targets use gate-cex-skill-audit
instead; this file does not restore a CEX MCP route.

## Decision order

1. Establish the user's requested scope and the exact dependency, account,
   resources and effects of setup, execution and teardown.
2. For automatic fixtures, require an enforceable synthetic boundary: an in-memory
   model or local peer with no real credentials, real business transport or
   process/network escape. A private IP, HTTP, nonstandard port or test-like name
   is only a label and never proof of isolation.
3. Real external integration requires separate explicit authorization covering
   the verified endpoint, account, permission, data and every setup/write/cleanup
   action. Generic permission to test a skill is insufficient.
4. If any prerequisite is unavailable, keep the write case BLOCKED with zero
   business writes. Use a synthetic case or static walkthrough instead.
5. Record actual events and final state. Failure or unknown outcomes in real integration prohibit
   automatic retries, reverse trades or state restoration. Synthetic fixtures may
   discard their own isolated state. Cleanup is a write
   too; it must be within scope and cannot be assumed harmless.

| Evidence | Result | Permitted effects |
|---|---|---|
| Enforceable synthetic dependencies and scoped fixture | SYNTHETIC | Only local synthetic state |
| Verified external context and separately explicit complete authorization | AUTHORIZED_INTEGRATION | Only the exact granted actions |
| Private/HTTP/test-name signal alone, including a production proxy | BLOCKED | Zero business writes |
| Missing endpoint/account/permission/grant or uncertain outcome | BLOCKED | No new write or automatic compensation |

Minimum amounts, distant limit/trigger prices and an expected rejection are
synthetic inputs, not a financial safety proof. Existing real orders can fill
during setup or teardown. Never infer permitted parameters or cleanup authority
from a method name.

## Evidence levels

Label static reasoning, synthetic events and real integration separately.
A model's textual tool markers are not execution events. Record permitted and
forbidden events, exact resource ownership, observed postconditions and residual
state; never count an unexecuted/blocked case as successful execution.
