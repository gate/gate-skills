#!/usr/bin/env bash
# Gate Codex One-Click Installer: MCP + all gate-skills
# Usage: install.sh [--mcp main|cex-public|cex-exchange|dex|info|news] ... [--no-skills]
#   cex-public / cex-exchange = Remote CEX at api.gatemcp.ai (see gate-mcp README)
# Installs all MCPs when no --mcp is passed. DEX uses fixed x-api-key: MCP_AK_8W2N7Q

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAG_DIR="$SCRIPT_DIR/mcp-fragments/codex"

GATE_SKILLS_REPO="https://github.com/gate/gate-skills.git"
GATE_SKILLS_BRANCH="${GATE_SKILLS_BRANCH:-master}"

# Codex user-level config and skills directory
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
CONFIG_TOML="${CODEX_HOME}/config.toml"
SKILLS_DIR="${CODEX_HOME}/skills"

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

# DEX x-api-key is defined in mcp-fragments/codex/gate-dex.toml (MCP_AK_8W2N7Q)

# ---------- 1. Merge and write mcp_servers to config.toml ----------
mkdir -p "$CODEX_HOME"
touch "$CONFIG_TOML"
# Ensure file ends with newline for appending
[[ $(tail -c1 "$CONFIG_TOML" 2>/dev/null | wc -l) -eq 0 ]] && echo "" >> "$CONFIG_TOML"

# Add [mcp_servers] header if not present (Codex accepts empty table followed by sub-tables)
if ! grep -q '^\[mcp_servers\]' "$CONFIG_TOML" 2>/dev/null; then
  echo "" >> "$CONFIG_TOML"
  echo "################################################################################" >> "$CONFIG_TOML"
  echo "# Gate MCP servers (added by gate-mcp-codex-installer)" >> "$CONFIG_TOML"
  echo "################################################################################" >> "$CONFIG_TOML"
  echo "[mcp_servers]" >> "$CONFIG_TOML"
fi

append_mcp_gate() {
  if grep -q '^\[mcp_servers\.Gate\]' "$CONFIG_TOML" 2>/dev/null; then
    echo "  [mcp_servers.Gate] already exists, skipping"
    return
  fi
  # Prefer global gate-mcp (avoids npx ESM path resolution failures with @modelcontextprotocol/sdk)
  if command -v gate-mcp &>/dev/null; then
    GATE_MAIN_USE_NPX=0
    if [[ -n "$USER_GATE_API_KEY" ]]; then
      cat >> "$CONFIG_TOML" << TOML

[mcp_servers.Gate]
command = "gate-mcp"
args = []
env = { GATE_API_KEY = "$USER_GATE_API_KEY", GATE_API_SECRET = "$USER_GATE_API_SECRET" }
TOML
    else
      cat "$FRAG_DIR/gate-main-gate-mcp-placeholder.toml" >> "$CONFIG_TOML"
    fi
  else
    GATE_MAIN_USE_NPX=1
    if [[ -n "$USER_GATE_API_KEY" ]]; then
      cat >> "$CONFIG_TOML" << TOML

[mcp_servers.Gate]
command = "npx"
args = ["-y", "gate-mcp"]
env = { GATE_API_KEY = "$USER_GATE_API_KEY", GATE_API_SECRET = "$USER_GATE_API_SECRET" }
TOML
    else
      cat "$FRAG_DIR/gate-main-npx-placeholder.toml" >> "$CONFIG_TOML"
    fi
  fi
  echo "  Added MCP: Gate (main)"
}

append_mcp_gate_remote_public() {
  if grep -q '^\[mcp_servers\.gate-cex-pub\]' "$CONFIG_TOML" 2>/dev/null; then
    echo "  [mcp_servers.gate-cex-pub] already exists, skipping"
    return
  fi
  cat "$FRAG_DIR/gate-cex-pub.toml" >> "$CONFIG_TOML"
  echo "  Added MCP: gate-cex-pub (Remote CEX public, no auth)"
}

append_mcp_gate_remote_exchange() {
  if grep -q '^\[mcp_servers\.gate-cex-ex\]' "$CONFIG_TOML" 2>/dev/null; then
    echo "  [mcp_servers.gate-cex-ex] already exists, skipping"
    return
  fi
  cat "$FRAG_DIR/gate-cex-ex.toml" >> "$CONFIG_TOML"
  echo "  Added MCP: gate-cex-ex (Remote CEX private, Gate OAuth2)"
}

append_mcp_gate_dex() {
  if grep -q '^\[mcp_servers\.gate-dex\]' "$CONFIG_TOML" 2>/dev/null; then
    echo "  [mcp_servers.gate-dex] already exists, skipping"
    return
  fi
  cat "$FRAG_DIR/gate-dex.toml" >> "$CONFIG_TOML"
  echo "  Added MCP: gate-dex"
}

append_mcp_gate_info() {
  if grep -q '^\[mcp_servers\.gate-info\]' "$CONFIG_TOML" 2>/dev/null; then
    echo "  [mcp_servers.gate-info] already exists, skipping"
    return
  fi
  cat "$FRAG_DIR/gate-info.toml" >> "$CONFIG_TOML"
  echo "  Added MCP: gate-info"
}

append_mcp_gate_news() {
  if grep -q '^\[mcp_servers\.gate-news\]' "$CONFIG_TOML" 2>/dev/null; then
    echo "  [mcp_servers.gate-news] already exists, skipping"
    return
  fi
  cat "$FRAG_DIR/gate-news.toml" >> "$CONFIG_TOML"
  echo "  Added MCP: gate-news"
}

echo "Writing MCP config to: $CONFIG_TOML"
GATE_MAIN_USE_NPX=0
[[ $MCP_MAIN -eq 1 ]] && append_mcp_gate
[[ $MCP_CEX_PUBLIC -eq 1 ]] && append_mcp_gate_remote_public
[[ $MCP_CEX_EXCHANGE -eq 1 ]] && append_mcp_gate_remote_exchange
[[ $MCP_DEX -eq 1 ]]  && append_mcp_gate_dex
[[ $MCP_INFO -eq 1 ]] && append_mcp_gate_info
[[ $MCP_NEWS -eq 1 ]] && append_mcp_gate_news
if [[ $MCP_MAIN -eq 1 && "$GATE_MAIN_USE_NPX" -eq 1 ]]; then
  echo ""
  echo "Note: Gate (main) is currently launched via npx. If you encounter ERR_MODULE_NOT_FOUND (@modelcontextprotocol/sdk) on startup, run:"
  echo "  npm install -g gate-mcp"
  echo "Then re-run this script, or manually change [mcp_servers.Gate] command to gate-mcp with args [] in config.toml."
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
  echo "  After creation, add GATE_API_KEY and GATE_API_SECRET to the [mcp_servers.Gate] env field in $CONFIG_TOML:"
  echo "    env = { GATE_API_KEY = \"your-key\", GATE_API_SECRET = \"your-secret\" }"
fi

if [[ $MCP_CEX_EXCHANGE -eq 1 ]]; then
  echo ""
  echo "gate-cex-ex (OAuth2): Complete Gate login when Codex prompts on first use."
  echo "  See https://github.com/gate/gate-mcp"
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

echo "Done. Please restart Codex to load the MCP servers and skills."
