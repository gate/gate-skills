# Fixture 框架规范

## 概述

Fixture（测试夹具）为 L1.5 写操作端到端测试提供自动化的前置状态构建和清理能力。

skill-tester 通过**自动推断**为任何 Skill 构建 Fixture，无需 Skill 开发者做任何额外配置：

```
自动推断流程：
  1. 读取目标 Skill 的 SKILL.md  → 提取所有引用的 MCP 工具
  2. 读取 MCP 工具 JSON Schema  → 分类读/写，分析参数依赖
  3. 对每个写操作场景          → 自动识别 Pattern + 构建 Setup/Teardown
  4. 执行测试                  → Setup → Execute → Verify → Teardown
```

---

## 隔离与授权门禁

先执行 [Fixture isolation and authorization contract](fixture-safety.md)。本文件的自动
推断和金额/价格样例只适用于可强制隔离的合成依赖，不构成真实写入许可。真实集成必须
单独核实环境、账号、权限、数据和每项写入/清理授权；证据缺失时 BLOCKED、零业务写入。
不能从内网地址、HTTP、端口或 server 名推断可安全写入。

---

## 自动推断机制

### Step 1: 工具提取与分类

从目标 Skill 的 SKILL.md 和 references/*.md 中提取所有 MCP 工具引用，按前缀自动分类：

| 前缀 | 分类 | 说明 |
|------|------|------|
| `create_` | 写 — 创建 | 创建资源（订单/借贷/转账等） |
| `cancel_` | 写 — 删除 | 取消/删除资源 |
| `amend_` / `update_` | 写 — 修改 | 修改资源或设置 |
| `delete_` | 写 — 删除 | 删除资源 |
| `set_` | 写 — 设置 | 修改配置/状态 |
| `get_` / `list_` | 读 | 查询操作 |

### Step 2: 参数依赖分析

对每个写操作工具，读取其 MCP 工具 JSON Schema（位于 `mcps/{server}/tools/{tool_name}.json`），分析必填参数：

```
对于 cancel_spot_order:
  required params: { order_id, currency_pair }
  ↓
  order_id 从何而来？ → 找到同 Skill 中的 create_spot_order → 它的返回值包含 order_id
  ↓
  推断: cancel_spot_order 依赖 create_spot_order 的产出
```

**依赖识别规则**：

| 参数名模式 | 依赖来源 | 推断逻辑 |
|-----------|---------|---------|
| `order_id` | `create_*_order` 的返回值 | 需要先创建订单 |
| `position` / `contract` + `size` | `create_*_order` 的开仓操作 | 需要先建仓 |
| `trigger_order_id` | `create_*_triggered_order` 的返回值 | 需要先创建触发单 |
| 无资源 ID 依赖 | — | 可直接执行（Pattern B） |

### Step 3: 自动识别 Pattern

根据写操作工具的特征和依赖关系，自动匹配 4 种 Pattern：

| Pattern | 名称 | 自动识别条件 | 典型场景 |
|---------|------|-------------|---------|
| A | Resource Lifecycle | 写工具需要另一个 create 工具的产出作为参数 | 撤单需 order_id → 先创建订单 |
| B | Instant Execution | 写工具不依赖其他写工具的产出，只需读操作前置查询 | 闪兑/市价单/Swap |
| C | State Transition | 写工具是 `set_*` / `update_*` 且操作对象是配置/状态而非资源 | 杠杆/模式/抵押设置 |
| D | Multi-Step Pipeline | Skill workflow 中写工具有明确的先后链式调用关系 | DEX: preview → sign → broadcast |

**自动识别流程**：

```
读取写工具的 JSON Schema
    ↓
检查 required params 中是否有资源 ID 类参数（order_id, position 等）
    ├── 有 → 找到对应的 create 工具 → Pattern A
    └── 无 → 继续
    ↓
检查工具是否为 set_* / update_* 且操作配置类字段（leverage, mode 等）
    ├── 是 → Pattern C
    └── 否 → 继续
    ↓
检查 Skill workflow 中是否有链式调用（步骤 N 的输出是步骤 N+1 的输入）
    ├── 是 → Pattern D
    └── 否 → Pattern B（直接执行）
```

### Step 4: 自动构建 Setup

根据识别的 Pattern，自动构建 Setup 步骤：

#### Pattern A — Resource Lifecycle

```
1. 找到目标写工具依赖的 create 工具
2. 读取 create 工具的 JSON Schema → 获取必填参数
3. 对每个必填参数，查找同 Skill 的读工具获取安全值：
   - currency_pair / contract → 使用 Skill 中最常引用的交易对（如 BTC_USDT）
   - price → 调用 get_tickers 获取当前价 → 偏移 ±30% 仅为合成输入，不保证真实订单不成交
   - amount / size → 调用 get_currency_pair 或 get_contract → 使用最小允许值
   - side → 默认 buy（挂单场景）
4. 调用 create 工具 → 记录返回的资源 ID
```

#### Pattern B — Instant Execution

```
1. 找到目标写工具的必填参数
2. 对每个参数，查找同 Skill 的读工具获取有效值：
   - 如闪兑: 调用 list_currency_pairs → 获取支持的币对和最小金额
   - 如 DEX Swap: 调用 tx.quote → 获取报价
3. 准备最小金额参数
4. 无需额外创建资源
```

#### Pattern C — State Transition

```
1. 找到对应的读工具（如 set_leverage → get_position 获取当前杠杆）
2. 调用读工具 → 记录原始状态值
3. Setup 完成（原始状态即为 Teardown 的恢复目标）
```

#### Pattern D — Multi-Step Pipeline

```
1. 从 Skill workflow 中提取步骤链
2. 依次构建每一步的参数（前一步输出 → 后一步输入）
3. 对第一步需要的参数，使用读工具获取
```

### Step 5: 自动构建 Teardown

| Pattern | Teardown 策略 |
|---------|--------------|
| A | 查找 Skill 中对应的 cancel/delete 工具 → 若资源仍存在则清理 |
| B | 不可逆操作仍须校验后置状态，记录残余；不能自动反向交易 |
| C | 用 Step 4 记录的原始状态值，调用 set/update 工具恢复 |
| D | 核验各步后置状态，失败不得自动补偿 |

**Teardown 工具自动匹配**：

| 创建工具模式 | 对应清理工具模式 |
|-------------|---------------|
| `create_*_order` | `cancel_*_order` |
| `create_*_batch_orders` | `cancel_*_batch_orders` 或逐个 `cancel_*_order` |
| `create_*_triggered_order` | `cancel_*_triggered_order` |
| 开仓 (`create_*_order` with size) | 仅合成状态清理；真实平仓需独立有效授权 |
| `set_*` / `update_*` | 仅合成状态恢复；真实状态修改需独立有效授权 |

### Step 6: 安全参数构建规则

自动推断时，参数值的构建遵循以下安全规则：

| 参数类型 | 安全策略 | 说明 |
|---------|---------|------|
| 价格 (price) | 偏离市价 ≥30% | buy: last × 0.7, sell: last × 1.3，仅为合成输入，不保证真实订单不成交 |
| 数量 (amount/size) | 使用最小允许值 | 从交易规则/合约信息中获取 min_base_amount 等 |
| 触发价 (trigger_price) | 偏离市价 ≥50% | buy: last × 0.5, sell: last × 2.0 |
| 金额 (quote amount) | 使用最小金额 | 如 min_quote_amount (通常 1 USDT) |
| 交易对/合约 | Skill 最常引用的 | 如 BTC_USDT |
| 订单类型 (type) | `limit`（挂单场景） | 仅为合成输入，不保证真实订单不立即成交 |
| 市价单 (type=market) | 仅 filled_trade 场景 | 使用最小金额 |
| 杠杆/模式等设置 | 先读后改后恢复 | Pattern C 专用 |

---

## 通用 Fixture 模式（Pattern）详解

### Pattern A: Resource Lifecycle

创建资源 → 操作资源 → 清理资源。

```
Setup:   自动创建资源（订单/仓位/借贷/触发单等）
           ↓
Execute: 对资源执行目标操作（撤销/修改/查询详情等）
           ↓
Teardown: 若资源仍存在则自动清理（撤单/平仓/还款等）
```

| 适用业务 | 示例 |
|---------|------|
| CEX Spot | 创建限价单 → 撤单/改单 → 撤掉残余 |
| CEX Futures | 开仓 → 平仓/改单 → 平掉残余 |
| CEX Unified | 借款 → 还款 → 确认无余额 |

### Pattern B: Instant Execution

直接执行写操作，无需前置创建资源。

```
Setup:   查询前置信息（交易对/限额/余额等）
           ↓
Execute: 直接执行写操作（闪兑/市价单/Swap 等）
           ↓
Teardown: 无（操作不可逆或无残留资源）
```

| 适用业务 | 示例 |
|---------|------|
| Flash Swap | 查询币对+限额 → 执行闪兑 → 无需清理 |
| DEX Swap | 查询报价 → 执行兑换 → 无需清理 |
| CEX Spot 市价单 | 查询余额 → 市价买入 → 无需清理 |

### Pattern C: State Transition

读取当前状态 → 切换到目标状态 → 验证 → 恢复原状态。

```
Setup:   读取当前状态并记录（作为恢复基准）
           ↓
Execute: 执行状态切换操作
           ↓
Verify:  确认状态已变更
           ↓
Teardown: 恢复到原始状态
```

| 适用业务 | 示例 |
|---------|------|
| Unified 模式切换 | 读当前模式 → 切换 → 验证 → 恢复 |
| Futures 杠杆设置 | 读当前杠杆 → 修改 → 验证 → 恢复 |
| Collateral 设置 | 读当前抵押币 → 启用/禁用 → 验证 → 恢复 |

### Pattern D: Multi-Step Pipeline

多步骤链式执行，每步的输出是下一步的输入。

```
Setup:   查询前置信息 + 准备管线输入
           ↓
Step 1:  预览/构建（如 transfer_preview, tx.quote）
           ↓
Step 2:  签名/确认（如 wallet.sign_transaction）
           ↓
Step 3:  广播/提交（如 tx.send_raw_transaction）
           ↓
Verify:  查询最终状态确认成功
           ↓
Teardown: 无（管线操作通常不可逆）
```

| 适用业务 | 示例 |
|---------|------|
| DEX Transfer | 预览转账 → 签名 → 广播 → 确认 |
| DEX DApp | 构建 calldata → 签名 → 广播 → 确认 |

---

## 推断示例

### 历史协议夹具示例 1：合成 Spot 订单生命周期（不是现存 Skill）

```
工具: cex_spot_cancel_spot_order
  ↓
Schema 分析: required = { order_id, currency_pair }
  ↓
order_id 来自哪里？ → 找到 cex_spot_create_spot_order
  ↓
Pattern: A (Resource Lifecycle)
  ↓
自动构建 Setup:
  1. Call cex_spot_get_currency_pair("BTC_USDT") → 获取 min_base_amount, precision
  2. Call cex_spot_get_spot_tickers("BTC_USDT") → 获取 last price
  3. Call cex_spot_create_spot_order(buy, limit, last×0.7, min_amount) → 得到 order_id
  ↓
自动构建 Teardown:
  若 order_id 仍 open → Call cex_spot_cancel_spot_order(order_id)
```

### 历史协议夹具示例 2：合成换币响应（不是现存 Skill）

```
工具: cex_fc_create_fc_order
  ↓
Schema 分析: required = { sell_currency, buy_currency, amount }
  ↓
无 order_id 类资源依赖 → 不依赖其他 create 工具的产出
  ↓
Pattern: B (Instant Execution)
  ↓
自动构建 Setup:
  1. Call cex_fc_list_fc_currency_pairs(currency="BTC") → 获取 pair, sell_min_amount
  2. 准备参数: sell_currency="USDT", buy_currency="BTC", amount=sell_min_amount
  ↓
Teardown: none (闪兑不可逆)
```

### 示例 3: gate-exchange-unified — set_unified_mode

```
工具: cex_unified_set_unified_mode
  ↓
Schema 分析: required = { mode }
  ↓
工具前缀 set_ + 参数为配置类（mode）
  ↓
Pattern: C (State Transition)
  ↓
自动构建 Setup:
  1. Call cex_unified_get_unified_mode → 记录 original_mode
  ↓
自动构建 Teardown:
  1. Call cex_unified_set_unified_mode(mode=original_mode) → 恢复
```

### 示例 4: gate-dex-mcptransfer — transfer pipeline

```
Skill workflow 中的步骤链:
  tx.transfer_preview → wallet.sign_transaction → tx.send_raw_transaction
  ↓
步骤间有数据传递: preview → unsigned_tx → sign → signed_tx → broadcast
  ↓
Pattern: D (Multi-Step Pipeline)
  ↓
自动构建 Setup:
  1. Call wallet.get_addresses → 获取 sender_address
  2. Call wallet.get_token_list → 确认余额
  3. Call tx.gas → 获取 gas 估算
  ↓
Teardown: none (转账不可逆)
```

---

## Fixture 使用规范

### Fixture 复用规则

同一 Fixture 在同一测试批次内可复用，减少不必要的 Setup/Teardown：

```
场景 A（撤单）需要 open_order  ← Fixture Setup #1
场景 B（改单）需要 open_order  ← 如果 A 没有撤掉，可复用；否则重新 Setup #2
```

复用条件：
- Fixture 创建的资源仍处于预期状态（如 order 仍为 open）
- 后续场景不会破坏前序场景需要的状态
- 如果无法确定，每个场景独立 Setup

### 错误处理

| Fixture 阶段 | 错误类型 | 处理 |
|-------------|---------|------|
| Setup | 创建资源失败（API 错误） | 标记 FIXTURE_FAIL 🔧，跳过该场景 |
| Setup | 超时（>30s） | 标记 BLOCKED 🔒 |
| Execute | 场景执行失败 | 标记 FAIL，核实状态；只清理合成状态或仍在有效授权内的明确真实状态 |
| Teardown | 清理失败 | 标记 FAIL（Teardown 失败），记录残留；不能宣称完整场景通过 |
| Teardown | 资源已不存在 | 正常（被测试场景消费了），跳过 |

### 安全约束

| 约束 | 规则 |
|------|------|
| 环境限制 | 默认仅可强制隔离的合成依赖；真实集成单独授权（见 fixture-safety.md） |
| 金额限制 | 使用允许的最小金额 |
| 价格策略 | 限价单价格偏离市价 ≥30%，仅是合成输入，不能证明真实订单不会成交 |
| Teardown 强制 | 合成依赖清理自有状态；真实清理须在授权和已知状态内，不得因失败自动反向交易 |
| ID 传播 | Setup 产出的资源 ID 自动注入到后续测试步骤 |
| 超时保护 | 单个 Fixture 超过 30 秒未完成则标记 BLOCKED |
