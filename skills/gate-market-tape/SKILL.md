---
name: gate-market-tape
version: "2026.3.5-2"
updated: "2026-03-05"
description: "Gate.io 行情分析智能助手。Use this skill whenever the user asks about market analysis, liquidity, momentum, liquidation, funding rate, basis, manipulation risk, or order book explanation. Trigger phrases include '流动性', '动能', '爆仓', '套利', '费率', '基差', '操控', '订单簿', '深度', 'liquidity', 'momentum', 'liquidation', 'funding rate', 'basis', or any request involving market analysis."
---

# Gate.io Market Intelligence (gate-market-tape)

行情分析智能助手，覆盖流动性、动能、爆仓、套利、基差、操控风险、订单簿解读等 7 大分析场景。**前置条件**：Gate MCP 已配置并可用；各场景 MCP 调用顺序与输出格式以 `references/scenarios.md` 为准。

## Domain Knowledge

### 现货 vs 合约识别

| 关键词 | 识别为 |
|--------|--------|
| 永续、合约、future、perp | 合约接口 |
| 现货、spot | 现货接口 |
| 无明确指定 | 默认现货 |

### 流动性评估标准

| 指标 | 健康值 | 警戒值 |
|------|--------|--------|
| 订单簿深度 | > 20 档 | < 10 档 |
| 24h 成交量 | > 30日均值 | < 30日均值 |
| 买卖价差 | < 0.1% | > 0.5% |

### 动能评估标准

| 指标 | 说明 |
|------|------|
| 买盘占比 > 70% | 买盘强势 |
| 卖盘占比 > 70% | 卖盘强势 |
| 成交量 > 30日均值 | 市场活跃 |

### 滑点计算公式

```
滑点率 = 2 × (ask1 - bid1) / (ask1 + bid1) × 100%
```

### 深度/成交比

```
深度比 = 前10档深度总量 / 24h成交量
深度比 < 0.5% → 深度薄，易被操控
```

## Workflow

When the user asks about market analysis, first identify the intent and market type.

### Step 0: 意图识别

| Case | 触发词 | 市场类型 |
|------|--------|----------|
| 1 | 流动性、深度怎么样 | 现货/合约 |
| 2 | 多头空头、动能、强势 | 现货/合约 |
| 3 | 爆仓、清洗、插针 | 仅合约 |
| 4 | 套利、费率异常 | 合约+现货 |
| 5 | 基差、期现价差 | 合约+现货 |
| 6 | 操控、深度成交比 | 现货为主 |
| 7 | 解释订单簿 | 现货/合约 |

Key data to extract:
- 场景编号 (1-7)
- 市场类型 (spot/futures)
- 币种/交易对

**MCP 调用速查**（详见 `references/scenarios.md`）：

| Case | 场景 | MCP 顺序 |
|------|------|----------|
| 1 | 流动性 | list_order_book → list_candlesticks → list_tickers（用户提永续/合约则用合约接口） |
| 2 | 动能 | list_trades → list_tickers → list_candlesticks → list_order_book → list_futures_funding_rate（合约则用合约接口） |
| 3 | 爆仓 | list_futures_liq_orders → list_futures_candlesticks → list_futures_tickers |
| 4 | 套利 | list_futures_tickers → list_futures_funding_rate → list_tickers → list_order_book |
| 5 | 基差 | list_tickers → list_futures_tickers → list_futures_premium_index |
| 6 | 操控 | list_order_book → list_tickers → list_trades |
| 7 | 订单簿 | list_order_book(limit=10) → list_tickers |

---

## Case 1: 流动性分析

**触发词**: "当前 ETH 的流动性如何"、"深度怎么样"、"滑点大吗"

**接口**：`get_spot_order_book` → `get_spot_candlesticks` → `get_spot_tickers`。当用户提及**永续、合约**等词语时，识别为合约场景，改用合约接口（`get_futures_order_book` → `get_futures_candlesticks` → `get_futures_tickers`）。

