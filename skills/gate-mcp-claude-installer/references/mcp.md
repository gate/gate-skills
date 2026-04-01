---
name: gate-mcp-claude-installer-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "Execution specification for installing Gate MCP servers and Gate Skills in Claude Code."
---

# Gate Claude Installer MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Install selected Gate MCP endpoints for Claude
- Install Gate skills bundle unless user opts out
- Merge into existing Claude config safely

Out of scope:
- Trading operations or market analysis execution

## 2. MCP Detection and Fallback

Detection:
1. Check runtime environment and presence of target config path.
2. Validate network reachability for installer sources when needed.

Fallback:
- If auto install fails, provide manual config snippet and next steps.

## 3. Authentication

- Installer flow itself does not require trading API keys.
- Local CEX trading usage may require `GATE_API_KEY` and `GATE_API_SECRET` after install.
- Remote exchange endpoint requires OAuth2 at first use.

## 4. MCP Resources

No mandatory MCP resources; primary action is local configuration/script execution.

## 5. Tool Calling Specification

No Gate MCP business tool call is required.
Installer entrypoint:
- `skills/gate-mcp-claude-installer/scripts/install.sh`

Key execution options:
- `--mcp <name>` (repeatable)
- `--no-skills`

## 6. Execution SOP (Non-Skippable)

1. Confirm target MCP subset (or default all).
2. Check config file location and existing entries.
3. Run installer script with selected options.
4. Verify resulting config sections and skills installation.
5. Return post-install actions (restart client, auth steps).

## 7. Output Templates

```markdown
## Installer Result (Claude)
- MCP Installed: {list}
- Skills Installed: {yes_or_no}
- Config Updated: {path}
- Next Steps: {restart_and_auth_notes}
```

## 8. Safety and Degradation Rules

1. Never overwrite unrelated existing MCP config blocks.
2. If merge conflicts occur, stop and provide manual remediation.
3. Do not claim successful install without verification.
4. Keep secrets out of logs and user-visible output.
