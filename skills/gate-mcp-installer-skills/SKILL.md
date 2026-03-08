---
name: gate-mcp-installer-skills
version: "2026.3.4-1"
updated: "2026-03-04"
description: One-click installer and configurator for Gate MCP (mcporter) in OpenClaw. Use when the user wants to (1) Install mcporter CLI tool, (2) Configure Gate MCP server connection, (3) Verify Gate MCP setup, or (4) Troubleshoot Gate MCP connectivity issues.
---

# Gate MCP Installer

This skill provides a one-click setup flow for Gate MCP (`mcporter`) in OpenClaw.

## Quick Start

To set up Gate MCP, run the installer:

```bash
bash ~/.openclaw/skills/gate-mcp-installer-skills/scripts/install-gate-mcp.sh
```

You can also invoke this skill directly and follow the guided installation flow.

## What This Skill Does

This skill automates the full Gate MCP setup workflow:

1. **Installs the `mcporter` CLI** globally with npm
2. **Configures the Gate MCP server** with the correct endpoint
3. **Verifies connectivity** by listing the available tools
4. **Provides example prompts** for common usage

## Manual Installation Steps

If the installer script does not succeed, follow these steps manually.

### Step 1: Install mcporter

```bash
npm i -g mcporter
# Or verify the installation
npx mcporter --version
```

### Step 2: Configure Gate MCP

```bash
mcporter config add gate https://api.gatemcp.ai/mcp --scope home
```

### Step 3: Verify Configuration

```bash
# Check that the config was written
mcporter config get gate

# List available tools
mcporter list gate --schema
```

If tools are listed, Gate MCP is ready to use.

## Common Usage Examples

After installation, Gate MCP can be used with prompts like:

- "check BTC/USDT price"
- "use gate mcp to analyze SOL"
- "what arbitrage opportunities are there on Gate?"
- "check ETH funding rate"

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `command not found: mcporter` | Run `npm i -g mcporter` |
| Config not found | Run the `config add` command again |
| Connection timeout | Check internet connectivity to `fulltrust.link` |
| No tools listed | Verify that the config URL is correct |

## Resources

- **Install script**: `scripts/install-gate-mcp.sh` - automated one-click installer