**判断逻辑**：
- asks/bids 深度 &lt; 10 档 → 标记「流动性低」
- 24h 成交量 &lt; 30 日成交量均值 → 标记「冷门对」
- `2×(ask1−bid1)/(bid1+ask1) > 0.5%` → 标记「滑点风险高」

输出须包含核心指标表、流动性评级(1～5⭐)、建议。

### Workflow

1. Call `get_spot_order_book` / `get_futures_order_book` (MCP: `list_order_book` / `list_futures_order_book`) with:
   - `currency_pair` / `contract` + `settle`: 交易对
   - `limit`: 20

   Key data to extract:
   - asks/bids 档位数量（深度级数）
   - 前 10 档深度总量

2. Call `get_spot_candlesticks` / `get_futures_candlesticks` (MCP: `list_candlesticks` / `list_futures_candlesticks`) with:
   - `interval`: `1d`
   - `limit`: 30

   Key data to extract:
   - 30 日成交量均值
   - 24h 成交量

3. Call `get_spot_tickers` / `get_futures_tickers` (MCP: `list_tickers` / `list_futures_tickers`)

   Key data to extract:
   - `last`: 最新价
   - 24h 成交量

4. **判断逻辑**（与上一致）:
   - asks/bids &lt; 10 档 → 🔴 流动性低
   - 24h 成交量 &lt; 30 日均值 → 🟡 冷门对
   - 滑点率 = 2×(ask1−bid1)/(bid1+ask1) &gt; 0.5% → 🔴 滑点风险高
   - 全部正常 → 🟢 流动性良好

---

## Case 2: 动能判断

**触发词**: "BTC 近 24h 多头厉害还是空头厉害，可持续吗"、"买盘卖盘"、"动能"

**接口**：`get_spot_trades` → `get_spot_tickers` → `get_spot_candlesticks` → `get_spot_order_book` → `get_futures_funding_rate`。若用户询问**合约**，则选用合约接口（get_futures_trades / get_futures_tickers / get_futures_candlesticks / get_futures_order_book / get_futures_funding_rate）。

**判断逻辑**：
- 24h 中 buy 占比 &gt; 70% → 标记「买盘强势」
- 24h 成交量 &gt; 30 日日均成交量 → 标记「活跃」
- 资金费率为正/负 → 多头/空头占优
- 订单簿前 10 档查看多空订单数量，辅助多空判断

输出须包含多空力量表、动能方向、可持续性、分析说明。

### Workflow

1. Call `get_spot_trades` / `get_futures_trades` (MCP: `list_trades`) with:
   - `currency_pair` / `contract` + `settle`: 交易对
   - `limit`: 1000 (或按时间筛选 24h)

   Key data to extract:
   - 买入/卖出成交笔数或金额
   - 买盘占比 = buy_volume / total_volume

2. Call `get_spot_tickers` / `get_futures_tickers` (MCP: `list_tickers`)

   Key data to extract:
   - 24h 成交量、24h 涨跌幅

3. Call `get_spot_candlesticks` / `get_futures_candlesticks` (MCP: `list_candlesticks`) with:
   - `interval`: `1d`, `limit`: 30

   Key data to extract:
   - 30 日日均成交量

4. Call `get_spot_order_book` / `get_futures_order_book` (MCP: `list_order_book`)

   Key data to extract:
   - 前 10 档买单与卖单数量/深度，用于多空对比

5. Call `get_futures_funding_rate`（若为合约或需费率信号）

   Key data to extract:
   - 当前资金费率；正 → 多头占优，负 → 空头占优

6. **判断逻辑**:
   - 买盘 &gt; 70% → 📈 买盘强势；卖盘 &gt; 70% → 📉 卖盘强势
   - 24h 成交量 &gt; 30 日均值 → 🔥 活跃；&lt; → 😴 冷淡
   - 资金费率 + 订单簿前 10 档多空量 → 综合多空方向与可持续性

---

## Case 3: 爆仓异常监控

**触发词**: "最近爆仓情况"、"哪些币爆得多"、"清洗"、"插针"

**接口**：`list_futures_liq_orders` → `get_futures_candlesticks` → `get_futures_tickers`

