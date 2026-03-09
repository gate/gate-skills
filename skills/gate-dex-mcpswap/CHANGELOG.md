# Changelog

All notable changes to `gate-dex-mcpswap` skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026.3.6-1] - 2026-03-06

### Added

- 3 Swap tools + 2 cross-Skill calls + 1 MCP Resource (all require authentication)
  - `tx.quote` — Get Swap quote
  - `tx.swap` — Execute Swap (One-shot: Quote→Build→Sign→Submit)
  - `tx.swap_detail` — Query Swap status
  - `wallet.get_token_list` — Balance validation (cross-Skill)
  - `wallet.get_addresses` — Get chain wallet address (cross-Skill)
  - `swap://supported_chains` — List of chains supported for Swap (MCP Resource)
- 4 operation flows (A-D): Standard Swap, modify slippage, query status, cross-chain Swap
- Mandatory three-step confirmation SOP (trade pair confirmation → quote display → sign approval confirmation)
- Exchange value diff calculation and tiered warnings (> 5% mandatory warning)
- Slippage interactive selection (AskQuestion + fallback text reply)
- High slippage MEV/sandwich attack risk prompt
- Cross-chain Swap support (including to_wallet address group logic)
- Support for 8 chains (ETH, BSC, Polygon, Arbitrum, Optimism, Avalanche, Base, Solana)
- MCP Server remote HTTP connection check (first session check + runtime error fallback)
- Skill routing: Post-Swap guidance to wallet / transfer / market
- Cross-Skill collaboration: Call wallet for balance and address, call market for security review
- Security rules: Three-step confirmation mandatory, value diff warning, balance validation, no auto retry, MEV risk prompt

### Changed

- Rewrote SKILL.md to match actual MCP tool definitions (`tx.quote` / `tx.swap` parameter structure updated)
- Added `wallet.get_addresses` cross-Skill call (`tx.quote` and `tx.swap` require `user_wallet`)
- Added MCP Resource `swap://supported_chains`, chain support must be verified before Swap
- `wallet.get_token_list` parameter update: `chain` / `account_id` now optional, added `network_keys` for multi-chain query
- `native_in` / `native_out` rules enhanced: clarified native coin vs Wrapped contract token logic
- `need_approved` logic corrected: Approve only when input is ERC20 contract token (non-native) and returns `need_approved=true`
- Slippage selection UX improved: AskQuestion structured options + fallback text reply
