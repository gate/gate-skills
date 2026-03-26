# Changelog

## [2026.3.25-2] - 2026-03-25

### Changed

- Remote CEX server keys shortened to **`gate-cex-pub`** and **`gate-cex-ex`** (replacing long `Gate-Remote-*` names).
- Remote CEX HTTP config: **`url` + `type` only** — removed optional `headers` block.

## [2026.3.25-1] - 2026-03-25

### Added

- Documented **Local CEX** vs **Remote CEX** (`/mcp` public, `/mcp/exchange` OAuth2) per [gate-mcp](https://github.com/gate/gate-mcp).
- `install.sh`: `--mcp cex-public` and `--mcp cex-exchange`; default install includes all six MCP slots (main, cex-public, cex-exchange, dex, info, news).

## [2026.3.11-1] - 2026-03-11

### Added

- Initialized the `gate-mcp-claude-installer` skill with one-click MCP installation and skill setup.
