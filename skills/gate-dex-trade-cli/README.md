# Gate DEX Trade CLI

## Overview

`gate-dex-trade-cli` is a Gate DEX execution skill for one-shot token swaps via the standalone `gate-dex` CLI. The `swap` command bundles quote, GV security check-in, server-side signing, and broadcast into a single invocation. Cross-chain bridges and ERC20 approve flows are handled internally by the CLI; the agent does not run any external `tx-checkin` binary.

This skill is intended for users aged 18 or above with full civil capacity. Availability may vary by product, account state, and local legal or regulatory restrictions.

## Core Capabilities

| Module | Description | Example |
|--------|-------------|---------|
| **Quote** | Preview swap output with no signing | `gate-dex quote --from-chain 1 --to-chain 1 --from - --to 0x... --amount 0.01` |
| **Same-chain swap** | One-shot quote → check-in → sign → broadcast | `gate-dex swap --from-chain 1 --to-chain 1 --from - --to 0x... --amount 0.01` |
| **Cross-chain bridge** | Source-chain bridge tx with async destination | `gate-dex swap --from-chain 1 --to-chain 42161 --from - --to 0x... --amount 0.1 --to-wallet 0x...` |
| **Solana swap** | Native Solana swap path | `gate-dex swap --from-chain 501 --to-chain 501 --from - --to EPjFW... --amount 0.05` |
| **Swap history** | List recent swaps and bridge orders | `gate-dex swap-history` |
| **Swap detail** | Inspect a specific order, including bridge settlement | `gate-dex swap-detail <order_id>` |
| **Token discovery** | Resolve swappable token addresses | `gate-dex swap-tokens --chain arb --search ARB` |
| **Bridge tokens** | List supported bridge token pairs | `gate-dex bridge-tokens --src-chain eth --dest-chain arb` |

## Architecture

The skill uses a single-file (standard) architecture:

- `SKILL.md` is the runtime entry point with skill boundaries, command reference, agent execution flow, confirmation gates, error handling, and risk disclosure.
- `references/scenarios.md` contains scenario-style examples for review and testing.

## CLI usage flow

1. Resolve token addresses with `swap-tokens` or `bridge-tokens` when needed.
2. Run `quote` and present the route, amount, fees, and slippage.
3. Require explicit confirmation before `swap`; the CLI performs check-in, signing, and broadcast internally.
4. Track a cross-chain order with `swap-detail` and review past orders with `swap-history`.

## Runtime Requirements

- The `gate-dex` executable must already be available on `PATH`.
- This skill documents CLI usage only; installation and distribution are managed by the host or project tooling.

## Credentials

- Authenticated via the `gate-dex login` flow handled by the `gate-dex-wallet-cli` skill (Gate or Google OAuth Device Flow).
- Auth token is stored in `~/.gate-dex/auth.json`.
- No API key or pasted secret is required for this skill. Never ask the user to paste credentials into chat.

## Safety and Confirmation

- Every `swap` execution must be preceded by a quote and an explicit user confirmation in chat.
- Without explicit user confirmation, only `quote`, `swap-tokens`, `bridge-tokens`, `swap-history`, and `swap-detail` may run.
- The CLI handles GV security check-in internally; do not run any external `tx-checkin` binary.
- For unfamiliar tokens, recommend running `gate-dex token-risk` (in the `gate-dex-market-cli` skill) before swapping.
- Cross-chain bridges settle asynchronously on the destination chain; track via `swap-detail <order_id>` rather than assuming arrival on broadcast.

## Data and Privacy

- Swap requests, quote responses, and broadcast transactions flow through the `gate-dex` CLI to Gate-managed swap and verification services.
- This skill does not define any extra telemetry, analytics, or persistence of its own.
- Local shell history may still record commands depending on the operator environment.

## Compliance

- Use of this skill must comply with local laws, platform rules, and product eligibility requirements.
- Some products may be unavailable due to account status, KYC state, geography, or risk controls.

## File Structure

```text
gate-dex-trade-cli/
├── README.md
├── SKILL.md
├── CHANGELOG.md
└── references/
    └── scenarios.md
```

## Support

For maintenance or review feedback, open an issue in this repository or contact the repository maintainers through the normal project support channel.
