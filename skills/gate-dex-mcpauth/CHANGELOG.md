# Changelog

All notable changes to `gate-dex-mcpauth` skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026.3.5-1] - 2026-03-05

### Added

- 5 authentication management tools
  - `auth.google_login_start` — Initiate Google Device Flow login
  - `auth.google_login_poll` — Poll login result
  - `auth.login_google_wallet` — Authorization Code login
  - `auth.refresh_token` — Token refresh
  - `auth.logout` — Logout
- 4 operation flows (A–D): Device Flow login, Token refresh, Logout, Authorization Code login
- MCP Server remote HTTP connection check (first-session check + runtime error fallback)
- Skill routing: Post-login routing to wallet / transfer / swap / dapp / market
- Cross-Skill collaboration: Provides mcp_token to all Skills that require authentication
- Security rules: token confidentiality, account_id masking, auto-refresh, single session single account
