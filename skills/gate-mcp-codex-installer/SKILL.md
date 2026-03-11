---
name: gate-mcp-codex-installer
description: 当用户要一键安装 Codex 的 Gate MCP 和全部 Gate Skills 时使用。可安装 Gate MCP（main/dex/info/news 可选）以及 gate-skills 仓库中的全部 skills；默认不选时安装所有 MCP + 全部 skills，skills 始终全部安装不可选。
---

# Gate 一键安装（Codex：MCP + Skills）

用户说「一键安装 Gate」「安装 Gate MCP 和 skills」「Codex 安装 gate-mcp」等且在使用 **Codex** 时，使用本技能。

## 资源地址

| 类型 | 名称 | 地址/配置 |
|------|------|-----------|
| MCP | Gate (main) | `npx -y gate-mcp`，见 [gate-mcp](https://github.com/gate/gate-mcp) |
| MCP | Gate Dex | https://api.gatemcp.ai/mcp/dex，x-api-key 固定 |
| MCP | Gate Info | https://api.gatemcp.ai/mcp/info |
| MCP | Gate News | https://api.gatemcp.ai/mcp/news |
| Skills | gate-skills | https://github.com/gate/gate-skills（安装 skills/ 下全部） |

## 行为规则

1. **默认**：用户未指定选哪几个 MCP 时，安装**全部 MCP**（main、dex、info、news）+ **全部 gate-skills**。
2. **可选 MCP**：用户可指定只安装部分 MCP（如只装 main、只装 dex 等），按用户选择执行。
3. **Skills**：未加 `--no-skills` 时，始终安装 gate-skills 仓库 **skills/** 下全部 skill。

## 安装步骤

### 1. 确认用户选择（MCP）

- 若用户未说明选哪些 MCP → 安装全部：main、dex、info、news。
- 若用户说明「只装 xxx」→ 仅安装指定的 MCP。

### 2. 写入 Codex MCP 配置

- 用户级配置：`~/.codex/config.toml`（或 `$CODEX_HOME/config.toml`）。若不存在会创建并写入 `[mcp_servers]` 及对应表。
- 若已存在则**合并**：仅当某 Gate MCP 段不存在时追加，不覆盖已有配置。
- 配置说明：
  - **Gate (main)**：stdio，`command = "npx"`, `args = ["-y", "gate-mcp"]`
  - **gate-dex**：streamable HTTP，`url` + `http_headers["x-api-key"]` 固定为 MCP_AK_8W2N7Q
  - **gate-info / gate-news**：streamable HTTP，`url`

### 3. 安装 gate-skills（全部）

- 从 https://github.com/gate/gate-skills 拉取 **skills/** 下所有子目录，复制到 `$CODEX_HOME/skills/`（默认 `~/.codex/skills/`）。
- 使用脚本时加 `--no-skills` 可仅安装 MCP、不安装 skills。

### 4. 完成后提示

- 告知用户已安装的 MCP 列表和「已安装 gate-skills 全部 skills」（若未使用 --no-skills）。
- 提示重启 Codex 以加载 MCP 与 Skills。
- **获取 API Key**：若用户使用 Gate (main) 现货/合约，提示其访问 https://www.gate.com/myaccount/profile/api-key/manage 创建 API Key 并配置 `GATE_API_KEY`、`GATE_API_SECRET`。
- **Gate-Dex 授权**：若安装了 Gate-Dex，当查询返回需要授权时，提示用户先打开 https://web3.gate.com/ 创建或绑定钱包，然后助手会返回可点击的 Google 授权链接供用户点击跳转完成授权。

## 脚本

使用本 skill 目录下的 **scripts/install.sh** 完成一键安装。

- 用法：  
  `./scripts/install.sh [--mcp main|dex|info|news] ... [--no-skills]`  
  不传 `--mcp` 时安装全部 MCP；传多个 `--mcp` 则只安装指定项；`--no-skills` 仅安装 MCP。
- DEX 的 x-api-key 已固定为 `MCP_AK_8W2N7Q`，写入 config.toml。

从 GitHub 下载本 skill 后，在仓库根目录执行：  
`bash skills/gate-mcp-codex-installer/scripts/install.sh`  
或（仅安装 MCP）：  
`bash skills/gate-mcp-codex-installer/scripts/install.sh --no-skills`
