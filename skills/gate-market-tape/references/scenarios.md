# Scenarios

本文档约定各场景的 **MCP 调用顺序、参数、必取字段与输出格式**。实现时请严格按各 Case 下的「MCP 调用规范」依次调用 Gate MCP，并按「计算与判断」「输出」要求生成报告，以保证与文档一致。

| Case | 场景 | 核心 MCP 调用顺序 |
|------|------|-------------------|
| 1 | 流动性分析 | list_order_book → list_candlesticks → list_tickers（用户提永续/合约则用合约接口） |
| 2 | 动能判断 | list_trades → list_tickers → list_candlesticks → list_order_book → list_futures_funding_rate（合约则用合约接口） |
| 3 | 爆仓异常监控 | list_futures_liq_orders → list_futures_candlesticks → list_futures_tickers |
| 4 | 资金费率套利 | list_futures_tickers → list_futures_funding_rate → list_tickers → list_order_book |
| 5 | 基差监控 | list_tickers(现货) → list_futures_tickers → list_futures_premium_index |
| 6 | 操控风险 | list_order_book → list_tickers → list_trades |
| 7 | 订单簿解读 | list_order_book(limit=10) → list_tickers |

---

## Case 1: 流动性分析

### MCP 调用规范（与文档一致）

执行流动性分析时，**必须按以下顺序调用** Gate MCP，并提取指定字段，输出符合下方 Report Template。

| 步骤 | MCP 工具 | 参数 | 必取字段 |
|------|----------|------|----------|
| 1 | `list_order_book`（现货） | `currency_pair={BASE}_USDT`, `limit=20` | asks/bids 档位数量；前 10 档买卖深度总量；bid1/ask1（用于价差与滑点） |
| 2 | `list_candlesticks`（现货） | `currency_pair={BASE}_USDT`, `interval=1d`, `limit=30` | 近 30 日成交量（用于 30 日均量）；最近一根为 24h 成交量参考 |
| 3 | `list_tickers`（现货） | `currency_pair={BASE}_USDT` | `last` 最新价；`quoteVolume` 24h 成交额（USDT）；`changePercentage` 24h 涨跌；`high24h`/`low24h` |
| 4（可选） | `list_trades`（现货） | `currency_pair={BASE}_USDT`, `limit=100` | 近期单笔大小分布，用于描述「近期成交流」、中大户参与度 |

**计算与判断**（与 SKILL 一致）：

- **接口选择**：用户提及「永续、合约」时使用合约接口（list_futures_order_book 等），否则现货。
- **滑点率** = `2×(ask1−bid1)/(bid1+ask1)×100%`；&gt; 0.5% → 标记「滑点风险高」。
- **订单簿深度**：asks/bids 深度 &lt; 10 档 → 标记「流动性低」。
- **24h 成交量** &lt; 30 日成交量均值 → 标记「冷门对」。
- **流动性评级**：综合上述指标给出 1～5 ⭐。

**输出**：必须包含「核心指标」表（订单簿深度、24h 成交量、30日均量、买卖价差、滑点风险 + 状态）、「评估结论」（流动性评级 x/5 ⭐）、以及简短「建议」。

---

### Scenario 1.1: 现货流动性查询

**User Prompt**: "当前 ETH 的流动性如何"

**Context**: 用户想了解 ETH 现货的交易条件

**Expected Behavior**:
1. 按 **MCP 调用规范** 依次调用：`list_order_book` → `list_candlesticks` → `list_tickers`（可选 `list_trades`）
2. 从订单簿提取档位数、前 10 档深度、bid1/ask1
3. 从 K 线计算 30 日均量、24h 成交量
4. 从 tickers 取最新价、24h 成交额、涨跌
5. 计算滑点率，按文档判断逻辑打状态与评级
6. 按 Report Template 输出核心指标表 + 评估结论 + 建议

