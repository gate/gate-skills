# Changelog

All notable changes to `gate-dex-mcpmarket` skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026.3.5-1] - 2026-03-05

### Added

- 7 public market data query tools (all require no authentication)
  - `market_get_kline` — K-line data
  - `market_get_tx_stats` — On-chain trading stats
  - `market_get_pair_liquidity` — Pair liquidity
  - `token_get_coin_info` — Token details
  - `token_ranking` — Token rankings
  - `token_get_coins_range_by_created_at` — New token discovery
  - `token_get_risk_info` — Security risk audit
- 5 operation flows (A–E): market view, token details, rankings, security review, new token discovery
- MCP Server remote HTTP connection check (first-session check + runtime error fallback)
- Skill routing: post-operation routing to swap / transfer / wallet / dapp
- Cross-Skill collaboration: token info and security review for swap, dapp
- Display rules: price precision, address masking, time format
- Security rules: read-only, objective display, no investment advice
