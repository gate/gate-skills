---
name: gate-futures-trading
version: "2026.3.5-1"
updated: "2026-03-05"
description: "Gate.io 合约交易全能助手。涵盖开仓、平仓、撤单、改单及行情监控。Use this skill for any futures trading operation including opening/closing positions, canceling/amending orders, and monitoring market risks. Trigger phrases: '开仓', '平仓', '撤单', '改单', '反手', '全平', '爆仓监控', '资金费率', 'open position', 'close position', 'cancel order', 'amend order', 'liquidation', 'funding rate'."
---

# Gate.io Futures Trading Suite

本 Skill 是 Gate.io 合约交易的统一入口，内部集成了五个核心子模块，根据用户意图自动路由到相应的工作流。

## 📦 子模块概览

| 模块 | 功能描述 | 触发关键词                                   |
|------|---------|-----------------------------------------|
| **🚀 开仓 (Open)** | 限价/市价开多开空，自动处理全/逐仓切换 | `开多`, `开空`, `下单`, `buy`, `sell`, `open` |
| **🛑 平仓 (Close)** | 全平、部分平仓、反手开仓 | `平仓`, `全平`, `反手`, `close`, `reverse`    |
    | **❌ 撤单 (Cancel)** | 撤销指定订单或批量撤单 | `撤单`, `取消`, `cancel`, `revoke`          |
| **✏️ 改单 (Amend)** | 修改挂单价格或数量 | `改单`, `修改`, `amend`, `modify`           |

## 🔄 智能路由规则 (Routing Rules)

系统将根据用户输入的**意图**和**关键词**自动加载对应子流程：

| 用户意图场景 | 匹配关键词示例 | 路由目标                                                    |
|--------------|----------------|---------------------------------------------------------|
| **新开仓位** | "BTC 开多 1 张", "市价开空 ETH", "10 倍杠杆做多" | Read `references/open-position.md`, follow its workflow |
| **减平仓位** | "全平 BTC", "平掉一半", "反手做空", "一键清仓" | Read `references/close-position.md`, follow its workflow |
| **管理挂单** | "撤掉那个买单", "撤销所有订单", "我有哪些挂单" | Read `references/cancel-order.md`, follow its workflow |
| **调整挂单** | "把价格改成 60000", "修改订单数量" | Read `references/amend-order.md`, follow its workflow |
| **模糊指令** | "帮我操作一下合约", "查看我的持仓" | **追问模式**: 先查询持仓/挂单，再引导用户选择操作                            |

## ⚙️ 执行工作流 (Execution Workflow)

### 1. 意图识别与参数提取
- 分析用户输入，确定目标模块（Open/Close/Cancel/Amend）。
- 提取关键参数：`contract` (合约), `side` (方向), `size` (数量), `price` (价格), `leverage` (杠杆)。
- **缺失处理**: 如果关键参数缺失（如未指定数量），进入**追问模式**。

### 2. 前置检查 (Pre-Flight Checks)
在执行具体操作前，统一执行以下检查：
- **合约有效性**: 调用 `get_futures_contract` 确认合约存在且未下架。
- **账户状态**: 检查余额是否充足，是否有冲突持仓（如切换仓位模式时）。
- **风险控制**:
    - 限价单检查是否超出 `order_price_deviate` 保护范围。
    - 大额头寸提示分批下单。

### 3. 模块执行逻辑

#### 🚀 Module A: 开仓 (Open Position)
1. **数量单位转换**: 若用户未以「张」为单位，先调用 `get_futures_contract` 获取 `mark_price`、`quanto_multiplier`，再按对应公式转换为张数后下单：
   - **以 U（USDT 金额）为单位**: 张 = u ÷ 标记价格 ÷ 合约乘数
   - **以币种（基础资产数量，如 BTC、ETH）为单位**: 张 = 币种 ÷ 合约乘数
   - 转换结果按合约 `order_size_min` 与精度要求取整/舍入。
2. **模式确认**: 默认全仓 (`cross`)，若用户指定逐仓则检查杠杆倍数。
3. **模式切换**: 若当前模式与目标不符且无持仓，自动调用 `update_futures_position_cross_mode`。
4. **杠杆设置**: 逐仓模式下调用 `update_futures_position_leverage`。
5. **下单前确认**: 向用户展示**最终下单信息**（合约、方向、数量/张、价格或市价、仓位模式、杠杆、预估保证金/强平价等），并请求确认（如「请确认以上信息无误后回复“确认”再下单」）。**用户确认后再执行下单**。
6. **下单执行**: 调用 `create_futures_order` (市价单自动设 `tif=ioc`, `price=0`)。
7. **结果验证**: 调用 `get_futures_position` 确认仓位已建立。

#### 🛑 Module B: 平仓 (Close Position)
1. **持仓查询**: 调用 `get_futures_position` 获取当前 `size` 和方向。
2. **策略分支**:
    - **全平**: 先查持仓再逐笔平仓（`get_futures_position` + `create_futures_order` reduce_only），或使用合约全平流程。
    - **部分平**: 计算反向数量，调用 `create_futures_order` (`reduce_only=true`)。
    - **反手**: 无专用 MCP。先 `create_futures_order`（`reduce_only=true`）平掉当前仓，再 `create_futures_order` 开反向仓（两步完成）。
3. **结果验证**: 确认剩余仓位符合预期。

#### ❌ Module C: 撤单 (Cancel Order)
1. **订单定位**:
    - 有 ID: 直接定位。
    - 无 ID: 调用 `list_futures_orders` 展示列表供用户选择。
2. **执行撤单**:
    - 单笔: `cancel_futures_order`。
    - 批量: `cancel_futures_batch_orders` 或 `cancel_all_futures_orders` (支持按合约过滤)。
3. **状态确认**: 验证 `finish_as` == `cancelled`。

#### ✏️ Module D: 改单 (Amend Order)
1. **订单检查**: 确认订单状态为 `open`。
2. **精度校验**: 根据合约配置校验新价格/数量的精度。
3. **执行修改**: 调用 `amend_futures_order` 更新 price 或 size。


## 📝 统一回复模板 (Report Template)

所有操作完成后，必须输出标准化结论：

## 🛡️ 安全与风控规则 (Safety Rules)

### 二次确认
- **开仓**：必须先展示**最终下单信息**（合约、方向、数量、价格/市价、模式、杠杆、预估强平价与保证金），待用户确认后再执行 `create_futures_order`。示例话术：*「请确认以上信息无误后回复“确认”再下单。」*
- **全平、反手、批量撤单**等高风险操作，必须先展示影响范围并请求用户确认。
- 示例话术：*「确定要平掉所有仓位吗？」*、*「将撤销该合约下全部挂单，是否继续？」*

### 风险警示
- **开仓时**：强制显示预估强平价格和保证金占用。
- **市价单**：必须提示滑点风险。

### 错误处理
| 错误码 | 处理方式 |
|--------|----------|
| `BALANCE_NOT_ENOUGH` | 提示充值或降低杠杆/数量。 |
| `PRICE_TOO_DEVIATED` | 自动计算合法价格区间并建议用户调整。 |
| `POSITION_NOT_EMPTY`（切换模式时） | 提示先平仓。 |

