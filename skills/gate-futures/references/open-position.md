# Gate.io Futures Open Position — Scenarios & Prompt Examples

Gate.io 合约开仓场景示例和预期行为。

## 数量单位转换 (Unit Conversion)

开仓时若用户未以「张」为单位，须先转换为 **张** 再下单：

| 用户单位 | 转换公式 | 说明 |
|----------|----------|------|
| **U（USDT 金额）** | 张 = u ÷ 标记价格 ÷ 合约乘数 | 无杠杆或全仓时：`size_contracts = u / mark_price / quanto_multiplier` |
| **U（USDT 金额）+ 杠杆** | 张 = u × 杠杆 ÷ 标记价格 ÷ 合约乘数 | 有杠杆时：`size_contracts = u * leverage / mark_price / quanto_multiplier` |
| **币种（基础资产数量，如 BTC、ETH）** | 张 = 币种 ÷ 合约乘数 | `size_contracts = base_amount / quanto_multiplier` |

- **数据来源**: 调用 `get_futures_contract(settle, contract)` 获取 `mark_price`、`quanto_multiplier`。
- **精度**: 转换后的张数需满足合约的 `order_size_min` 及数量精度，不足最小下单量时提示用户。

## 下单前确认 (Pre-Order Confirmation)

**开仓前必须**先向用户展示**最终下单信息**，待用户确认后再调用 `create_futures_order`。

- **杠杆查询**：根据**仓位上的合约 + 下单方向**查询当前杠杆——调用 `get_position(settle, contract)`，若有该方向持仓则取该仓位杠杆展示；无该方向持仓则取该合约下该方向的杠杆设置或默认杠杆并展示。
- **展示内容**：合约、方向（开多/开空）、数量（张）、价格（限价或“市价”）、仓位模式（全仓/逐仓）、**杠杆**（由上一步查询得到）、预估保证金、预估强平价格；市价单另提示滑点风险。
- **确认话术**：*「请确认以上信息无误后回复“确认”再下单。」* 仅当用户明确确认（如回复“确认”“可以”“下单”等）后再执行下单。

## Scenario 1: 限价单开多仓（全仓模式）

**Context**: 用户希望在 BTC_USDT 合约以指定价格开多仓，使用全仓模式。

**Prompt Examples**:
- "帮我在 BTC_USDT 合约开多 1 张，限价 65000"
- "BTC_USDT 永续合约，全仓模式，开多 1 张，价格 65000"
- "limit buy 1 BTC_USDT futures at 65000"

**Expected Behavior**:
1. Fetch contract info via `get_futures_contract(settle="usdt", contract="BTC_USDT")`
2. Switch to cross mode via `update_futures_position_cross_mode(settle="usdt", cross=true)`
3. Query leverage via `get_position(settle="usdt", contract="BTC_USDT")`（按合约+开多方向），取该方向仓位/杠杆。
4. **展示最终下单信息**（合约、方向、数量、价格、模式、**杠杆**、预估强平价/保证金），请用户确认。
5. 用户确认后，Place order via `create_futures_order(settle="usdt", contract="BTC_USDT", size="1", price="65000", tif="gtc")`
6. Query position via `get_futures_position(settle="usdt", contract="BTC_USDT")`
7. Output 开仓结果报告

**Response Template**:
```
开仓成功！

订单ID: 123456789
合约: BTC_USDT
方向: 开多 (buy)
数量: 1 张
价格: 65000 USDT
状态: open (挂单中)
模式: 全仓
杠杆: 10x（据当前仓位查询）
```

---

## Scenario 2: 市价单开空仓（逐仓 10x）

**Context**: 用户希望以市价立即开空仓，使用逐仓模式并设置 10 倍杠杆。

**Prompt Examples**:
- "市价开空 ETH_USDT 合约 2 张，逐仓 10 倍"
- "ETH_USDT 合约，逐仓模式，10 倍杠杆，市价开空 2 张"
- "market sell 2 ETH_USDT futures with 10x leverage"

**Expected Behavior**:
1. Fetch contract info via `get_futures_contract(settle="usdt", contract="ETH_USDT")`
2. Switch to isolated mode via `update_futures_position_cross_mode(settle="usdt", cross=false)`
3. Set leverage via `update_futures_position_leverage(settle="usdt", contract="ETH_USDT", leverage="10")`
4. Place market order via `create_futures_order(settle="usdt", contract="ETH_USDT", size="-2", price="0", tif="ioc")`
5. Query position via `get_futures_position(settle="usdt", contract="ETH_USDT")`
6. Output 成交结果和仓位信息

**Response Template**:
```
市价开空成功！

订单ID: 123456790
合约: ETH_USDT
方向: 开空 (sell)
数量: 2 张
成交均价: 3500.50 USDT
状态: finished (已成交)
模式: 逐仓 10x

当前仓位:
- 持仓: -2 张
- 开仓均价: 3500.50
- 强平价格: 3850.00
```

---

## Scenario 3: FOK 订单全部成交或取消

**Context**: 用户希望使用 FOK（Fill or Kill）订单类型，确保订单要么全部成交，要么全部取消，避免部分成交。

**Prompt Examples**:
- "FOK 限价买入 BTC_USDT 1 张，价格 65000"
- "BTC_USDT 合约，FOK 订单，开多 1 张，65000"
- "fill or kill buy 1 BTC_USDT at 65000"

