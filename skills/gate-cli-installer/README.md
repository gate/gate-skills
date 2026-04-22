# gate-cli + gate-skills installer

This skill helps users install **gate-cli** and **[gate-skills](https://github.com/gate/gate-skills)** on **Cursor**, **Claude Code**, **Codex**, or **OpenClaw** (e.g. mcporter), without relying on separate Gate MCP server setup.

## Quick start

### 1. `gate-cli`

From the repository root (where `skills/gate-cli-installer/setup.sh` lives):

```bash
bash skills/gate-cli-installer/setup.sh
```

Ensure `gate-cli` is reachable: **`setup.sh`** installs to **`~/.local/bin`** (the script may suggest `export PATH="$HOME/.local/bin:$PATH"`). Older installs may use **`~/.openclaw/skills/bin`** — resolve in the order documented in **`SKILL.md`** (*Which `gate-cli` runs (agents / shells)*). Then:

```bash
gate-cli --version
```

On auth or config errors:

```bash
gate-cli config init
```

### 2. gate-skills

Use your client’s skills workflow, for example:

```bash
npx skills add https://github.com/gate/gate-skills
```

Or copy skill folders into the right directory (`~/.cursor/skills/`, `~/.claude/skills/`, `~/.codex/skills/`, or `~/.openclaw/skills/` for OpenClaw). See the main [gate-skills README](https://github.com/gate/gate-skills) for full options.

## Optional: migrate away from legacy Gate MCP

```bash
gate-cli migrate --dry-run
gate-cli migrate --apply
```

## Details

See **`SKILL.md`** in this folder for agent-facing instructions and the full workflow.
