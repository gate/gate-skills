#!/usr/bin/env bash
# Gate Claude Code 一键安装：MCP（main/dex/info/news 可选）+ gate-skills 全部
# 用法: install.sh [--mcp main] [--mcp dex] ... [--no-skills]  不传 --mcp 则安装全部 MCP
# DEX MCP 使用固定 x-api-key: MCP_AK_8W2N7Q

set -e

GATE_SKILLS_REPO="https://github.com/gate/gate-skills.git"
GATE_SKILLS_BRANCH="${GATE_SKILLS_BRANCH:-master}"

# Claude Code 用户级配置与 skills 目录（macOS/Linux）
if [[ -n "$CLAUDE_USER_HOME" ]]; then
  CLAUDE_HOME="$CLAUDE_USER_HOME"
else
  CLAUDE_HOME="${HOME}"
fi
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  CLAUDE_JSON="${CLAUDE_HOME}/.claude.json"
  SKILLS_DIR="${CLAUDE_HOME}/.claude/skills"
else
  CLAUDE_JSON="${CLAUDE_HOME}/.claude.json"
  SKILLS_DIR="${CLAUDE_HOME}/.claude/skills"
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

# DEX MCP 固定 x-api-key
GATE_API_KEY="MCP_AK_8W2N7Q"

# ---------- 1. 合并写入 ~/.claude.json 的 mcpServers ----------
mkdir -p "$(dirname "$SKILLS_DIR")"

# 构建要添加的 mcpServers 片段（Claude Code 格式：stdio 用 command/args，http 用 type/url/headers）
# main: stdio npx -y gate-mcp
# dex/info/news: type http + url [+ headers]
ADD_JSON="{"
first=1
if [[ $MCP_MAIN -eq 1 ]]; then
  [[ $first -eq 0 ]] && ADD_JSON="${ADD_JSON},"
  ADD_JSON="${ADD_JSON}\"Gate\":{\"command\":\"npx\",\"args\":[\"-y\",\"gate-mcp\"]}"
  first=0
fi
if [[ $MCP_DEX -eq 1 ]]; then
  [[ $first -eq 0 ]] && ADD_JSON="${ADD_JSON},"
  ADD_JSON="${ADD_JSON}\"Gate-Dex\":{\"type\":\"http\",\"url\":\"https://api.gatemcp.ai/mcp/dex\",\"headers\":{\"x-api-key\":\"${GATE_API_KEY}\"}}"
  first=0
fi
if [[ $MCP_INFO -eq 1 ]]; then
  [[ $first -eq 0 ]] && ADD_JSON="${ADD_JSON},"
  ADD_JSON="${ADD_JSON}\"Gate-Info\":{\"type\":\"http\",\"url\":\"https://api.gatemcp.ai/mcp/info\"}"
  first=0
fi
if [[ $MCP_NEWS -eq 1 ]]; then
  [[ $first -eq 0 ]] && ADD_JSON="${ADD_JSON},"
  ADD_JSON="${ADD_JSON}\"Gate-News\":{\"type\":\"http\",\"url\":\"https://api.gatemcp.ai/mcp/news\"}"
  first=0
fi
ADD_JSON="${ADD_JSON}}"

if command -v node &>/dev/null; then
  EXISTING="{}"
  if [[ -f "$CLAUDE_JSON" ]]; then
    EXISTING=$(cat "$CLAUDE_JSON")
  fi
  TMP_JSON=$(mktemp)
  echo "$EXISTING" > "$TMP_JSON"
  node -e "
    const fs = require('fs');
    const existingPath = process.argv[1];
    const addJson = process.argv[2];
    const outPath = process.argv[3];
    let existing = {};
    try {
      const raw = fs.readFileSync(existingPath, 'utf8');
      if (raw.trim()) existing = JSON.parse(raw);
    } catch (e) {
      existing = {};
    }
    const add = JSON.parse(addJson);
    existing.mcpServers = existing.mcpServers || {};
    Object.assign(existing.mcpServers, add);
    fs.writeFileSync(outPath, JSON.stringify(existing, null, 2));
  " "$TMP_JSON" "$ADD_JSON" "$CLAUDE_JSON"
  rm -f "$TMP_JSON"
  echo "已写入 MCP 配置: $CLAUDE_JSON"
else
  echo "未检测到 node，请手动将以下内容合并到 $CLAUDE_JSON 的 mcpServers 中："
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

echo "完成。请重新打开 Claude Code 或新开会话以加载 MCP 与 Skills。"
