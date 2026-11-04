---
name: gate-dex-wallet-cli-route
version: "2026.11.3-1"
updated: "2026-11-03"
description: "Routing note for direct gate-dex CLI wallet operations. The executable and command reference are maintained by gate-dex-wallet-cli."
---

# CLI usage route

Direct command-line wallet operations belong to [`gate-dex-wallet-cli`](../../gate-dex-wallet-cli/SKILL.md). Use that skill for:

- OAuth login, logout, and session status
- balances, addresses, token holdings, and transaction history
- transfer previews and confirmed sends
- raw message or transaction signing
- CLI confirmation and built-in GV check-in behavior

Use [`gate-dex-trade-cli`](../../gate-dex-trade-cli/SKILL.md) for swaps and bridges, and [`gate-dex-market-cli`](../../gate-dex-market-cli/SKILL.md) for market or token data.

The wallet MCP skill does not install, upgrade, or distribute the CLI executable. A host that already provides `gate-dex` on `PATH` can run the command examples documented by the CLI skill.
