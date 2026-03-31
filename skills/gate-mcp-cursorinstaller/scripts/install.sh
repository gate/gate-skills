#!/usr/bin/env bash
# Gate Cursor One-Click Installer: MCP + all gate-skills
# Usage: install.sh [--mcp main|cex-public|cex-exchange|dex|info|news] ... [--no-skills]
#   main / cex-public / cex-exchange: see gate-mcp README (Local vs Remote CEX)
# Installs all MCPs when no --mcp is passed. DEX fixed x-api-key: MCP_AK_8W2N7Q

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

GATE_SKILLS_REPO="https://github.com/gate/gate-skills.git"
GATE_SKILLS_BRANCH="${GATE_SKILLS_BRANCH:-master}"
# Cursor user-level config and skills directory (macOS/Linux)
if [[ -n "$CURSOR_USER_HOME" ]]; then
  CURSOR_HOME="$CURSOR_USER_HOME"
else
  CURSOR_HOME="${HOME}"
fi
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  MCP_JSON="${APPDATA:-$CURSOR_HOME/AppData/Roaming}/Cursor/mcp.json"
  SKILLS_DIR="${APPDATA:-$CURSOR_HOME/AppData/Roaming}/Cursor/skills"
else
  MCP_JSON="${CURSOR_HOME}/.cursor/mcp.json"
  SKILLS_DIR="${CURSOR_HOME}/.cursor/skills"
fi

# Default: install all MCPs, install skills
MCP_MAIN=0
MCP_CEX_PUBLIC=0
MCP_CEX_EXCHANGE=0
MCP_DEX=0
MCP_INFO=0
MCP_NEWS=0
INSTALL_SKILLS=1

usage() {
  echo "Usage: $0 [--mcp main|cex-public|cex-exchange|dex|info|news] ... [--no-skills]"
  echo "  Installs all MCPs when no --mcp is passed; pass multiple --mcp to install only specified ones."
  echo "  --no-skills  Install MCP only, do not clone gate-skills."
  echo "Examples: $0"
  echo "          $0 --mcp main --mcp dex"
  echo "          $0 --mcp cex-public --mcp cex-exchange"
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mcp)
      shift
      case "$1" in
        main)         MCP_MAIN=1 ;;
        cex-public)   MCP_CEX_PUBLIC=1 ;;
        cex-exchange) MCP_CEX_EXCHANGE=1 ;;
        dex)          MCP_DEX=1 ;;
        info)         MCP_INFO=1 ;;
        news)         MCP_NEWS=1 ;;
        *)            echo "Unknown MCP: $1 (available: main, cex-public, cex-exchange, dex, info, news)" >&2; exit 1 ;;
      esac
      shift
      ;;
    --no-skills) INSTALL_SKILLS=0; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown argument: $1" >&2; usage ;;
  esac
done

# If no --mcp specified, select all
if [[ $MCP_MAIN -eq 0 && $MCP_CEX_PUBLIC -eq 0 && $MCP_CEX_EXCHANGE -eq 0 && $MCP_DEX -eq 0 && $MCP_INFO -eq 0 && $MCP_NEWS -eq 0 ]]; then
  MCP_MAIN=1
  MCP_CEX_PUBLIC=1
  MCP_CEX_EXCHANGE=1
  MCP_DEX=1
  MCP_INFO=1
  MCP_NEWS=1
fi

# Gate (main) requires node + npx; check before installation and attempt to install npx if missing
if [[ $MCP_MAIN -eq 1 ]]; then
  if ! command -v node &>/dev/null; then
    echo "Error: Node.js not found. Gate (main) MCP requires Node.js (with npx)." >&2
    echo "Please install first: https://nodejs.org or use nvm/fnm to install Node.js, then retry." >&2
    exit 1
  fi
  if ! command -v npx &>/dev/null; then
    echo "npx not found, attempting to install: npm install -g npx ..."
    if npm install -g npx 2>/dev/null; then
      echo "npx installed successfully."
    else
      echo "Error: npx not found, and automatic installation failed." >&2
      echo "Please run manually: npm install -g npx" >&2
      exit 1
    fi
  fi
fi

# Gate (main) spot/futures requires user's API Key
USER_GATE_API_KEY=""
USER_GATE_API_SECRET=""
if [[ $MCP_MAIN -eq 1 ]]; then
  echo ""
  echo "Gate (main) spot/futures trading requires an API Key to operate your account."
  echo "Visit the link below to create an API Key (enable spot/futures trading permissions):"
  echo "  https://www.gate.com/myaccount/profile/api-key/manage"
  echo ""
  read -p "  GATE_API_KEY (leave empty to skip): " USER_GATE_API_KEY
  if [[ -n "$USER_GATE_API_KEY" ]]; then
    read -s -p "  GATE_API_SECRET: " USER_GATE_API_SECRET
    echo ""
    if [[ -z "$USER_GATE_API_SECRET" ]]; then
      echo "Warning: GATE_API_SECRET is empty; spot/futures trading will not work." >&2
      USER_GATE_API_KEY=""
    fi
  fi
fi

# ---------- 1. Merge and write mcp.json ----------
mkdir -p "$(dirname "$MCP_JSON")"

# MCP fragments live under scripts/mcp-fragments/cursor/*.json (readable multi-line JSON)
# main: prefer global gate-mcp (avoids npx ESM path resolution failures with @modelcontextprotocol/sdk)
GATE_MAIN_CMD=""
FRAG_DIR="$SCRIPT_DIR/mcp-fragments/cursor"
FRAGS=()
if [[ $MCP_MAIN -eq 1 ]] && command -v gate-mcp &>/dev/null; then
  GATE_MAIN_CMD="gate-mcp"
  FRAGS+=("$FRAG_DIR/gate-main-gate-mcp.json")
