# 测试用例 TSV 模板与字段说明

## TSV 列定义

| 列名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `编号` | 整数 | ✅ | 全局唯一编号，从 1 开始递增 |
| `模块` | 文本 | ✅ | 功能模块名（如：开仓、平仓、撤单、改单） |
| `测试层级` | 文本 | ✅ | L0–L5，标识用例所属测试层级 |
| `测试场景` | 文本 | ✅ | 场景简述，≤20 字 |
| `测试 Prompt` | 文本 | ✅ | 自然语言提问词，模拟真实用户输入 |
| `预期行为（Expected Behavior）` | 文本 | ✅ | MCP 工具调用链及关键参数，按执行顺序编号 |
| `预期输出 / 关键校验点` | 文本 | ✅ | 判定通过/失败的核心检查项 |
| `涉及 MCP 工具` | 文本 | ✅ | 逗号分隔的 MCP 工具名列表 |
| `状态` | 文本 | ⬜ | 留空，执行测试后填入结果状态 |

### 测试层级取值说明

| 取值 | 含义 | 自动生成 |
|------|------|---------|
| L0 | Skill 编写规范校验 | ✅ |
| L1 | 文本 / 逻辑测试 | ✅ |
| L2 | 相似问法 & 多语言 | ✅ |
| L3 | 业务场景端到端 | ⬜（需人工补充或确认） |
| L4 | 跨 Skill 联动 | ⬜（需人工补充或确认） |
| L5 | 多模型对比 | ✅（复用 L1 用例，切换模型执行） |

---

## Prompt 生成规范

### 语言风格
- 以**第一人称命令式**为主："帮我…" / "查一下…" / "我想…"
- 混合中英文：交易对用英文（BTC_USDT），操作用中文
- 参数直接融入自然语言，不使用 JSON 或 key=value 格式

### 覆盖维度

每个模块的 Prompt 需覆盖以下维度：

```
必选参数完整 → 可选参数变体 → 隐式默认值 → 模糊表达 → 异常/边界 → 相似问法 → 多语言
```

#### 示例：开仓模块

| 维度 | 示例 Prompt | 层级 |
|------|------------|------|
| 必选参数完整 | 帮我在 BTC_USDT 合约开多 1 张，限价 65000 | L1 |
| 可选参数变体 | 市价开空 ETH_USDT 合约 2 张，逐仓 10 倍 | L1 |
| 隐式默认值 | BTC_USDT 开多 1 张（未指定价格 → 市价，未指定模式 → 全仓） | L1 |
| 模糊表达 | 帮我买点比特币合约 | L1 |
| 异常/边界 | BTC_USDT 开多，价格 100000（超出限价保护范围） | L1 |
| 口语化变体 | 买一张比特币合约做多 | L2 |
| 简略变体 | BTC 开多 1 张 | L2 |
| 英文变体 | Open a long position on BTC_USDT futures, 1 contract | L2 |
| 中英混合变体 | help me open long BTC_USDT 合约 1 张 | L2 |

---

## L2 — 相似问法 & 多语言 Prompt 生成规则

### 生成策略

针对每个 L1 核心 Prompt，生成以下变体：

| 变体类型 | 说明 | 每个核心 Prompt 生成数 |
|---------|------|---------------------|
| **口语化** | 使用日常口语表达，省略正式术语 | 1 条 |
| **简略** | 最精简的表达，省略非必要信息 | 1 条 |
| **详细** | 加入完整上下文和详细参数描述 | 0-1 条 |
| **英文** | 完整英文 Prompt | 1 条 |
| **中英混合** | 关键词英文 + 操作中文（或反之） | 0-1 条 |
| **同义替换** | 使用同义词/近义词替换关键动词 | 0-1 条 |

### 变体示例

原始 Prompt（L1）：`"帮我在 BTC_USDT 合约开多 1 张"`

| 变体类型 | 生成的 L2 Prompt |
|---------|-----------------|
| 口语化 | 买一张比特币合约做多 |
| 简略 | BTC 开多 1 张 |
| 详细 | 请在 Gate.io 的 BTC_USDT 永续合约市场帮我开一个多头仓位，数量为 1 张 |
| 英文 | Open a long position on BTC_USDT futures, 1 contract |
| 中英混合 | help me open long BTC_USDT 合约 1 张 |
| 同义替换 | 做多一手 BTC 永续 |

### L2 变体的预期行为

- 所有 L2 变体应与对应 L1 原始 Prompt 有**相同的预期行为**
- 在 TSV 中，L2 用例的"预期行为"列直接引用对应 L1 用例编号：`"同 Case #{L1编号}"`
- 判定标准一致：只要 agent 正确理解意图并执行相同的工具调用链，即为 PASS

---

## 非交易类 Skill 的 Prompt 生成适配

对于非交易类 skill，按以下维度生成 Prompt：

| 维度 | 替代策略 | 示例 |
|------|---------|------|
| 必选参数 | 按 skill 定义的核心参数生成 | "查询 xxx 的文档" |
| 参数变体 | 按 skill 参数空间枚举 | "按日期/按类别 查询" |
| 边界条件 | 输入长度/格式/编码 | 超长文本、特殊字符、空值 |
| 异常处理 | skill 相关错误码 | 权限不足、资源不存在 |
| 相似问法 | 同义改写（通用） | 同 L2 生成规则 |
| 多语言 | 英文/中英混合（通用） | 同 L2 生成规则 |

