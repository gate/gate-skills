# Changelog

## [2026.4.14-4] - 2026-04-14

### Changed

- **gate-dex-sec** (Gate Verify check-in) MCP URL: **`https://api.gatemcp.ai/mcp/dex/sec`** (replaces `https://ai-higress-dev.fulltrust.link/gate-mcp/dex/sec`) in Cursor/Claude JSON fragments, Codex TOML, OpenClaw **servers.manifest**, and docs.

## [2026.4.14-3] - 2026-04-14

### Changed

- Cursor / Claude JSON fragments: Verify MCP **`mcpServers`** key renamed from **`Gate-Verify`** to **`gate-dex-sec`** (aligned with Codex / mcporter).

## [2026.4.14-2] - 2026-04-14

### Changed

- **Gate Verify** is **MCP-only** (`tx_checkin` / `/v1/tx/checkin`); removed installer/docs references to legacy **`tools/tx-checkin/bin`** and **`echo_gate_dex_no_skills_warning`**.
- **install.sh**: When **`dex`** is selected, also merges **`gate-dex-sec`** (`https://api.gatemcp.ai/mcp/dex/sec`) for Cursor/Claude JSON, Codex TOML, and OpenClaw **servers.manifest** + `mcporter`. **OpenClaw `--select`**: choosing **gate-dex** auto-registers **gate-dex-sec** if missing.

### Added

- **mcp-fragments**: `cursor/gate-verify.json`, `claude/gate-verify.json`, `codex/gate-verify.toml`; **openclaw/servers.manifest** line **`gate-dex-sec`**.

## [2026.4.14-1] - 2026-04-14

### Added

- **Gate Verify (tx check-in)**: First-pass docs (superseded by **2026.4.14-2** for MCP-based flow and bundled install).

## [2026.4.10-2] - 2026-04-10

### Added

- **gatepay-merchant-discovery** (Gate Pay merchant catalog, HTTP): optional install via `--mcp gatepay-discovery`. URL `http://dev.halftrust.xyz/pay-mcp-server/mcp`; Cursor/Claude JSON uses `transport: streamable-http` aligned with other remote MCP fragments. OpenClaw: **servers.manifest** entry + `mcporter` URL registration.

## [2026.4.10-1] - 2026-04-10

### Added

- **gatepay-local-mcp** (Gate Pay x402, stdio): optional install via `--mcp gatepay-local` on Cursor, Claude Code, Codex, and OpenClaw (`mcporter`). Fragments use `npx -y gatepay-local-mcp` with placeholder **`env`** (`PLUGIN_WALLET_TOKEN`, `EVM_PRIVATE_KEY`, `SVM_PRIVATE_KEY`); document alignment with **gate-pay-x402**.
- OpenClaw: **servers.manifest** seventh entry and dynamic interactive **--select** menu range.

### Notes

- Not part of the default six trading MCPs; users opt in when they need x402 / Gate Pay MCP tools.

## [2026.4.1-1] - 2026-04-01

### Added

- **`gate-mcp-installer`**: unified installer for Cursor, Claude Code, Codex, and OpenClaw/mcporter.
- Auto platform detection with **failure when multiple** environments match; **`--platform`** override.
- OpenClaw: **`--mcp`** filtering aligned with other platforms; **`--select`** preserved; **gate-skills** clone to `~/.openclaw/skills/` when skills install is enabled.
- Reuses existing JSON/TOML fragments and `merge-mcp-config.js` from the previous per-platform skills.

### Notes

- Supersedes `gate-mcp-cursor-installer`, `gate-mcp-claude-installer`, `gate-mcp-codex-installer`, `gate-mcp-openclaw-installer` (those may remain as redirect stubs).
