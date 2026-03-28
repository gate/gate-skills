# MCP Server Setup Guide

Display this guide when MCP detection fails. Show only the section matching the user's current platform. Display at most once per session.

---

## Server Information

- **Name**: gate-dex (recommended, customizable — system auto-identifies by tool features)
- **Type**: HTTP
- **URL**: https://api.gatemcp.ai/mcp/dex

---

## Platform Configuration

### Cursor

Method A: Settings → MCP → Add new MCP server → Fill in above information

Method B: Edit `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "gate-dex": {
      "transport": "http",
      "url": "https://api.gatemcp.ai/mcp/dex",
      "headers": {
        "Authorization": "Bearer <your_mcp_token>"
      }
    }
  }
}
```

### Claude Code

Edit `~/.claude.json` (or project `.mcp.json`):
```json
{
  "mcpServers": {
    "gate-dex": {
      "type": "url",
      "url": "https://api.gatemcp.ai/mcp/dex",
      "headers": {
        "Authorization": "Bearer <your_mcp_token>"
      }
    }
  }
}
```

### Windsurf

Edit `~/.codeium/windsurf/mcp_config.json`:
```json
{
  "mcpServers": {
    "gate-dex": {
      "transport": "http",
      "serverUrl": "https://api.gatemcp.ai/mcp/dex",
      "headers": {
        "Authorization": "Bearer <your_mcp_token>"
      }
    }
  }
}
```

### Other Platforms

Add the above HTTP-type Server in the platform's MCP configuration, including authentication header.

---

## Authentication

- `<your_mcp_token>` is obtained through MCP login process
- On first use, MCP Server will guide OAuth authentication (supports Google OAuth or Gate OAuth)
- Token is automatically saved after acquisition; subsequent calls use it automatically

## Connection Verification

After configuration, verify with:
```
CallMcpTool(server="gate-dex", toolName="dex_chain_config", arguments={"chain": "ETH"})
```

After installation and authentication, future transactions will automatically use MCP mode.
