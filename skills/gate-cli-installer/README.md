# gate-cli + gate-skills installer

This skill installs **gate-cli** for **Cursor**, **Claude Code**, **Codex**, or **OpenClaw**. Install the selected skills separately using the product-specific path below. The script does not install MCP servers.

## Quick start

### 1. Install or upgrade `gate-cli` to the latest release

For the default flow, on every install or upgrade query [GitHub's latest release](https://api.github.com/repos/gate/gate-cli/releases/latest) and compare its `tag_name` with the current CLI's `--version` output. A working older CLI still needs upgrading. The skill downloads the CLI at run time and does not bundle or prescribe a fixed version; the target advances as official releases are published.

From the repository root (where `skills/gate-cli-installer/setup.sh` lives):

For the six CEX skills, also follow [CEX setup](../_shared/cex/cli-setup.md) and
verify the exact required command and flags after installation or upgrade. The
latest release version alone does not establish that a required operation is supported.

```bash
# Omit --version so the installer resolves the latest official release each run.
bash skills/gate-cli-installer/setup.sh
```

Ensure `shasum` or `sha256sum` is available so the installer can verify the downloaded archive. Use `--version <release-tag>` only for a user-requested specific version or rollback, never as the default; in that exceptional flow, verify against the requested official published tag and report the explicit selection rather than claiming it is latest. Ask before replacing a development/custom build or downgrading a version newer than the latest official release.

Ensure `gate-cli` is reachable: **`setup.sh`** installs to **`~/.local/bin`** first and prints the actual installation path. Older installs may use **`~/.openclaw/skills/bin`**, and PATH may still select another older binary. For the usual user-local installation, verify both the installed file and the active command:

```bash
# Compare both versions with the latest release tag resolved for this run.
"$HOME/.local/bin/gate-cli" --version
command -v gate-cli
gate-cli --version
```

If PATH selects an older binary, put the new installation directory first for the session, refresh the shell's command cache, and repeat verification. If the client cannot update PATH, use the verified new binary's absolute path and report the remaining PATH setup. Do not automatically edit shell startup files. A failed latest-release lookup, download, checksum check, or version verification leaves the upgrade incomplete; do not silently keep an old version and report success. See **`SKILL.md`** for executable resolution and the full completion rules.

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