**Output**:
```
## ETH 流动性分析

### 📊 核心指标

| 指标 | 值 | 状态 |
|------|-----|------|
| 订单簿深度 | 20 档 | 🟢 正常 |
| 24h 成交量 | $485M | 🟢 活跃 |
| 30日均量 | $320M | - |
| 买卖价差 | 0.02% | 🟢 极佳 |
| 滑点风险 | 0.03% | 🟢 极低 |

### 📈 评估结论

**流动性评级**: 5/5 ⭐

ETH 流动性极佳，适合大额交易。
```

---

### Scenario 1.2: 合约流动性查询

**User Prompt**: "BTC永续合约深度怎么样"

**Context**: 用户询问合约，触发合约接口

**Expected Behavior**:
1. 识别「永续/合约」关键词，使用**合约** MCP：`list_futures_order_book`（`settle=usdt`, `contract=BTC_USDT`, `limit=20`）→ 可选 `list_futures_tickers`、`list_futures_candlesticks`(1d, 30)
2. 提取档位数、前 10 档深度、bid1/ask1，计算滑点率
3. 按流动性评估标准输出核心指标表 + 流动性评级

**Output**:
```
## BTC_USDT 永续合约 流动性分析

| 指标 | 值 | 状态 |
|------|-----|------|
| 订单簿深度 | 50 档 | 🟢 极佳 |
| 滑点风险 | 0.01% | 🟢 极低 |

流动性评级: 5/5 ⭐
```

---

### Scenario 1.3: 冷门币流动性警告

**User Prompt**: "XYZ币的流动性如何"

**Context**: 用户查询冷门小市值币种

**Expected Behavior**:
1. 仍按 **Case 1 MCP 调用规范** 调用 order_book → candlesticks → tickers
2. 若档位 &lt; 10、或 24h 量 &lt; 30 日均值、或滑点率 &gt; 0.5%，在核心指标表标注 🔴，并输出风险提示与低流动性评级

**Output**:
```
## XYZ 流动性分析

### ⚠️ 风险提示

| 指标 | 值 | 状态 |
|------|-----|------|
| 订单簿深度 | 5 档 | 🔴 深度不足 |
| 24h 成交量 | $15K | 🔴 冷门币 |
| 滑点风险 | 2.3% | 🔴 滑点高 |

**流动性评级**: 1/5 ⭐

⚠️ 该币种流动性差，大额交易会产生严重滑点！
```

---

## Case 2: 动能判断

### MCP 调用规范（与文档一致）

**触发词**："BTC 近 24h 多头厉害还是空头厉害，可持续吗"。执行动能分析时，**必须按以下顺序调用** Gate MCP；若用户询问**合约**则选用合约接口。

| 步骤 | MCP 工具 | 参数 | 必取字段 |
|------|----------|------|----------|
| 1 | `list_trades`（现货/合约） | `currency_pair` 或 `contract`+`settle`, `limit=1000` | 买入/卖出量；买盘占比 = buy_volume / total_volume |
| 2 | `list_tickers`（现货/合约） | 同交易对 | 24h 成交量、24h 涨跌 |
| 3 | `list_candlesticks`（现货/合约） | `interval=1d`, `limit=30` | 30 日日均成交量 |
| 4 | `list_order_book`（现货/合约） | `limit=20` | 前 10 档买卖深度，用于多空订单数量对比 |
| 5 | `list_futures_funding_rate` 或等价 | 合约时 | 资金费率；正→多头占优，负→空头占优 |

**计算与判断**（与 SKILL 一致）：

- 24h 中 **buy &gt; 70%** → 标记「买盘强势」；卖盘 &gt; 70% → 卖盘强势。
- **24h 成交量 &gt; 30 日日均成交量** → 标记「活跃」。
- **资金费率** 正/负 → 多头/空头占优；**订单簿前 10 档** 多空订单数量辅助判断。

**输出**：必须包含「多空力量」表、动能方向、可持续性、分析说明。

---

### Scenario 2.1: 基础动能查询

**User Prompt**: "BTC 近 24h 多头厉害还是空头厉害，可持续吗"

