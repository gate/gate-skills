# Gate.io Futures Cancel Order — Scenarios & Prompt Examples

Gate.io 合约撤单场景示例和预期行为。

## Scenario 1: 查询挂单并选择撤销（推荐流程）

**Context**: 用户想撤单但不知道订单 ID，需要先查看有哪些挂单。

**Prompt Examples**:
- "帮我撤单"
- "我有哪些挂单"
- "撤销订单"（不带 ID）
- "查看我的挂单"

**Expected Behavior**:
1. Detect no order_id provided → query mode
2. Call `list_futures_orders(settle="usdt", status="open")`
3. Display order list to user with numbered options
4. Wait for user selection
5. Execute cancellation based on selection

**Response Template (查询阶段)**:
```
您当前有 3 个未完成订单：

| # | 合约 | 方向 | 数量 | 价格 | 未成交 | 下单时间 |
|---|------|------|------|------|--------|----------|
| 1 | BTC_USDT | 买入 | 1 | 50000 | 1 | 10:30:25 |
| 2 | BTC_USDT | 卖出 | 2 | 80000 | 2 | 10:35:12 |
| 3 | ETH_USDT | 买入 | 10 | 2800 | 10 | 11:02:45 |

请告诉我您要撤销哪个订单？
- 输入序号（如 "1" 或 "1,2"）
- 输入 "全部" 撤销所有订单
```

---

## Scenario 2: 根据序号撤销订单

**Context**: 用户看到订单列表后，选择序号撤销。

**Prompt Examples**:
- "撤销第 1 个"
- "1"
- "撤销 1 和 3"
- "1,2"

**Expected Behavior**:
1. Parse user selection: sequence number(s)
2. Map to order_id from the displayed list
3. Call `cancel_futures_order` for each selected order
4. Output cancellation results

**Response Template**:
```
撤单成功！

已撤销订单 #1:
- 订单ID: 94294117235059656
- 合约: BTC_USDT
- 方向: 买入
- 价格: 50000
- 结果: ✅ 已撤销
```

---

## Scenario 3: 撤销所有订单（批量撤单）

**Context**: 用户想一次性撤销所有挂单。

**Prompt Examples**:
- "撤销所有订单"
- "全部撤单"
- "取消全部挂单"
- "清空所有订单"
- "全部"（在订单列表后）

**Expected Behavior**:
1. Confirm with user: "确定要撤销所有订单吗？"
2. 先 `list_futures_orders(settle="usdt", status="open")` 得到有挂单的合约；对每个有挂单的合约调用 `cancel_all_futures_orders(settle="usdt", contract=合约)`（**必填入参**: `settle`, `contract`）。
3. Output batch cancellation results

**Response Template**:
```
确定要撤销所有订单吗？当前共 3 个挂单。

（用户确认后）

批量撤单完成！

| 订单ID | 合约 | 方向 | 价格 | 结果 |
|--------|------|------|------|------|
| 94294117235059656 | BTC_USDT | 买入 | 50000 | ✅ 已撤销 |
| 94294117235059657 | BTC_USDT | 卖出 | 80000 | ✅ 已撤销 |
| 94294117235059658 | ETH_USDT | 买入 | 2800 | ✅ 已撤销 |

✅ 共撤销 3 个订单
```

---

## Scenario 4: 撤销指定合约的所有订单

**Context**: 用户只想撤销某个合约的挂单。

**Prompt Examples**:
- "撤销 BTC_USDT 的所有订单"
- "取消 ETH 合约的挂单"
- "撤销所有 BTC 订单"

**Expected Behavior**:
1. Parse contract: `BTC_USDT`
2. Call `cancel_all_futures_orders(settle="usdt", contract="BTC_USDT")`（**必填入参**: `settle`, `contract`；可选: `side`, `exclude_reduce_only`, `text`）
3. Output results for that contract only

**Response Template**:
```
已撤销 BTC_USDT 的所有订单：

| 订单ID | 方向 | 价格 | 结果 |
|--------|------|------|------|
| 94294117235059656 | 买入 | 50000 | ✅ 已撤销 |
| 94294117235059657 | 卖出 | 80000 | ✅ 已撤销 |

✅ 共撤销 2 个订单
```

---

## Scenario 5: 通过订单 ID 直接撤单

**Context**: 用户知道订单 ID，直接撤销。

**Prompt Examples**:
- "撤销订单 94294117235059656"
- "取消订单 94294117235059656"
- "cancel order 94294117235059656"

**Expected Behavior**:
1. Parse order_id: `94294117235059656`
2. Call `cancel_futures_order(settle="usdt", order_id="94294117235059656")`
3. Verify `finish_as == "cancelled"`
4. Output cancellation result

**Response Template**:
```
撤单成功！

订单ID: 94294117235059656
合约: BTC_USDT
方向: 买入
价格: 50000
状态: finished
结果: ✅ 已撤销
```

---

## Scenario 6: 通过自定义 text 撤单

**Context**: 用户下单时使用了自定义 text 标识，现在想通过该标识撤单。

**Prompt Examples**:
- "撤销订单 t-my-order-001"
- "取消 t-my-order-001"

**Expected Behavior**:
1. Detect order_id starts with `t-`, use as text identifier
2. Call `cancel_futures_order(settle="usdt", order_id="t-my-order-001")`
3. Output cancellation result

**Response Template**:
```
撤单成功！

自定义标识: t-my-order-001
订单ID: 94294117235059656
合约: BTC_USDT
结果: ✅ 已撤销
```

---

## Scenario 7: 没有待撤销订单

**Context**: 用户想撤单，但当前没有挂单。

**Prompt Examples**:
- "帮我撤单"
- "撤销所有订单"

**Expected Behavior**:
1. Call `list_futures_orders(settle="usdt", status="open")`
2. Return empty list
3. Inform user no orders to cancel

**Response Template**:
```
当前没有未完成的挂单，无需撤销。

如需下单，可以说：
- "BTC_USDT 开多 1 张，限价 50000"
```

---

## Scenario 8: 撤销已成交订单（失败）

**Context**: 用户尝试撤销一个已经成交的订单。

**Prompt Examples**:
- "撤销订单 94294117235059656"（该订单已成交）

**Expected Behavior**:
1. Call `cancel_futures_order(settle="usdt", order_id="94294117235059656")`
2. Receive ORDER_NOT_FOUND error
3. Output failure message

**Response Template**:
```
撤单失败

订单ID: 94294117235059656
原因: 订单不存在或已完成

可能的情况：
1. 订单已全部成交
2. 订单已被撤销
3. 订单 ID 错误

建议查看订单历史确认订单状态。
```

---

## Scenario 9: 只撤销买单或卖单

**Context**: 用户只想撤销特定方向的订单。

**Prompt Examples**:
- "撤销所有买单"
- "取消全部卖单"
- "撤销 BTC 的买单"

**Expected Behavior**:
1. Parse side: `bid` (买) or `ask` (卖)
2. 按合约撤单时调用 `cancel_all_futures_orders(settle="usdt", contract=合约, side="bid")`（**必填**: `settle`, `contract`；**可选**: `side`, `exclude_reduce_only`, `text`）。若撤销「所有合约的某方向」需先 list 再对每个合约带 side 调用。
3. Output results

**Response Template**:
```
已撤销所有买单：

| 订单ID | 合约 | 价格 | 结果 |
|--------|------|------|------|
| 94294117235059656 | BTC_USDT | 50000 | ✅ 已撤销 |
| 94294117235059658 | ETH_USDT | 2800 | ✅ 已撤销 |

✅ 共撤销 2 个买单
```
