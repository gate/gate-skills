# Gate CEX One-Click Installer (Cursor MCP + Skills)

One-click installation of Gate MCP servers and all [gate-skills](https://github.com/gate/gate-skills) skills for Cursor, ready to use right after downloading from GitHub.

## Installation

### One-click install from this repository

```bash
# Run from the gate-skills repository root
bash skills/gate-mcp-cursor-installer/scripts/install.sh
```

### Install MCP only (without gate-skills)

```bash
bash skills/gate-mcp-cursor-installer/scripts/install.sh --no-skills
```

### Install specific MCPs only

```bash
# Install only Gate (main) and Gate-Dex
bash skills/gate-mcp-cursor-installer/scripts/install.sh --mcp main --mcp dex

# Install only Gate, Info, and News
bash skills/gate-mcp-cursor-installer/scripts/install.sh --mcp main --mcp info --mcp news
```

## What Gets Installed

| Component | Description |
|-----------|-------------|
| **Gate** | Main MCP, `npx -y gate-mcp`, [gate-mcp](https://github.com/gate/gate-mcp) |
| **Gate-Dex** | https://api.gatemcp.ai/mcp/dex (x-api-key built-in, Authorization: Bearer ${GATE_MCP_TOKEN}) |
| **Gate-Info** | https://api.gatemcp.ai/mcp/info |
| **Gate-News** | https://api.gatemcp.ai/mcp/news |
| **gate-skills** | Cloned from [gate-skills](https://github.com/gate/gate-skills), installs all skills under `skills/` |

## Config File Locations

- **MCP config**: `~/.cursor/mcp.json` (Windows: `%APPDATA%\Cursor\mcp.json`), merged with existing config.
- **Skills**: `~/.cursor/skills/` (Windows: `%APPDATA%\Cursor\skills`).

## Dependencies

- **Bash**: Required to run `install.sh` (built-in on macOS/Linux; use Git Bash or WSL on Windows).
- **Node.js**: Used to merge `mcp.json`; if Node is unavailable, the script outputs a JSON snippet for manual merging.
- **git**: Used to clone gate-skills (not required when using `--no-skills`).

## Getting API Keys & Authorization

- **Gate (main)** spot/futures requires API Key + Secret: Visit **https://www.gate.com/myaccount/profile/api-key/manage** to create one, then set the environment variables `GATE_API_KEY` and `GATE_API_SECRET`.
- **Gate-Dex**: When a query returns an authorization required message, first open https://web3.gate.com/ to create or bind a wallet, then click the Google authorization link returned by the assistant to complete the process.

## After Installation

Restart Cursor to load the new MCP servers and skills.
