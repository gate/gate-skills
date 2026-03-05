# Gate.io Futures Amend Order — Scenarios & Prompt Examples

Gate.io 合约改单场景示例和预期行为。

## MCP 工具与入参

| 工具名 | 用途 | 必填入参 | 可选入参 |
|--------|------|----------|----------|
| **amend_futures_order** | 修改单笔订单 | `settle`, `order_id` | `price`, `size`, `amend_text`, `text` |
| **amend_futures_batch_orders** | 批量改单 | `settle`, `orders`（JSON 数组，每项含 order_id 及 price/size 等） | — |

- 仅支持修改**未成交挂单**（status=open）；已成交或已撤订单会报错。
- 改价/改量前可先调用 `get_futures_contract(settle, contract)` 校验价格/数量精度（`order_price_round`, `order_size_min` 等）。

## 改单前确认

执行 `amend_futures_order` 前，建议先展示**当前订单信息**与**修改后参数**，请用户确认后再提交。示例话术：*「将把价格从 49000 改为 50000，确认修改吗？」*

---

## Scenario 1: 仅修改价格

**Context**: 用户有一个未成交的挂单，想调整挂单价格。

**Prompt Examples**:
- "把订单 94294117235059656 的价格改成 50000"
- "修改订单价格为 50000，订单号 94294117235059656"
- "amend order 94294117235059656 price to 50000"

**Expected Behavior**:
1. Parse order_id: `94294117235059656`, new_price: `50000`
2. （可选）调用 `get_futures_order(settle="usdt", order_id="94294117235059656")` 获取当前订单；调用 `get_futures_contract` 校验价格精度
3. 展示修改前后对比（当前价格 → 新价格），请用户确认
4. 用户确认后调用 `amend_futures_order(settle="usdt", order_id="94294117235059656", price="50000")`
5. 校验返回 `price == "50000"`，Output 修改成功结果

**Response Template**:
```
订单修改成功！

订单ID: 94294117235059656
合约: BTC_USDT
价格: 49000 → 50000
数量: 1（未修改）
状态: open
```

---

## Scenario 2: 仅修改数量

**Context**: 用户想调整挂单数量，价格保持不变。

**Prompt Examples**:
- "把订单 94294117235059656 的数量改成 10"
- "修改订单数量为 10 张"
- "订单 94294117235059656 数量改成 10"

**Expected Behavior**:
1. Parse order_id: `94294117235059656`, new_size: `10`
2. （可选）调用 `get_futures_order` 获取当前订单；调用 `get_futures_contract` 校验数量精度（order_size_min 等）
3. 展示修改前后对比（当前数量 → 新数量），请用户确认
4. 用户确认后调用 `amend_futures_order(settle="usdt", order_id="94294117235059656", size="10")`
5. 校验返回 `size == "10"`，Output 修改成功结果

**Response Template**:
```
订单修改成功！

订单ID: 94294117235059656
合约: BTC_USDT
价格: 50000（未修改）
数量: 5 → 10
状态: open
```

---

## Scenario 3: 同时修改价格和数量

**Context**: 用户想同时调整价格和数量。

**Prompt Examples**:
- "订单 94294117235059656 价格改成 51000，数量改成 8"
- "修改订单 94294117235059656 价格 51000 数量 8"
- "amend order 94294117235059656 price 51000 size 8"

**Expected Behavior**:
1. Parse order_id, new_price: `51000`, new_size: `8`
2. （可选）获取当前订单与合约精度，展示修改前后对比，请用户确认
3. 用户确认后调用 `amend_futures_order(settle="usdt", order_id="94294117235059656", price="51000", size="8")`
4. 校验返回的 price、size，Output 修改成功结果

**Response Template**:
```
订单修改成功！

订单ID: 94294117235059656
合约: BTC_USDT
价格: 50000 → 51000
数量: 5 → 8
状态: open
```

---

## Scenario 4: 通过自定义 text 定位订单后修改

**Context**: 用户下单时使用了自定义 text（如 `t-my-order-001`），现在想通过该标识修改订单。API 改单必填为 `order_id`（数字 ID），若用户只提供 text 需先查到对应 order_id。

