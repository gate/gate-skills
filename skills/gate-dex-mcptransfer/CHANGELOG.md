# Changelog

All notable changes to `gate-dex-mcptransfer` skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026.3.5-1] - 2026-03-05

### Added

- 4 transfer tools + 1 cross-Skill call (all require auth)
  - `tx.gas` — Gas fee estimation
  - `tx.transfer_preview` — Build transaction preview
  - `wallet.sign_transaction` — Server-side signing
  - `tx.send_raw_transaction` — Broadcast transaction
  - `wallet.get_token_list` — Balance verification (cross-Skill)
- 2 operation flows (A-B): Standard transfer, Batch transfer
- Mandatory balance verification (token + Gas token)
- Mandatory user confirmation gate (must show confirmation summary and wait for user confirm before signing)
- Batch transfer with per-transfer confirmation
- Address format validation (EVM / Solana)
- Support for 8 chains (ETH, BSC, Polygon, Arbitrum, Optimism, Avalanche, Base, Solana)
- MCP Server remote HTTP connection check (first-session check + runtime error fallback)
- Skill routing: Post-transfer routing to wallet for balance/tx details
- Cross-Skill collaboration: Call wallet for balance and address
- Security rules: Mandatory balance verification, confirmation gate, batch per-transfer confirmation, raw_tx not leaked