**判断逻辑**：
- 1h 爆仓量 &gt; 日均 × 3 → 标记「异常」
- 爆仓方向集中 &gt; 80%（多头或空头）→ 标记「多头清洗」或「空头清洗」
- 价格已恢复（相对插针低/高点）→ 标记「插针行情」

输出须包含全市场概览表、异常合约表。

### Workflow

1. Call `list_futures_liq_orders` (MCP: 同名) with:
   - `settle`: `usdt`
   - `from` / `to`: 最近 1h（及可选 24h 用于日均基准）

   Key data to extract:
   - 按合约聚合爆仓量；多头爆仓 (size&gt;0)、空头爆仓 (size&lt;0)

2. Call `get_futures_candlesticks` (MCP: `list_futures_candlesticks`) with:
   - `settle`, `contract`, `interval`: 如 5m, `limit`: 12

   Key data to extract:
   - 爆仓时段价格、当前价、价格恢复程度

3. Call `get_futures_tickers` (MCP: `list_futures_tickers`)

   Key data to extract:
   - 当前价格、24h 涨跌

4. **判断逻辑**:
   - 1h 爆仓 &gt; 日均×3 → 🔴 爆仓异常
   - 爆仓方向集中 &gt; 80% → 📉 多头清洗 或 📈 空头清洗
   - 价格已恢复 → 📌 插针行情

---

## Case 4: 资金费率套利扫描

**触发词**: "现在有没有套利机会"、"费率异常的币"、"资金费率"

**接口**：`get_futures_tickers` → `get_futures_funding_rate` → `get_spot_tickers` → `get_spot_order_book`

**判断逻辑**：
- \|rate\| &gt; 0.05% 且 24h vol &gt; $10M → 进入候选
- 现货合约价差 &gt; 0.2% → 加分
- book depth 太薄 → 排除

输出须包含套利机会表、策略说明、风险提示。

### Workflow

1. Call `get_futures_tickers` (MCP: `list_futures_tickers`) with `settle`: `usdt`

   Key data to extract:
   - 所有合约费率、24h 成交量；筛选 \|rate\|&gt;0.05% 且 vol&gt;$10M

2. Call `get_futures_funding_rate`（对候选或全市场）获取费率明细

3. For each candidate, Call `get_spot_tickers` (MCP: `list_tickers`)

   Key data to extract:
   - 现货价格；计算现货与合约价差

4. For top candidates, Call `get_spot_order_book` (MCP: `list_order_book`)

   Key data to extract:
   - 订单簿深度；深度太薄则排除

5. **判断逻辑**:
   - \|rate\| &gt; 0.05% 且 24h vol &gt; $10M → 候选
   - 现货合约价差 &gt; 0.2% → 加分
   - 深度太薄 → 排除
   - rate &gt; 0 → 正套（空合约+多现货）；rate &lt; 0 → 反套（多合约+空现货）

---

## Case 5: 现货 vs 合约基差监控

**触发词**: "基差怎么样"、"期现价差"、"溢价"

**接口**：`get_spot_tickers` → `get_futures_tickers` → `get_futures_premium_index`

**判断逻辑**：
- 当前基差 vs 历史均值偏离度
- 基差走阔/收窄趋势判断

输出须包含基差数据表、分析结论、建议。

### Workflow

1. Call `get_spot_tickers` (MCP: `list_tickers`)

   Key data to extract:
   - 现货价格

2. Call `get_futures_tickers` (MCP: `list_futures_tickers`) with `settle`: `usdt`

   Key data to extract:
   - 合约价格、mark_price、index_price

3. Call `get_futures_premium_index` (MCP: 同名或等价) with `settle`, `contract`

   Key data to extract:
   - premium_index；若有历史则用于均值与偏离度

4. **计算与判断**:
   - 基差 = 合约价 − 现货价；基差率 = 基差/现货价 × 100%
   - 当前基差与历史均值比较 → 偏离度
   - 基差走阔 → 情绪升温；基差收窄 → 回归均值

---

## Case 6: 币种操控风险分析

**触发词**: "这个币深度和成交比怎么样"、"容易操控吗"、"有主力吗"

**接口**：`get_spot_order_book` → `get_spot_tickers` → `get_spot_trades`

