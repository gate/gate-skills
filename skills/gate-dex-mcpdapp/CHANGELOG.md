# Changelog

All notable changes to `gate-dex-mcpdapp` skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026.3.5-1] - 2026-03-05

### Added

- 4 DApp interaction tools + cross-Skill invocation (all require authentication)
  - `wallet.get_addresses` — Get wallet addresses (cross-Skill)
  - `wallet.sign_message` — Sign message (personal_sign / EIP-712)
  - `wallet.sign_transaction` — Sign DApp transaction
  - `tx.send_raw_transaction` — Broadcast transaction
- 5 operation flows (A-E): Wallet connection, message signing, DApp transaction execution, ERC20 Approve, arbitrary contract call
- DApp interaction scenarios: DeFi liquidity/lending/Staking, NFT mint/trading, Token Approve, arbitrary contract call
- Mandatory confirmation gating (must display confirmation summary before signing and wait for user confirmation)
- Contract security review integration (invoke gate-dex-mcpmarket's token_get_risk_info)
- ERC20 Approve supports exact and unlimited authorization (default exact, unlimited requires secondary confirmation)
- EIP-712 signature data parsing specification (Domain, Primary Type, known type recognition)
- ERC20 Approve calldata encoding specification
- Support for 8 chains (ETH, BSC, Polygon, Arbitrum, Optimism, Avalanche, Base, Solana)
- MCP Server remote HTTP connection check (first-session check + runtime error fallback)
- Skill routing: Post-DApp operation guidance to wallet / market / transfer / swap
- Cross-Skill collaboration: Invoke wallet for address and balance, invoke market for contract security review
- Security rules: Confirmation gating, security review, exact authorization default, EIP-712 transparent display, raw_tx not leaked, Permit risk warning, phishing prevention
