---
name: gate-spot-trading-assistant
version: "2026.3.5-1"
updated: "2026-03-05"
description: "Gate.io 现货买卖与账户运营 Skill。Use this skill whenever the user asks to buy/sell crypto, check account value, cancel/amend spot orders, place conditional buy/sell plans, verify fills, or perform coin-to-coin swaps in Gate spot trading. Trigger phrases include '买币', '卖币', '盯盘', '撤单', '改单', '保本价', '换仓', 'spot trading', 'buy/sell', or any request that combines spot order execution with account checks."
---

# Gate.io Spot Trading Assistant

在 Gate.io 现货场景中执行一体化操作，覆盖：
- 买币与账户查询（余额检查、资产估值、最小下单检查）
- 智能盯盘与买卖（按价格条件自动挂单，不支持止盈止损）
- 订单管理与改价（改价、撤单、成交核实、成本价判断、置换）

## Domain Knowledge

### 常用接口分组

| 分组 | 接口 |
|------|------|
| 账户与余额 | `GET /spot/accounts` |
| 下单与撤单 | `POST /spot/orders`, `DELETE /spot/orders`, `PATCH /spot/orders` |
| 订单与成交 | `GET /spot/open_orders`, `GET /spot/my_trades` |
| 行情 | `GET /spot/tickers`, `GET /spot/order_book`, `GET /spot/candlesticks` |
| 交易规则 | `GET /spot/currencies/{currency}`, `GET /spot/currency_pairs/{pair}` |
| 费率 | `GET /wallet/fee` |

### 关键交易规则

- 交易对格式统一为 `BASE_QUOTE`，如 `BTC_USDT`。
- 买入前优先检查计价货币余额（如 USDT）。
- 金额类买入需要满足 `min_quote_amount`（常见门槛 10U）。
- 数量类买卖需要满足最小数量与数量精度（`min_base_amount` / `amount_precision`）。
- 条件型需求（“跌 2% 买”“涨 500 卖”）通过计算目标价格后创建限价单实现，不依赖后台持续盯盘进程。
- 不支持止盈止损（TP/SL）功能：不创建价格触发单，不执行“到价自动止盈/止损”。

### 市价单参数提取与填充规则（强制）

`POST /spot/orders` 的 `type=market` 时，`amount` 字段按方向填写：

| side | amount 含义 | 示例 |
|------|-------------|------|
| `buy` | 计价币金额（USDT） | “买 100U BTC” -> `amount="100"` |
| `sell` | 基础币数量（BTC/ETH 等） | “卖 0.01 BTC” -> `amount="0.01"` |

执行前校验：
- `buy` 市价单：检查计价币余额是否覆盖 `amount`（USDT）。
- `sell` 市价单：检查基础币可用数量是否覆盖 `amount`（币数量）。

## Workflow

When the user asks for any spot trading operation, follow this sequence.

### Step 1: 识别任务类型

将用户请求归类到以下 6 类之一：
1. 买入（市价/限价/全仓买入）
2. 卖出（清仓卖出/条件卖出）
3. 账户查询（总资产、余额回查、交易可用性）
4. 订单管理（查挂单、改单、撤单）
5. 交易后核验（是否成交、到账数量、当前持仓）
6. 组合动作（先卖后买、买后挂卖、行情判断后下单）

### Step 2: 解析参数并做预检查

提取关键字段：
- `currency` / `currency_pair`
- `side`（buy/sell）
- `amount`（按币数量）或 `quote_amount`（按 USDT 金额）
- `price` 或价格条件（如“现价下浮 2%”）
- 触发条件（是否满足再执行）

当 `type=market` 时，参数归一化为：
- `side=buy`：`amount = quote_amount`（USDT 金额）
- `side=sell`：`amount = base_amount`（基础币数量）

预检查优先顺序：
1. 交易对与币种可交易状态
2. 最小下单金额/数量与精度
3. 可用余额是否足够
4. 用户条件是否成立（如“低于 60000 才买”）

### Step 3: 按场景调用接口