elif [[ $MCP_MAIN -eq 1 ]]; then
  GATE_MAIN_CMD="npx"
  FRAGS+=("$FRAG_DIR/gate-main-npx.json")
fi
[[ $MCP_CEX_PUBLIC -eq 1 ]]   && FRAGS+=("$FRAG_DIR/gate-cex-pub.json")
[[ $MCP_CEX_EXCHANGE -eq 1 ]] && FRAGS+=("$FRAG_DIR/gate-cex-ex.json")
[[ $MCP_DEX -eq 1 ]]          && FRAGS+=("$FRAG_DIR/gate-dex.json")
[[ $MCP_INFO -eq 1 ]]         && FRAGS+=("$FRAG_DIR/gate-info.json")
[[ $MCP_NEWS -eq 1 ]]         && FRAGS+=("$FRAG_DIR/gate-news.json")

MERGE_JS="$SCRIPT_DIR/merge-mcp-config.js"

if command -v node &>/dev/null; then
  EXISTING="{}"
  [[ -f "$MCP_JSON" ]] && EXISTING=$(cat "$MCP_JSON")
  TMP_JSON=$(mktemp)
  echo "$EXISTING" > "$TMP_JSON"
  unset GATE_USER_API_KEY GATE_USER_API_SECRET 2>/dev/null || true
  if [[ -n "$USER_GATE_API_KEY" ]]; then
    export GATE_USER_API_KEY="$USER_GATE_API_KEY"
    export GATE_USER_API_SECRET="$USER_GATE_API_SECRET"
  fi
  node "$MERGE_JS" "$TMP_JSON" "$MCP_JSON" "${FRAGS[@]}"
  unset GATE_USER_API_KEY GATE_USER_API_SECRET 2>/dev/null || true
  rm -f "$TMP_JSON"
  echo "MCP config written to: $MCP_JSON"
  if [[ $MCP_MAIN -eq 1 && "$GATE_MAIN_CMD" == "npx" ]]; then
    echo ""
    echo "Note: Gate (main) is currently launched via npx. If you encounter ERR_MODULE_NOT_FOUND (@modelcontextprotocol/sdk) on startup, run:"
    echo "  npm install -g gate-mcp"
    echo "Then re-run this script, or manually change the Gate command in mcp.json to gate-mcp with args []."
  fi
else
  echo "Node.js not found. Install Node.js to merge MCP config, or manually copy the following JSON fragments into mcpServers in $MCP_JSON:"
  for f in "${FRAGS[@]}"; do
    echo ""
    echo "  # $f"
    sed 's/^/  /' "$f"
  done
fi

# ---------- 2. Install all gate-skills (optional) ----------
if [[ $INSTALL_SKILLS -eq 0 ]]; then
  echo "Skipped gate-skills installation (--no-skills)."
else
  echo "Installing gate-skills (all)..."
  TMP_CLONE=$(mktemp -d 2>/dev/null || mktemp -d -t gate-skills)
  trap "rm -rf '$TMP_CLONE'" EXIT

  if command -v git &>/dev/null; then
    git clone --depth 1 -b "$GATE_SKILLS_BRANCH" "$GATE_SKILLS_REPO" "$TMP_CLONE"
  else
    echo "git is required to clone gate-skills. Please install git or use --no-skills to install MCP only." >&2
    exit 1
  fi

  mkdir -p "$SKILLS_DIR"
  SKILLS_SRC="$TMP_CLONE/skills"
  if [[ ! -d "$SKILLS_SRC" ]]; then
    echo "skills directory not found in the gate-skills repository" >&2
    exit 1
  fi

  for dir in "$SKILLS_SRC"/*; do
    [[ -d "$dir" ]] || continue
    name=$(basename "$dir")
    dst="$SKILLS_DIR/$name"
    if [[ -d "$dst" ]]; then
      rm -rf "$dst"
    fi
    cp -R "$dir" "$dst"
    echo "  Installed skill: $name"
  done

  echo "Skills installed to: $SKILLS_DIR"
fi

if [[ $MCP_MAIN -eq 1 && -z "$USER_GATE_API_KEY" ]]; then
  echo ""
  echo "Gate (main) API Key reminder:"
  echo "  Spot/futures trading requires an API Key. Visit the link below to create one:"
  echo "    https://www.gate.com/myaccount/profile/api-key/manage"
  echo "  After creation, add GATE_API_KEY and GATE_API_SECRET to the Gate env field in $MCP_JSON:"
  echo "    \"Gate\": { ..., \"env\": { \"GATE_API_KEY\": \"your-key\", \"GATE_API_SECRET\": \"your-secret\" } }"
fi

if [[ $MCP_CEX_EXCHANGE -eq 1 ]]; then
  echo ""
  echo "gate-cex-ex (OAuth2): Complete Gate login when Cursor prompts on first connect."
  echo "  Docs: https://github.com/gate/gate-mcp"
  echo ""
fi

if [[ $MCP_DEX -eq 1 ]]; then
  echo ""
  echo "Gate-Dex authorization note: When a gate-dex query returns an authorization required message,"
  echo "  first open the link below to create or bind a wallet, then the assistant will return a"
  echo "  clickable Google authorization link for you to complete OAuth."
  echo "  https://web3.gate.com/"
  echo ""
fi

echo "Done. Please restart Cursor to load the MCP servers."