**Context**: 用户想判断短期多空力量

**Expected Behavior**:
1. 按 **MCP 调用规范** 依次调用：`list_trades` → `list_tickers` → `list_candlesticks` → `list_order_book` → `list_futures_funding_rate`（合约则用合约接口）
2. 从 trades 统计买卖量、买盘占比；从 tickers 取 24h 成交量与涨跌；从 candlesticks 得 30 日日均量；从 order_book 取前 10 档多空深度；从 funding_rate 看多空占优
3. 按文档判断逻辑（买盘&gt;70%→买盘强势，24h 量&gt;30 日均→活跃，资金费率+订单簿多空）给出动能方向与可持续性
4. 按 Report Template 输出多空力量表 + 判断 + 分析说明

**Output**:
```
## BTC 动能分析

### 📊 多空力量

| 指标 | 值 |
|------|-----|
| 买盘占比 | 65% |
| 卖盘占比 | 35% |
| 24h 成交量 | $2.1B |
| 30日均量 | $1.8B |
| 活跃度 | 🔥 活跃 |

### 📈 判断

**动能方向**: 📈 买盘略占优

买盘占比 65%，但未达到 70% 的"强势"阈值，
目前处于多头占优但非单边行情。

成交量高于 30 日均值，市场活跃度上升。
```

---

### Scenario 2.2: 单边强势行情

**User Prompt**: "ETH买盘强吗"

**Context**: 用户询问买盘情况

**Expected Behavior**:
1. 按 **MCP 调用规范** 调用 `list_trades`（ETH_USDT）→ `list_tickers` → `list_candlesticks`
2. 统计买卖比例，若买盘占比 &gt; 70% 则标记为买盘强势
3. 输出多空力量表 + 动能方向（📈 买盘强势）

**Output**:
```
## ETH 动能分析

### 📊 多空力量

| 指标 | 值 |
|------|-----|
| 买盘占比 | 78% |
| 卖盘占比 | 22% |

### 📈 判断

**动能方向**: 📈 买盘强势

买盘占比达到 78%，远超 70% 阈值，
当前处于明显的多头主导行情。

配合成交量放大，趋势可能延续。
```

---

### Scenario 2.3: 合约动能查询

**User Prompt**: "BTC合约动能判断"

**Context**: 用户明确询问合约

**Expected Behavior**:
1. 识别「合约」关键词，使用合约 MCP：`list_trades`（futures，`settle=usdt`, `contract=BTC_USDT`）→ `list_futures_tickers` → `list_futures_candlesticks`
2. 按 **MCP 调用规范** 提取买卖占比、24h 量、30 日均量，输出格式同上

**Output**: 同上结构，数据来源为合约

---

## Case 3: 爆仓异常监控

### MCP 调用规范（与文档一致）

**触发词**："最近爆仓情况"、"哪些币爆得多"。执行爆仓监控时，**必须按以下顺序调用** Gate MCP（仅合约）。

| 步骤 | MCP 工具 | 参数 | 必取字段 |
|------|----------|------|----------|
| 1 | `list_futures_liq_orders` | `settle=usdt`, 时间范围（含最近 1h，可选 24h 作日均基准） | 按 contract 聚合爆仓量；多头(size&gt;0)/空头(size&lt;0)；1h 总爆仓 |
| 2 | `list_futures_candlesticks` | `settle=usdt`, `contract`, `interval=5m`, `limit=12` | 爆仓时段价格、当前价、价格恢复程度 |
| 3 | `list_futures_tickers` | `settle=usdt`（或指定 contract） | 当前价、24h 涨跌 |

**计算与判断**（与 SKILL 一致）：

- **1h 爆仓量 &gt; 日均×3** → 标记「异常」。
- **爆仓方向集中 &gt; 80%**（多头或空头）→ 标记「多头清洗」或「空头清洗」。
- **价格已恢复**（相对插针低/高点）→ 标记「插针行情」。

**输出**：必须包含「全市场概览」表、「异常合约」表，必要时插针分析（最低点、当前价、恢复程度）。