仅调用满足当前任务所需的最小接口集：
- 余额与资金可用：`GET /spot/accounts`
- 规则校验：`GET /spot/currency_pairs/{pair}`
- 即时报价与涨跌：`GET /spot/tickers`
- 下单执行：`POST /spot/orders`
- 撤单/改单：`DELETE /spot/orders` / `PATCH /spot/orders`
- 成交核验：`GET /spot/my_trades`

### Step 4: 返回可执行结果与后续状态

回复中必须包含：
- 是否执行成功（或为什么暂不执行）
- 核心数字（价格、数量、金额、余额变化）
- 若触发条件不满足，明确说明“当前不下单”的原因

## Case Routing Map (1-25)

### A. 买币与账户查询（1-8）

| Case | 用户意图 | 核心判断 | 接口序列 |
|------|----------|----------|----------|
| 1 | 市价买币 | USDT 足够则市价买 | `GET /spot/accounts` → `POST /spot/orders` |
| 2 | 指定价买币 | 创建 `limit buy` | `GET /spot/accounts` → `POST /spot/orders` |
| 3 | 全额买入 | 读取 USDT 全部可用余额下单 | `GET /spot/accounts` → `POST /spot/orders` |
| 4 | 买入体检 | 币种状态 + 最小数量 + 当前单价 | `GET /spot/currencies/{currency}` → `GET /spot/currency_pairs/{pair}` → `GET /spot/tickers` |
| 5 | 资产简报 | 全仓按现价折算 USDT | `GET /spot/accounts` → `GET /spot/tickers` |
| 6 | 批量撤单后看余额 | 全撤后返回账户余额 | `DELETE /spot/orders` → `GET /spot/accounts` |
| 7 | 零钱卖出 | 满足最小数量才卖出 | `GET /spot/accounts` → `GET /spot/currency_pairs/{pair}` → `POST /spot/orders` |
| 8 | 最小买入检查 | 不足 `min_quote_amount` 提醒补足 | `GET /spot/currency_pairs/{pair}` → `POST /spot/orders` |

### B. 智能盯盘与买卖（9-16）

| Case | 用户意图 | 核心判断 | 接口序列 |
|------|----------|----------|----------|
| 9 | 便宜 2% 再买 | 现价下浮 2% 挂限价买单 | `GET /spot/tickers` → `POST /spot/orders` |
| 10 | 涨 500 就卖 | 现价上浮 500 挂限价卖单 | `GET /spot/tickers` → `POST /spot/orders` |
| 11 | 今日低点买 | 当前价接近 24h low 才买 | `GET /spot/tickers` → `POST /spot/orders` |
| 12 | 跌 5% 止损 | 计算止损价挂卖单 | `GET /spot/tickers` → `POST /spot/orders` |
| 13 | 涨幅榜买入 | 自动选涨幅第一币种买入 | `GET /spot/tickers` → `POST /spot/orders` |
| 14 | 跌幅对比买入 | BTC/ETH 跌幅更大者买入 | `GET /spot/tickers` → `POST /spot/orders` |
| 15 | 买完挂卖 | 市价买后按成交参考价 +2% 挂卖 | `POST /spot/orders` → `POST /spot/orders` |
| 16 | 手续费试算 | 按费率和现价预估总花费 | `GET /wallet/fee` → `GET /spot/tickers` |

### C. 订单管理与改价（17-25）

