# Gate DEX Wallet

> **Wallet routing skill** — MCP-based authentication, asset queries, transfers, withdrawals, x402 payments, and DApp interactions.

This skill is the MCP wallet entry point. It routes each request to the focused module under `references/` and keeps signing flows behind the Gate Verify MCP check-in requirement.

## Core modules

| Module | Scope |
|---|---|
| Authentication | Gate or Google OAuth, session status, logout |
| Assets | Balances, addresses, token holdings, transaction and swap history |
| Transfers | Preview, confirmation, signing, and broadcast for EVM and Solana |
| Withdrawals | On-chain withdrawal to a Gate Exchange account or another address |
| x402 | HTTP 402 payment flows with the required preview and check-in order |
| DApp | Wallet connection, message signing, approvals, and contract calls |

## MCP connection

The MCP server is an HTTP endpoint:

- URL: `https://api.gatemcp.ai/mcp/dex`
- Type: HTTP
- The server name is user-defined; `gate-dex` or `gate-wallet` are common choices.

Configure it in the host's MCP settings, then complete the first OAuth login when prompted. Signing operations also require the Gate Verify MCP described in [`references/tx-checkin.md`](./references/tx-checkin.md).

## CLI usage

Use the separate [`gate-dex-wallet-cli`](../gate-dex-wallet-cli/SKILL.md) skill for direct command-line operations. It is the source of truth for `gate-dex` commands, authentication state, transfer previews, confirmation gates, and built-in GV check-in behavior.

Typical read-only commands are:

```bash
gate-dex login
gate-dex status
gate-dex balance
gate-dex address
gate-dex tokens
gate-dex tx-history
```

Route swaps to [`gate-dex-trade-cli`](../gate-dex-trade-cli/SKILL.md) and market or token data to [`gate-dex-market-cli`](../gate-dex-market-cli/SKILL.md). This document does not install or distribute the CLI binary.

## Routing

| User intent | Reference |
|---|---|
| Login, logout, or session recovery | [`references/auth.md`](./references/auth.md) |
| Balance, address, holdings, transaction history | [`references/asset-query.md`](./references/asset-query.md) |
| Transfer or send tokens | [`references/transfer.md`](./references/transfer.md) |
| Withdraw to Gate Exchange | [`references/withdraw.md`](./references/withdraw.md) |
| x402 payment | [`references/x402.md`](./references/x402.md) |
| DApp connection, signing, approval, contract calls | [`references/dapp.md`](./references/dapp.md) |
| Gate Verify check-in before signing | [`references/tx-checkin.md`](./references/tx-checkin.md) |
| Direct `gate-dex` CLI operations | [`gate-dex-wallet-cli`](../gate-dex-wallet-cli/SKILL.md) |

## Security rules

- Never expose `mcp_token` or local auth files.
- Confirm chain, recipient, asset, amount, and payment URL before any write operation.
- Complete the Gate Verify MCP check-in immediately before an MCP signing call.
- Treat token risk and analytical output as informational, not a guarantee of safety or financial advice.

## Related skills

- [`gate-dex-market`](../gate-dex-market/SKILL.md) — read-only market and token data
- [`gate-dex-trade`](../gate-dex-trade/SKILL.md) — MCP-based swap execution
- [`gate-dex-wallet-cli`](../gate-dex-wallet-cli/SKILL.md) — `gate-dex` command-line wallet operations
