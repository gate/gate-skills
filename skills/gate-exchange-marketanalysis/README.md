# gate-exchange-MarketAnalysis

**Language / 语言：** This document is bilingual (EN & 中文). 本文档支持中英双语。

---

## Overview / 概述

**EN:** An AI Agent skill that provides market analysis on [Gate.io](https://www.gate.io), covering liquidity, momentum, liquidation monitoring, funding rate arbitrage, basis (spot–futures) monitoring, manipulation risk, and order book explanation. All scenarios use a defined **MCP call order and output format** in `references/scenarios.md`.

**中文：** Gate Exchange 行情分析技能，覆盖流动性、动能、爆仓监控、资金费率套利、基差（期现）监控、操控风险与订单簿解读。各场景的 **MCP 调用顺序与输出格式** 在 `references/scenarios.md` 中统一约定。

---

### Core Capabilities / 核心能力

| Capability / 能力 | Description / 说明 | Example / 示例 |
|------------|-------------|---------|
| **Liquidity analysis** 流动性分析 | Order book depth, 24h vs 30d volume, slippage 订单簿深度、24h/30日量、滑点 | "How is ETH liquidity?" / "ETH 流动性如何" |
| **Momentum** 动能 | Buy vs sell share, funding rate 买卖占比、资金费率 | "Is BTC more long or short?" / "BTC 多头还是空头强" |
| **Liquidation monitoring** 爆仓监控 | 1h liq vs baseline, squeeze, wicks 1h 爆仓、清洗、插针 | "Recent liquidations?" / "最近爆仓情况" |
| **Funding arbitrage** 费率套利 | Rate + volume, spot–futures spread 费率与成交量、期现价差 | "Any arbitrage opportunities?" / "有套利机会吗" |
| **Basis monitoring** 基差监控 | Spot–futures price, premium index 期现价、溢价指数 | "What is the basis for BTC?" / "BTC 基差怎么样" |
| **Manipulation risk** 操控风险 | Depth/volume ratio, large orders 深度/成交比、大单 | "Easy to manipulate?" / "容易操控吗" |
| **Order book explainer** 订单簿解读 | Bids/asks, spread, depth 买卖盘、价差、深度 | "Explain the order book" / "解释订单簿" |

> 📊 **Seven scenarios / 七大场景：** Ask about liquidity, momentum, liquidation, arbitrage, basis, manipulation risk, or order book; the skill routes to the right case. 询问流动性、动能、爆仓、套利、基差、操控风险或订单簿时，技能会路由到对应 Case。

---

## Architecture / 架构

```
Natural Language Input / 自然语言输入
    ↓
Intent Routing (Case 1–7, spot vs futures) / 意图路由（现货/合约）
    ↓
Gate MCP Tools
    ├── list_order_book / list_futures_order_book
    ├── list_tickers / list_futures_tickers
    ├── list_candlesticks / list_futures_candlesticks
    ├── list_trades / list_futures_funding_rate
    ├── list_futures_liq_orders (when available)
    └── list_futures_premium_index
    ↓
Analysis & Judgment Logic / 分析与判断逻辑
    ↓
Structured Report → Natural language response / 结构化报告 → 自然语言回复
```

**Sub-Modules / 子模块：** `references/scenarios.md` — MCP call order, parameters, required fields, report templates per case. MCP 调用顺序、参数、必取字段、各 Case 报告模板。

---

## Agent Use Cases / 使用场景

### 1. Liquidity check / 流动性查询
> "How is ETH liquidity?" / "当前 ETH 的流动性如何"

Depth levels, 24h vs 30d volume, slippage; liquidity rating. 永续/合约用合约深度与 K 线。深度档位、24h/30日量、滑点；流动性评级。

### 2. Momentum (buy vs sell) / 动能（多空）
> "Is BTC more long or short in 24h?" / "BTC 近 24h 多头还是空头强"

Trades → buy/sell share; tickers, candlesticks, order book top 10, funding rate. 成交→买卖占比；ticker、K 线、订单簿前 10 档、资金费率。

### 3. Liquidation monitoring / 爆仓监控
> "Recent liquidations?" / "最近爆仓情况"

Liquidation orders (if MCP provides), candlesticks, tickers; anomaly and squeeze labels. 爆仓订单（若 MCP 提供）、K 线、ticker；异常与清洗标记。

### 4. Funding arbitrage scan / 费率套利扫描
> "Any arbitrage opportunities?" / "费率异常的币"

Screen by |rate| and volume; spot tickers and order book; exclude thin books. 按费率和成交量筛选；现货 ticker 与订单簿；排除深度过薄。

### 5. Basis (spot–futures) / 基差（期现）
> "What is the basis for BTC?" / "基差怎么样"

Spot and futures tickers, premium index; current vs history, widening/narrowing. 现货与合约 ticker、溢价指数；当前与历史、走阔/收窄。

### 6. Manipulation risk / 操控风险
> "Is this coin easy to manipulate?" / "深度和成交比怎么样"

Depth ratio (top 10 / 24h volume); large and consecutive same-side trades. 深度比（前 10 档/24h 量）；大单与连续同向成交。

### 7. Order book explainer / 订单簿解读
> "Explain the order book" / "解释订单簿示例"

Live order book (e.g. limit=10) + ticker; explain bids/asks, spread, depth. 实时订单簿（如 limit=10）+ ticker；解释买卖盘、价差、深度。

---

## Quick Start / 快速开始

### Prerequisites / 前置条件

1. Gate MCP configured and connected（Gate MCP 已配置并连接，可选用 `gate-mcp-installer` 技能）.
2. No extra dependencies. 无其他依赖。

### Example Prompts / 示例提问

```
# Liquidity 流动性
"How is ETH liquidity?"   "ETH 流动性如何"

# Momentum 动能
"BTC 24h more long or short, sustainable?"   "BTC 多头强还是空头强，可持续吗"

# Liquidation 爆仓
"Recent liquidations?"   "最近爆仓情况"

# Arbitrage 套利
"Any funding rate arbitrage opportunities?"   "有套利机会吗"

# Basis 基差
"What is the basis for ETH?"   "基差怎么样"

# Manipulation 操控
"Is PEPE easy to manipulate?"   "这个币容易操控吗"

# Order book 订单簿
"Explain the order book with an example"   "解释订单簿示例"
```

See `references/scenarios.md` for full MCP call order and report templates. 完整 MCP 调用顺序与报告模板见 `references/scenarios.md`。

---

## File Structure / 文件结构

```
gate-exchange-MarketAnalysis/
├── README.md                          # This file / 本文件
├── SKILL.md                           # Skill routing and instructions / 技能路由与说明
├── CHANGELOG.md                       # Version history / 版本历史
└── references/
    ├── scenarios.md                   # MCP call order, judgment logic, report templates / 调用顺序、判断逻辑、报告模板
    └── case-test-report.md            # Optional: simulation test summary / 可选：模拟测试摘要
```

---

## Security / 安全

- No external scripts or executable code. 无外部脚本或可执行代码。
- Uses Gate MCP tools only — no direct API calls. 仅使用 Gate MCP 工具，不直连 API。
- No credential handling or storage. 不处理或存储凭证。
- Read-only market data analysis, no trading operations. 仅读行情分析，不执行交易。
- No file system writes. 不写文件系统。
- No data collection, telemetry, or analytics. 无数据采集、遥测或统计。

## License / 许可

MIT