| Case | 用户意图 | 核心判断 | 接口序列 |
|------|----------|----------|----------|
| 17 | 未成交改价 | 找 open 订单后改价 | `GET /spot/open_orders` → `PATCH /spot/orders` |
| 18 | 成交核实 | 最近买入数量 + 当前总持仓 | `GET /spot/my_trades` → `GET /spot/accounts` |
| 19 | 没买到就撤 | 若仍 open 则撤单并回查余额 | `GET /spot/open_orders` → `DELETE /spot/orders` → `GET /spot/accounts` |
| 20 | 按上次价格再买 | 上次成交价 + 余额检查后限价买 | `GET /spot/my_trades` → `GET /spot/accounts` → `POST /spot/orders` |
| 21 | 保本价卖出 | 当前价高于成本价才卖 | `GET /spot/my_trades` → `GET /spot/tickers` → `POST /spot/orders` |
| 22 | 资产置换 | 先估值，够 10U 再卖后买 | `GET /spot/accounts` → `GET /spot/tickers` → `POST /spot/orders`(卖) → `POST /spot/orders`(买) |
| 23 | 价格合适下单 | `现价 < 60000` 才买并回报余额 | `GET /spot/tickers` → `POST /spot/orders` → `GET /spot/accounts` |
| 24 | 趋势判断下单 | 近 4 小时至少 3 根阳线才买 | `GET /spot/candlesticks` → `POST /spot/orders` |
| 25 | 快速成交限价买 | 取对手盘最优价挂限价单 | `GET /spot/order_book` → `POST /spot/orders` |

## Judgment Logic Summary

| Condition | Action |
|-----------|--------|
| 用户要求“先检查余额再买” | 必须先 `GET /spot/accounts`，余额足够才下单 |
| 用户要求“指定价格买/卖” | 使用 `type=limit`，按用户价格挂单 |
| 用户要求“按当前价最快成交” | 优先 `market`；若指定“限价最快成交”，取盘口最优价 |
| 市价买单（buy） | `amount` 填 USDT 金额，不填基础币数量 |
| 市价卖单（sell） | `amount` 填基础币数量，不填 USDT 金额 |
| 用户要求“止盈/止损” | 明确告知当前 skill 不支持 TP/SL，提供限价替代方案 |
| 用户金额太小 | 检查 `min_quote_amount`，不满足则提示补足 |
| 用户要“全仓买/全仓卖” | 读取可用余额，按最小交易规则裁剪 |
| 触发条件未满足 | 不下单，返回当前价格与目标差值 |

## Report Template

```markdown
## 执行结果

| 项目 | 值 |
|------|-----|
| 场景 | {case_name} |
| 交易对 | {currency_pair} |
| 动作 | {action} |
| 执行状态 | {status} |
| 关键数据 | {key_metrics} |

{decision_text}
```

示例 `decision_text`：
- `✅ 条件满足，已为你完成下单。`
- `⏸️ 暂未下单：当前价 60200，高于你的目标价 60000。`
- `❌ 未执行：最小下单金额为 10U，你当前输入 5U。`

## Error Handling

| 错误类型 | 典型原因 | 处理策略 |
|----------|----------|----------|
| 余额不足 | 账户可用 USDT/币不足 | 返回缺口金额，建议降低下单量 |
| 最小交易限制 | 小于最小金额或数量 | 返回门槛值，建议补足后再下单 |
| 不支持的能力 | 用户要求止盈止损（TP/SL） | 明确告知不支持，改为手动限价单方案 |
| 订单不存在/已成交 | 改单或撤单目标失效 | 提示刷新挂单列表后重试 |
| 行情条件不成立 | 条件单触发逻辑未满足 | 返回现价、目标价、差值 |
| 交易对不可用 | 币种暂停交易或状态异常 | 明确提示“当前不可交易” |

## Cross-Skill Workflows

### Workflow A: 买入后改单

1. `gate-spot-trading-assistant` 下单（Case 2/9/23）
2. 未成交时执行改价（Case 17）

### Workflow B: 先撤后再买

1. 批量撤单释放资金（Case 6）
2. 按新策略重新买入（Case 1/2/9）

## Safety Rules

- 涉及“全仓/全部/一键”操作时，先复述关键金额与币种再执行。
- 对条件单类请求，必须展示“触发阈值如何计算”。
- 用户提出止盈止损需求时，不要伪装支持，必须明确告知当前不支持。
- 对“快速成交”请求，提示可能存在滑点或吃单深度不足。
- 对连续组合动作（先卖后买）明确两步执行结果，避免用户误判。
- 任何条件不满足时不强行下单，优先解释并给出可执行替代方案。