**判断逻辑**：
- 前 10 档深度总量 / 24h volume &lt; 0.5% → 「深度薄」
- 24h trades 中有连续同方向大单 → 「可能有主力在控盘」

输出须包含深度分析表、大单追踪、操控风险结论。

### Workflow

1. Call `get_spot_order_book` (MCP: `list_order_book`) with:
   - `currency_pair`: 交易对（如 PEPE_USDT）
   - `limit`: 20

   Key data to extract:
   - 前 10 档买单深度总量
   - 前 10 档卖单深度总量

2. Call `get_spot_tickers` (MCP: `list_tickers`)，同上 `currency_pair`

   Key data to extract:
   - 24h 成交量（quoteVolume）

3. Call `get_spot_trades` (MCP: `list_trades`) with:
   - `currency_pair`: 同上
   - `limit`: 500

   Key data to extract:
   - 大单记录（单笔 > 平均 × 5）
   - 连续同方向大单

4. **计算深度比**（深度与成交量均用 USDT 口径）:
   ```
   深度比 = (前10档买深度 + 前10档卖深度) / 24h 成交额(quote) × 100%
   ```

5. **判断逻辑**:

   | 条件 | 标记 |
   |------|------|
   | 深度比 < 0.5% | 🔴 深度薄，易被操控 |
   | 深度比 0.5%-2% | 🟡 深度一般 |
   | 深度比 > 2% | 🟢 深度较好 |
   | 连续大单同方向 | ⚠️ 可能有主力控盘 |
   | 大单分散 | ✅ 交易分散 |

---

## Case 7: 订单簿解读

**触发词**: "解释订单簿示例"、"订单簿是什么"、"怎么看盘口"

**接口**：`get_spot_order_book` → `get_spot_tickers`

**判断/解读逻辑**：
- 示例 bids/asks 深度（档位与数量）
- 结合 ticker 最新价解释 spread（买卖价差）
- 价格波动快、深度深 → 流动性好

输出须包含订单簿教学、实时订单簿表示例、关键指标（买一/卖一/价差）、解读要点。

### Workflow

1. Call `get_spot_order_book` / `get_futures_order_book` (MCP: `list_order_book`) with:
   - `limit`: 10

   Key data to extract:
   - bids（买单）、asks（卖单）深度示例

2. Call `get_spot_tickers` / `get_futures_tickers` (MCP: `list_tickers`)

   Key data to extract:
   - last（最新成交价），用于解释 spread

3. **解读内容**:
   - 示例 bids/asks 深度
   - 结合 ticker 价解释 spread
   - 价格波动快、深度深 → 流动性好

---

## Judgment Logic Summary

| Case | 场景 | 核心指标 | 输出 |
|------|------|----------|------|
| 1 | 流动性 | 深度、成交量、滑点 | 流动性评级 |
| 2 | 动能 | 买卖比、成交活跃度 | 多空判断 |
| 3 | 爆仓 | 爆仓量、多空比 | 异常标记 |
| 4 | 套利 | 费率、价差、深度 | 套利机会列表 |
| 5 | 基差 | 期现价差、趋势 | 基差分析 |
| 6 | 操控 | 深度/成交比、大单 | 风险评估 |
| 7 | 订单簿 | 教学+实时数据 | 解读报告 |

## Report Template

### Case 1: 流动性分析报告

```markdown
## {currency} 流动性分析

**分析时间**: {timestamp}

### 📊 核心指标

| 指标 | 值 | 状态 |
|------|-----|------|
| 订单簿深度 | {depth} 档 | {status} |
| 24h 成交量 | ${volume}M | {status} |
| 30日均量 | ${avg_volume}M | - |
| 买卖价差 | {spread}% | {status} |
| 滑点风险 | {slippage}% | {status} |

### 📈 评估结论

**流动性评级**: {rating}/5 ⭐

{标记列表}

### 💡 建议

{根据评级给出建议}
```

### Case 2: 动能分析报告

