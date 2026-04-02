# Changelog

## [2026.4.1-1] - 2026-04-01

### Added

- **`gate-mcp-installer`**: unified installer for Cursor, Claude Code, Codex, and OpenClaw/mcporter.
- Auto platform detection with **failure when multiple** environments match; **`--platform`** override.
- OpenClaw: **`--mcp`** filtering aligned with other platforms; **`--select`** preserved; **gate-skills** clone to `~/.openclaw/skills/` when skills install is enabled.
- Reuses existing JSON/TOML fragments and `merge-mcp-config.js` from the previous per-platform skills.

### Notes

- Supersedes `gate-mcp-cursor-installer`, `gate-mcp-claude-installer`, `gate-mcp-codex-installer`, `gate-mcp-openclaw-installer` (those may remain as redirect stubs).