**Prompt Examples**:
- "把订单 t-my-order-001 的价格改成 48000"
- "修改 t-my-order-001 价格为 48000"

**Expected Behavior**:
1. 若用户只提供 text：先 `list_futures_orders(settle="usdt", status="open")`，在返回列表中按 `text` 字段匹配得到 `order_id`
2. 展示当前订单与修改后参数，请用户确认
3. 调用 `amend_futures_order(settle="usdt", order_id="<查到的数字ID>", price="48000")`（若 API 支持以 text 作为 order_id 传参则可直接传 `t-my-order-001`，以实际 MCP 为准）
4. Output 修改成功结果

**Response Template**:
```
订单修改成功！

自定义标识: t-my-order-001
订单ID: 94294117235059656
价格: 50000 → 48000
状态: open
```

---

## Scenario 5: 修改已成交订单（失败）

**Context**: 用户尝试修改一个已经成交的订单。

**Prompt Examples**:
- "修改订单 94294117235059656 价格为 50000"（该订单已成交）

**Expected Behavior**:
1. 调用 `amend_futures_order(settle="usdt", order_id="94294117235059656", price="50000")`
2. 接口返回 ORDER_NOT_FOUND、ORDER_FINISHED 或类似错误（订单已成交/已撤/不存在）
3. Output 无法修改提示与可能原因

**Response Template**:
```
修改失败

订单ID: 94294117235059656
原因: 订单不存在或已完成

可能的情况：
1. 订单已全部成交
2. 订单已被撤销
3. 订单 ID 错误
```

---

## Scenario 6: 价格不符合精度

**Context**: 用户输入的价格不符合合约精度要求。

**Prompt Examples**:
- "把订单价格改成 50000.123456"（精度超出限制）

**Expected Behavior**:
1. 建议先调用 `get_futures_contract(settle="usdt", contract="BTC_USDT")` 获取 `order_price_round`，校验用户输入价格精度
2. 若精度不符，直接提示建议价格（如 50000.12），避免无效请求；若仍提交则调用 `amend_futures_order` 会收到 INVALID_PARAM_VALUE 等错误
3. Output 精度错误提示与合约要求

**Response Template**:
```
修改失败

订单ID: 94294117235059656
输入价格: 50000.123456
错误: 价格精度不符合要求

BTC_USDT 合约价格精度要求：0.01
建议价格: 50000.12
```

---

## Scenario 7: 未提供任何修改参数

**Context**: 用户说要修改订单但没有说明修改什么。

**Prompt Examples**:
- "修改订单 94294117235059656"

**Expected Behavior**:
1. Detect missing price and size parameters
2. Ask user to specify what to modify

**Response Template**:
```
请告诉我您想修改什么？

订单ID: 94294117235059656

可修改项：
1. 价格 (price)
2. 数量 (size)

示例："把价格改成 50000" 或 "数量改成 10"
```

---

## Scenario 8: 无订单 ID 时先查再改

**Context**: 用户想改单但未提供订单 ID，需先查挂单列表再选择修改哪一笔。

**Prompt Examples**:
- "帮我改一下挂单价格"
- "修改我的订单"（未给 ID）

**Expected Behavior**:
1. 调用 `list_futures_orders(settle="usdt", status="open")` 展示当前挂单列表
2. 引导用户选择要修改的订单（序号或合约+方向），或让用户补充订单 ID
3. 用户指定订单及新价格/数量后，按 Scenario 1～3 流程执行（含确认后再 amend）

---

## Scenario 9: 批量改单

**Context**: 用户想一次性修改多笔挂单（如统一调价或调量）。

**Prompt Examples**:
- "把 1 号订单价格改成 50000，2 号改成 50100"
- "批量修改：订单 A 价格 50000，订单 B 价格 50200"

**Expected Behavior**:
1. 解析多笔订单的 order_id 及对应新 price/size
2. 展示每笔修改前后对比，请用户确认
3. 用户确认后调用 `amend_futures_batch_orders(settle="usdt", orders="[{\"order_id\":\"...\",\"price\":\"50000\"},...]")`（JSON 数组格式以实际 MCP 要求为准）
4. Output 每笔改单结果
