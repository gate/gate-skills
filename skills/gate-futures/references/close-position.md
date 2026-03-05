# Gate.io Futures Close Position — Scenarios & Prompt Examples

Gate.io 合约平仓场景示例和预期行为。

## Scenario 1: 全平仓（一键清仓）

**Context**: 用户想平掉所有仓位，不管具体持有多少。

**Prompt Examples**:
- "全平"
- "一键平仓"
- "平掉所有仓位"
- "close all positions"

**Expected Behavior**:
1. Call `list_futures_positions(settle="usdt")` 获取当前全部持仓。
2. 向用户展示持仓列表，确认话术：「确定要平掉所有仓位吗？」
3. 用户确认后，对每个有持仓的合约：调用 `create_futures_order(settle="usdt", contract=合约, size=反向数量, reduce_only=true, ...)` 市价平仓（开多仓用负 size、开空仓用正 size，tif="ioc", price="0"）。
4. 再次查询 `list_futures_positions` 验证已无持仓（或仅剩零头）。
5. Output close result with realized PnL

**Response Template**:
```
确定要平掉所有仓位吗？当前持有：
- BTC_USDT 多仓 5 张，未实现盈亏 +$200

（用户确认后）

全部平仓完成！

| 合约 | 方向 | 数量 | 成交价 | 实现盈亏 |
|------|------|------|--------|---------|
| BTC_USDT | 多仓 | 5 张 | $52,000 | +$200 |

✅ 当前无持仓
```

---

## Scenario 2: 部分平仓（指定数量）

**Context**: 用户只想平掉部分仓位，保留剩余仓位。

**Prompt Examples**:
- "平掉 2 张"
- "平掉 BTC 的 3 张"
- "减仓 1 张"
- "部分平仓，平 2 张多仓"

**Expected Behavior**:
1. Query current position to verify sufficient size
2. Calculate close size (negative for long, positive for short)
3. Call `create_futures_order(size=-2, reduce_only=true, tif="ioc")`
4. Verify remaining position

**Response Template**:
```
部分平仓成功！

| 项目 | 值 |
|------|-----|
| 合约 | BTC_USDT |
| 平仓数量 | 2 张 |
| 成交价 | $52,000 |
| 剩余仓位 | 多仓 3 张 |

✅ 平仓完成，保留 3 张多仓
```

---

## Scenario 3: 平一半仓位

**Context**: 用户想平掉一半仓位。

**Prompt Examples**:
- "平一半"
- "平掉一半仓位"
- "减仓 50%"

**Expected Behavior**:
1. Query current position: size = 10
2. Calculate half: close_size = 5
3. Call `create_futures_order(size=-5, reduce_only=true)`
4. Verify remaining position = 5

**Response Template**:
```
已平掉一半仓位！

| 项目 | 原仓位 | 当前仓位 |
|------|--------|---------|
| 数量 | 10 张 | 5 张 |
| 方向 | 多仓 | 多仓 |
| 成交价 | - | $52,000 |

✅ 平仓完成，剩余 50% 仓位
```

---

## Scenario 4: 反手开仓（多转空）

**Context**: 用户持有多仓，想反手做空。

**Prompt Examples**:
- "反手"
- "反手做空"
- "从多转空"
- "多头反手空头"
- "平多开空"

**Expected Behavior**:
1. Query current position via `get_futures_position`: long +5
2. 展示反手方案，请用户确认（含预估强平价/保证金）
3. 用户确认后：先 `create_futures_order(settle, contract, size="-5", reduce_only=true, price="0", tif="ioc")` 市价平多仓，再 `create_futures_order(..., size="-5", price="0", tif="ioc")` 市价开 5 张空（无 reduce_only）
4. Verify new position via `get_futures_position`: short -5

**Response Template**:
```
反手开仓成功！

| 项目 | 原仓位 | 新仓位 |
|------|--------|--------|
| 方向 | 多仓 | 空仓 |
| 数量 | 5 张 | 5 张 |
| 均价 | $50,000 | $52,000 |

✅ 已从多仓反手至空仓
```

---

## Scenario 5: 反手开仓（空转多）

**Context**: 用户持有空仓，想反手做多。

**Prompt Examples**:
- "反手做多"
- "空转多"
- "平空开多"

**Expected Behavior**:
1. Query current position via `get_futures_position`: short -3
2. 展示反手方案，请用户确认后：先 `create_futures_order(..., size="3", reduce_only=true, price="0", tif="ioc")` 市价平空仓，再 `create_futures_order(..., size="3", price="0", tif="ioc")` 市价开 3 张多
3. Verify new position via `get_futures_position`: long +3

