# Gate DEX Market CLI

## Overview

`gate-dex-market-cli` is a read-only Gate DEX skill that surfaces on-chain market and token data through the standalone `gate-dex` CLI. No MCP server is required, and no commands in this skill sign or move funds.

This skill is intended for users aged 18 or above with full civil capacity. Availability may vary by product, account state, and local legal or regulatory restrictions.

## Core Capabilities

| Module | Description | Example |
|--------|-------------|---------|
| **K-line** | OHLCV candlestick data per token | `gate-dex kline --chain eth --address 0x...` |
| **Liquidity** | Pool add/remove events | `gate-dex liquidity --chain eth --address 0x...` |
| **Trading stats** | Volume, tx count, buy/sell breakdown | `gate-dex tx-stats --chain eth --address 0x...` |
| **Token info** | Price, market cap, 24h volume, supply | `gate-dex token-info --chain eth --address 0x...` |
| **Token risk** | Honeypot/audit/contract ownership checks | `gate-dex token-risk --chain eth --address 0x...` |
| **Token rank** | Price-change leaderboards | `gate-dex token-rank --chain eth --limit 20` |
| **New tokens** | Recently listed tokens, optionally filtered by time | `gate-dex new-tokens --chain sol --start ...` |
| **Token discovery** | Resolve token addresses by symbol | `gate-dex swap-tokens --chain arb --search USDC` |
| **Bridge tokens** | Cross-chain bridge token catalog | `gate-dex bridge-tokens --src-chain eth --dest-chain arb` |
| **Chain config** | Network metadata for supported chains | `gate-dex chain-config eth` |
| **Raw RPC** | Pass-through `eth_*` / Solana RPC calls | `gate-dex rpc --chain ETH --method eth_gasPrice` |

## Architecture

The skill uses a single-file (standard) architecture:

- `SKILL.md` is the runtime entry point with skill boundaries, command reference, security rules, and risk disclosure.
- `references/scenarios.md` contains scenario-style examples for review and testing.

## CLI usage flow

1. Run one read-only command from the command reference in `SKILL.md`.
2. If the CLI reports `Not logged in`, route to `gate-dex-wallet-cli` for login, then retry.
3. Keep this skill read-only; route transfers and swaps to the wallet or trade CLI skills.

## Runtime Requirements

- The `gate-dex` executable must already be available on `PATH`.
- This skill documents CLI usage only; installation and distribution are managed by the host or project tooling.

## Credentials

Read-only market commands generally do not require an authenticated session. If a command surfaces `Not logged in`, run `gate-dex login` (handled by the `gate-dex-wallet-cli` skill). No API key, env var, or pasted secret is required for this skill's read-only commands.

## Data and Privacy

- Queries flow through the `gate-dex` CLI to Gate-managed market and token APIs.
- This skill does not define any extra telemetry, analytics, or persistence of its own.
- Local shell history may still record commands depending on the operator environment.

## Compliance

- Use of this skill must comply with local laws, platform rules, and product eligibility requirements.
- Token security audits are advisory only; absence of a flagged risk is not a guarantee of safety.

## File Structure

```text
gate-dex-market-cli/
├── README.md
├── SKILL.md
├── CHANGELOG.md
└── references/
    └── scenarios.md
```

## Support

For maintenance or review feedback, open an issue in this repository or contact the repository maintainers through the normal project support channel.
