#!/usr/bin/env bash
# Gate CEX One-Click Installer: MCP (main/dex/info/news selectable) + all gate-skills
# Usage: install.sh [--mcp main] [--mcp dex] ... [--no-skills]  Installs all MCPs when no --mcp is passed
# DEX MCP uses fixed x-api-key: MCP_AK_8W2N7Q

set -e

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
MCP_DEX=0
MCP_INFO=0
MCP_NEWS=0
INSTALL_SKILLS=1

usage() {
  echo "Usage: $0 [--mcp main|dex|info|news] ... [--no-skills]"
  echo "  Installs all MCPs when no --mcp is passed; pass multiple --mcp to install only specified ones."
  echo "  --no-skills  Install MCP only, do not clone gate-skills."
  echo "Examples: $0"
  echo "          $0 --mcp main --mcp dex"
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mcp)
      shift
      case "$1" in
        main)   MCP_MAIN=1 ;;
        dex)    MCP_DEX=1 ;;
        info)   MCP_INFO=1 ;;
        news)   MCP_NEWS=1 ;;
        *)      echo "Unknown MCP: $1 (available: main, dex, info, news)" >&2; exit 1 ;;
      esac
      shift
      ;;
    --no-skills) INSTALL_SKILLS=0; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown argument: $1" >&2; usage ;;
  esac
done

# If no --mcp specified, select all
if [[ $MCP_MAIN -eq 0 && $MCP_DEX -eq 0 && $MCP_INFO -eq 0 && $MCP_NEWS -eq 0 ]]; then
  MCP_MAIN=1
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

# DEX MCP fixed x-api-key
GATE_API_KEY="MCP_AK_8W2N7Q"

# ---------- 1. Merge and write mcp.json ----------
mkdir -p "$(dirname "$MCP_JSON")"

# Build mcpServers fragment to add (Bash 3 compatible)
# main: prefer global gate-mcp (avoids npx ESM path resolution failures with @modelcontextprotocol/sdk)
# dex: url + x-api-key header + Authorization Bearer token
# info/news: url + streamable-http
if [[ $MCP_MAIN -eq 1 ]] && command -v gate-mcp &>/dev/null; then
  GATE_MAIN_CMD="gate-mcp"
  GATE_MAIN_ARGS="[]"
elif [[ $MCP_MAIN -eq 1 ]]; then
  GATE_MAIN_CMD="npx"
  GATE_MAIN_ARGS="[\"-y\",\"gate-mcp\"]"
fi
ADD_JSON="{"
first=1
if [[ $MCP_MAIN -eq 1 ]]; then
  [[ $first -eq 0 ]] && ADD_JSON="${ADD_JSON},"
  if [[ -n "$USER_GATE_API_KEY" ]]; then
    ADD_JSON="${ADD_JSON}\"Gate\":{\"command\":\"${GATE_MAIN_CMD}\",\"args\":${GATE_MAIN_ARGS},\"env\":{\"GATE_API_KEY\":\"${USER_GATE_API_KEY}\",\"GATE_API_SECRET\":\"${USER_GATE_API_SECRET}\"}}"
  else
    ADD_JSON="${ADD_JSON}\"Gate\":{\"command\":\"${GATE_MAIN_CMD}\",\"args\":${GATE_MAIN_ARGS},\"env\":{\"GATE_API_KEY\":\"your-api-key\",\"GATE_API_SECRET\":\"your-api-secret\"}}"
  fi
  first=0
fi
if [[ $MCP_DEX -eq 1 ]]; then
  [[ $first -eq 0 ]] && ADD_JSON="${ADD_JSON},"
  ADD_JSON="${ADD_JSON}\"Gate-Dex\":{\"url\":\"https://api.gatemcp.ai/mcp/dex\",\"transport\":\"streamable-http\",\"headers\":{\"x-api-key\":\"${GATE_API_KEY}\",\"Authorization\":\"Bearer \${GATE_MCP_TOKEN}\"}}"
  first=0
fi
if [[ $MCP_INFO -eq 1 ]]; then
  [[ $first -eq 0 ]] && ADD_JSON="${ADD_JSON},"
  ADD_JSON="${ADD_JSON}\"Gate-Info\":{\"url\":\"https://api.gatemcp.ai/mcp/info\",\"transport\":\"streamable-http\"}"
  first=0
fi
if [[ $MCP_NEWS -eq 1 ]]; then
  [[ $first -eq 0 ]] && ADD_JSON="${ADD_JSON},"
  ADD_JSON="${ADD_JSON}\"Gate-News\":{\"url\":\"https://api.gatemcp.ai/mcp/news\",\"transport\":\"streamable-http\"}"
  first=0
fi
ADD_JSON="${ADD_JSON}}"

if command -v node &>/dev/null; then
  EXISTING="{}"
  [[ -f "$MCP_JSON" ]] && EXISTING=$(cat "$MCP_JSON")
  TMP_JSON=$(mktemp)
  echo "$EXISTING" > "$TMP_JSON"
  node -e "
    const fs = require('fs');
    const existingPath = process.argv[1];
    const addJson = process.argv[2];
    const outPath = process.argv[3];
    const existing = JSON.parse(fs.readFileSync(existingPath, 'utf8'));
    const add = JSON.parse(addJson);
    existing.mcpServers = existing.mcpServers || {};
    Object.assign(existing.mcpServers, add);
    fs.writeFileSync(outPath, JSON.stringify(existing, null, 2));
  " "$TMP_JSON" "$ADD_JSON" "$MCP_JSON"
  rm -f "$TMP_JSON"
  echo "MCP config written to: $MCP_JSON"
  if [[ $MCP_MAIN -eq 1 && "$GATE_MAIN_CMD" == "npx" ]]; then
    echo ""
    echo "Note: Gate (main) is currently launched via npx. If you encounter ERR_MODULE_NOT_FOUND (@modelcontextprotocol/sdk) on startup, run:"
    echo "  npm install -g gate-mcp"
    echo "Then re-run this script, or manually change the Gate command in mcp.json to gate-mcp with args []."
  fi
else
  echo "Node.js not found. Please manually merge the following into the mcpServers section of $MCP_JSON:"
  echo "  $ADD_JSON"
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

if [[ $MCP_DEX -eq 1 ]]; then
  echo ""
  echo "Gate-Dex authorization note: When a gate-dex query returns an authorization required message,"
  echo "  first open the link below to create or bind a wallet, then the assistant will return a"
  echo "  clickable Google authorization link for you to complete OAuth."
  echo "  https://web3.gate.com/"
  echo ""
fi

echo "Done. Please restart Cursor to load the MCP servers."
