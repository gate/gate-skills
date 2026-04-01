---
name: gate-mcp-codex-installer-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "Execution specification for installing Gate MCP servers and Gate Skills in Codex."
---

# Gate Codex Installer MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Configure selected Gate MCP servers in Codex config
- Install Gate skills bundle unless disabled
- Preserve existing non-Gate config entries

Out of scope:
- Any exchange business action (trading, transfer, account ops)

## 2. MCP Detection and Fallback

Detection:
1. Detect `$CODEX_HOME` and config path availability.
2. Validate installer prerequisites.

Fallback:
- If script flow fails, provide manual config update guidance with exact blocks.

## 3. Authentication

- Installer does not require exchange API key to complete config wiring.
- Local/remote exchange auth is required later when users call private tools.

## 4. MCP Resources

No mandatory MCP resources; this is a local installer/config workflow.

## 5. Tool Calling Specification

No Gate MCP business tool call is required.
Installer entrypoint:
- `skills/gate-mcp-codex-installer/scripts/install.sh`

Key execution options:
- `--mcp <name>` (repeatable)
- `--no-skills`

## 6. Execution SOP (Non-Skippable)

1. Confirm install scope (default all MCPs + skills).
2. Backup/check existing `config.toml` context.
3. Run installer script with user-selected options.
4. Verify `[mcp_servers.*]` entries and skills directory state.
5. Return restart/auth next steps.

## 7. Output Templates

```markdown
## Installer Result (Codex)
- MCP Installed: {list}
- Skills Installed: {yes_or_no}
- Config Updated: {path}
- Next Steps: {restart_and_auth_notes}
```

## 8. Safety and Degradation Rules

1. Never remove unrelated existing `config.toml` sections.
2. Abort on parse/merge errors and report explicit remediation.
3. Do not claim success without post-install verification.
4. Keep sensitive env values masked in output.