**Expected Behavior**:
1. Fetch contract info via `get_futures_contract(settle="usdt", contract="BTC_USDT")`
2. Place FOK order via `create_futures_order(settle="usdt", contract="BTC_USDT", size="1", price="65000", tif="fok")`
3. If market depth insufficient, return ORDER_FOK error
4. If successful, output 完全成交结果

**Error Case Response**:
```
FOK 订单未能成交

原因: 市场深度不足，无法全部成交
建议: 
1. 减小订单数量
2. 调高买入价格
3. 改用 GTC 或 IOC 订单类型
```

---

## Scenario 4: 价格超出限价保护

**Context**: 用户输入的价格与当前市场价格偏离过大，触发交易所限价保护机制。

**Prompt Examples**:
- "BTC_USDT 开多，价格 100000"（当前价格 65000，偏离过大）

**Expected Behavior**:
1. Fetch contract info via `get_futures_contract(settle="usdt", contract="BTC_USDT")`
2. Calculate price limit: `mark_price * (1 + order_price_deviate)`
3. Detect price 100000 exceeds limit
4. Return PRICE_TOO_DEVIATED error with suggested price range

**Response Template**:
```
下单失败：价格超出限价保护范围

当前标记价格: 65000 USDT
限价保护范围: 45500 - 84500 USDT
您的下单价格: 100000 USDT

建议: 请将价格调整到 84500 USDT 以内
```

---

## Scenario 5: 余额不足

**Context**: 用户账户保证金余额不足以支持开仓所需的保证金要求。

**Prompt Examples**:
- "开多 BTC_USDT 100 张"（账户余额不足）

**Expected Behavior**:
1. Fetch contract info via `get_futures_contract(settle="usdt", contract="BTC_USDT")`
2. Place order via `create_futures_order(settle="usdt", contract="BTC_USDT", size="100", ...)`
3. Receive BALANCE_NOT_ENOUGH error
4. Output 余额不足提示和建议

**Response Template**:
```
下单失败：保证金不足

所需保证金: 6500 USDT
当前可用: 1000 USDT

建议:
1. 减小开仓数量
2. 充值更多 USDT
3. 提高杠杆倍数（当前 10x，可提高到 20x）
```

---

## Scenario 6: 切换模式失败（有持仓）

**Context**: 用户尝试切换全逐仓模式，但当前有未平仓的仓位，导致切换失败。

**Prompt Examples**:
- "切换到全仓模式"（当前逐仓模式有持仓）
- "全仓开多 BTC_USDT"（当前逐仓模式有持仓）

**Expected Behavior**:
1. Switch mode via `update_futures_position_cross_mode(settle="usdt", cross=true)`
2. Receive POSITION_NOT_EMPTY error
3. Query current position via `get_futures_position(settle="usdt", contract="BTC_USDT")`
4. Output 切换失败提示和当前持仓信息

**Response Template**:
```
切换模式失败：当前有持仓

当前持仓: BTC_USDT 多仓 5 张
当前模式: 逐仓 10x

建议: 请先平掉所有仓位，再切换全逐仓模式
```

---

## Scenario 7: POC（Post Only）订单

**Context**: 用户希望以 Maker 身份挂单，节省手续费，如果订单会立即成交（作为 Taker）则取消。

**Prompt Examples**:
- "POC 限价买入 BTC_USDT 1 张，价格 64000"
- "只做 Maker，BTC_USDT 开多 1 张，64000"
- "post only buy 1 BTC_USDT at 64000"

**Expected Behavior**:
1. Fetch contract info via `get_futures_contract(settle="usdt", contract="BTC_USDT")`
2. Place POC order via `create_futures_order(settle="usdt", contract="BTC_USDT", size="1", price="64000", tif="poc")`
3. If order would immediately match, return ORDER_POC error
4. If order hangs as Maker, output 挂单成功结果

**Response Template**:
```
挂单成功！（Post Only）

订单ID: 123456791
合约: BTC_USDT
方向: 开多 (buy)
数量: 1 张
价格: 64000 USDT
状态: open (挂单中)
角色: Maker

注意: 此订单只会作为 Maker 成交，享受 Maker 手续费优惠
```

---

## Scenario 8: 按 U（USDT 金额）开仓

**Context**: 用户以 USDT 金额（U）指定开仓规模，需先转换为张数再下单。

**Prompt Examples**:
- "BTC_USDT 开多 1000U"
- "用 500 U 市价开空 ETH_USDT"
- "开多 2000 USDT 的 BTC 合约"

**Expected Behavior**:
1. Fetch contract via `get_futures_contract(settle="usdt", contract="BTC_USDT")`，取得 `mark_price`、`quanto_multiplier`。
2. 计算张数：无杠杆时 张 = u ÷ mark_price ÷ quanto_multiplier；**有杠杆时** 张 = u × 杠杆 ÷ mark_price ÷ quanto_multiplier（按合约精度与 `order_size_min` 处理）。
3. 若张数 &lt; order_size_min，提示「金额换算后不足最小下单量」。
4. 按所得张数执行开仓流程（模式切换、杠杆、`create_futures_order` 等）。
5. 报告中可同时展示「约 xxx U」与「yy 张」。