---

### Scenario 3.1: 全市场爆仓概览

**User Prompt**: "最近爆仓情况"

**Context**: 用户想了解全市场爆仓

**Expected Behavior**:
1. 按 **MCP 调用规范** 依次调用：`list_futures_liq_orders` → `list_futures_candlesticks` → `list_futures_tickers`
2. 按合约聚合爆仓量，计算多空占比；若有日均基准则算 1h 相对日均倍数
3. 按判断逻辑：1h 爆仓&gt;日均×3→异常；爆仓方向集中&gt;80%→多头/空头清洗；价格已恢复→插针行情
4. 输出全市场概览表 + 异常合约表

**Output**:
```
## 爆仓异常监控

**监控时间**: 2026-03-05 15:30

### 📊 全市场概览

| 指标 | 值 |
|------|-----|
| 1h 总爆仓 | $45M |
| 多头爆仓 | $38M (84%) |
| 空头爆仓 | $7M (16%) |

### 🔴 异常合约

| 合约 | 爆仓量 | 倍数 | 类型 |
|------|--------|------|------|
| ETH_USDT | $18M | 4.2x | 📉 多头清洗 |
| SOL_USDT | $8M | 3.5x | 📉 多头清洗 |

多头爆仓占比 84%，当前行情正在清洗多头杠杆。
```

---

### Scenario 3.2: 插针行情识别

**User Prompt**: "刚才BTC是不是插针了"

**Context**: 用户怀疑发生插针

**Expected Behavior**:
1. 按 **MCP 调用规范** 调用：`list_futures_liq_orders`(1h，可筛 contract=BTC_USDT) → `list_futures_candlesticks`(BTC_USDT, 5m, 12) → `list_futures_tickers`
2. 从爆仓数据看多空爆仓占比；从 K 线取最低点、当前价，计算恢复程度 = (当前价 - 最低) / (爆仓前高 - 最低) 或类似
3. 若多头集中爆仓且价格恢复 &gt; 80%，输出插针分析（爆仓数据表 + 最低点/当前价/恢复程度 + 📌 插针判断）

**Output**:
```
## BTC 插针分析

### 📊 爆仓数据

| 指标 | 值 |
|------|-----|
| 1h 爆仓 | $25M |
| 多头爆仓 | $23M (92%) |
| 最低点 | $62,100 |
| 当前价 | $63,800 |
| 恢复程度 | 85% |

### 📌 判断

**类型**: 📌 插针行情

特征:
- 多头集中爆仓 (92%)
- 价格已恢复 85%
- 典型的短期插针清洗多头杠杆
```

---

## Case 4: 资金费率套利扫描

### MCP 调用规范（与文档一致）

**触发词**："现在有没有套利机会"、"费率异常的币"。执行套利扫描时，**必须按以下顺序调用** Gate MCP。

| 步骤 | MCP 工具 | 参数 | 必取字段 |
|------|----------|------|----------|
| 1 | `list_futures_tickers` | `settle=usdt` | 所有合约 funding_rate、24h 成交量 |
| 2 | `list_futures_funding_rate` 或等价 | 对候选/全市场 | 费率明细 |
| 3 | `list_tickers`（现货） | 对每个候选 `currency_pair={BASE}_USDT` | 现货 last；现货合约价差 |
| 4 | `list_order_book`（现货） | 对 Top 候选 `currency_pair`, `limit=20` | 前 10 档深度；depth 太薄则排除 |

**计算与判断**（与 SKILL 一致）：

- **\|rate\| &gt; 0.05% 且 24h vol &gt; $10M** → 进入候选。
- **现货合约价差 &gt; 0.2%** → 加分。
- **book depth 太薄** → 排除。

**输出**：必须包含「套利机会」表、策略说明（正套/反套）、风险提示。

---

### Scenario 4.1: 全市场套利扫描

**User Prompt**: "现在有没有套利机会"

**Context**: 用户想寻找套利机会

