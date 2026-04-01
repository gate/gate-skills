---
name: gate-mcp-cursor-installer-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "Execution specification for installing Gate MCP servers and Gate Skills in Cursor."
---

# Gate Cursor Installer MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Configure selected Gate MCP servers in Cursor MCP config
- Install Gate skills bundle unless disabled
- Preserve existing non-Gate MCP configuration

Out of scope:
- Trading/account business operations

## 2. MCP Detection and Fallback

Detection:
1. Detect Cursor config path availability.
2. Validate installer prerequisites and network reachability.

Fallback:
- If script install fails, provide manual `mcp.json` merge guidance.

## 3. Authentication

- Installer itself does not require exchange API keys.
- Local CEX trading and remote exchange private calls require post-install auth setup.

## 4. MCP Resources

No mandatory MCP resources; this is a local installer/config workflow.

## 5. Tool Calling Specification

No Gate MCP business tool call is required.
Installer entrypoint:
- `skills/gate-mcp-cursor-installer/scripts/install.sh`

Key options:
- `--mcp <name>` (repeatable)
- `--no-skills`

## 6. Execution SOP (Non-Skippable)

1. Confirm target install scope (default all MCPs + skills).
2. Inspect existing `~/.cursor/mcp.json` and merge strategy.
3. Run installer script with selected options.
4. Verify resulting MCP entries and skills path.
5. Return restart/auth instructions.

## 7. Output Templates

```markdown
## Installer Result (Cursor)
- MCP Installed: {list}
- Skills Installed: {yes_or_no}
- Config Updated: {path}
- Next Steps: {restart_and_auth_notes}
```

## 8. Safety and Degradation Rules

1. Never overwrite unrelated MCP server blocks.
2. Abort and explain on malformed JSON or merge conflict.
3. Do not claim success without verification.
4. Mask secrets in user-visible output.
