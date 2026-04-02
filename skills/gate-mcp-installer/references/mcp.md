---
name: gate-mcp-installer-mcp
version: "2026.4.1-1"
updated: "2026-04-01"
description: "Execution specification for unified Gate MCP + gate-skills installer (Cursor, Claude Code, Codex, OpenClaw)."
---

# Gate MCP Installer — execution specification

## 1. Scope

**In scope**

- Detect or accept target platform; merge/write MCP config without removing unrelated servers.
- Install selected Gate MCP endpoints (default: all six).
- Clone **gate-skills** into the platform skills directory unless `--no-skills`.

**Out of scope**

- Exchange trading or account operations via MCP tools (installer only).

---

## 2. Platform detection

1. If `--platform cursor|claude|codex|openclaw` is set, use it.
2. Otherwise detect signals:
   - **cursor**: `~/.cursor` (or Windows `%APPDATA%\Cursor`)
   - **claude**: `~/.claude.json` or `~/.claude/`
   - **codex**: `$CODEX_HOME` or `~/.codex/`
   - **openclaw**: `mcporter` on `PATH`
3. If **more than one** signal is present, **stop** and require `--platform` (no guessing).
4. If **none**, stop with install instructions.

**Fallback**

- JSON merge: if Node is missing, print fragments for manual merge (Cursor / Claude).
- OpenClaw: if `mcporter` is missing, print `npm install -g mcporter`.

---

## 3. Authentication

- The installer does not require valid trading keys to finish wiring.
- Local CEX trading needs `GATE_API_KEY` / `GATE_API_SECRET` after install.
- Remote exchange needs OAuth2 at first use.
- DEX may need wallet + OAuth as documented in [gate-mcp](https://github.com/gate/gate-mcp).

---

## 4. Tool calling

No Gate business MCP calls. Entrypoint:

- `skills/gate-mcp-installer/scripts/install.sh`

**Flags**

| Flag | Meaning |
|------|---------|
| `--platform` | `cursor` \| `claude` \| `codex` \| `openclaw` |
| `--mcp` | Repeatable: `main`, `cex-public`, `cex-exchange`, `dex`, `info`, `news` |
| `--no-skills` | Skip gate-skills clone |
| `--select` / `-s` | OpenClaw only: interactive menu for one server |

---

## 5. Execution SOP

1. Confirm scope (default all MCPs + skills unless user narrows).
2. Resolve platform; abort if ambiguous without `--platform`.
3. Run `install.sh` with agreed flags.
4. Verify:
   - **Cursor / Claude**: `mcpServers` keys present in JSON target file.
   - **Codex**: `[mcp_servers.gate-cex-pub]` (etc.) present in `config.toml` when selected.
   - **OpenClaw**: `mcporter config list` includes expected server names.
5. Return restart + OAuth / API key next steps; mask secrets in output.

---

## 6. Output templates

```markdown
## Installer Result (unified)
- Platform: {cursor|claude|codex|openclaw}
- MCP Installed: {list}
- Skills Installed: {yes|no}
- Config / tool: {path_or_mcporter}
- Next Steps: {restart + auth}
```

---

## 7. Safety

1. Never delete unrelated MCP server entries.
2. On malformed JSON/TOML, stop and explain remediation.
3. Do not claim success without checking the target config or `mcporter list`.
4. Do not echo API secrets.
