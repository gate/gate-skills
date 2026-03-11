#!/usr/bin/env bash
# Gate Codex 一键安装：MCP（main/dex/info/news 可选）+ gate-skills 全部
# 用法: install.sh [--mcp main] [--mcp dex] ... [--no-skills]  不传 --mcp 则安装全部 MCP
# DEX MCP 使用固定 x-api-key: MCP_AK_8W2N7Q

set -e

GATE_SKILLS_REPO="https://github.com/gate/gate-skills.git"
GATE_SKILLS_BRANCH="${GATE_SKILLS_BRANCH:-master}"

# Codex 用户级配置与 skills 目录
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
CONFIG_TOML="${CODEX_HOME}/config.toml"
SKILLS_DIR="${CODEX_HOME}/skills"

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

# ---------- 1. 合并写入 config.toml 的 mcp_servers ----------
mkdir -p "$CODEX_HOME"
touch "$CONFIG_TOML"
# 确保文件以换行结尾，便于追加
[[ $(tail -c1 "$CONFIG_TOML" 2>/dev/null | wc -l) -eq 0 ]] && echo "" >> "$CONFIG_TOML"

# 若尚无 [mcp_servers] 表头，先追加空表（Codex 接受空表后再挂子表）
if ! grep -q '^\[mcp_servers\]' "$CONFIG_TOML" 2>/dev/null; then
  echo "" >> "$CONFIG_TOML"
  echo "################################################################################" >> "$CONFIG_TOML"
  echo "# Gate MCP servers (added by gate-mcp-codexinstaller)" >> "$CONFIG_TOML"
  echo "################################################################################" >> "$CONFIG_TOML"
  echo "[mcp_servers]" >> "$CONFIG_TOML"
fi

append_mcp_gate() {
  if grep -q '^\[mcp_servers\.Gate\]' "$CONFIG_TOML" 2>/dev/null; then
    echo "  [mcp_servers.Gate] 已存在，跳过"
    return
  fi
  cat >> "$CONFIG_TOML" << 'TOML'

[mcp_servers.Gate]
command = "npx"
args = ["-y", "gate-mcp"]
TOML
  echo "  已添加 MCP: Gate (main)"
}

append_mcp_gate_dex() {
  if grep -q '^\[mcp_servers\.gate-dex\]' "$CONFIG_TOML" 2>/dev/null; then
    echo "  [mcp_servers.gate-dex] 已存在，跳过"
    return
  fi
  cat >> "$CONFIG_TOML" << TOML

[mcp_servers.gate-dex]
url = "https://api.gatemcp.ai/mcp/dex"
http_headers = { "x-api-key" = "$GATE_API_KEY" }
TOML
  echo "  已添加 MCP: gate-dex"
}

append_mcp_gate_info() {
  if grep -q '^\[mcp_servers\.gate-info\]' "$CONFIG_TOML" 2>/dev/null; then
    echo "  [mcp_servers.gate-info] 已存在，跳过"
    return
  fi
  cat >> "$CONFIG_TOML" << 'TOML'

[mcp_servers.gate-info]
url = "https://api.gatemcp.ai/mcp/info"
TOML
  echo "  已添加 MCP: gate-info"
}

append_mcp_gate_news() {
  if grep -q '^\[mcp_servers\.gate-news\]' "$CONFIG_TOML" 2>/dev/null; then
    echo "  [mcp_servers.gate-news] 已存在，跳过"
    return
  fi
  cat >> "$CONFIG_TOML" << 'TOML'

[mcp_servers.gate-news]
url = "https://api.gatemcp.ai/mcp/news"
TOML
  echo "  已添加 MCP: gate-news"
}

echo "正在写入 MCP 配置: $CONFIG_TOML"
[[ $MCP_MAIN -eq 1 ]] && append_mcp_gate
[[ $MCP_DEX -eq 1 ]]  && append_mcp_gate_dex
[[ $MCP_INFO -eq 1 ]] && append_mcp_gate_info
[[ $MCP_NEWS -eq 1 ]] && append_mcp_gate_news

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

echo "完成。请重启 Codex 以加载 MCP 与 Skills。"
