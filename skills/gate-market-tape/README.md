# Gate.io Market Intelligence (gate-market-tape)

Gate.io 行情分析智能助手，一站式市场分析技能。所有场景的 **MCP 调用顺序与输出格式** 在 `references/scenarios.md` 中统一约定，实现时按该文档执行即可与文档一致。

## Overview

整合 7 大分析场景：流动性、动能、爆仓、套利、基差、操控风险、订单簿解读；支持现货/合约智能识别，依赖 Gate MCP 拉取行情与深度数据。

## Core Capabilities

### 📊 分析场景

| Case | 场景 | 触发词示例 | 市场 |
|------|------|-----------|------|
| 1 | 流动性分析 | "ETH流动性如何" | 现货/合约 |
| 2 | 动能判断 | "BTC多头强还是空头强" | 现货/合约 |
| 3 | 爆仓监控 | "最近爆仓情况" | 合约 |
| 4 | 费率套利 | "有套利机会吗" | 合约+现货 |
| 5 | 基差监控 | "基差怎么样" | 合约+现货 |
| 6 | 操控风险 | "这币容易操控吗" | 现货为主 |
| 7 | 订单簿解读 | "解释订单簿" | 现货/合约 |

## Prerequisites

- **Gate MCP** 已配置并可用（否则无法拉取订单簿、Ticker、K 线等）。若未配置，可参考仓库中的 `gate-mcp-installer` 技能。

## Architecture

```
┌─────────────────────────────────────────────┐
│         gate-market-tape                    │
│         行情分析智能助手                      │
└──────────────────┬──────────────────────────┘
                   │
         ┌─────────▼─────────┐
         │    意图识别层      │  Case 1～7
         │  Intent Router    │
         └─────────┬─────────┘
                   │
     ┌─────────────┼─────────────┐
     │             │             │
┌────▼────┐  ┌────▼────┐  ┌────▼────┐
│ 现货分析 │  │ 合约分析 │  │ 跨市场  │
│ 流动性   │  │ 爆仓    │  │ 套利    │
│ 动能/操控│  │ 流动性  │  │ 基差    │
│ 订单簿  │  │ 动能    │  │         │
└────┬────┘  └────┬────┘  └────┬────┘
     └─────────────┼─────────────┘
                   │
         ┌─────────▼─────────┐
         │   Gate MCP        │  调用顺序见 references/scenarios.md
         ├───────────────────┤
         │ list_order_book   │  list_tickers  list_candlesticks
         │ list_trades       │  list_futures_*  list_futures_liq_orders
         └───────────────────┘
```

## Usage

### 流动性分析
```
User: "ETH的流动性如何"
Bot: [分析订单簿深度、成交量、滑点风险]
```

### 动能判断
```
User: "BTC近24h多头厉害还是空头厉害"
Bot: [统计买卖成交占比、评估可持续性]
```

### 爆仓监控
```
User: "最近爆仓情况"
Bot: [扫描异常爆仓、识别多空清洗、插针行情]
```

### 套利扫描
```
User: "有没有套利机会"
Bot: [筛选高费率、计算年化、评估深度]
```

### 基差监控
```
User: "BTC基差怎么样"
Bot: [计算期现价差、判断趋势]
```

### 操控风险
```
User: "这个币容易被操控吗"
Bot: [计算深度/成交比、追踪大单]
```

### 订单簿解读
```
User: "帮我解释一下订单簿"
Bot: [教学式解读 + 实时数据示例]
```

## Trigger Phrases

### Case 1: 流动性
- "流动性如何"
- "深度怎么样"
- "滑点大吗"

### Case 2: 动能
- "多头强还是空头强"
- "买盘卖盘情况"
- "动能可持续吗"

### Case 3: 爆仓
- "爆仓情况"
- "哪些币爆得多"
- "多头清洗"

### Case 4: 套利
- "套利机会"
- "费率异常"
- "资金费率"

### Case 5: 基差
- "基差怎么样"
- "期现价差"
- "溢价"

### Case 6: 操控
- "这个币深度和成交比怎么样"
- "容易操控吗"
- "有主力吗"

### Case 7: 订单簿
- "解释订单簿示例"
- "怎么看盘口"

## MCP 调用规范速查

| Case | 场景     | MCP 调用顺序 |
|------|----------|----------------|
| 1 | 流动性   | list_order_book → list_candlesticks → list_tickers（永续/合约则用合约接口） |
| 2 | 动能     | list_trades → list_tickers → list_candlesticks → list_order_book → list_futures_funding_rate（合约则用合约接口） |
| 3 | 爆仓     | list_futures_liq_orders → list_futures_candlesticks → list_futures_tickers |
| 4 | 套利     | list_futures_tickers → list_futures_funding_rate → list_tickers → list_order_book |
| 5 | 基差     | list_tickers(现货) → list_futures_tickers → list_futures_premium_index |
| 6 | 操控风险 | list_order_book → list_tickers → list_trades |
| 7 | 订单簿   | list_order_book(limit=10) → list_tickers |

详细参数、必取字段与输出格式见 **`references/scenarios.md`**。

## Key Features

- **智能识别**: 自动区分现货/合约场景
- **规范调用**: 各场景 MCP 调用顺序与输出格式在 scenarios 中统一约定
- **多维分析**: 7 大场景覆盖流动性、动能、爆仓、套利、基差、操控、订单簿
- **量化指标**: 滑点、深度比、买盘占比等有明确公式与阈值
- **风险提示**: 高风险情况醒目标注；分析仅供参考，不构成投资建议

## File Structure

```
gate-market-tape/
├── README.md           # 本文件
├── SKILL.md            # Agent 执行逻辑、Workflow、Report Template
├── CHANGELOG.md
└── references/
    └── scenarios.md    # 各场景 MCP 调用规范、示例与输出约定
```