**Expected Behavior**:
1. 按 **MCP 调用规范** 依次调用：`list_futures_tickers` → `list_futures_funding_rate` → `list_tickers`(候选) → `list_order_book`(Top 候选)
2. 判断逻辑：\|rate\|&gt;0.05% 且 24h vol&gt;$10M→候选；现货合约价差&gt;0.2%→加分；depth 太薄→排除
3. 输出套利机会表 + 策略说明 + 风险提示

**Output**:
```
## 资金费率套利扫描

**扫描时间**: 2026-03-05 15:30

### 🎯 套利机会 (Top 5)

| 合约 | 费率 | 年化 | 基差 | 深度 | 策略 |
|------|------|------|------|------|------|
| DOGE_USDT | +0.15% | 164% | +0.3% | 🟢 | 正套 |
| PEPE_USDT | +0.12% | 131% | +0.2% | 🟡 | 正套 |
| WIF_USDT | -0.10% | 109% | -0.1% | 🟢 | 反套 |

### 📖 策略说明

**正套**: 空合约 + 多现货
**反套**: 多合约 + 空现货 (需借币)

⚠️ 风险提示: 实际收益需扣除交易成本
```

---

### Scenario 4.2: 费率异常查询

**User Prompt**: "哪些币费率异常"

**Context**: 用户想找费率极端的币

**Expected Behavior**:
1. 按 **MCP 调用规范** 调用 `list_futures_tickers`(settle=usdt)，筛选 \|funding_rate\| &gt; 0.001 (0.1%) 的合约
2. 按费率绝对值排序，标注异常程度（如极端正费率、高负费率）
3. 输出「费率异常币种」表（合约、费率、状态）

**Output**:
```
## 费率异常币种

| 合约 | 费率 | 状态 |
|------|------|------|
| DOGE_USDT | +0.18% | 🔴 极端正费率 |
| SHIB_USDT | +0.15% | 🔴 高正费率 |
| WIF_USDT | -0.12% | 🔵 高负费率 |

正费率 > 0.1% 表示做多成本高，
可能预示短期回调风险。
```

---

## Case 5: 现货 vs 合约基差监控

### MCP 调用规范（与文档一致）

**触发词**："基差怎么样"、"期现价差"。执行基差监控时，**必须按以下顺序调用** Gate MCP。

| 步骤 | MCP 工具 | 参数 | 必取字段 |
|------|----------|------|----------|
| 1 | `list_tickers`（现货） | `currency_pair={BASE}_USDT` | 现货 `last` 价格 |
| 2 | `list_futures_tickers` | `settle=usdt`，可指定 `contract={BASE}_USDT` | 合约价、mark_price、index_price |
| 3 | `list_futures_premium_index` 或等价 | `settle=usdt`, `contract={BASE}_USDT` | premium_index；若有历史则用于均值与偏离度 |

**计算与判断**（与 SKILL 一致）：

- **当前基差 vs 历史均值偏离度**。
- **基差走阔/收窄趋势判断**（走阔→情绪升温，收窄→回归均值）。

**输出**：必须包含「基差数据」表、当前基差与历史均值比较、基差走阔/收窄结论及简短建议。

---

### Scenario 5.1: 单币基差查询

**User Prompt**: "BTC基差怎么样"

**Context**: 用户查询 BTC 的期现价差

**Expected Behavior**:
1. 按 **MCP 调用规范** 依次调用：`list_tickers`(BTC_USDT) → `list_futures_tickers`(usdt, BTC_USDT) → 可选 `list_futures_premium_index`
2. 计算基差、基差率；若有历史溢价数据可算历史均值
3. 按 Report Template 输出基差数据表 + 分析 + 建议

**Output**:
```
## BTC 期现基差分析

### 📊 基差数据

| 指标 | 值 |
|------|-----|
| 现货价格 | $63,500 |
| 合约价格 | $63,700 |
| 基差 | +$200 |
| 基差率 | +0.31% |
| 历史均值 | +0.15% |

### 📈 分析

当前基差率 0.31%，高于历史均值 0.15%，
处于**高正基差**状态。

可能原因:
- 市场看涨情绪较强
- 适合套利者做正套
```

