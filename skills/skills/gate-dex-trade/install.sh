#!/bin/bash

# Gate Trade MCP Installer
# Interactive installer focusing on trading functionality

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Repository root is one level up from gate-dex-trade/
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${BOLD}🔄 Gate Trade MCP Installer${NC}"
echo "=================================="
echo "Interactive installer for trading functionality"
echo ""

# Platform detection
detect_platforms() {
    local platforms=()
    
    if command -v cursor &> /dev/null; then
        platforms+=("cursor")
    fi
    
    if command -v claude &> /dev/null; then
        platforms+=("claude")
    fi
    
    if command -v codex &> /dev/null; then
        platforms+=("codex")
    fi
    
    if command -v mcporter &> /dev/null; then
        platforms+=("openclaw")
    fi
    
    echo "${platforms[@]}"
}

# Interactive platform selection
select_platform() {
    local detected_platforms=($(detect_platforms))
    
    echo -e "${BLUE}🔍 Detected AI Platforms:${NC}"
    if [ ${#detected_platforms[@]} -eq 0 ]; then
        echo "  ❌ No supported platforms detected"
        echo ""
        echo -e "${YELLOW}Please install one of the following AI platforms:${NC}"
        echo "  • Cursor: https://cursor.com"
        echo "  • Claude Code: https://docs.anthropic.com/claude-code"
        echo "  • Codex CLI: https://developers.openai.com/codex"
        echo "  • OpenClaw (mcporter): https://github.com/mcporter-dev/mcporter"
        exit 1
    fi
    
    local i=1
    for platform in "${detected_platforms[@]}"; do
        case "$platform" in
            cursor) echo "  $i) Cursor ✅" ;;
            claude) echo "  $i) Claude Code ✅" ;;
            codex) echo "  $i) Codex CLI ✅" ;;
            openclaw) echo "  $i) OpenClaw (mcporter) ✅" ;;
        esac
        ((i++))
    done
    echo "  a) All platforms (recommended)"
    echo ""
    
    read -p "Please select platforms to configure [1-${#detected_platforms[@]}/a] (default a): " choice
    choice=${choice:-a}
    
    if [ "$choice" = "a" ]; then
        echo "${detected_platforms[@]}"
    elif [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le ${#detected_platforms[@]} ]; then
        echo "${detected_platforms[$((choice-1))]}"
    else
        echo -e "${RED}Invalid selection, using all platforms${NC}"
        echo "${detected_platforms[@]}"
    fi
}

# Create OpenAPI configuration
create_openapi_config() {
    echo -e "${CYAN}⚡ Configuring OpenAPI fallback support...${NC}"
    
    local config_dir="$HOME/.gate-dex-openapi"
    local config_file="$config_dir/config.json"
    
    mkdir -p "$config_dir"
    chmod 700 "$config_dir"
    
    if [ ! -f "$config_file" ]; then
        cat > "$config_file" << 'EOF'
{
  "api_key": "ak_default_demo_key",
  "secret_key": "sk_default_demo_key_PLACEHOLDER",
  "default_slippage": 0.005,
  "base_url": "https://openapi.gateweb3.cc/api/v1/dex"
}
EOF
        chmod 600 "$config_file"
        echo -e "${GREEN}  ✓${NC} OpenAPI default configuration created"
        echo -e "${BLUE}  ℹ${NC} Config location: $config_file"
        echo -e "${BLUE}  ℹ${NC} Get dedicated keys: https://www.gatedex.com/developer"
    else
        echo -e "${YELLOW}  ⚠${NC} OpenAPI configuration already exists, skipping creation"
    fi
}

# Install functions (trade-focused)
install_cursor() {
    echo -e "${CYAN}📱 Configuring Cursor (trading priority)...${NC}"
    
    # Create MCP config
    local cursor_mcp_path="$HOME/.cursor/mcp.json"
    local cursor_mcp_dir="$(dirname "$cursor_mcp_path")"
    
    mkdir -p "$cursor_mcp_dir"
    
    if [ -f "$cursor_mcp_path" ]; then
        echo -e "${YELLOW}  ⚠${NC} Existing MCP configuration detected, backing up to mcp.json.backup"
        cp "$cursor_mcp_path" "$cursor_mcp_path.backup"
    fi
    
    cat > "$cursor_mcp_path" << 'EOF'
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
EOF
    
    # Create skills directory and link
    mkdir -p .cursor/skills
    if [ ! -e ".cursor/skills/gate-dex-trade" ]; then
        ln -s "$(pwd)" ".cursor/skills/gate-dex-trade"
        echo -e "${GREEN}  ✓${NC} Skills link created"
    else
        echo -e "${YELLOW}  ⚠${NC} Skills link already exists"
    fi
    
    # Create routing rules
    mkdir -p .cursor/rules
    cat > .cursor/rules/gate-dex-trade.md << 'EOF'
# Gate DEX Trade Priority Routing

When users mention the following keywords, prioritize trading-related functions:

- 🔄 Swap, exchange, buy, sell, quote → gate-dex-trade/SKILL.md
- 💱 Cross-chain exchange, bridge → gate-dex-trade/SKILL.md (MCP mode)
- 📊 Trade after checking market data → First gate-dex-market, then route to gate-dex-trade

Intelligent mode selection:
- User explicitly says "OpenAPI" → Force OpenAPI mode  
- Cross-chain requirements → Force MCP mode
- Other situations → Auto-detect optimal mode

Security rules:
- All trades must have three-step confirmation (trading pair→quote→signature)
- Exchange value difference > 5% forced warning
- Cross-chain trading additional risk warnings
EOF
    
    echo -e "${GREEN}  ✓${NC} Cursor trading configuration completed"
}

install_claude() {
    echo -e "${CYAN}🤖 Configuring Claude Code (trading priority)...${NC}"
    
    # Create project-level MCP config
    cat > .mcp.json << 'EOF'
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
EOF
    echo -e "${GREEN}  ✓${NC} .mcp.json created"
    
    # Create routing file
    cat > CLAUDE.md << 'EOF'
# Gate DEX Trade Skills

When users request the following operations, read the corresponding SKILL.md file and strictly follow its processes:

## Core Trading Functions
- 🔄 Swap, exchange, buy, sell, quote → `gate-dex-trade/SKILL.md`
- 💱 Cross-chain exchange → `gate-dex-trade/SKILL.md` (Force MCP mode)
- 📊 View transaction status, order history → `gate-dex-trade/SKILL.md`

## Collaboration Functions  
- 💰 Trade after checking balance → Guide to `gate-dex-trade/SKILL.md`
- 📈 Buy after checking market data → Guide to `gate-dex-trade/SKILL.md`

## Mode Selection
- User explicitly specifies "OpenAPI"/"AK/SK" → Force OpenAPI mode
- Cross-chain requirements → Force MCP mode (OpenAPI doesn't support cross-chain)
- Other situations → Intelligent routing selects optimal mode

## Security Rules
- All trades must have three-step confirmation (trading pair confirmation → quote display → signature authorization)
- Auto-fallback to OpenAPI mode when MCP Server unavailable
- Exchange value difference > 5% triggers forced warning
- Cross-chain trading includes additional risk warnings

Prioritize trading-related functions. Auto-guide to MCP login process or configure OpenAPI credentials when authentication needed.
EOF
    
    echo -e "${GREEN}  ✓${NC} CLAUDE.md trading routing created"
}

install_codex() {
    echo -e "${CYAN}⚙️ Configuring Codex CLI (trading priority)...${NC}"
    
    # Create AGENTS.md for Codex CLI
    cat > AGENTS.md << 'EOF'
# Gate DEX Trade Skills

When users request the following operations, read the corresponding SKILL.md file and strictly follow its processes:

## Core Trading Functions
- 🔄 Swap, exchange, buy, sell, quote → `gate-dex-trade/SKILL.md`
- 💱 Cross-chain exchange → `gate-dex-trade/SKILL.md` (Force MCP mode)
- 📊 View transaction status, order history → `gate-dex-trade/SKILL.md`

## Collaboration Functions  
- 💰 Trade after checking balance → Guide to `gate-dex-trade/SKILL.md`
- 📈 Buy after checking market data → Guide to `gate-dex-trade/SKILL.md`

Prioritize trading-related functions. Auto-fallback to OpenAPI mode when MCP Server unavailable.
EOF
    
    echo -e "${GREEN}  ✓${NC} AGENTS.md created"
    echo -e "${BLUE}  ℹ${NC} Please manually run: codex mcp add gate-dex --transport http --url https://api.gatemcp.ai/mcp/dex"
}

install_openclaw() {
    echo -e "${CYAN}🐾 Configuring OpenClaw (trading priority)...${NC}"
    
    # Create opencode.json config
    cat > opencode.json << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "gate-dex": {
      "type": "remote",
      "url": "https://api.gatemcp.ai/mcp/dex",
      "enabled": true,
      "headers": {
        "Authorization": "Bearer <your_mcp_token>"
      }
    }
  }
}
EOF
    echo -e "${GREEN}  ✓${NC} opencode.json created"
    
    # Create AGENTS.md routing
    cat > AGENTS.md << 'EOF'
# Gate DEX Trade Skills

When users request the following operations, read the corresponding SKILL.md file and strictly follow its processes:

## Core Trading Functions
- 🔄 Swap, exchange, buy, sell, quote → `gate-dex-trade/SKILL.md`
- 💱 Cross-chain exchange → `gate-dex-trade/SKILL.md` (Force MCP mode)
- 📊 View transaction status, order history → `gate-dex-trade/SKILL.md`

## Intelligent Routing
- Auto-detect MCP Server availability
- Fallback to OpenAPI mode when MCP unavailable
- Cross-chain requirements force MCP mode

Prioritize trading-related functions.
EOF
    
    echo -e "${GREEN}  ✓${NC} OpenClaw trading configuration completed"
}

