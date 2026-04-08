# Gate Skills

[English](README.md) | [中文](README_zh.md)

Gate Skills 是一个开放的技能市场，让 AI Agent 能够原生接入 Gate 的加密生态。从市场分析、衍生品监控到一键 MCP 配置，全部可通过自然语言完成。

由 Gate 构建，为加密社区而生。

### 一键安装

使用我们的统一安装器 skill，秒级完成配置：

- **全平台（Cursor / Claude Code / Codex / OpenClaw）**：使用 `gate-mcp-installer` — 一键安装全部 Gate MCP 服务器 + Skills

**快速开始**：只需对 AI 助手说：

> **"帮我自动安装 Gate Skills 和 MCP：https://github.com/gate/gate-skills"**

或直接从仓库运行安装脚本。

### 框架兼容性

这些 skills 设计为可兼容任意 AI Agent 框架。无论你使用 Cursor、OpenClaw，还是自研 Agent 栈，都可以通过最少配置接入 Gate 的加密智能能力。

---

## Skills 总览

| Skill | 描述 | 版本 | 状态 |
|-------|------|------|------|
| [gate-exchange-tradfi](#-gate-exchange-tradfi) | Gate TradFi（传统金融）只读查询：订单、持仓、行情、资产与 MT5 账户信息 | `2026.3.13-6` | ✅ Active |
| [gate-exchange-simpleearn](#-gate-exchange-simpleearn) | Gate Simple Earn（活期理财）：持仓、利息、Top APY 利率查询（不支持申购/赎回） | `2026.3.12-2` | ✅ Active |
| [gate-exchange-affiliate](#-gate-exchange-affiliate) | Gate 交易所联盟/合伙人计划：佣金、交易量、净手续费、客户数、交易用户数查询与申请指引 | `2026.3.13` | ✅ Active |
| [gate-exchange-unified](#-gate-exchange-unified) | Gate 统一账户：权益、借还、借贷与利息、模式切换、杠杆与抵押币 | `2026.3.13-4` | ✅ Active |
| [gate-exchange-assets](#-gate-exchange-assets) | Gate 交易所资产查询：总资产、现货持仓、账户估值、账户流水（只读） | `2026.3.12-3` | ✅ Active |
| [gate-info-coinanalysis](#-gate-info-coinanalysis) | 单币种综合分析：基本面、技术面、新闻、社交情绪 | `2026.3.25-1` | ✅ Active |
| [gate-exchange-dual](#-gate-exchange-dual) | Gate 双币理财：产品发现、结算模拟、持仓与余额查询（只读） | `2026.3.12-1` | ✅ Active |
| [gate-exchange-staking](#-gate-exchange-staking) | Gate 理财/质押：持仓、收益、产品发现、订单历史（只读） | `2026.3.12-1` | ✅ Active |
| [gate-exchange-autoinvest](#-gate-exchange-autoinvest) | Gate Earn 极速定投（DCA）：创建/更新/终止/加仓计划；支持币种、最小金额、记录、计划详情；现货与活期理财余额上下文 | `2026.4.2-3` | ✅ Active |
| [gate-exchange-subaccount](#-gate-exchange-subaccount) | Gate 子账户管理：查询状态、列表、创建、锁定/解锁（写操作需确认） | `2026.3.12-1` | ✅ Active |
| [gate-info-addresstracker](#-gate-info-addresstracker) | 链上地址追踪：地址画像、交易历史、资金流向分析 | `2026.3.25-1` | ✅ Active |
| [gate-info-coincompare](#-gate-info-coincompare) | 多币种对比：多维度对比表与总结 | `2026.3.25-1` | ✅ Active |
| [gate-info-defianalysis](#-gate-info-defianalysis) | DeFi 生态：TVL 排行、协议指标、收益/稳定币、跨链桥、交易所储备、爆仓热力图等（Gate-Info；只读） | `2026.3.30-6` | ✅ Active |
| [gate-info-macroimpact](#-gate-info-macroimpact) | 宏观与加密联动：经济日历、指标、相关新闻与行情快照（Gate-Info + Gate-News；只读） | `2026.3.30-6` | ✅ Active |
| [gate-info-marketoverview](#-gate-info-marketoverview) | 加密市场总览：板块排行、DeFi、事件、宏观摘要 | `2026.3.25-1` | ✅ Active |
| [gate-info-riskcheck](#-gate-info-riskcheck) | 代币与合约风险评估：蜜罐检测、Rug Pull、税费、持币集中度 | `2026.3.25-1` | ✅ Active |
| [gate-info-tokenonchain](#-gate-info-tokenonchain) | 代币链上：持币分布、活跃度、大额划转（本版不含 Smart Money；Gate-Info；只读） | `2026.3.30-5` | ✅ Active |
| [gate-info-trendanalysis](#-gate-info-trendanalysis) | 趋势与技术分析：K线、RSI、MACD、多周期信号 | `2026.3.25-1` | ✅ Active |
| [gate-news-briefing](#-gate-news-briefing) | 加密新闻简报：重大事件、热门新闻、社交情绪 | `2026.3.25-1` | ✅ Active |
| [gate-news-communityscan](#-gate-news-communityscan) | 社区 / X 情绪：讨论扫描 + 量化社交情绪（多平台 UGC 上线后扩展；Gate-News；只读） | `2026.3.30-5` | ✅ Active |
| [gate-news-eventexplain](#-gate-news-eventexplain) | 事件归因与解释：价格异动原因追溯与影响链分析 | `2026.3.25-1` | ✅ Active |
| [gate-news-listing](#-gate-news-listing) | 交易所上架/下架追踪：公告监控与新币基本面补充 | `2026.3.25-1` | ✅ Active |
| [gate-dex-market](#-gate-dex-market) | Gate DEX 行情数据（OpenAPI 模式）：代币信息、K线、排行、安全审计 | `2026.3.12-1` | ✅ Active |
| [gate-dex-trade](#-gate-dex-trade) | Gate DEX 交易：MCP + OpenAPI 双模式，智能路由执行 Swap | `2026.3.12-1` | ✅ Active |
| [gate-exchange-marketanalysis](#-gate-exchange-marketanalysis) | 市场盘口分析：流动性、动量、爆仓、资金费套利、基差、操纵风险、订单簿解读、滑点模拟、K线突破、周末与工作日对比 | `2026.3.11-1` | ✅ Active |
| [gate-exchange-pay](#-gate-exchange-pay) | Gate Pay 支付执行：完成商户支付、支付优先流程、输出收据 | `2026.3.27-2` | ✅ Active |
| [gate-mcp-installer](#-gate-mcp-installer) | 全平台一键安装 Gate MCP 与 Skills（Cursor、Claude Code、Codex、OpenClaw） | `2026.4.1-1` | ✅ Active |
| [gate-exchange-spot](#-gate-exchange-spot) | Gate 现货交易：买卖下单、订单管理、账户查询、资产兑换 | `2026.3.10-1` | ✅ Active |
| [gate-dex-wallet](#-gate-dex-wallet) | Gate DEX 综合钱包：身份认证、资产查询、转账执行、DApp 交互 | `2026.3.10-1` | ✅ Active |
| [gate-exchange-trading](#-gate-exchange-trading) | 端到端交易：行情判断、风控、下单、执行与交易后管理 | `2026.3.14-3` | ✅ Active |
| [gate-exchange-alpha](#-gate-exchange-alpha) | Gate Alpha 代币发现、行情查看与账户持仓查询 | `2026.3.13-1` | ✅ Active |
| [gate-exchange-coupon](#-gate-exchange-coupon) | Gate 优惠券/券码管理：列表、详情、使用规则、来源追溯 | `2026.3.13-1` | ✅ Active |
| [gate-exchange-crossex](#-gate-exchange-crossex) | Gate CrossEx 跨所交易：订单、持仓与历史查询（Gate、Binance、OKX） | `2026.3.12-1` | ✅ Active |
| [gate-exchange-transfer](#-gate-exchange-transfer) | Gate 内部划转：在现货、杠杆、合约、交割、期权账户间转移资金 | `2026.3.16-2` | ✅ Active |
| [gate-exchange-flashswap](#-gate-exchange-flashswap) | Gate 闪兑查询：币对列表、兑换限额、订单历史与详情 | `2026.3.11-5` | ✅ Active |
| [gate-exchange-smallbalance](#-gate-exchange-smallbalance) | Gate 小额资产/粉尘：可兑列表、兑换 GT、兑换历史 | `2026.3.20-1` | ✅ Active |
| [gate-exchange-vipfee](#-gate-exchange-vipfee) | Gate VIP 等级与手续费率查询：现货费率、合约费率、VIP 等级 | `2026.3.11-2` | ✅ Active |
| [gate-info-liveroomlocation](#-gate-info-liveroomlocation) | Gate 直播与回放列表：按分类、币种、热度/最新排序筛选 | `2026.3.13-1` | ✅ Active |
| [gate-exchange-futures](#-gate-exchange-futures) | Gate 合约交易：开仓、平仓、撤单、改单 | `2026.3.5-1` | ✅ Active |
| [gate-exchange-referral](#-gate-exchange-referral) | 邀请好友：活动推荐与规则解读（Earn Together、助领券、超级返佣）等（只读） | `2026.3.26-1` | ✅ Active |
| [gate-exchange-assets-manager](#-gate-exchange-assets-manager) | L2 账户资产管家：多账户概览、保证金/爆仓风险、理财/质押/联盟、统一账户借还抵押（读+写） | `2026.3.25-1` | ✅ Active |
| [gate-info-research](#-gate-info-research) | L2 市场研究 Copilot：聚合 Gate-Info 与 Gate-News 只读研报、对比与风险检查 | `2026.3.23-1` | ✅ Active |
| [gate-exchange-welfare](#-gate-exchange-welfare) | 福利中心：新用户任务与奖励（MCP 查询，禁止编造奖励） | `2026.3.23-1` | ✅ Active |
| [gate-exchange-launchpool](#-gate-exchange-launchpool) | LaunchPool：项目浏览、质押、赎回、质押记录、空投奖励 | `2026.3.23-1` | ✅ Active |
| [gate-exchange-kyc](#-gate-exchange-kyc) | KYC：门户引导（仅官网完成身份验证） | `2026.3.23-1` | ✅ Active |
| [gate-exchange-collateralloan](#-gate-exchange-collateralloan) | 多币抵押借贷：查询、还款、追加/赎回抵押品 | `2026.3.23-1` | ✅ Active |
| [gate-exchange-activitycenter](#-gate-exchange-activitycenter) | 活动中心：平台活动推荐、活动列表、我的活动 | `2026.3.23-1` | ✅ Active |

---

## 🤝 gate-exchange-affiliate

> **路径**: `skills/gate-exchange-affiliate/`

Gate 交易所联盟/合伙人计划数据查询与管理：佣金追踪、团队表现分析、申请指引。支持单次最多 30 天、合计最多 180 天的历史查询（超 30 天时由 Agent 自动拆分请求）。需合伙人权限认证。

**示例提示词**：
- `我的联盟数据`
- `本周佣金`
- `合伙人收益`
- `团队表现`
- `客户交易量`
- `返佣收入`
- `申请联盟计划`

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

## 🤖 gate-exchange-trading

> **路径**: `skills/gate-exchange-trading/`

Gate 交易所端到端交易。在一个 skill 中完成完整交易闭环：行情判断 → 风险评估 → 订单草案 → 用户确认 → 执行下单 → 交易后管理。同时支持现货和合约。

**示例提示词**：
- `分析 BTC 后下单`
- `现在买 ETH 安全吗？安全的话帮我买`
- `检查风险然后做多 BTC 合约 10 倍杠杆`
- `分析一下再买 SOL`

---

## 🔮 gate-exchange-alpha

> **路径**: `skills/gate-exchange-alpha/`

Gate Alpha 代币发现、行情查看和账户操作。浏览 Alpha 可交易代币、查看 Alpha 行情/价格、查看 Alpha 持仓与组合价值。

**示例提示词**：
- `Alpha 上有什么币？`
- `SOL 在 Alpha 上的价格`
- `显示我的 Alpha 持仓`
- `Alpha 组合价值`
- `Solana 链上有哪些 Alpha 代币？`

---

## 🎟️ gate-exchange-coupon

> **路径**: `skills/gate-exchange-coupon/`

Gate 优惠券/券码管理：查看可用券、按类型搜索、查看已过期/已使用记录、查看券详情、阅读使用规则、追溯券的获取来源。

**示例提示词**：
- `我的优惠券`
- `我有什么券可以用？`
- `券的详情`
- `我的优惠券什么时候过期？`
- `这个券是怎么获得的？`

---

## 🌐 gate-exchange-crossex

> **路径**: `skills/gate-exchange-crossex/`

Gate CrossEx 跨所交易操作：订单查询、持仓查询、历史记录查询，支持 Gate、Binance、OKX 跨所。

**示例提示词**：
- `查询所有 CrossEx 挂单`
- `查看我的 CrossEx 持仓`
- `CrossEx 订单历史`
- `CrossEx 成交历史`

---

## 💸 gate-exchange-transfer

> **路径**: `skills/gate-exchange-transfer/`

Gate 同 UID 内部划转：在现货、逐仓杠杆、永续合约（USDT/BTC 本位）、交割、期权账户间转移资金。执行前需用户明确确认并预校验余额。

**示例提示词**：
- `从现货转 100 USDT 到合约`
- `把资金从现货移到永续`
- `转 BTC 到交割账户`
- `从杠杆转 USDT 到现货`

---

## ⚡ gate-exchange-flashswap

> **路径**: `skills/gate-exchange-flashswap/`

Gate 闪兑查询：浏览支持的币对、验证兑换额度限制、查看闪兑订单历史、查询指定订单详情。只读，不执行兑换。

**示例提示词**：
- `哪些币对支持闪兑？`
- `BTC/USDT 闪兑限额`
- `显示我的闪兑订单历史`
- `查询闪兑订单 #12345`

---

## 🪙 gate-exchange-smallbalance

> **路径**: `skills/gate-exchange-smallbalance/`

查询符合平台阈值的现货 **粉尘/小额资产**、将指定或全部可兑资产 **兑换为 GT**（不可撤销；写操作前需用户确认），以及 **小额兑换历史**。需认证；兑换需具备钱包写权限的 API。

**示例提示词**：
- `有哪些小额可以换成 GT？`
- `把粉尘全部换成 GT`
- `把 FLOKI 粉尘换成 GT`
- `小额兑换历史`

---

## 👑 gate-exchange-vipfee

> **路径**: `skills/gate-exchange-vipfee/`

查询 Gate VIP 等级与交易手续费率，包括现货和合约费率信息。

**示例提示词**：
- `我的 VIP 等级是什么？`
- `查看现货和合约手续费`
- `查看我的 VIP 等级和费率`
- `我的手续费率是多少？`

---

## 🎬 gate-info-liveroomlocation

> **路径**: `skills/gate-info-liveroomlocation/`

Gate 直播与回放列表。按业务分类（行情分析、热点话题、区块链、其他）、币种、排序方式（最热/最新）和数量进行筛选。

**示例提示词**：
- `最热的直播间`
- `找 5 个 SOL 相关的直播`
- `最新的行情分析回放`
- `有 BTC 相关的直播吗？`

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

## 📦 gate-exchange-assets

> **路径**: `skills/gate-exchange-assets/`

Gate 交易所只读资产与余额查询：总资产、现货持仓、USDT 估值、账户流水。不涉及交易或划转。

**示例提示词**：
- `我的账户总价值多少？`
- `查一下我的 USDT 余额`
- `显示我的总资产`
- `我的 BTC 余额是多少？`
- `显示最近 BTC 账户流水和当前余额`

---

## 📋 gate-exchange-dual

> **路径**: `skills/gate-exchange-dual/`

Gate 交易所双币理财：浏览产品（APY、目标价）、结算模拟、查看持仓与余额。只读，不支持下单。

**示例提示词**：
- `有哪些 BTC 双币理财计划？`
- `卖高目标价 62000，如果涨到 65000 会怎样？`
- `双币理财持仓汇总`
- `双币里锁了多少？`

---

## 🪙 gate-exchange-staking

> **路径**: `skills/gate-exchange-staking/`

Gate 理财/质押查询：持仓、收益、产品发现、订单历史。只读，不支持申购/赎回操作。

**示例提示词**：
- `显示我的质押持仓`
- `我的质押收益是多少？`
- `找一下 BTC 的理财产品`
- `显示理财/质押历史`

---

## 📗 gate-exchange-autoinvest

> **路径**: `skills/gate-exchange-autoinvest/`

Gate Exchange Earn **极速定投（DCA）**：通过 **MCP 工具名**完成计划与查询（见 `SKILL.md` → **MCP tools**），含 **11** 个 earn auto-invest 工具及 `cex_spot_get_spot_accounts`、`cex_earn_list_user_uni_lends`；本 skill 正文不暴露 REST 路径。

**示例提示词**：
- `每周用 100 USDT 定投 BTC`
- `终止我的 ETH 定投计划`
- `USDT 定投最小金额是多少？`

---

## 💸 gate-exchange-simpleearn

> **路径**: `skills/gate-exchange-simpleearn/`

Gate Simple Earn（活期理财）只读查询：支持单币/全量持仓、单币累计利息，以及 Top APY 利率查询。本 skill 当前不支持申购与赎回执行。

**示例提示词**：
- `我的 USDT Simple Earn 持仓`
- `显示所有 Simple Earn 持仓`
- `我累计赚了多少 USDT 利息？`
- `哪个币种的 Simple Earn APY 最高？`
- `申购 100 USDT 到 Simple Earn`（将回复暂不支持）

---

## 🏦 gate-exchange-tradfi

> **路径**: `skills/gate-exchange-tradfi/`

Gate TradFi（传统金融）只读查询技能：支持订单、持仓、行情、资产与 MT5 账户信息查询。本 skill 不执行下单、撤单或资金划转。

**示例提示词**：
- `我的 TradFi 挂单`
- `显示我的持仓历史`
- `TradFi 分类列表`
- `查询 EURUSD 的 ticker`
- `显示我的 MT5 账户信息`

---

## 🔗 gate-exchange-unified

> **路径**: `skills/gate-exchange-unified/`

Gate 统一账户：账户总览与模式、借还、借贷与利息记录、可划转额度、杠杆与抵押币设置。涉及写操作时需用户明确确认。

**示例提示词**：
- `查一下我的统一账户总权益和当前模式`
- `统一账户里最多能借多少 USDT？`
- `借 200 USDT，先看最大可借`
- `还清我的 BTC 借款`
- `把 ETH 杠杆设成 5 倍`

---

## 👥 gate-exchange-subaccount

> **路径**: `skills/gate-exchange-subaccount/`

Gate 交易所子账户管理：按 UID 查询状态、列出全部子账户、创建子账户、锁定/解锁。写操作需用户明确确认。

**示例提示词**：
- `显示我所有子账户`
- `子账户 UID 123456 的状态是什么？`
- `创建一个新的子账户`
- `锁定子账户 UID 123456`

---

## 📊 gate-dex-market

> **路径**: `skills/gate-dex-market/`

Gate DEX 行情数据 Skill，使用 OpenAPI 模式通过 AK/SK 认证直接调用 API。提供代币信息、K线数据、排行榜、安全审计等只读查询。

**示例提示词**：
- `查询 BTC 代币信息`
- `显示 ETH 的 K 线数据`
- `最近有什么热门代币？`
- `检查这个代币的安全审计`

---

## 🔄 gate-dex-trade

> **路径**: `skills/gate-dex-trade/`

Gate DEX 交易综合 Skill，支持 MCP + OpenAPI 双模式。智能路由根据环境自动选择最优交易方式，支持跨链与单链 Swap 执行。

**示例提示词**：
- `用 100 USDT 兑换 ETH`
- `把 BNB 换成 PEPE`
- `获取 SOL 换 USDC 的报价`
- `使用 OpenAPI 模式买入代币`

---

## 💼 gate-dex-wallet

> **路径**: `skills/gate-dex-wallet/`

Gate DEX 综合钱包 Skill。统一入口，支持身份认证、资产查询、转账执行、DApp 交互四大模块，根据用户意图路由到具体子模块。

**示例提示词**：
- `登录我的钱包`
- `查看钱包余额`
- `转账 0.1 ETH 到 0x...`
- `将钱包连接到 Uniswap`
- `签名这条消息`

---

## 🔍 gate-info-addresstracker

> **路径**: `skills/gate-info-addresstracker/`

链上地址追踪与分析。提供地址画像、交易历史与资金流向追踪，支持基础查询和深度追踪两种模式，覆盖多链地址。

**示例提示词**：
- `追踪这个地址 0x...`
- `这个地址的持有者是谁？`
- `查看 bc1... 的资金流向`
- `检查地址活动`

---

## 📊 gate-info-coinanalysis

> **路径**: `skills/gate-info-coinanalysis/`

单币种综合分析。并行获取基本面、行情、技术面、新闻和社交情绪数据，由 LLM 汇总为结构化分析报告。

**示例提示词**：
- `分析一下 ETH`
- `SOL 现在怎么样？`
- `BTC 现在值得买吗？`
- `帮我全面分析 DOGE`

---

## ⚖️ gate-info-coincompare

> **路径**: `skills/gate-info-coincompare/`

多币种对比（2–5 个币种）。并行获取各币种行情快照和基本面数据，生成多维度对比表与总结。

**示例提示词**：
- `对比 BTC 和 ETH`
- `SOL 和 AVAX 哪个更好？`
- `对比 BTC、ETH、SOL 和 BNB`
- `DOGE 和 SHIB 有什么区别？`

---

## 🌐 gate-info-marketoverview

> **路径**: `skills/gate-info-marketoverview/`

加密市场总览。并行获取全市场数据、板块排行、DeFi 概览、近期事件和宏观摘要，生成市场简报式报告。

**示例提示词**：
- `今天市场怎么样？`
- `给我一个市场概览`
- `加密市场最近发生了什么？`
- `展示整体市场状况`

---

## 🛡️ gate-info-riskcheck

> **路径**: `skills/gate-info-riskcheck/`

代币与合约风险评估。执行 30+ 项风险检查，包括蜜罐检测、税费分析、持币集中度和名称风险等，生成结构化风险报告。

**示例提示词**：
- `这个代币安全吗？0x...`
- `检查 PEPE 的合约风险`
- `这是蜜罐吗？`
- `这个会不会是 Rug Pull？`

---

## 📉 gate-info-trendanalysis

> **路径**: `skills/gate-info-trendanalysis/`

趋势与技术分析。并行获取 K 线数据、指标历史、多周期信号和行情快照，生成多维度技术分析报告。

**示例提示词**：
- `BTC 技术分析`
- `看一下 ETH 的 RSI 和 MACD`
- `SOL 的趋势如何？`
- `查看 BNB 的支撑和阻力位`

---

## 🏗️ gate-info-defianalysis

> **路径**: `skills/gate-info-defianalysis/`

DeFi 生态分析（Gate-Info MCP）。按意图路由到总览、单协议深挖、收益池、稳定币、跨链桥、交易所链上储备或爆仓热力图等子场景；部分场景支持「先列表后细化」。只读。

**示例提示词**：
- `DeFi 总览和 TVL 前十协议`
- `Uniswap TVL 和成交量`
- `Aave 上 USDC 借贷收益`
- `币安 BTC 储备`
- `BTC 爆仓热力图`

---

## 🗓️ gate-info-macroimpact

> **路径**: `skills/gate-info-macroimpact/`

宏观与加密联动分析（Gate-Info + Gate-News MCP）：并行获取经济日历、宏观指标或摘要、相关新闻、关联币种行情快照。只读。

**示例提示词**：
- `CPI 对 BTC 有什么影响`
- `今天有没有重要宏观数据`
- `美联储决议对加密市场的影响`
- `最新非农和风险资产`

---

## ⛓️ gate-info-tokenonchain

> **路径**: `skills/gate-info-tokenonchain/`

代币级链上分析（Gate-Info MCP）：持币分布、链上活跃度、大额划转等。本版 **不包含** Smart Money / `smart_money` 维度，仅用 holders、activity、transfers。只读。

**示例提示词**：
- `ETH 持币分布`
- `SOL 链上活跃度`
- `BTC 大额转账`
- `ARB 链上综合情况`

---

## 📰 gate-news-briefing

> **路径**: `skills/gate-news-briefing/`

加密新闻简报。并行获取重大事件、热门新闻和社交情绪，生成分层新闻简报。

**示例提示词**：
- `最近加密圈发生了什么？`
- `今天的加密货币头条`
- `市场有什么新动态？`
- `给我最新的加密新闻`

---

## 🗣️ gate-news-communityscan

> **路径**: `skills/gate-news-communityscan/`

社区与社交情绪（Gate-News MCP），当前以 **X/Twitter** 为主：X 讨论检索与量化社交情绪并行。多平台 UGC 未上线时须标明 **仅 X/Crypto Twitter**。只读。

**示例提示词**：
- `大家怎么看 ETH`
- `比特币推特情绪`
- `社区对 ETF 怎么说`
- `今天 SOL 上的 KOL 观点`

---

## 💡 gate-news-eventexplain

> **路径**: `skills/gate-news-eventexplain/`

事件归因与解释。当用户询问价格异动原因时，多步调用追溯事件来源，结合行情和链上数据，输出「事件 → 影响链 → 市场反应」分析报告。

**示例提示词**：
- `BTC 为什么暴跌？`
- `ETH 刚才怎么了？`
- `SOL 为什么在涨？`
- `DOGE 暴跌的原因是什么？`

---

## 📋 gate-news-listing

> **路径**: `skills/gate-news-listing/`

交易所上架/下架追踪。获取交易所上新、下架和维护公告，为高关注度新币补充基本面和行情数据。

**示例提示词**：
- `最近有什么新币上架？`
- `币安这周上了什么币？`
- `查看最近的下架公告`
- `今天有新代币上线吗？`

---

## 🛠️ gate-mcp-installer

> **路径**: `skills/gate-mcp-installer/`

全平台统一安装器，支持 Cursor、Claude Code、Codex 和 OpenClaw/mcporter，一键安装 Gate MCP 与全部 Gate Skills。

**快速开始**：
```bash
# 在仓库根目录执行
bash skills/gate-mcp-installer/scripts/install.sh
```

可选：`--no-skills` 仅安装 MCP；`--mcp main --mcp dex` 等只安装指定 MCP。

---

## 🎁 gate-exchange-referral

> **路径**: `skills/gate-exchange-referral/`

邀请好友活动推荐与规则解读：介绍 Earn Together、助领券、超级返佣等主计划，说明规则与奖励，并引导至官方邀请页。

**示例提示词**：
- `邀请好友活动怎么玩？`
- `Earn Together 规则是什么？`
- `我的邀请链接在哪里？`
- `邀请好友有什么奖励？`

---

## 🗂️ gate-exchange-assets-manager

> **路径**: `skills/gate-exchange-assets-manager/`

L2 复合账户资产管家：多账户余额全景、保证金与爆仓风险、活期/质押收益快照、联盟佣金，以及统一账户借还、抵押与杠杆等写操作（需用户确认）。

**示例提示词**：
- `我所有账户总资产是多少？`
- `我 ETH 仓位的爆仓风险是多少？`
- `总结我的理财和质押收益`
- `我想在统一账户借 USDT`

---

## 🔬 gate-info-research

> **路径**: `skills/gate-info-research/`

Market Research Copilot — L2 复合技能，聚合 Gate-Info 与 Gate-News 只读工具，产出市场简报、单币深挖、多币对比、趋势与事件归因及风险检查（不涉及交易）。

**示例提示词**：
- `帮我做一份市场研究简报`
- `对比 BTC 和 ETH 基本面与风险`
- `为什么 SOL 今天大涨？`
- `今日加密市场概览`

---

## 🎉 gate-exchange-welfare

> **路径**: `skills/gate-exchange-welfare/`

福利中心新用户任务与奖励，基于 MCP 真实数据，不得编造奖励金额；区分新老用户引导。

**示例提示词**：
- `有哪些福利任务可以做？`
- `新用户奖励怎么领取？`
- `新用户有什么福利？`

---

## 🌊 gate-exchange-launchpool

> **路径**: `skills/gate-exchange-launchpool/`

LaunchPool：浏览项目、质押与赎回、质押记录与空投奖励记录。

**示例提示词**：
- `现在有哪些 LaunchPool 项目？`
- `参与 LaunchPool 质押 X 项目`
- `我的 LaunchPool 空投记录`
- `从 LaunchPool 赎回质押资产`

---

## 🪪 gate-exchange-kyc

> **路径**: `skills/gate-exchange-kyc/`

引导用户前往 Gate KYC 门户完成身份验证；不在对话内完成认证流程。

**示例提示词**：
- `在哪里完成 KYC？`
- `为什么我无法提币？`
- `身份验证页面链接`

---

## 💰 gate-exchange-collateralloan

> **路径**: `skills/gate-exchange-collateralloan/`

多币抵押借贷：活期/定期借款、还款、追加/赎回抵押品（写操作需明确确认）。

**示例提示词**：
- `我的抵押借贷订单`
- `部分还款`
- `给订单追加抵押`
- `当前借款利率和 LTV`

---

## 🎯 gate-exchange-activitycenter

> **路径**: `skills/gate-exchange-activitycenter/`

活动中心：平台活动类型、热门推荐、活动列表与我的活动入口（交易赛、空投、新人活动等）。

**示例提示词**：
- `现在有哪些平台活动？`
- `推荐交易竞赛类活动`
- `我的活动入口`

---

## 💳 gate-exchange-pay

> **路径**: `skills/gate-exchange-pay/`

Gate Pay 支付执行 Skill。完成商户支付、满足支付优先流程（如 HTTP 402）并输出收据。需先完成 Gate 支付授权。

**示例提示词**：
- `用 Gate Pay 支付`
- `完成这笔订单的支付`
- `帮我支付这个订单`

---

## 快速开始

### 前置要求

- 支持 skill 加载的 AI Agent 环境（例如 Cursor、OpenClaw）
- Node.js 与 npm

### 配置步骤

使用统一安装器 `gate-mcp-installer`，自动检测你的环境（Cursor、Claude Code、Codex 或 OpenClaw）：

```bash
# 在仓库根目录执行
bash skills/gate-mcp-installer/scripts/install.sh
```

或直接向 AI 助手说：
```
帮我安装 Gate MCP
```

仅安装 MCP：`bash skills/gate-mcp-installer/scripts/install.sh --no-skills`

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
    ├── gate-dex-market/                # DEX 行情数据 skill（OpenAPI 模式）
    ├── gate-dex-trade/                 # DEX 交易 skill（MCP + OpenAPI 双模式）
    ├── gate-dex-wallet/                # DEX 综合钱包 skill
    ├── gate-exchange-affiliate/        # 交易所联盟/合伙人计划
    ├── gate-exchange-alpha/            # Alpha 代币发现、行情与账户
    ├── gate-exchange-assets/           # 交易所资产/余额查询（只读）
    ├── gate-exchange-coupon/           # 优惠券/券码管理与查询
    ├── gate-exchange-crossex/          # CrossEx 跨所交易操作
    ├── gate-exchange-dual/             # 双币理财查询（只读）
    ├── gate-exchange-flashswap/        # 闪兑查询：币对、限额、历史
    ├── gate-exchange-futures/          # 合约交易 skill
    ├── gate-exchange-marketanalysis/   # 市场盘口分析 skill
    ├── gate-exchange-pay/              # Gate Pay 支付执行 skill
    ├── gate-exchange-simpleearn/       # Simple Earn（活期理财）查询：持仓、利息、利率（只读）
    ├── gate-exchange-smallbalance/     # 粉尘/小额资产：列表、兑 GT、历史
    ├── gate-exchange-spot/             # 现货交易 skill
    ├── gate-exchange-staking/          # 理财/质押查询（只读）
    ├── gate-exchange-autoinvest/       # Earn 极速定投（DCA）：计划、记录、现货与 Uni 上下文
    ├── gate-exchange-subaccount/       # 子账户管理：列表、创建、锁定/解锁
    ├── gate-exchange-tradfi/           # TradFi 查询：订单、持仓、行情、资产、MT5（只读）
    ├── gate-exchange-trading/          # 端到端交易（判断 → 执行）
    ├── gate-exchange-transfer/         # 内部划转（账户间转移资金）
    ├── gate-exchange-unified/          # 统一账户：借还、杠杆、抵押币
    ├── gate-exchange-vipfee/           # VIP 等级与手续费率查询
    ├── gate-info-addresstracker/       # 链上地址追踪 skill
    ├── gate-info-coinanalysis/         # 单币种分析 skill
    ├── gate-info-coincompare/          # 多币种对比 skill
    ├── gate-info-defianalysis/         # DeFi TVL、协议、收益、桥、储备、爆仓 skill
    ├── gate-info-liveroomlocation/     # 直播与回放列表 skill
    ├── gate-info-macroimpact/          # 宏观日历、指标、新闻与行情联动 skill
    ├── gate-info-marketoverview/       # 市场总览 skill
    ├── gate-info-riskcheck/            # 代币风险评估 skill
    ├── gate-info-tokenonchain/         # 代币链上持币、活跃度、大额划转 skill
    ├── gate-info-trendanalysis/        # 趋势与技术分析 skill
    ├── gate-news-briefing/             # 新闻简报 skill
    ├── gate-news-communityscan/       # 社区 / X 情绪 skill
    ├── gate-news-eventexplain/         # 事件解释 skill
    ├── gate-news-listing/              # 上架/下架追踪 skill
    └── gate-mcp-installer/             # 全平台统一 MCP + Skills 安装 skill（Cursor、Claude Code、Codex、OpenClaw）
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

Gate Skills 仅为信息工具。所有输出均按"现状"和"可用"基础提供，不构成任何明示或暗示的保证。其内容不构成投资、金融、交易或任何其他形式的建议，也不构成买入、卖出或持有任何资产的推荐。数字资产价格具有高风险和高波动性。你需要对自己的投资决策负责。历史表现不代表未来结果。进行任何投资前，请咨询独立的专业财务顾问。
