# gate-cli + gate-skills installer

This skill installs **gate-cli** for **Cursor**, **Claude Code**, **Codex**, or **OpenClaw**. Install the selected skills separately using the product-specific path below. The script does not install MCP servers.

## Quick start

### 1. `gate-cli`

From the repository root (where `skills/gate-cli-installer/setup.sh` lives):

Reuse an existing trusted CLI when it already supports the required operation;
run the installer only when installation or an approved update is needed. For the
six CEX skills, follow [CEX setup](../_shared/cex/cli-setup.md) and verify the exact
required command and flags; the installed version label alone is insufficient.

```bash
bash skills/gate-cli-installer/setup.sh
```

Ensure `gate-cli` is reachable: **`setup.sh`** installs to **`~/.local/bin`** (the script may suggest `export PATH="$HOME/.local/bin:$PATH"`). Older installs may use **`~/.openclaw/skills/bin`** — resolve in the order documented in **`SKILL.md`** (*Which `gate-cli` runs (agents / shells)*). Then:

```bash
gate-cli --version
```

For an authorized local credential setup when the selected private operation needs it:

```bash
gate-cli config init
```

### 2. gate-skills

**Six CEX skills:** build and copy the requested standalone packages using the
[repository CEX guide](../../README.md#gate-cex-skill-20). Each generated package
contains its shared rules. Directly copying a CEX source folder leaves shared
references unresolved.

**Non-CEX skills:** use your client’s skills workflow and select the intended
product, for example:

```bash
npx skills add https://github.com/gate/gate-skills --skill gate-info-research
```

Or copy only the required non-CEX skill folders into the right directory
(`~/.cursor/skills/`, `~/.claude/skills/`, `~/.codex/skills/`, or
`~/.openclaw/skills/`). See the [repository installation guide](../../README.md#skills-installation-guide).
Pay products that require MCP setup use the separate [MCP installer](../gate-mcp-installer/README.md).

## Optional: migrate away from legacy Gate MCP

This cleanup is for a selected Info/News migration, not a CEX prerequisite.
Review the preview and authorize the affected entries before applying it. Preserve
Exchange MCP connections still used by Pay; a CLI installation does not authorize
removing them.

```bash
# Preview the proposed changes without modifying client configuration.
gate-cli migrate --dry-run
```

## Details

See [SKILL.md](SKILL.md) for agent-facing instructions, the authorized migration
flow and the full installation workflow.
