---
name: gate-exchange-Marketanalysis
version: "2026.3.5-1"
updated: "2026-03-05"
description: "The market analysis function of Gate Exchange — liquidity, momentum, liquidation, funding arbitrage, basis, manipulation risk, order book explainer. Use when the user asks about liquidity, depth, slippage, buy/sell pressure, liquidation, funding rate arbitrage, basis/premium, manipulation risk, or order book explanation. Trigger phrases: liquidity, depth, slippage, momentum, buy/sell pressure, liquidation, squeeze, funding rate, arbitrage, basis, premium, manipulation, order book, spread, or equivalent in other languages (e.g. 流动性, 深度, 滑点, 动能, 爆仓, 套利, 基差, 操控, 订单簿)."
---

# gate-exchange-MarketAnalysis

**EN:** Market tape analysis covering seven scenarios: liquidity, momentum, liquidation monitoring, funding arbitrage, basis monitoring, manipulation risk, and order book explanation. This skill provides structured market insights by orchestrating Gate MCP tools; call order and judgment logic are defined in `references/scenarios.md`.

**中文：** 行情分析覆盖七大场景：流动性、动能、爆仓监控、资金费率套利、基差监控、操控风险、订单簿解读。本技能通过 Gate MCP 按序调用并输出结构化结论；调用顺序与判断逻辑见 `references/scenarios.md`。

**Language / 语言：** Reports default to 中文 with English technical terms retained; documentation below is bilingual. 报告默认中文、术语保留英文；下文文档中英双语。

---

## Sub-Modules / 子模块

| Module / 模块 | Purpose / 用途 | Document |
|--------|---------|----------|
| **Liquidity** 流动性 | Order book depth, 24h vs 30d volume, slippage 订单簿深度、24h/30日量、滑点 | `references/scenarios.md` (Case 1) |
| **Momentum** 动能 | Buy vs sell share, funding rate 买卖占比、资金费率 | `references/scenarios.md` (Case 2) |
| **Liquidation** 爆仓 | 1h liq vs baseline, squeeze, wicks 1h 爆仓、清洗、插针 | `references/scenarios.md` (Case 3) |
| **Funding arbitrage** 费率套利 | Rate + volume screen, spot–futures spread 费率与成交量筛选、期现价差 | `references/scenarios.md` (Case 4) |
| **Basis** 基差 | Spot–futures price, premium index 期现价、溢价指数 | `references/scenarios.md` (Case 5) |
| **Manipulation risk** 操控风险 | Depth/volume ratio, large orders 深度/成交比、大单 | `references/scenarios.md` (Case 6) |
| **Order book explainer** 订单簿解读 | Bids/asks, spread, depth 买卖盘、价差、深度 | `references/scenarios.md` (Case 7) |

---

## Routing Rules / 路由规则

**EN:** Determine which module (case) to run based on user intent.

**中文：** 根据用户意图确定执行哪个模块（Case）。

| User Intent / 用户意图 | Keywords / 关键词 | Action / 动作 |
|-------------|----------------------|--------|
| Liquidity / depth 流动性/深度 | 流动性, 深度, 滑点, liquidity, depth, slippage | Read Case 1, follow MCP order（永续/合约用合约接口） |
| Momentum 动能 | 多头空头, 动能, 可持续, buy vs sell, momentum | Read Case 2, follow MCP order |
| Liquidation 爆仓 | 爆仓, 清洗, 插针, liquidation, squeeze | Read Case 3（仅合约） |
| Funding arbitrage 套利 | 套利, 费率异常, arbitrage, funding rate | Read Case 4 |
| Basis 基差 | 基差, 期现价差, basis, premium | Read Case 5 |
| Manipulation risk 操控风险 | 深度和成交比, 容易操控吗, manipulation | Read Case 6（按关键词选现货/合约） |
| Order book explainer 订单簿 | 解释订单簿, 盘口, order book, spread | Read Case 7 |

---

## Execution / 执行步骤

1. **Match user intent** 匹配用户意图 → 对照上表确定 Case 与市场类型（现货/合约）
2. **Read** 阅读 `references/scenarios.md` 中对应 Case 的 MCP 调用顺序与必取字段
3. **Call Gate MCP** 按该 Case 顺序调用 Gate MCP
4. **Apply judgment logic** 按 scenarios 中的阈值与标记规则做判断
5. **Output the report** 按该 Case 的 Report Template 输出报告
6. **Suggest related actions** 建议后续提问（如：如需基差可问「XXX 基差怎么样」）

---

## Domain Knowledge (short) / 领域知识摘要

- **Spot vs futures 现货/合约：** “perpetual”“contract”“future”“perp” → 用合约 MCP；未指明则现货。
- **Liquidity (Case 1)：** 深度 &lt; 10 档 → 流动性低；24h 量 &lt; 30 日均 → 冷门对；滑点率 &gt; 0.5% → 滑点风险高。
- **Momentum (Case 2)：** 买盘占比 &gt; 70% → 买盘强势；24h 量 &gt; 30 日均 → 活跃；资金费率符号 + 订单簿前 10 档辅助多空。
- **Liquidation (Case 3)：** 1h 爆仓 &gt; 日均×3 → 异常；单边爆仓 &gt; 80% → 多头/空头清洗；价格恢复 → 插针。
- **Arbitrage (Case 4)：** |rate| &gt; 0.05% 且 24h vol &gt; $10M → 候选；期现价差 &gt; 0.2% → 加分；深度过薄 → 排除。
- **Basis (Case 5)：** 当前基差与历史比较；基差走阔/收窄表示情绪变化。
- **Manipulation (Case 6)：** 前 10 档深度/24h 量 &lt; 0.5% → 深度薄；连续同向大单 → 可能有主力在控盘；默认现货，永续/合约用合约接口。
- **Order book (Case 7)：** 展示买卖盘示例、结合最新价解释价差与深度。

---

## Important Notes / 重要说明

- All analysis is read-only — no trading. 仅读分析，不执行交易。
- Gate MCP must be configured（须先配置 Gate MCP，可选用 `gate-mcp-installer` 技能）.
- MCP call order and output format are in `references/scenarios.md`；follow for consistent behavior. 调用顺序与输出格式以 scenarios 为准，保持一致。
- Reports default to 中文 with English technical terms. 报告默认中文，技术术语保留英文。
- Always include a disclaimer: 分析仅供参考，不构成投资建议。analysis is data-based, not investment advice.