---

### Scenario 5.2: 负基差警示

**User Prompt**: "ETH期现价差"

**Context**: 查询 ETH 基差

**Expected Behavior**:
1. 按 **MCP 调用规范** 调用 `list_tickers`(ETH_USDT) → `list_futures_tickers`(usdt, ETH_USDT)
2. 计算基差、基差率；若基差率为负，输出基差数据表 + ⚠️ 负基差警示（看跌/空头拥挤等说明）

**Output**:
```
## ETH 期现基差分析

### 📊 基差数据

| 指标 | 值 |
|------|-----|
| 现货价格 | $3,200 |
| 合约价格 | $3,185 |
| 基差 | -$15 |
| 基差率 | -0.47% |

### ⚠️ 异常提示

当前处于**负基差**，合约价低于现货价，
这通常表示:
- 市场看跌情绪浓厚
- 或空头拥挤
```

---

## Case 6: 币种操控风险分析

### MCP 调用规范（与文档一致）

**触发词**："这个币深度和成交比怎么样"、"容易操控吗"。执行操控风险分析时，**必须按以下顺序调用** Gate MCP（现货）。

| 步骤 | MCP 工具 | 参数 | 必取字段 |
|------|----------|------|----------|
| 1 | `list_order_book` | `currency_pair={BASE}_USDT`, `limit=20` | 前 10 档买深度总和、前 10 档卖深度总和 |
| 2 | `list_tickers` | `currency_pair={BASE}_USDT` | 24h 成交额（quoteVolume） |
| 3 | `list_trades` | `currency_pair={BASE}_USDT`, `limit=500` | 单笔分布；连续同方向大单 |

**计算与判断**（与 SKILL 一致）：

- **前 10 档深度总量 / 24h volume &lt; 0.5%** → 「深度薄」。
- **24h trades 中有连续同方向大单** → 「可能有主力在控盘」。

**输出**：必须包含「深度分析」表（前10档深度、24h 成交量、深度比、评估）、「大单追踪」简述、「操控风险」结论。

---

### Scenario 6.1: 操控风险查询

**User Prompt**: "PEPE这个币容易被操控吗"

**Context**: 用户担心小市值币被操控

**Expected Behavior**:
1. 按 **MCP 调用规范** 依次调用：`list_order_book`(PEPE_USDT) → `list_tickers` → `list_trades`(limit=500)
2. 计算深度比；从 trades 中识别大单与连续同向
3. 按 Report Template 输出深度分析表 + 大单追踪 + 风险评估

**Output**:
```
## PEPE 操控风险分析

### 📊 深度分析

| 指标 | 值 | 评估 |
|------|-----|------|
| 前10档深度 | $850K | - |
| 24h 成交量 | $320M | - |
| 深度比 | 0.27% | 🔴 深度薄 |

### 🔍 大单追踪

最近 500 笔交易中发现:
- 3 笔大单连续买入 (占比 15%)
- 单笔最大: $125K

### ⚠️ 风险评估

**操控风险**: 🔴 高

- 深度比 < 0.5%，意味着较小资金即可影响价格
- 检测到连续同方向大单，可能存在主力控盘
```

---

### Scenario 6.2: 正常币种

**User Prompt**: "BTC深度成交比怎么样"

**Context**: 查询主流币

**Expected Behavior**:
1. 按 **MCP 调用规范** 调用 `list_order_book`(BTC_USDT) → `list_tickers` → 可选 `list_trades`
2. 计算深度比；若 &gt; 2% 则评估为深度好、操控风险低
3. 输出深度分析表 + 风险评估（🟢 低）

