#!/usr/bin/env bash
# Gate MCP unified installer: Cursor / Claude Code / Codex / OpenClaw (mcporter)
# Usage:
#   install.sh [--platform cursor|claude|codex|openclaw]
#              [--mcp main|cex-public|cex-exchange|dex|info|news] ...
#              [--no-skills] [--select|-s]
#   --platform  Force target; required if multiple dev environments are detected.
#   --mcp       Repeatable; omit to install all six MCP surfaces.
#   --no-skills MCP only (no gate-skills clone).
#   --select    OpenClaw: interactive pick one server (legacy mcporter UX).
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MERGE_JS="$SCRIPT_DIR/merge-mcp-config.js"
GATE_SKILLS_REPO="https://github.com/gate/gate-skills.git"
GATE_SKILLS_BRANCH="${GATE_SKILLS_BRANCH:-master}"
OPENCLAW_MANIFEST="$SCRIPT_DIR/mcp-fragments/openclaw/servers.manifest"

PLATFORM=""
MCP_MAIN=0
MCP_CEX_PUBLIC=0
MCP_CEX_EXCHANGE=0
MCP_DEX=0
MCP_INFO=0
MCP_NEWS=0
INSTALL_SKILLS=1
SELECT_MODE=0

usage() {
  echo "Usage: $0 [--platform cursor|claude|codex|openclaw]"
  echo "          [--mcp main|cex-public|cex-exchange|dex|info|news] ..."
  echo "          [--no-skills] [--select|-s]"
  echo ""
  echo "  Auto-detects platform when exactly one of: ~/.cursor, Claude config, ~/.codex,"
  echo "  or mcporter (OpenClaw) is present. Use --platform when multiple match."
  echo "  OpenClaw: --select opens interactive menu; --mcp filters non-interactive installs."
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform)
      shift
      case "$1" in
        cursor|claude|codex|openclaw) PLATFORM="$1" ;;
        *) echo "Unknown --platform: $1" >&2; exit 1 ;;
      esac
      shift
      ;;
    --mcp)
      shift
      case "$1" in
        main)         MCP_MAIN=1 ;;
        cex-public)   MCP_CEX_PUBLIC=1 ;;
        cex-exchange) MCP_CEX_EXCHANGE=1 ;;
        dex)          MCP_DEX=1 ;;
        info)         MCP_INFO=1 ;;
        news)         MCP_NEWS=1 ;;
        *) echo "Unknown MCP: $1 (main, cex-public, cex-exchange, dex, info, news)" >&2; exit 1 ;;
      esac
      shift
      ;;
    --no-skills) INSTALL_SKILLS=0; shift ;;
    --select|-s) SELECT_MODE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ $MCP_MAIN -eq 0 && $MCP_CEX_PUBLIC -eq 0 && $MCP_CEX_EXCHANGE -eq 0 && $MCP_DEX -eq 0 && $MCP_INFO -eq 0 && $MCP_NEWS -eq 0 ]]; then
  MCP_MAIN=1
  MCP_CEX_PUBLIC=1
  MCP_CEX_EXCHANGE=1
  MCP_DEX=1
  MCP_INFO=1
  MCP_NEWS=1
fi

detect_cursor() {
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    local base="${APPDATA:-$HOME/AppData/Roaming}"
    [[ -d "$base/Cursor" ]]
  else
    [[ -d "${HOME}/.cursor" ]]
  fi
}

detect_claude() {
  [[ -f "${HOME}/.claude.json" ]] || [[ -d "${HOME}/.claude" ]]
}

detect_codex() {
  local h="${CODEX_HOME:-$HOME/.codex}"
  [[ -d "$h" ]]
}

detect_openclaw() {
  command -v mcporter &>/dev/null
}