# Main
main() {
    local selected_platforms=($(select_platform))
    
    echo ""
    echo -e "${CYAN}🚀 Starting trading functionality configuration...${NC}"
    echo ""
    
    # Always create OpenAPI config for fallback
    create_openapi_config
    echo ""
    
    for platform in "${selected_platforms[@]}"; do
        case "$platform" in
            cursor) install_cursor ;;
            claude) install_claude ;;
            codex) install_codex ;;
            openclaw) install_openclaw ;;
        esac
        echo ""
    done
    
    echo "=================================="
    echo -e "${GREEN}🎉 Gate Trade Installation Complete!${NC}"
    echo ""
    echo -e "${BLUE}📱 Configured Platforms:${NC}"
    for platform in "${selected_platforms[@]}"; do
        echo "  ✓ $platform"
    done
    echo ""
    echo -e "${BLUE}🔧 Configuration Summary:${NC}"
    echo "  • MCP Server: gate-dex (https://api.gatemcp.ai/mcp/dex)"
    echo "  • OpenAPI Fallback: ~/.gate-dex-openapi/config.json"
    echo "  • Routing Priority: Trading functions prioritized"
    echo ""
    echo -e "${BLUE}🎯 Next Steps:${NC}"
    echo "1. Restart your AI tool"
    echo "2. Try trading: \"Swap 100 USDT for ETH\""
    echo "3. Check modes: \"Use OpenAPI mode to swap\" or \"Cross-chain exchange\""
    echo "4. View documentation: ./gate-dex-trade/README.md"
    echo ""
    echo -e "${CYAN}💡 Tips:${NC}"
    echo "  • Supports MCP + OpenAPI dual modes, auto-selects optimal calling method"
    echo "  • Cross-chain trading requires MCP mode, same-chain trading supports both modes"
    echo "  • All trades have three-step confirmation gateway for security"
    echo ""
    echo -e "${YELLOW}🔧 Troubleshooting:${NC}"
    echo "  • MCP connection failed → Check network and platform configuration"
    echo "  • OpenAPI authentication failed → Get dedicated keys to replace default config"
    echo "  • Cross-chain not supported → Ensure MCP Server connection is normal"
    echo ""
    echo -e "${CYAN}🔐 Authentication Instructions:${NC}"
    echo "  • MCP mode supports Google OAuth and Gate OAuth login"
    echo "  • First use will auto-guide authentication method selection"
    echo "  • Token automatically saved after successful authentication, no need to re-login"
    echo ""
}

# Parse arguments
case "${1:-}" in
    --help|-h)
        echo "Gate Trade MCP Installer"
        echo "Interactive installer for trading functionality"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help"
        echo "  --list, -l     List detected platforms"
        echo ""
        exit 0
        ;;
    --list|-l)
        echo -e "${BLUE}🔍 Detected Platforms:${NC}"
        platforms=($(detect_platforms))
        for platform in "${platforms[@]}"; do
            echo "  ✓ $platform"
        done
        exit 0
        ;;
    "") main ;;
    *) echo -e "${RED}Unknown option: $1${NC}"; exit 1 ;;
esac