**Output**:
```
## BTC 操控风险分析

### 📊 深度分析

| 指标 | 值 | 评估 |
|------|-----|------|
| 前10档深度 | $85M | - |
| 24h 成交量 | $2.1B | - |
| 深度比 | 4.0% | 🟢 深度好 |

### ⚠️ 风险评估

**操控风险**: 🟢 低

BTC 深度充足，需要大量资金才能影响价格，
操控风险极低。
```

---

## Case 7: 订单簿解读

### MCP 调用规范（与文档一致）

**触发词**："解释订单簿示例"、"订单簿是什么"、"怎么看盘口"。执行订单簿解读时，**必须按以下顺序调用** Gate MCP。

| 步骤 | MCP 工具 | 参数 | 必取字段 |
|------|----------|------|----------|
| 1 | `list_order_book`（现货/合约） | `currency_pair` 或 `contract`+`settle`, `limit=10` | bids/asks 深度示例（每档价格与数量） |
| 2 | `list_tickers`（同市场） | 对应交易对 | `last` 最新价，用于解释 spread |

**判断/解读逻辑**（与 SKILL 一致）：

- **示例 bids/asks 深度**（档位与数量）。
- **结合 ticker 价解释 spread**（买卖价差）。
- **价格波动快、深度深** → 流动性好。

**输出**：必须包含订单簿教学、实时订单簿表示例、关键指标（买一、卖一、价差）、解读要点。

---

### Scenario 7.1: 入门解读

**User Prompt**: "帮我解释一下订单簿"

**Context**: 用户是新手，需要教学

**Expected Behavior**:
1. 按 **MCP 调用规范** 调用 `list_order_book`（可用 BTC_USDT，limit=10）→ `list_tickers`
2. 用真实数据填写订单簿表与关键指标，配合教学文案（Bids/Asks/Spread、价差含义）
3. 输出教学 + 实时示例 + 解读要点

**Output**:
```
## 订单簿解读

### 📖 什么是订单簿

订单簿是交易所的"挂单列表":

- **Asks (卖单)**: 想卖出的人挂的单，价格从低到高
- **Bids (买单)**: 想买入的人挂的单，价格从高到低
- **Spread (价差)**: 最低卖价和最高买价的差距

### 📊 BTC 实时订单簿示例

**卖单 (Asks)** ↑
| 价格 | 数量 | 累计 |
|------|------|------|
| 63,550 | 2.5 | 7.8 |
| 63,530 | 1.8 | 5.3 |
| 63,510 | 3.5 | 3.5 | ← 卖一 (最低卖价)

------- 当前价: 63,505 -------

**买单 (Bids)** ↓
| 价格 | 数量 | 累计 |
|------|------|------|
| 63,500 | 4.2 | 4.2 | ← 买一 (最高买价)
| 63,480 | 2.1 | 6.3 |
| 63,460 | 3.0 | 9.3 |

### 💡 关键概念

- **价差** = 63,510 - 63,500 = $10 (0.016%)
- 价差越小，流动性越好
- 深度越厚，大单影响越小
```

---

### Scenario 7.2: 特定币种订单簿

**User Prompt**: "看下ETH的盘口"

**Context**: 用户想看特定币种

**Expected Behavior**:
1. 按 **MCP 调用规范** 调用 `list_order_book`(ETH_USDT, limit=10) → `list_tickers`(ETH_USDT)
2. 输出 ETH 实时订单簿表（卖单/买单、价格、数量、累计）+ 当前价 + 价差与简短解读（如流动性良好、支撑强弱）

**Output**:
```
## ETH 订单簿

**卖单 (Asks)**
| 价格 | 数量 | 累计 |
|------|------|------|
| 3,205 | 45 | 120 |
| 3,203 | 32 | 75 |
| 3,201 | 43 | 43 | ← 卖一

--- 当前价: 3,200 ---

**买单 (Bids)**
| 价格 | 数量 | 累计 |
|------|------|------|
| 3,200 | 55 | 55 | ← 买一
| 3,198 | 28 | 83 |
| 3,196 | 40 | 123 |

价差: $1 (0.03%) - 流动性良好
买单深度厚于卖单，下方支撑较强
```