---

## 参数组合矩阵

对于支持多参数的操作，生成参数组合矩阵：

```
方向:    [多/空]
模式:    [全仓/逐仓]
价格类型: [限价/市价]
TIF:     [gtc/fok/ioc/poc]
杠杆:    [默认/自定义]
```

不需要全量组合（指数爆炸），选取有业务意义的组合，每个参数至少在一条用例中被覆盖。

---

## 预期行为编写规范

### 格式
```
1. tool_name(key_param=value) — 目的
2. tool_name(key_param=value) — 目的
3. 展示摘要，请用户确认
4. tool_name(key_param=value) — 执行操作
5. tool_name() — 验证结果
```

### 规则
- 仅列出关键参数，省略默认值
- 明确标注需要用户确认的步骤
- 错误处理场景列出预期错误码
- 条件分支用"若...则..."描述

### L0 用例的预期行为

L0 用例不涉及 MCP 调用，预期行为描述为校验结果：
```
1. 读取 SKILL.md — 解析文件内容
2. 检查 YAML front-matter — 验证必填字段
3. 输出校验结果 — 列出通过/不通过项
```

---

## 预期输出 / 关键校验点编写规范

校验点分为：

| 类型 | 示例 |
|------|------|
| **返回值** | 返回订单 ID、状态 open |
| **格式要求** | 展示杠杆倍数和预估强平价 |
| **业务规则** | 未经用户确认不得下单 |
| **错误处理** | 提示"余额不足"并展示所需保证金 |
| **安全约束** | 拒绝单笔超过仓位 50% 的操作 |
| **规范校验** (L0) | YAML front-matter 包含所有必填字段 |
| **意图理解** (L2) | 正确识别简略/口语化/英文表达的用户意图 |

---

## TSV 示例

```tsv
编号	模块	测试层级	测试场景	测试 Prompt	预期行为（Expected Behavior）	预期输出 / 关键校验点	涉及 MCP 工具	状态
1	规范校验	L0	YAML front-matter 校验	（自动校验，无用户 Prompt）	1. 读取 SKILL.md；2. 解析 YAML front-matter；3. 检查 name/version/updated/description 字段	所有必填字段存在且非空	N/A	
2	规范校验	L0	触发条件检查	（自动校验，无用户 Prompt）	1. 读取 SKILL.md；2. 搜索"触发条件"或等价章节；3. 验证触发词列表非空	存在触发条件章节，且至少定义 1 个触发词	N/A	
3	开仓	L1	限价开多（全仓）	帮我在 BTC_USDT 合约开多 1 张，限价 65000	1. get_futures_contract 查合约信息；2. update_futures_position_cross_mode(cross=true) 切全仓；3. get_position 查当前杠杆；4. 展示下单摘要，请用户确认；5. create_futures_order(size=1, price=65000, tif=gtc)；6. get_futures_position 验证持仓	返回订单ID、状态 open（挂单中），展示杠杆倍数和预估强平价；未经用户确认不得下单	get_futures_contract, update_futures_position_cross_mode, get_position, create_futures_order, get_futures_position	
4	开仓	L1	市价开空（逐仓 10x）	市价开空 ETH_USDT 合约 2 张，逐仓 10 倍	1. get_futures_contract；2. update_futures_position_cross_mode(cross=false) 切逐仓；3. update_futures_position_leverage(leverage=10)；4. 展示下单摘要，请用户确认；5. create_futures_order(size=-2, price=0, tif=ioc)；6. get_futures_position 验证	返回成交均价、订单状态 finished；显示强平价格和当前仓位；提示市价单滑点风险	get_futures_contract, update_futures_position_cross_mode, update_futures_position_leverage, create_futures_order, get_futures_position	
5	开仓	L2	口语化开多	买一张比特币合约做多	同 Case #3	正确识别"比特币"→ BTC_USDT，"做多"→ 开多意图	get_futures_contract, create_futures_order	
6	开仓	L2	英文开多	Open a long position on BTC_USDT futures, 1 contract	同 Case #3	正确理解英文 Prompt 并执行相同工具调用链	get_futures_contract, create_futures_order	
7	开仓	L2	中英混合开多	help me open long BTC_USDT 合约 1 张	同 Case #3	正确理解中英混合表达	get_futures_contract, create_futures_order	
```

---

## 每模块用例数量指引

| 类型 | 层级 | 每模块最少 | 说明 |
|------|------|-----------|------|
| 正常流程 | L1 | 2 条 | 标准参数的正向操作 |
| 参数变体 | L1 | 2 条 | 不同参数组合 |
| 边界条件 | L1 | 1 条 | 极值、精度、限价保护等 |
| 异常处理 | L1 | 2 条 | 余额不足、无持仓、参数错误等 |
| 组合场景 | L1 | 1 条 | 多步骤联动操作 |
| 口语化变体 | L2 | 1 条 | 同一意图的口语化表达 |
| 简略变体 | L2 | 1 条 | 最精简的表达方式 |
| 英文变体 | L2 | 1 条 | 完整英文 Prompt |
| 中英混合 | L2 | 0-1 条 | 按需生成 |
