# Gate CEX 一键安装（Cursor MCP + Skills）

一键为 Cursor 安装 Gate 相关 MCP 与 [gate-skills](https://github.com/gate/gate-skills) 全部 skills，便于从 GitHub 下载后直接使用。

## 安装方式

### 从 GitHub 下载后一键安装

```bash
# 克隆本仓库（或下载 ZIP 解压后进入该目录）
git clone <本仓库地址>
cd gate-cex-installer

# 一键安装全部 MCP + 全部 gate-skills
bash scripts/install.sh
```

### 仅安装 MCP（不安装 gate-skills）

```bash
bash scripts/install.sh --no-skills
```

### 只安装部分 MCP

```bash
# 只安装 Gate (main) 和 Gate-Dex
bash scripts/install.sh --mcp main --mcp dex

# 只安装 Gate、Info、News
bash scripts/install.sh --mcp main --mcp info --mcp news
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

- **MCP 配置**：`~/.cursor/mcp.json`（Windows：`%APPDATA%\Cursor\mcp.json`），会与已有配置合并。
- **Skills**：`~/.cursor/skills/`（Windows：`%APPDATA%\Cursor\skills`）。

## 依赖

- **Bash**：用于执行 `install.sh`（macOS/Linux 自带，Windows 可用 Git Bash 或 WSL）。
- **Node.js**：用于合并 `mcp.json`；若无 Node，脚本会输出需手动合并的 JSON 片段。
- **git**：用于克隆 gate-skills（使用 `--no-skills` 时不需要）。

## 安装完成后

重启 Cursor 以加载新 MCP 和 skills。若使用 Gate (main) 的 OAuth，首次连接时按提示在浏览器中完成授权。