**Response Template**:
```
反手开仓成功！

| 项目 | 原仓位 | 新仓位 |
|------|--------|--------|
| 方向 | 空仓 | 多仓 |
| 数量 | 3 张 | 3 张 |

✅ 已从空仓反手至多仓
```

---

## Scenario 6: 反手开仓（指定数量不同）

**Context**: 用户想反手但新仓位数量与原仓位不同。

**Prompt Examples**:
- "反手做空 3 张"（当前多仓 5 张）
- "平掉多仓，开 2 张空"

**Expected Behavior**:
1. Query current position via `get_futures_position`: long +5
2. 展示反手方案（平 5 张多 → 开 3 张空），请用户确认后：先 `create_futures_order(..., size="-5", reduce_only=true, ...)` 市价全平多仓，再 `create_futures_order(..., size="-3", ...)` 市价开 3 张空
3. Verify new position via `get_futures_position`: short -3

**Response Template**:
```
反手开仓成功！

| 项目 | 原仓位 | 新仓位 |
|------|--------|--------|
| 方向 | 多仓 | 空仓 |
| 数量 | 5 张 | 3 张 |

✅ 已反手至空仓 3 张（原多仓 5 张已全部平仓）
```

---

## Scenario 7: 查询后选择平仓方式

**Context**: 用户想平仓但没有说明具体方式。

**Prompt Examples**:
- "帮我平仓"
- "我想平仓"
- "平仓"

**Expected Behavior**:
1. Query current position
2. Display position info and ask user to choose
3. Execute based on user selection

**Response Template (查询阶段)**:
```
当前仓位：

| 合约 | 方向 | 数量 | 开仓价 | 当前价 | 未实现盈亏 |
|------|------|------|--------|--------|-----------|
| BTC_USDT | 多仓 | 5 张 | $50,000 | $52,000 | +$200 |

请问您要：
1. **全平** - 平掉所有 5 张
2. **部分平仓** - 输入数量，如 "平 2 张"
3. **反手** - 平掉多仓，开空仓

请选择或输入具体操作：
```

---

## Scenario 8: 没有仓位时平仓

**Context**: 用户想平仓但当前没有仓位。

**Prompt Examples**:
- "平掉 BTC 的仓位"

**Expected Behavior**:
1. Query position: size = 0
2. Inform user no position to close

**Response Template**:
```
当前没有 BTC_USDT 的持仓，无需平仓。

如需开仓，可以说：
- "BTC_USDT 开多 1 张，市价"
- "BTC_USDT 开空 1 张，限价 50000"
```

---

## Scenario 9: 平仓数量超过持仓

**Context**: 用户想平仓的数量超过实际持仓。

**Prompt Examples**:
- "平掉 10 张"（实际只有 5 张）

**Expected Behavior**:
1. Query position: size = 5
2. Detect 10 > 5, suggest alternatives
3. Wait for user decision

**Response Template**:
```
您当前只有 5 张多仓，无法平掉 10 张。

请选择：
1. 全平 - 平掉所有 5 张
2. 修改数量 - 输入 1-5 张之间的数量

请输入您的选择：
```

---

## Scenario 10: 平掉指定合约的所有仓位

**Context**: 用户想平掉某个合约的所有仓位。

**Prompt Examples**:
- "平掉 BTC 的仓位"
- "平掉 ETH 的所有仓位"
- "close BTC position"

**Expected Behavior**:
1. Query position for specific contract
2. Close all positions for that contract
3. Verify and report result

**Response Template**:
```
已平掉 BTC_USDT 的所有仓位！

| 项目 | 值 |
|------|-----|
| 合约 | BTC_USDT |
| 原仓位 | 多仓 5 张 |
| 成交价 | $52,000 |
| 实现盈亏 | +$200 |

✅ BTC_USDT 仓位已清空
```

---

## Scenario 11: 多个合约同时全平

**Context**: 用户持有多个合约的仓位，想全部平掉。

**Prompt Examples**:
- "全部平仓"
- "平掉所有合约"

**Expected Behavior**:
1. Query all positions
2. Display all positions and confirm
3. Close all contracts

**Response Template**:
```
确定要平掉所有仓位吗？当前持有：

| 合约 | 方向 | 数量 | 未实现盈亏 |
|------|------|------|-----------|
| BTC_USDT | 多仓 | 5 张 | +$200 |
| ETH_USDT | 空仓 | 10 张 | -$50 |

（用户确认后）

全部平仓完成！

✅ 已平掉 2 个合约的仓位
总实现盈亏: +$150
```
