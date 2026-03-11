# Gate Codex 一键安装（MCP + Skills）

一键为 **Codex** 安装 Gate 相关 MCP 与 [gate-skills](https://github.com/gate/gate-skills) 全部 skills。

## 安装方式

### 从本仓库一键安装

```bash
# 在 gate-skills 仓库根目录执行
bash skills/gate-mcp-codex-installer/scripts/install.sh
```

### 仅安装 MCP（不安装 gate-skills）

```bash
bash skills/gate-mcp-codex-installer/scripts/install.sh --no-skills
```

### 只安装部分 MCP

```bash
# 只安装 Gate (main) 和 Gate-Dex
bash skills/gate-mcp-codex-installer/scripts/install.sh --mcp main --mcp dex

# 只安装 Gate、Info、News
bash skills/gate-mcp-codex-installer/scripts/install.sh --mcp main --mcp info --mcp news
```

## 将安装的内容

| 项目 | 说明 |
|------|------|
| **Gate** | 主 MCP，`npx -y gate-mcp`，[gate-mcp](https://github.com/gate/gate-mcp) |
| **gate-dex** | https://api.gatemcp.ai/mcp/dex（x-api-key 已内置） |
| **gate-info** | https://api.gatemcp.ai/mcp/info |
| **gate-news** | https://api.gatemcp.ai/mcp/news |
| **gate-skills** | 从 [gate-skills](https://github.com/gate/gate-skills) 克隆并安装 `skills/` 下全部 skill |

## 配置写入位置

- **MCP 配置**：`~/.codex/config.toml`（或 `$CODEX_HOME/config.toml`）的 `[mcp_servers]` 下追加 Gate 相关表，不覆盖已有配置。
- **Skills**：`~/.codex/skills/`（或 `$CODEX_HOME/skills/`）。

## 依赖

- **Bash**：用于执行 `install.sh`（macOS/Linux 自带，Windows 可用 Git Bash 或 WSL）。
- **git**：用于克隆 gate-skills（使用 `--no-skills` 时不需要）。

## 获取 API Key 与授权

- **Gate (main)** 现货/合约需 API Key + Secret：访问 **https://www.gate.com/myaccount/profile/api-key/manage** 创建并配置环境变量 `GATE_API_KEY`、`GATE_API_SECRET`。
- **Gate-Dex**：首次使用钱包或交易时，请在浏览器中完成 OAuth 授权。

## 安装完成后

重启 Codex 以加载 MCP 与 Skills。
