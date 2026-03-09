# Changelog

All notable changes to `gate-dex-mcpwallet` skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026.3.6-1] - 2026-03-06

### Added

- 7 wallet asset and transaction history query tools (all require authentication)
  - `wallet.get_token_list` — Token list (with balance)
  - `wallet.get_total_asset` — Total asset value
  - `wallet.get_addresses` — Wallet addresses
  - `chain.config` — Chain config info
  - `tx.list` — Transfer transaction list
  - `tx.detail` — Transaction details
  - `tx.history_list` — Swap history records
- 7 operation flows (A–G): token balance, total assets, wallet addresses, chain config, transfer history, transaction details, Swap history
- Support for 8 chains (ETH, BSC, Polygon, Arbitrum, Optimism, Avalanche, Base, Solana)
- MCP Server remote HTTP connection check (first-session check + runtime error fallback)
- Skill routing: post-query guidance to market / transfer / swap / dapp
- Cross-Skill collaboration: balance verification and address retrieval for transfer, swap, dapp
- Display rules: balance sorting, zero-balance filter, precision control, address integrity
- Security rules: read-only, token confidentiality, auto-refresh

### Changed

- Migrated `tx.list`, `tx.detail`, `tx.history_list` from market skill; tool count 4 → 7, operation flows A–D → A–G
- `wallet.get_token_list` added `network_keys` parameter for multi-chain query (e.g. `"ETH,SOL,ARB"`); `chain` / `account_id` now optional
- Skill routing added "view token security audit" guidance to `gate-dex-mcpmarket`
- Cross-Skill collaboration table added transfer/swap/dapp post-transaction history view scenarios