```markdown
## {currency} 动能分析

**分析时间**: {timestamp}

### 📊 多空力量

| 指标 | 值 |
|------|-----|
| 买盘占比 | {buy_ratio}% |
| 卖盘占比 | {sell_ratio}% |
| 24h 成交量 | ${volume}M |
| 30日均量 | ${avg}M |
| 活跃度 | {active_status} |

### 📈 判断

**动能方向**: {direction}
**可持续性**: {sustainability}

{分析说明}
```

### Case 3: 爆仓监控报告

```markdown
## 爆仓异常监控

**监控时间**: {timestamp}

### 📊 全市场概览

| 指标 | 值 |
|------|-----|
| 1h 总爆仓 | ${total}M |
| 多头爆仓 | ${long}M ({long_ratio}%) |
| 空头爆仓 | ${short}M ({short_ratio}%) |

### 🔴 异常合约

| 合约 | 爆仓量 | 倍数 | 类型 |
|------|--------|------|------|
| {contract} | ${liq}M | {ratio}x | {type} |

{详细分析}
```

### Case 4: 套利扫描报告

```markdown
## 资金费率套利扫描

**扫描时间**: {timestamp}

### 🎯 套利机会

| 合约 | 费率 | 年化 | 基差 | 策略 |
|------|------|------|------|------|
| {contract} | {rate}% | {apr}% | {basis}% | {strategy} |

{详细分析}
```

### Case 5: 基差监控报告

```markdown
## 期现基差分析

**分析时间**: {timestamp}

### {currency} 基差数据

| 指标 | 值 |
|------|-----|
| 现货价格 | {spot} |
| 合约价格 | {futures} |
| 基差 | {basis} ({basis_rate}%) |
| 趋势 | {trend} |

{分析和建议}
```

### Case 6: 操控风险报告

```markdown
## {currency} 操控风险分析

**分析时间**: {timestamp}

### 📊 深度分析

| 指标 | 值 | 评估 |
|------|-----|------|
| 前10档深度 | ${depth}K | - |
| 24h 成交量 | ${volume}M | - |
| 深度比 | {ratio}% | {status} |

### 🔍 大单追踪

{大单记录分析}

### ⚠️ 风险评估

**操控风险**: {risk_level}

{详细说明}
```

### Case 7: 订单簿解读

```markdown
## 订单簿解读

### 📖 什么是订单簿

订单簿是交易所的"挂单列表"，分为：
- **Bids (买单)**: 想买入的订单，从高到低排列
- **Asks (卖单)**: 想卖出的订单，从低到高排列

### 📊 {currency} 实时订单簿

**卖单 (Asks)**
| 价格 | 数量 | 累计 |
|------|------|------|
| {ask3} | {qty} | {cum} |
| {ask2} | {qty} | {cum} |
| {ask1} | {qty} | {cum} | ← 卖一

--- 当前价格: {last} ---

**买单 (Bids)**
| 价格 | 数量 | 累计 |
|------|------|------|
| {bid1} | {qty} | {cum} | ← 买一
| {bid2} | {qty} | {cum} |
| {bid3} | {qty} | {cum} |

### 📈 关键指标

| 指标 | 值 | 含义 |
|------|-----|------|
| 买一价 | {bid1} | 最高买入价 |
| 卖一价 | {ask1} | 最低卖出价 |
| 价差 | {spread} | 流动性指标 |

### 💡 解读要点

1. **价差小** = 流动性好，交易成本低
2. **深度厚** = 大单也不容易影响价格
3. **买单多** = 下方支撑强
4. **卖单多** = 上方压力大
```

## Error Handling

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| MCP 未响应/超时 | Gate MCP 未配置或网络问题 | 提示用户检查 MCP 配置与网络；参考 gate-mcp-installer |
| 无交易数据 | 新币或冷门币 | 提示数据不足、无法计算指标 |
| API 超时 | 请求量大 | 分批请求或减少 limit |
| 合约不存在 | 仅现货有该交易对 | 说明无合约数据，仅给出现货分析或切换接口 |

## Safety Rules

- 所有分析仅供参考，不构成投资建议
- 明确标注数据时效性
- 高风险标记需醒目提示
- 套利建议需提醒风险
