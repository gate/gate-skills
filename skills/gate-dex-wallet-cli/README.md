# Gate DEX Wallet CLI

## Overview

`gate-dex-wallet-cli` is a Gate DEX wallet skill backed by the standalone `gate-dex` CLI (pure REST, no MCP). It covers OAuth login, balance and address queries, transaction history, on-chain transfers, and message/transaction signing. GV security check-in is built into every signing command — no external `tx-checkin` binary is required.

For token swaps, use the `gate-dex-trade-cli` skill. For market data, K-line, and token security audits, use the `gate-dex-market-cli` skill. For DApp interactions, x402, and the MCP-based wallet flow, use the `gate-dex-wallet` skill.

This skill is intended for users aged 18 or above with full civil capacity. Availability may vary by product, account state, and local legal or regulatory restrictions.

## Core Capabilities

| Module | Description | Example |
|--------|-------------|---------|
| **Auth** | Login / logout / status / web3-domain via Gate or Google OAuth | `gate-dex login`, `gate-dex login --google` |
| **Balance & address** | Total portfolio value, per-chain wallet addresses | `gate-dex balance`, `gate-dex address` |
| **Token list** | Per-chain token holdings with pagination | `gate-dex tokens --chain ETH,SOL --page 1 --size 50` |
| **Transaction history** | Transfer history and per-tx detail | `gate-dex tx-history`, `gate-dex tx-detail <hash>` |
| **Transfer (preview)** | Build a transfer without signing | `gate-dex transfer ...` |
| **Send (one-shot)** | Preview → GV check-in → sign → broadcast | `gate-dex send ...` |
| **Signing primitives** | Sign 32-byte hex messages or raw transactions | `gate-dex sign-msg <hex>`, `gate-dex sign-tx <raw>` |
| **Solana helper** | Build Solana unsigned tx with latest blockhash | `gate-dex sol-tx ...` |
| **Gas query** | Per-chain gas price and gas limit | `gate-dex gas eth` |
| **Maintenance** | Reset local CLI state | `gate-dex cleanup` |

## Architecture

The skill uses a routing architecture. `SKILL.md` is a thin router that delegates to per-module documents:

- `references/auth.md` — login, logout, session expiry, OAuth flows, web3-domain.
- `references/asset-query.md` — balance, address, tokens, tx-history, tx-detail.
- `references/transfer.md` — preview, send (one-shot), sign-msg, sign-tx, sol-tx, gas.

`SKILL.md` retains skill boundaries, runtime and credentials notes, security rules, follow-up routing tables, and the risk disclosure block.

## CLI usage flow

1. Run `login` or `status` to establish and verify the session.
2. Use `balance`, `address`, `tokens`, and history commands for read-only queries.
3. Run `transfer` as a preview, confirm the chain, recipient, asset, and amount in chat, then run `send`.
4. Route swaps to `gate-dex-trade-cli` and market or token queries to `gate-dex-market-cli`.

## Runtime Requirements

- The `gate-dex` executable must already be available on `PATH`.
- This skill documents CLI usage only; installation and distribution are managed by the host or project tooling.

## Credentials

- Authenticated via OAuth Device Flow: `gate-dex login` (Gate, default) or `gate-dex login --google`.
- Auth token is persisted at `~/.gate-dex/auth.json` (override with `--auth-dir`, `--auth-file`, or env vars `GATE_DEX_HOME` / `GATE_DEX_AUTH_FILE`).
- No API key or pasted secret is required. Never ask the user to paste credentials into chat.
- `~/.gate-dex/auth.json` must never be displayed to the user or committed to a VCS.

## Safety and Confirmation

- `send` involves real funds and is the only write-capable command in this skill. Always confirm chain, recipient address, token contract, and amount with the user in chat before executing.
- Without explicit user confirmation, only read-only commands (`balance`, `address`, `tokens`, `tx-history`, `tx-detail`, `transfer` preview) are allowed.
- Use `transfer` (preview-only) before `send`.
- Do not run any external `tx-checkin` binary; the CLI handles GV check-in internally.

## Data and Privacy

- Auth, balance, history, and transfer requests flow through the `gate-dex` CLI to Gate-managed wallet, gateway, and verification services.
- This skill does not define any extra telemetry, analytics, or persistence of its own.
- Local shell history may still record commands depending on the operator environment.

## Compliance

- Use of this skill must comply with local laws, platform rules, and product eligibility requirements.
- Some products may be unavailable due to account status, KYC state, geography, or risk controls.

## File Structure

```text
gate-dex-wallet-cli/
├── README.md
├── SKILL.md
├── CHANGELOG.md
└── references/
    ├── auth.md
    ├── asset-query.md
    └── transfer.md
```

## Support

For maintenance or review feedback, open an issue in this repository or contact the repository maintainers through the normal project support channel.
