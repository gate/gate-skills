#!/usr/bin/env bash
# Gate CEX 一键安装：MCP（main/dex/info/news 可选）+ gate-skills 全部
# 用法: install.sh [--mcp main] [--mcp dex] ... [--no-skills]  不传 --mcp 则安装全部 MCP
# DEX MCP 使用固定 x-api-key: MCP_AK_8W2N7Q

set -e

GATE_SKILLS_REPO="https://github.com/gate/gate-skills.git"
GATE_SKILLS_BRANCH="${GATE_SKILLS_BRANCH:-master}"
# Cursor 用户级配置与 skills 目录（macOS/Linux）
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

# 默认安装全部 MCP，默认安装 skills
MCP_MAIN=0
MCP_DEX=0
MCP_INFO=0
MCP_NEWS=0
INSTALL_SKILLS=1

usage() {
  echo "用法: $0 [--mcp main|dex|info|news] ... [--no-skills]"
  echo "  不传 --mcp 时安装全部 MCP；传多个 --mcp 则只安装指定项。"
  echo "  --no-skills  仅安装 MCP，不克隆安装 gate-skills。"
  echo "示例: $0"
  echo "示例: $0 --mcp main --mcp dex"
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
        *)      echo "未知 MCP: $1 (可选: main, dex, info, news)" >&2; exit 1 ;;
      esac
      shift
      ;;
    --no-skills) INSTALL_SKILLS=0; shift ;;
    -h|--help) usage ;;
    *) echo "未知参数: $1" >&2; usage ;;
  esac
done

# 若未指定任何 --mcp，则全选
if [[ $MCP_MAIN -eq 0 && $MCP_DEX -eq 0 && $MCP_INFO -eq 0 && $MCP_NEWS -eq 0 ]]; then
  MCP_MAIN=1
  MCP_DEX=1
  MCP_INFO=1
  MCP_NEWS=1
fi

# Gate (main) 依赖 node + npx，安装前检查并在缺 npx 时尝试安装
if [[ $MCP_MAIN -eq 1 ]]; then
  if ! command -v node &>/dev/null; then
    echo "错误: 未检测到 Node.js。Gate (main) MCP 需要 Node.js（含 npx）。" >&2
    echo "请先安装: https://nodejs.org 或使用 nvm/fnm 安装 Node.js 后重试。" >&2
    exit 1
  fi
  if ! command -v npx &>/dev/null; then
    echo "未检测到 npx，正在尝试安装: npm install -g npx ..."
    if npm install -g npx 2>/dev/null; then
      echo "npx 已安装。"
    else
      echo "错误: 未检测到 npx，且自动安装失败。" >&2
      echo "请手动运行: npm install -g npx" >&2
      exit 1
    fi
  fi
fi

# Gate (main) 现货/合约需要用户的 API Key
USER_GATE_API_KEY=""
USER_GATE_API_SECRET=""
if [[ $MCP_MAIN -eq 1 ]]; then
  echo ""
  echo "Gate (main) 现货/合约交易需要 API Key 才能操作账户。"
  echo "请访问以下链接创建 API Key（需开启现货/合约交易权限）："
  echo "  https://www.gate.com/myaccount/profile/api-key/manage"
  echo ""
  read -p "  GATE_API_KEY (留空则跳过): " USER_GATE_API_KEY
  if [[ -n "$USER_GATE_API_KEY" ]]; then
    read -s -p "  GATE_API_SECRET: " USER_GATE_API_SECRET
    echo ""
    if [[ -z "$USER_GATE_API_SECRET" ]]; then
      echo "警告: GATE_API_SECRET 为空，现货/合约交易将无法使用。" >&2
      USER_GATE_API_KEY=""
    fi
  fi
fi

# DEX MCP 固定 x-api-key
GATE_API_KEY="MCP_AK_8W2N7Q"

# ---------- 1. 合并写入 mcp.json ----------
mkdir -p "$(dirname "$MCP_JSON")"

