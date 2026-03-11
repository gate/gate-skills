# Gate Claude Code 一键安装（MCP + Skills）

一键为 **Claude Code（Claude CLI）** 安装 Gate 相关 MCP 与 [gate-skills](https://github.com/gate/gate-skills) 全部 skills。

## 安装方式

### 从本仓库一键安装

```bash
# 在 gate-skills 仓库根目录执行
bash skills/gate-mcp-claude-installer/scripts/install.sh
```

### 仅安装 MCP（不安装 gate-skills）

```bash
bash skills/gate-mcp-claude-installer/scripts/install.sh --no-skills
```

### 只安装部分 MCP

```bash
# 只安装 Gate (main) 和 Gate-Dex
bash skills/gate-mcp-claude-installer/scripts/install.sh --mcp main --mcp dex

# 只安装 Gate、Info、News
bash skills/gate-mcp-claude-installer/scripts/install.sh --mcp main --mcp info --mcp news
```

## 将安装的内容

| 项目 | 说明 |
|------|------|
| **Gate** | 主 MCP，`npx -y gate-mcp`，[gate-mcp](https://github.com/gate/gate-mcp) |
| **Gate-Dex** | https://api.gatemcp.ai/mcp/dex（x-api-key 已内置） |
| **Gate-Info** | https://api.gatemcp.ai/mcp/info |
| **Gate-News** | https://api.gatemcp.ai/mcp/news |
| **gate-skills** | 从 [gate-skills](https://github.com/gate/gate-skills) 克隆并安装 `skills/` 下全部 skill |

## 配置写入位置

- **MCP 配置**：`~/.claude.json` 的 `mcpServers` 字段（Windows：`%USERPROFILE%\.claude.json`），会与已有配置合并。
- **Skills**：`~/.claude/skills/`（Windows：`%USERPROFILE%\.claude\skills`）。

## 依赖

- **Bash**：用于执行 `install.sh`（macOS/Linux 自带，Windows 可用 Git Bash 或 WSL）。
- **Node.js**：用于合并 `~/.claude.json`；若无 Node，脚本会输出需手动合并的 JSON 片段。
- **git**：用于克隆 gate-skills（使用 `--no-skills` 时不需要）。

## 获取 API Key 与授权

- **Gate (main)** 现货/合约需 API Key + Secret：访问 **https://www.gate.com/myaccount/profile/api-key/manage** 创建并配置环境变量 `GATE_API_KEY`、`GATE_API_SECRET`。
- **Gate-Dex**：当查询返回需要授权时，请先打开 https://web3.gate.com/ 创建或绑定钱包，然后点击助手返回的 Google 授权链接完成授权。

## 安装完成后

重新打开 Claude Code 或新开一个会话以加载 MCP 与 Skills。