resolve_platform() {
  [[ -n "$PLATFORM" ]] && return 0
  PLATFORM_CANDIDATES=()
  local c=0
  detect_cursor && { PLATFORM_CANDIDATES+=("cursor"); c=$((c + 1)); }
  detect_claude && { PLATFORM_CANDIDATES+=("claude"); c=$((c + 1)); }
  detect_codex && { PLATFORM_CANDIDATES+=("codex"); c=$((c + 1)); }
  detect_openclaw && { PLATFORM_CANDIDATES+=("openclaw"); c=$((c + 1)); }

  if [[ $c -eq 0 ]]; then
    echo "Could not detect environment. Install Cursor, Claude Code, Codex, or mcporter," >&2
    echo "or pass --platform cursor|claude|codex|openclaw" >&2
    exit 1
  fi
  if [[ $c -gt 1 ]]; then
    echo "Multiple environments detected: ${PLATFORM_CANDIDATES[*]}" >&2
    echo "Re-run with: --platform cursor|claude|codex|openclaw" >&2
    exit 1
  fi
  PLATFORM="${PLATFORM_CANDIDATES[0]}"
}

install_gate_skills_to() {
  local SKILLS_DIR="$1"
  if [[ $INSTALL_SKILLS -eq 0 ]]; then
    echo "Skipped gate-skills installation (--no-skills)."
    return 0
  fi
  echo "Installing gate-skills (all)..."
  if ! command -v git &>/dev/null; then
    echo "git is required to clone gate-skills. Use --no-skills for MCP only." >&2
    exit 1
  fi
  local TMP_CLONE
  TMP_CLONE=$(mktemp -d 2>/dev/null || mktemp -d -t gate-skills)
  # shellcheck disable=SC2064
  trap "rm -rf \"$TMP_CLONE\"" EXIT
  git clone --depth 1 -b "$GATE_SKILLS_BRANCH" "$GATE_SKILLS_REPO" "$TMP_CLONE"
  mkdir -p "$SKILLS_DIR"
  local SKILLS_SRC="$TMP_CLONE/skills"
  if [[ ! -d "$SKILLS_SRC" ]]; then
    echo "skills/ not found in gate-skills repo" >&2
    exit 1
  fi
  for dir in "$SKILLS_SRC"/*; do
    [[ -d "$dir" ]] || continue
    local name
    name=$(basename "$dir")
    local dst="$SKILLS_DIR/$name"
    [[ -d "$dst" ]] && rm -rf "$dst"
    cp -R "$dir" "$dst"
    echo "  Installed skill: $name"
  done
  trap - EXIT
  rm -rf "$TMP_CLONE"
  echo "Skills installed to: $SKILLS_DIR"
}

ensure_node_for_main() {
  if [[ $MCP_MAIN -ne 1 ]]; then return 0; fi
  if ! command -v node &>/dev/null; then
    echo "Error: Node.js required for Gate (main). https://nodejs.org" >&2
    exit 1
  fi
  if ! command -v npx &>/dev/null; then
    echo "npx not found; trying: npm install -g npx ..."
    if ! npm install -g npx 2>/dev/null; then
      echo "Error: install npx manually: npm install -g npx" >&2
      exit 1
    fi
  fi
}

prompt_gate_api_keys() {
  USER_GATE_API_KEY=""
  USER_GATE_API_SECRET=""
  if [[ $MCP_MAIN -ne 1 ]]; then return 0; fi
  echo ""
  echo "Gate (main) trading uses API Key + Secret:"
  echo "  https://www.gate.com/myaccount/profile/api-key/manage"
  echo ""
  read -r -p "  GATE_API_KEY (empty to skip): " USER_GATE_API_KEY
  if [[ -n "$USER_GATE_API_KEY" ]]; then
    read -r -s -p "  GATE_API_SECRET: " USER_GATE_API_SECRET
    echo ""
    if [[ -z "$USER_GATE_API_SECRET" ]]; then
      echo "Warning: empty secret; clearing key." >&2
      USER_GATE_API_KEY=""
    fi
  fi
}

install_json_merge_platform() {
  local kind="$1"
  local CONFIG_JSON SKILLS_DIR FRAG_DIR

  if [[ "$kind" == "cursor" ]]; then
    local CURSOR_HOME="${CURSOR_USER_HOME:-$HOME}"
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
      CONFIG_JSON="${APPDATA:-$CURSOR_HOME/AppData/Roaming}/Cursor/mcp.json"
      SKILLS_DIR="${APPDATA:-$CURSOR_HOME/AppData/Roaming}/Cursor/skills"
    else
      CONFIG_JSON="${CURSOR_HOME}/.cursor/mcp.json"
      SKILLS_DIR="${CURSOR_HOME}/.cursor/skills"
    fi
    FRAG_DIR="$SCRIPT_DIR/mcp-fragments/cursor"
  else
    local CLAUDE_HOME="${CLAUDE_USER_HOME:-$HOME}"
    CONFIG_JSON="${CLAUDE_HOME}/.claude.json"
    SKILLS_DIR="${CLAUDE_HOME}/.claude/skills"
    mkdir -p "$(dirname "$SKILLS_DIR")"
    FRAG_DIR="$SCRIPT_DIR/mcp-fragments/claude"
  fi

  ensure_node_for_main
  prompt_gate_api_keys

  mkdir -p "$(dirname "$CONFIG_JSON")"

  local GATE_MAIN_CMD="" FRAGS=()
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

  if command -v node &>/dev/null; then
    local EXISTING="{}"
    [[ -f "$CONFIG_JSON" ]] && EXISTING=$(cat "$CONFIG_JSON")
    local TMP_JSON
    TMP_JSON=$(mktemp)
    echo "$EXISTING" > "$TMP_JSON"
    unset GATE_USER_API_KEY GATE_USER_API_SECRET 2>/dev/null || true
    if [[ -n "$USER_GATE_API_KEY" ]]; then
      export GATE_USER_API_KEY="$USER_GATE_API_KEY"
      export GATE_USER_API_SECRET="$USER_GATE_API_SECRET"
    fi
    node "$MERGE_JS" "$TMP_JSON" "$CONFIG_JSON" "${FRAGS[@]}"
    unset GATE_USER_API_KEY GATE_USER_API_SECRET 2>/dev/null || true
    rm -f "$TMP_JSON"
    echo "MCP config written to: $CONFIG_JSON"
    if [[ $MCP_MAIN -eq 1 && "$GATE_MAIN_CMD" == "npx" ]]; then
      echo ""
      echo "If ERR_MODULE_NOT_FOUND (@modelcontextprotocol/sdk) appears, run: npm install -g gate-mcp"
      echo "then re-run this script (global gate-mcp is preferred over npx)."
    fi
  else
    echo "Node.js not found; merge manually into mcpServers in $CONFIG_JSON:"
    for f in "${FRAGS[@]}"; do echo ""; echo "# $f"; sed 's/^/  /' "$f"; done
  fi

  install_gate_skills_to "$SKILLS_DIR"

  if [[ $MCP_MAIN -eq 1 && -z "$USER_GATE_API_KEY" ]]; then
    echo ""
    echo "Add GATE_API_KEY / GATE_API_SECRET in Gate entry env in $CONFIG_JSON when ready."
  fi
  if [[ $MCP_CEX_EXCHANGE -eq 1 ]]; then
    echo ""
    echo "gate-cex-ex: complete Gate OAuth2 when the client prompts (first connect)."
    echo "  Docs: https://github.com/gate/gate-mcp"
  fi
  if [[ $MCP_DEX -eq 1 ]]; then
    echo ""
    echo "Gate-Dex: wallet at https://web3.gate.com/ then OAuth via assistant link if required."
  fi

  if [[ "$kind" == "cursor" ]]; then
    echo "Done. Restart Cursor to load MCP servers."
  else
    echo "Done. Reopen Claude Code or start a new session to load MCP servers."
  fi
}

install_codex_platform() {
  local FRAG_DIR="$SCRIPT_DIR/mcp-fragments/codex"
  local CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
  local CONFIG_TOML="${CODEX_HOME}/config.toml"
  local SKILLS_DIR="${CODEX_HOME}/skills"

  ensure_node_for_main
  prompt_gate_api_keys

  mkdir -p "$CODEX_HOME"
  touch "$CONFIG_TOML"
  [[ $(tail -c1 "$CONFIG_TOML" 2>/dev/null | wc -l) -eq 0 ]] && echo "" >> "$CONFIG_TOML"

  if ! grep -q '^\[mcp_servers\]' "$CONFIG_TOML" 2>/dev/null; then
    echo "" >> "$CONFIG_TOML"
    echo "################################################################################" >> "$CONFIG_TOML"
    echo "# Gate MCP servers (added by gate-mcp-installer)" >> "$CONFIG_TOML"
    echo "################################################################################" >> "$CONFIG_TOML"
    echo "[mcp_servers]" >> "$CONFIG_TOML"
  fi

  local GATE_MAIN_USE_NPX=0

  append_gate() {
    if grep -q '^\[mcp_servers\.Gate\]' "$CONFIG_TOML" 2>/dev/null; then
      echo "  [mcp_servers.Gate] exists, skip"
      return
    fi
    if command -v gate-mcp &>/dev/null; then
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

  append_named() {
    local key="$1" file="$2" label="$3"
    if grep -q "^\[mcp_servers\.${key}\]" "$CONFIG_TOML" 2>/dev/null; then
      echo "  [mcp_servers.${key}] exists, skip"
      return
    fi
    cat "$file" >> "$CONFIG_TOML"
    echo "  Added MCP: $label"
  }

  echo "Writing MCP config to: $CONFIG_TOML"
  [[ $MCP_MAIN -eq 1 ]] && append_gate
  [[ $MCP_CEX_PUBLIC -eq 1 ]]   && append_named "gate-cex-pub" "$FRAG_DIR/gate-cex-pub.toml" "gate-cex-pub"
  [[ $MCP_CEX_EXCHANGE -eq 1 ]] && append_named "gate-cex-ex" "$FRAG_DIR/gate-cex-ex.toml" "gate-cex-ex"
  [[ $MCP_DEX -eq 1 ]]          && append_named "gate-dex" "$FRAG_DIR/gate-dex.toml" "gate-dex"
  [[ $MCP_INFO -eq 1 ]]         && append_named "gate-info" "$FRAG_DIR/gate-info.toml" "gate-info"
  [[ $MCP_NEWS -eq 1 ]]         && append_named "gate-news" "$FRAG_DIR/gate-news.toml" "gate-news"

  if [[ $MCP_MAIN -eq 1 && $GATE_MAIN_USE_NPX -eq 1 ]]; then
    echo ""
    echo "If npx fails with ERR_MODULE_NOT_FOUND, run: npm install -g gate-mcp"
  fi

  install_gate_skills_to "$SKILLS_DIR"

  if [[ $MCP_MAIN -eq 1 && -z "$USER_GATE_API_KEY" ]]; then
    echo ""
    echo "Set env in [mcp_servers.Gate] in $CONFIG_TOML when you have API keys."
  fi
  if [[ $MCP_CEX_EXCHANGE -eq 1 ]]; then
    echo ""
    echo "gate-cex-ex (OAuth2): complete login when Codex prompts. https://github.com/gate/gate-mcp"
  fi
  if [[ $MCP_DEX -eq 1 ]]; then
    echo ""
    echo "Gate-Dex: https://web3.gate.com/ for wallet; OAuth via assistant if needed."
  fi
  echo "Done. Restart Codex to load MCP servers."
}

# --- OpenClaw / mcporter ---
GATE_DEX_API_KEY="MCP_AK_8W2N7Q"

load_openclaw_servers() {
  OPENCLAW_SERVERS=()
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" || "$line" == \#* ]] && continue
    OPENCLAW_SERVERS+=("$line")
  done < "$OPENCLAW_MANIFEST"
}

openclaw_wants_name() {
  local n="$1"
  case "$n" in
    gate)          [[ $MCP_MAIN -eq 1 ]] ;;
    gate-cex-pub)  [[ $MCP_CEX_PUBLIC -eq 1 ]] ;;
    gate-cex-ex)   [[ $MCP_CEX_EXCHANGE -eq 1 ]] ;;
    gate-dex)      [[ $MCP_DEX -eq 1 ]] ;;
    gate-info)     [[ $MCP_INFO -eq 1 ]] ;;
    gate-news)     [[ $MCP_NEWS -eq 1 ]] ;;
    *)             false ;;
  esac
}

openclaw_check_existing() {
  mcporter config list 2>/dev/null | grep -q "^${1}$"
}

openclaw_install_stdio() {
  local name="$1" cmd="$2" api_key="$3" api_secret="$4"
  if [[ -n "$api_key" && -n "$api_secret" ]]; then
    mcporter config add "$name" --stdio --command "$cmd" \
      --env "GATE_API_KEY=$api_key" \
      --env "GATE_API_SECRET=$api_secret" 2>/dev/null || return 1
  else
    mcporter config add "$name" --stdio --command "$cmd" \
      --env "GATE_API_KEY=your-api-key" \
      --env "GATE_API_SECRET=your-api-secret" 2>/dev/null || return 1
  fi
}

openclaw_install_http() {
  local name="$1" url="$2" api_key="$3"
  if [[ -n "$api_key" ]]; then
    mcporter config add "$name" --url "$url" \
      --header "x-api-key:$api_key" \
      --header "Authorization:Bearer \${GATE_MCP_TOKEN}" 2>/dev/null || return 1
  else
    mcporter config add "$name" --url "$url" 2>/dev/null || return 1
  fi
}

openclaw_install_oauth_http() {
  mcporter config add "$1" --url "$2" --auth oauth 2>/dev/null || return 1
}

openclaw_install_server_line() {
  local config="$1" gate_key="$2" gate_secret="$3" dex_key="$4"
  local name type endpoint auth_type desc
  IFS='|' read -r name type endpoint auth_type desc <<< "$config"
  printf "  %-15s " "$name"
  if openclaw_check_existing "$name"; then
    echo "(exists)"
    return 0
  fi
  case "$auth_type" in
    api_key_secret)
      openclaw_install_stdio "$name" "$endpoint" "$gate_key" "$gate_secret" || { echo "failed"; return 1; }
      ;;
    oauth)
      openclaw_install_oauth_http "$name" "$endpoint" || { echo "failed"; return 1; }
      ;;
    x_api_key)
      openclaw_install_http "$name" "$endpoint" "$dex_key" || { echo "failed"; return 1; }
      ;;
    none)
      if [[ "$type" == "stdio" ]]; then
        openclaw_install_stdio "$name" "$endpoint" "" "" || { echo "failed"; return 1; }
      else
        openclaw_install_http "$name" "$endpoint" "" || { echo "failed"; return 1; }
      fi
      ;;
  esac
  echo "installed"
}

install_openclaw_platform() {
  if ! command -v mcporter &>/dev/null; then
    echo "mcporter not found. npm install -g mcporter" >&2
    echo "https://github.com/mcporter-dev/mcporter" >&2
    exit 1
  fi

  load_openclaw_servers

  local OPENCLAW_SKILLS="${OPENCLAW_HOME:-$HOME/.openclaw}/skills"
  mkdir -p "${OPENCLAW_HOME:-$HOME/.openclaw}"

  if [[ $SELECT_MODE -eq 1 ]]; then
    echo "Gate MCP OpenClaw — interactive select"
    local i=1
    for server in "${OPENCLAW_SERVERS[@]}"; do
      local name type endpoint auth_type desc
      IFS='|' read -r name type endpoint auth_type desc <<< "$server"
      local st=""
      openclaw_check_existing "$name" && st=" [installed]"
      printf "  %d) %-15s - %s%s\n" "$i" "$name" "$desc" "$st"
      i=$((i + 1))
    done
    echo ""
    read -r -p "Enter choice [1-6]: " choice
    local selected=""
    case "$choice" in
      1) selected="${OPENCLAW_SERVERS[0]}" ;;
      2) selected="${OPENCLAW_SERVERS[1]}" ;;
      3) selected="${OPENCLAW_SERVERS[2]}" ;;
      4) selected="${OPENCLAW_SERVERS[3]}" ;;
      5) selected="${OPENCLAW_SERVERS[4]}" ;;
      6) selected="${OPENCLAW_SERVERS[5]}" ;;
      *) echo "Invalid choice" >&2; exit 1 ;;
    esac
    local name type endpoint auth_type desc gate_key="" gate_secret=""
    IFS='|' read -r name type endpoint auth_type desc <<< "$selected"
    case "$auth_type" in
      api_key_secret)
        echo "API Key: https://www.gate.com/myaccount/profile/api-key/manage"
        read -r -p "  API Key: " gate_key
        read -r -s -p "  API Secret: " gate_secret
        echo ""
        ;;
      oauth)
        echo "After install: mcporter auth $name"
        ;;
    esac
    openclaw_install_server_line "$selected" "$gate_key" "$gate_secret" "$GATE_DEX_API_KEY"
    install_gate_skills_to "$OPENCLAW_SKILLS"
    echo "mcporter auth gate-cex-ex  # when using remote exchange"
    return 0
  fi

  local filtered=()
  for server in "${OPENCLAW_SERVERS[@]}"; do
    local name
    IFS='|' read -r name _ <<< "$server"
    if openclaw_wants_name "$name"; then
      filtered+=("$server")
    fi
  done

  if [[ ${#filtered[@]} -eq 0 ]]; then
    echo "No servers selected."
    exit 1
  fi

  USER_GATE_API_KEY=""
  USER_GATE_API_SECRET=""
  if [[ $MCP_MAIN -eq 1 ]]; then
    prompt_gate_api_keys
  fi
  local gk="$USER_GATE_API_KEY" gs="$USER_GATE_API_SECRET"

  echo "Installing via mcporter..."
  for server in "${filtered[@]}"; do
    openclaw_install_server_line "$server" "$gk" "$gs" "$GATE_DEX_API_KEY"
  done

  install_gate_skills_to "$OPENCLAW_SKILLS"

  echo ""
  echo "Verifying mcporter registrations..."
  for server in "${filtered[@]}"; do
    local n
    IFS='|' read -r n _ <<< "$server"
    if openclaw_check_existing "$n"; then
      if mcporter list "$n" --schema &>/dev/null; then
        echo "  ✓ $n"
      else
        echo "  ⚠ $n (check credentials / network)"
      fi
    fi
  done

  echo ""
  if openclaw_check_existing "gate-cex-ex"; then
    echo "Remote CEX OAuth: mcporter auth gate-cex-ex"
  fi
  if openclaw_check_existing "gate-dex"; then
    echo "Gate-Dex: https://web3.gate.com/ then OAuth if tools require it."
  fi
  echo "Quick: mcporter list gate-cex-pub | mcporter call gate-info.list_tickers currency_pair=BTC_USDT"
}

resolve_platform

case "$PLATFORM" in
  cursor)  install_json_merge_platform cursor ;;
  claude)  install_json_merge_platform claude ;;
  codex)   install_codex_platform ;;
  openclaw) install_openclaw_platform ;;
  *) echo "Internal error: platform=$PLATFORM" >&2; exit 1 ;;
esac