# 构建要添加的 mcpServers 片段（兼容 Bash 3）
# main: 优先使用全局 gate-mcp（避免 npx 下 @modelcontextprotocol/sdk 的 ESM 路径解析失败）
# dex: url + x-api-key header
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
    ADD_JSON="${ADD_JSON}\"Gate\":{\"command\":\"${GATE_MAIN_CMD}\",\"args\":${GATE_MAIN_ARGS}}"
  fi
  first=0
fi
if [[ $MCP_DEX -eq 1 ]]; then
  [[ $first -eq 0 ]] && ADD_JSON="${ADD_JSON},"
  ADD_JSON="${ADD_JSON}\"Gate-Dex\":{\"url\":\"https://api.gatemcp.ai/mcp/dex\",\"transport\":\"streamable-http\",\"headers\":{\"x-api-key\":\"${GATE_API_KEY}\"}}"
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
  echo "已写入 MCP 配置: $MCP_JSON"
  if [[ $MCP_MAIN -eq 1 && "$GATE_MAIN_CMD" == "npx" ]]; then
    echo ""
    echo "提示: Gate (main) 当前使用 npx 启动。若启动时报错 ERR_MODULE_NOT_FOUND（找不到 @modelcontextprotocol/sdk），请执行："
    echo "  npm install -g gate-mcp"
    echo "然后重新运行本脚本，或手动将 mcp.json 中 Gate 的 command 改为 gate-mcp、args 改为 []。"
  fi
else
  echo "未检测到 node，请手动将以下内容合并到 $MCP_JSON 的 mcpServers 中："
  echo "  $ADD_JSON"
fi

# ---------- 2. 安装 gate-skills 全部（可选） ----------
if [[ $INSTALL_SKILLS -eq 0 ]]; then
  echo "已跳过 gate-skills 安装（--no-skills）。"
else
  echo "正在安装 gate-skills（全部）..."
  TMP_CLONE=$(mktemp -d 2>/dev/null || mktemp -d -t gate-skills)
  trap "rm -rf '$TMP_CLONE'" EXIT

  if command -v git &>/dev/null; then
    git clone --depth 1 -b "$GATE_SKILLS_BRANCH" "$GATE_SKILLS_REPO" "$TMP_CLONE"
  else
    echo "需要 git 才能克隆 gate-skills。请安装 git 或使用 --no-skills 仅安装 MCP。" >&2
    exit 1
  fi

  mkdir -p "$SKILLS_DIR"
  SKILLS_SRC="$TMP_CLONE/skills"
  if [[ ! -d "$SKILLS_SRC" ]]; then
    echo "gate-skills 仓库中未找到 skills 目录" >&2
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
    echo "  已安装 skill: $name"
  done

  echo "Skills 已安装到: $SKILLS_DIR"
fi

if [[ $MCP_MAIN -eq 1 && -z "$USER_GATE_API_KEY" ]]; then
  echo ""
  echo "Gate (main) API Key 配置提示:"
  echo "  现货/合约交易功能需要 API Key。请访问以下链接创建："
  echo "    https://www.gate.com/myaccount/profile/api-key/manage"
  echo "  创建后，请将 GATE_API_KEY 和 GATE_API_SECRET 添加到 $MCP_JSON 中 Gate 的 env 字段："
  echo "    \"Gate\": { ..., \"env\": { \"GATE_API_KEY\": \"你的Key\", \"GATE_API_SECRET\": \"你的Secret\" } }"
fi

if [[ $MCP_DEX -eq 1 ]]; then
  echo ""
  echo "Gate-Dex 授权提示: 当 gate-dex 查询返回需要授权时，请先打开下方链接创建或绑定钱包，"
  echo "  然后助手会返回可点击的 Google 授权链接，点击即可跳转完成授权。"
  echo "  https://web3.gate.com/"
  echo ""
fi

echo "完成。请重启 Cursor 以加载 MCP。"
