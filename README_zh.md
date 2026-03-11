# Gate Skills

[English](README.md) | [中文](README_zh.md)

Gate Skills 是一个开放的技能市场，让 AI Agent 能够原生接入 gate.com 的加密生态。从市场分析、衍生品监控到一键 MCP 配置，全部可通过自然语言完成。

由 gate.com 构建，为加密社区而生。

### 一键安装

使用我们的安装器 skill，秒级完成配置：

- **Cursor 用户**：使用 `gate-mcp-cursorinstaller` — 一条命令安装全部 Gate MCP 服务器 + Skills
- **OpenClaw 用户**：使用 `gate-mcp-openclawinstaller` — 完整的 Gate MCP 安装器，支持交互式选择

只需对 AI 助手说 **"帮我安装 Gate MCP"**，或直接运行安装脚本即可。

### 框架兼容性

这些 skills 设计为可兼容任意 AI Agent 框架。无论你使用 Cursor、OpenClaw，还是自研 Agent 栈，都可以通过最少配置接入 gate.com 的加密智能能力。

---

## Skills 总览

| Skill | 描述 | 版本 | 状态 |
|-------|------|------|------|
| [gate-mcp-cursorinstaller](#-gate-mcp-cursorinstaller) | 为 Cursor 提供的一键安装 Gate MCP 与 Skills 脚本 | `2026.3.10-1` | ✅ Active |
| [gate-mcp-openclawinstaller](#-gate-mcp-openclawinstaller) | 为 OpenClaw 提供的 Gate MCP 完整安装器 | `2026.3.10-1` | ✅ Active |
| [gate-exchange-marketanalysis](#-gate-exchange-marketanalysis) | 市场盘口分析：流动性、动量、爆仓、资金费套利、基差、操纵风险、订单簿解读、滑点模拟、K线突破、周末与工作日对比 | `2026.3.7-1` | ✅ Active |
| [gate-exchange-futures](#-gate-exchange-futures) | Gate 合约交易：开仓、平仓、撤单、改单 | `2026.3.5-1` | ✅ Active |
| [gate-exchange-spot](#-gate-exchange-spot) | Gate 现货交易：买卖下单、订单管理、账户查询、资产兑换 | `2026.3.9-1` | ✅ Active |
| [gate-dex-mcpmarket](#-gate-dex-mcpmarket) | Gate Wallet DEX 行情：K线、交易统计、流动性、代币信息、排行、安全审计、新币发现 | `2026.3.5-1` | ✅ Active |
| [gate-dex-mcpwallet](#-gate-dex-mcpwallet) | Gate Wallet 资产与历史记录：余额查询、总资产、代币持有、转账与兑换历史 | `2026.3.6-1` | ✅ Active |
| [gate-dex-mcpswap](#-gate-dex-mcpswap) | Gate Wallet Swap/DEX 交易：获取报价，执行跨链与单链 Swap | `2026.3.6-1` | ✅ Active |
| [gate-dex-mcptransfer](#-gate-dex-mcptransfer) | Gate Wallet 转账操作：执行 EVM 多链与 Solana 的原生/代币转账 | `2026.3.5-1` | ✅ Active |
| [gate-dex-mcpdapp](#-gate-dex-mcpdapp) | Gate Wallet DApp 交互：连接钱包，签名消息，执行 DApp 交易与授权 | `2026.3.5-1` | ✅ Active |
| [gate-dex-mcpauth](#-gate-dex-mcpauth) | Gate Wallet 身份验证：Google OAuth 登录、会话管理 | `2026.3.5-1` | ✅ Active |

---

## 📈 gate-exchange-marketanalysis

> **路径**: `skills/gate-exchange-marketanalysis/`

只读市场盘口分析，涵盖十个场景：流动性、动量、爆仓监控、资金费套利、基差、操纵风险、订单簿解读、滑点模拟、K线突破/支撑阻力，以及周末与工作日成交量对比。

**示例提示词**：
- `Check BTC liquidity and slippage`
- `What is the momentum of ETH?`
- `Simulate a $10K market buy on ETH`
- `Is there manipulation risk on DOGE?`
- `Compare BTC weekend vs weekday volume`

---

## 📊 gate-exchange-futures

> **路径**: `skills/gate-exchange-futures/`

Gate 交易所 USDT 永续合约交易，支持四类操作：开仓、平仓、撤单、改单。含盘前检查、保证金/杠杆处理，以及下单前用户确认机制。

**示例提示词**：
- `Long BTC 1 contract with 10x leverage`
- `Close all ETH positions`
- `Cancel my BTC buy order`
- `Change order price to 60000`

---

## 💱 gate-exchange-spot

> **路径**: `skills/gate-exchange-spot/`

Gate 现货交易，支持市价/限价买卖、条件单、订单管理（改单/撤单）、账户查询、成交验证和资产兑换。所有下单操作需用户明确确认。

**示例提示词**：
- `Buy 100 USDT worth of BTC`
- `Sell ETH when price hits 3500`
- `Cancel my unfilled BTC order and check balance`
- `Swap USDT to SOL`

---

## 🌐 gate-dex-mcpmarket

> **路径**: `skills/gate-dex-mcpmarket/`

Gate Wallet DEX 行情数据，全部只读、无需认证。涵盖 K线、交易统计、流动性池、代币详情、排行榜、新币发现和合约安全审计。

**示例提示词**：
- `Show me the ETH K-line on the last 24h`
- `What tokens are trending on BSC?`
- `Check the security of contract 0x...`
- `List newly launched tokens on ETH`

---

## 💼 gate-dex-mcpwallet

> **路径**: `skills/gate-dex-mcpwallet/`

Gate Wallet 资产与历史记录。查询余额、总资产、代币持有、钱包地址、转账历史、交易详情和 Swap 历史。支持 EVM 多链和 Solana。

**示例提示词**：
- `How much ETH do I have?`
- `Check my wallet balance and total assets`
- `Show my transfer records`
- `What is my Solana wallet address?`

---

## 🔄 gate-dex-mcpswap

> **路径**: `skills/gate-dex-mcpswap/`

Gate Wallet Swap/DEX 交易。获取报价，执行 EVM 和 Solana 的跨链及单链 Swap，并跟踪状态。包含强制的三步确认流程。

**示例提示词**：
- `Swap 100 USDT for ETH`
- `Exchange 1 SOL for USDC`
- `Buy some PEPE with BNB`
- `Cross-chain swap ETH to Solana SOL`

---

## 💸 gate-dex-mcptransfer

> **路径**: `skills/gate-dex-mcptransfer/`

Gate Wallet 转账操作。构建交易、签名并广播。支持 EVM 多链和 Solana 的原生与代币转账，包含强制余额验证和确认机制。

**示例提示词**：
- `Send 0.1 ETH to 0x...`
- `Transfer 100 USDT on Polygon to 0x...`
- `Send 5 SOL to my other wallet`
- `Batch transfer USDC to these addresses`

---

## 🔌 gate-dex-mcpdapp

> **路径**: `skills/gate-dex-mcpdapp/`

Gate Wallet DApp 交互。连接钱包，签名消息（EIP-712/personal_sign），执行 DApp 交易以及授权 ERC20 Approve。包含安全审查。

**示例提示词**：
- `Connect my wallet to Uniswap`
- `Sign this EIP-712 message`
- `Approve 1000 USDC for Aave`
- `Add ETH-USDC liquidity on Uniswap`

---

## 🔐 gate-dex-mcpauth

> **路径**: `skills/gate-dex-mcpauth/`

Gate Wallet 身份验证。管理 Google OAuth 登录、刷新 Token 和注销。操作前自动验证 MCP 服务器连接状态。

**示例提示词**：
- `Log in to my wallet`
- `Sign in`
- `Log out of my account`
- `Refresh my session`

---

## 🛠️ gate-mcp-cursorinstaller

> **路径**: `skills/gate-mcp-cursorinstaller/`

专为 Cursor 环境提供的 Gate MCP 及 Skills 一键安装脚本。

**快速开始**：
```bash
bash scripts/install.sh
```

---

## 🛠️ gate-mcp-openclawinstaller

> **路径**: `skills/gate-mcp-openclawinstaller/`

专为 OpenClaw 环境提供的 Gate MCP 完整安装器，支持配置现货/合约交易、钱包、行情与新闻服务器。

**快速开始**：
```bash
./scripts/install.sh
```

---

## 快速开始

### 前置要求

- 支持 skill 加载的 AI Agent 环境（例如 Cursor、OpenClaw）
- Node.js 与 npm

### 配置步骤

根据你的环境选择对应的安装器：

#### Cursor 用户

使用 `gate-mcp-cursorinstaller` 一键安装 Gate MCP 和 Skills：

```bash
# 执行安装脚本
bash skills/gate-mcp-cursorinstaller/scripts/install.sh
```

或直接向 AI 助手说：
```
帮我安装 Gate MCP
```

#### OpenClaw 用户

使用 `gate-mcp-openclawinstaller`：

```bash
# 安装全部 Gate MCP 服务器（默认）
./skills/gate-mcp-openclawinstaller/scripts/install.sh

# 选择性安装
./skills/gate-mcp-openclawinstaller/scripts/install.sh --select
```

### 开始使用 Skills

安装完成后，向 AI Agent 提出任意市场或交易问题即可。

---

## Skills 安装说明

### 通用安装（推荐）

1. 检查是否已安装 `npx`（未安装见附录）：

   ```bash
   npx -v
   ```

   若返回版本号（例如 `11.8.0`），说明 `npx` 已安装。

![检查 npx 版本](image/general-install-1.png)

2. 通过交互方式安装 skills：

   ```bash
   npx skills add https://github.com/gate/gate-skills
   ```

![选择并安装 skills](image/general-install-2.png)

3. 安装指定 skill（示例：`gate-market`）：

   ```bash
   npx skills add https://github.com/gate/gate-skills --skill gate-market
   ```

![安装指定 skill](image/general-install-3.png)

### 在 Claude CLI 中安装 Skills

#### 方式一：自然语言安装（推荐）

```text
help me to install skills, github url is: https://github.com/gate/gate-skills
```

![Claude 自然语言安装](image/claude-install-1.png)

安装完成。

![Claude 安装完成](image/claude-install-2.png)

#### 方式二：手动安装

Step 1：下载 Skills 包（GitHub：<https://github.com/gate/gate-skills>）

Step 2：解压后复制到 `~/.claude/skills/` 目录。

- 显示隐藏目录：打开用户主目录后按 `Command + Shift + .`（再次按下可隐藏）
- 复制到目标路径：将 `gate-skills-master` 中的 `skills` 子目录复制到 `~/.claude/skills/`
- 验证安装：在 Claude CLI 输入 `/skills`，或提问 `how many skills have I installed?`

### 在 Codex CLI 中安装 Skills

#### 方式一：自然语言安装（推荐）

```text
help me to install skills, github url is: https://github.com/gate/gate-skills
```

![Codex 自然语言安装步骤](image/codex-nl-install-1.png)

重启 Codex 后生效。

![Codex 自然语言安装完成](image/codex-nl-install-2.png)

#### 方式二：终端安装

1. 在终端输入 `/skills`，选择 `1. List skills`，再选择 `Skill Installer`，输入 `https://github.com/gate/gate-skills`

   ![Codex 终端安装 - 进入 skills 菜单](image/codex-terminal-install-1.png)
   ![Codex 终端安装 - 选择 Skill Installer](image/codex-terminal-install-2.png)
   ![Codex 终端安装 - 输入仓库地址](image/codex-terminal-install-3.png)
   ![Codex 终端安装 - 安装过程](image/codex-terminal-install-4.png)

2. 验证安装：重启终端后执行 `/skills` -> `List Skills`

   ![Codex 终端安装 - 验证已安装](image/codex-terminal-install-5.png)

#### 方式三：手动安装

Step 1：下载 Skills 包（GitHub：<https://github.com/gate/gate-skills>）

![Codex 手动安装 - 下载仓库](image/codex-manual-install-1.png)

Step 2：解压后复制到 `~/.codex/skills/` 目录。

1. 显示隐藏目录：打开用户主目录后按 `Command + Shift + .`（再次按下可隐藏）

   ![Codex 手动安装 - 打开隐藏目录](image/codex-manual-install-2.png)

2. 复制到目标路径：将 `gate-skills-master` 中所有 `skills` 子目录复制到 `~/.codex/skills/`

   ![Codex 手动安装 - 复制 skills 子目录](image/codex-manual-install-3.png)

3. 验证安装：重启终端后执行 `/skills` -> `List Skills`

   ![Codex 手动安装 - 验证安装结果](image/codex-manual-install-4.png)

### 在 OpenClaw 中安装 Skills

#### 方式一：对话安装（推荐）

在 OpenClaw 聊天界面（如 Telegram、飞书）直接发送 GitHub 链接给助手，例如：

```text
帮我安装这个技能：https://github.com/gate/gate-skills
```

助手会自动拉取仓库、配置环境并尝试加载该 skill。

#### 方式二：使用 ClawHub 自动安装（推荐）

- 官方市场（需先安装 `npx`，见附录）：

  ```bash
  npx clawhub@latest install gate-skills
  ```

- GitHub 仓库：

  ```bash
  npx clawhub@latest add https://github.com/gate/gate-skills
  ```

#### 方式三：手动安装

Step 1：下载 Skills 包（GitHub：<https://github.com/gate/gate-skills>）

![OpenClaw 手动安装 - 下载仓库](image/openclaw-manual-install-1.png)

Step 2：解压后复制到 `~/.openclaw/skills/` 目录。

1. 显示隐藏目录：打开用户主目录后按 `Command + Shift + .`（再次按下可隐藏）
2. 复制到目标路径：将 `gate-skills-master` 中所有 `skills` 子目录复制到 `~/.openclaw/skills/`

Step 3：重启 OpenClaw Gateway。

### 附录：macOS 安装 npx

1. 检查是否已安装 `npx`：

   ```bash
   npx -v
   ```

   若返回版本号（例如 `11.8.0`），说明 `npx` 已安装。

2. 若未安装，可使用以下方式：

   - 方式一：通过 Homebrew 安装

     ```bash
     # 安装 Homebrew（官方）
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

     # 安装 Homebrew（国内镜像）
     /bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"

     # 验证 Homebrew
     brew --version

     # 安装 Node.js（包含 npx）
     brew install node

     # 验证 npx
     npx -v
     ```

   - 方式二：从 Node.js 官网下载安装包：
     <https://nodejs.org/en/download>

---

## 仓库结构

```
gate-github-skills/
├── README.md
├── README_zh.md
├── image/                              # 安装截图
└── skills/
    ├── gate-dex-mcpauth/               # 钱包身份验证 skill
    ├── gate-dex-mcpdapp/               # 钱包 DApp 交互 skill
    ├── gate-dex-mcpmarket/             # 钱包 DEX 行情数据 skill
    ├── gate-dex-mcpswap/               # 钱包 Swap/DEX 交易 skill
    ├── gate-dex-mcptransfer/           # 钱包转账执行 skill
    ├── gate-dex-mcpwallet/             # 钱包资产与记录 skill
    ├── gate-exchange-futures/          # 合约交易 skill
    ├── gate-exchange-marketanalysis/   # 市场盘口分析 skill
    ├── gate-exchange-spot/             # 现货交易 skill
    ├── gate-mcp-cursorinstaller/       # Cursor MCP 安装 skill
    └── gate-mcp-openclawinstaller/     # OpenClaw MCP 安装 skill
```

---

## 关于本仓库

每个 skill 都位于 `skills/` 下独立目录，包含：

- **`SKILL.md`** — Skill 定义（YAML frontmatter：名称、版本、描述、触发词）及结构化说明（路由规则、工作流等）
- **`references/`** — 复杂子模块的详细文档、步骤工作流与报告模板
- **`CHANGELOG.md`** — 版本历史与变更记录

---

## 贡献指南

欢迎贡献！新增 skill 的流程如下：

1. **Fork 仓库**并创建新分支：
   ```bash
   git checkout -b feature/<skill-name>
   ```

2. 在 `skills/` 下创建新目录，至少包含一个 `SKILL.md` 文件。

3. 按要求格式编写：
   ```markdown
   ---
   name: <skill-name>
   version: "<version>"
   updated: "<YYYY-MM-DD>"
   description: A clear description of what the skill does and when to trigger it.
   ---

   # <Skill Title>

   [Add instructions, routing rules, workflows, and report templates here]
   ```

4. 对复杂子模块，在 `references/` 子目录中补充参考文档。

5. 向 `main` 分支发起 Pull Request。

---

## 免责声明

Gate Skills 仅为信息工具。所有输出均按"现状"和"可用"基础提供，不构成任何明示或暗示的保证。其内容不构成投资、金融、交易或任何其他形式的建议，也不构成买入、卖出或持有任何资产的推荐。所有分析均为数据驱动且只读，这些 skills 不执行任何交易操作。数字资产价格具有高风险和高波动性。你需要对自己的投资决策负责。历史表现不代表未来结果。进行任何投资前，请咨询独立的专业财务顾问。
