---
name: skill-tester
version: "2026.3.9-5"
updated: "2026-03-09"
description: "Automated skill testing framework. Reads a target SKILL.md, generates full test cases (TSV), executes self-testing, and produces a Lark-compatible markdown test report. Supports layered testing (L0-L5), external document authentication, MCP authentication, production environment call detection (Gate.io highlighting), multi-session report merging, and multi-model performance comparison."
---

# Skill Tester — 自动化 Skill 测试框架

根据目标 Skill 定义自动生成测试用例、执行测试、输出Lark兼容的 Markdown 测试报告。
支持分层测试策略（L0-L5）、外部需求文档认证获取、多 session 报告合并、多模型对比。

## 触发条件

当用户提及以下意图时激活本 skill：
- "测试 xxx skill" / "test xxx skill"
- "生成测试用例" / "生成测试报告"
- "skill 质量评估" / "测试覆盖率"
- "skill 规范检查" / "skill 编写校验"
- "多模型对比测试" / "model comparison"

---

## 分层测试策略（L0 – L5）

skill-tester 按 6 个层级组织测试，优先级从高到低：

| 层级 | 名称 | 优先级 | 执行方式 | 说明 |
|------|------|--------|---------|------|
| **L0** | Skill 编写规范校验 | P0 | AI 自动 | 校验 SKILL.md 结构、YAML front-matter、必填字段、模块完整性 |
| **L1** | 文本 / 逻辑测试 | P0 | AI 自动 | 触发词→模块路由准确性、Prompt 理解、输出格式、工具调用链 |
| **L2** | 相似问法 & 多语言 | P1 | AI 自动 | 同义改写、口语化表达、英文 / 中英混合 Prompt 测试 |
| **L3** | 业务场景端到端 | P1 | 人 + AI | 真实业务流程（下单→查仓→平仓）、前置状态依赖 |
| **L4** | 跨 Skill 联动 | P2 | 人 + AI | 多 skill 协同（如先用现货 skill 查价格，再用合约 skill 下单） |
| **L5** | 多模型表现对比 | P2 | AI 自动 | 同一用例集在不同模型上执行，对比通过率和调用准确率 |

### 默认执行范围

- 用户未指定时，默认执行 **L0 + L1**（P0 优先级）
- 用户可通过 Prompt 指定层级：`"测试到 L3"` / `"只跑 L0 规范检查"`
- L3/L4 需要真实环境，自动提示用户确认

### 每层级触发示例

| 层级 | 用户 Prompt 示例 |
|------|-----------------|
| L0 | "检查 gate-exchange-futures 的 skill 编写规范" |
| L1 | "测试 gate-exchange-futures skill" |
| L2 | "帮我生成 gate-exchange-futures 的多语言测试用例" |
| L3 | "端到端跑一下合约下单到平仓的完整流程" |
| L4 | "测试现货查价 + 合约下单的联动场景" |
| L5 | "用 Claude 和 GPT 分别跑一遍测试用例对比下" |

---

## 执行流程总览

```
Step 0: 获取外部文档（可选）
    ↓
Step 1: 解析目标 Skill
    ↓
Step 2: 生成测试用例 TSV
    ↓
Step 3: 执行测试
    ↓
Step 4: 生成测试报告
    ↓
Step 5: 多 session 合并（可选）
```

---

## Step 0: 获取外部需求文档（可选）

当用户提供外部文档链接（飞书、Confluence、GitHub 等）作为需求补充时：

### 0.1 文档获取流程

```
用户提供 URL
    ↓
尝试获取文档内容
    ↓
成功 → 解析文档，提取补充测试需求
失败（401/403）→ 进入认证流程
```

### 0.2 认证错误处理

当访问外部文档返回 **401 Unauthorized** 或 **403 Forbidden** 时：

1. **识别文档来源**，按域名判定平台：

| 域名特征 | 平台 | 建议认证方式 |
|---------|------|-------------|
| `*.feishu.cn` / `*.larksuite.com` | 飞书 | Bearer Token 或 Cookie |
| `*.atlassian.net` / `*/confluence/*` | Confluence | Cookie 或 Personal Access Token |
| `github.com` / `raw.githubusercontent.com` | GitHub | `token ghp_xxx` 或 Cookie |
| 其他 | 未知平台 | Cookie |

2. **向用户请求凭证**，使用以下模板：

```
⚠️ 访问文档 {url} 时收到 {status_code} 错误，需要认证。

请提供以下任一凭证：
1. **Cookie**: 在浏览器中打开该文档 → F12 开发者工具 → Network 标签 → 复制请求头中的 Cookie 值
2. **Bearer Token**: 如果平台支持 API Token，提供 Token 即可

提示：凭证仅用于本次文档获取，不会持久化存储。
```

3. **使用凭证重试**，在请求头中携带认证信息
4. **安全原则**：
   - 凭证仅在当前 session 使用，不写入任何文件
   - 不在日志、报告中输出凭证内容
   - 获取文档后立即丢弃凭证

### 0.3 MCP 认证处理

在执行 L1/L2 测试前，需确认 MCP Server 可用。当 MCP 调用返回 `401 Unauthorized` 或 `403 Forbidden` 时，执行以下流程：

#### 0.3.1 自动检测

```
mcporter list <server-name> 2>&1
```

如果输出包含 `401` 或 `403`，进入认证处理流程。

#### 0.3.2 尝试自动认证

```
mcporter auth <server-name>
```

如果自动认证成功，继续测试。如果失败（仍返回 401/403），进入手动认证流程。

#### 0.3.3 手动认证 — 向用户请求凭证

向用户展示以下提示：

```
⚠️ MCP Server "{server-name}" 认证失败（{status_code}），需要手动提供凭证。

📋 获取 Token / Cookie 的步骤：
1. 浏览器打开 {base_url} 或对应平台页面并登录
2. 按 F12 → 打开开发者工具 → 切换到 Network 标签
3. 刷新页面，找到任意一个请求
4. 查看请求头中的：
   - Authorization 值（Bearer Token），格式如：Bearer eyJhbGci...
   - 或 Cookie 值，格式如：session=abc123; token=xyz789

🔧 获取后，请提供以下任一凭证：
- Bearer Token: 粘贴 Authorization 头的完整值
- Cookie: 粘贴 Cookie 头的完整值
```

> **注意**：`{base_url}` 从 MCP 配置中获取，可通过 `mcporter config get <server-name> --json` 查看。例如 gate 的 base_url 为 `https://api.gatemcp.ai`。

#### 0.3.4 注入凭证

收到用户提供的凭证后，使用以下命令注入：

- **Bearer Token**：
  ```bash
  mcporter config add <server-name> --header "Authorization=Bearer <token>"
  ```

- **Cookie**：
  ```bash
  mcporter config add <server-name> --header "Cookie=<cookie-value>"
  ```

注入后重新验证：
```bash
mcporter list <server-name>
```

如果工具列表正常返回，认证成功，继续测试。

#### 0.3.5 安全原则

- 凭证通过 mcporter 配置注入，仅影响当前环境
- 不在测试报告、日志或 TSV 文件中输出任何凭证内容
- 测试完成后提示用户可通过 `mcporter config remove` 清理凭证
- 如果使用 Gate 平台测试网（Testnet），优先引导用户使用测试网凭证

### 0.4 文档内容解析

获取成功后，从文档中提取：
- 补充的测试场景和边界条件
- 业务规则约束
- 特殊的预期行为要求
- 将提取的内容合并到 Step 1 的测试维度中

---

## Step 1: 解析目标 Skill

### 1.1 定位目标 Skill

向用户确认要测试的 skill 名称，然后读取：
- `skills/<skill-name>/SKILL.md` — 主定义文件
- `skills/<skill-name>/references/*.md` — 所有参考文件

### 1.2 L0 — Skill 编写规范校验

在解析阶段自动执行规范检查，校验项：

| # | 检查项 | 判定标准 | 严重级别 |
|---|--------|---------|---------|
| 1 | YAML front-matter | 包含 `name`, `version`, `updated`, `description` | 🔴 高 |
| 2 | 触发条件 | 存在 `## 触发条件` 或等价章节 | 🔴 高 |
| 3 | 执行流程 | 存在清晰的分步执行流程 | 🔴 高 |
| 4 | 模块定义 | 至少定义 1 个功能模块 | 🟡 中 |
| 5 | 错误处理 | 存在异常/错误处理章节 | 🟡 中 |
| 6 | 参考文件 | references 目录存在且有内容 | 🟢 低 |
| 7 | 工具映射 | MCP 工具或 API 调用有明确映射 | 🟡 中 |
| 8 | 示例 | 包含至少 1 个快速启动示例 | 🟢 低 |
| 9 | 变更操作二次确认 | 涉及资金/账户/用户数据变更的操作，SKILL 中明确要求用户二次确认后再执行 | 🔴 高 |

> **重点说明**：第 9 项为安全关键校验。任何会改变用户资产（下单、转账、提现等）、账户设置（修改杠杆、修改密码等）或个人信息的操作，SKILL 定义中必须包含"用户确认"环节。L0 阶段检查 SKILL.md 中是否有此定义，L1 阶段验证实际执行时确认步骤是否被正确触发。

规范校验结果记录在测试报告的独立章节中。

### 1.3 提取测试维度

从 SKILL.md 中提取以下信息，构建测试矩阵：

| 提取项 | 来源 | 用途 |
|--------|------|------|
| **模块列表** | `## Module overview` 或路由表 | 按模块组织用例 |
| **触发关键词** | `Trigger keywords` / `Trigger phrases` | 生成自然语言 Prompt |
| **MCP 工具映射** | `Tool Mapping` / 工作流中的 API 调用 | 预期行为 & MCP 工具列 |
| **错误处理表** | Error handling / 错误码表 | 异常场景用例 |
| **业务规则** | Trading rules / Domain knowledge | 边界条件用例 |
| **工作流步骤** | Workflow / Execution steps | 预期行为链 |

从 references 中补充提取：
- 每个操作的具体 Scenario 定义
- 参数校验规则与取值范围
- 错误码与对应处理逻辑

### 1.4 非交易类 Skill 适配

对于不涉及金融交易的 skill（如文档处理、数据查询、通知类 skill），调整测试重点：

| 维度 | 交易类 Skill | 非交易类 Skill |
|------|-------------|---------------|
| 用户确认 | 交易前必须确认 | 按 skill 定义判断 |
| 安全约束 | 仓位/金额限制 | 权限/数据安全 |
| 参数组合 | 方向/模式/杠杆 | 按 skill 参数空间生成 |
| 边界条件 | 极值/精度/限价保护 | 输入长度/格式/编码 |
| 错误码 | API 交易错误码 | skill 相关错误码 |

### 1.5 测试用例覆盖策略

每个模块生成以下类型的测试用例：

| 类型 | 说明 | 每模块最少 |
|------|------|-----------|
| **正常流程** | 标准参数的正向操作 | 2 条 |
| **参数变体** | 不同参数组合（模式/杠杆/订单类型等） | 2 条 |
| **边界条件** | 极值、精度、限价保护等 | 1 条 |
| **异常处理** | 余额不足、无持仓、参数错误等 | 2 条 |
| **组合场景** | 多步骤联动操作 | 1 条 |
| **相似问法** (L2) | 同一意图的不同表达方式 | 2 条 |
| **多语言** (L2) | 英文 / 中英混合 Prompt | 1 条 |

---

## Step 2: 生成测试用例 TSV

### 2.1 TSV 格式定义

生成的 TSV 文件包含以下列：

```
编号	模块	测试层级	测试场景	测试 Prompt	预期行为（Expected Behavior）	预期输出 / 关键校验点	涉及 MCP 工具	状态
```

各列说明见 [references/test-case-template.md](references/test-case-template.md)。

> 相比原版新增 `测试层级` 列，取值 L0–L5，用于标识用例所属层级。

### 2.2 Prompt 生成规则

- 使用**自然语言**，模拟真实用户提问方式
- 覆盖中文和英文混合表达（如"BTC_USDT 开多 1 张"）
- 包含隐式参数（如未指定模式时使用默认值）
- 包含模糊表达（如"帮我买点比特币合约"）
- 每个 Prompt 应可独立执行，不依赖上一条的状态

### 2.3 L2 — 相似问法 & 多语言 Prompt 生成

针对每个核心 Prompt，额外生成变体：

| 变体类型 | 示例（原始："帮我在 BTC_USDT 合约开多 1 张"） |
|---------|----------------------------------------------|
| **口语化** | "买一张比特币合约做多" |
| **简略** | "BTC 开多 1 张" |
| **详细** | "请在 Gate.io 的 BTC_USDT 永续合约市场帮我开一个多头仓位，数量为 1 张" |
| **英文** | "Open a long position on BTC_USDT futures, 1 contract" |
| **中英混合** | "help me open long BTC_USDT 合约 1 张" |
| **同义替换** | "做多一手 BTC 永续" |

### 2.4 预期行为编写规则

按执行顺序列出 MCP 工具调用链，格式：
```
1. tool_name(key_params) — 目的说明
2. tool_name(key_params) — 目的说明
...
```

### 2.5 输出文件

TSV 文件保存至项目根目录：`<skill-name>-test-cases.tsv`

---

## Step 3: 执行测试

### 3.1 测试执行模式

每条测试用例按以下流程执行：

```
1. 发送测试 Prompt（模拟用户输入）
2. 观察 agent 响应中的工具调用序列
3. 对比预期行为与实际行为
4. 记录结果状态和详细信息
```

### 3.2 结果状态定义

| 状态 | 符号 | 判定标准 |
|------|------|----------|
| **PASS** | ✅ | API 调用成功 + 业务逻辑正确 + 输出格式符合预期 |
| **PASS (有注意点)** | ⚠️ | API 成功但需 skill 特殊处理或存在优化空间 |
| **FAIL** | ❌ | 行为与预期不符 / 调用链错误 / 输出缺失关键信息 |
| **BLOCKED** | 🔒 | 因环境限制无法执行（余额不足/无持仓/无挂单等） |
| **SKIP** | ⏭ | 当前版本不支持的功能 |
| **存疑** | ❓ | API 语义待确认 / 行为需进一步验证 |

### 3.3 执行记录项

每条用例记录：
- 实际工具调用链（含参数和返回值摘要）
- 调用方式标记：`API` 直接调用 / `MCP` 通过 mcporter CLI
- 与预期行为的差异点
- Skill 定义覆盖情况（引用 SKILL.md 或 references 中的具体章节）

### 3.4 异常处理与容错

| 异常场景 | 处理策略 |
|---------|---------|
| MCP Server 不可用 | 标记 BLOCKED，提示用户检查 MCP 配置后继续 |
| MCP 认证失败 (401/403) | 执行 Step 0.3 MCP 认证处理流程，认证成功后继续测试 |
| 单条用例超时 | 标记 BLOCKED，记录超时信息，继续下一条 |
| 连续 5 条 BLOCKED | 暂停执行，提示用户确认是否继续 |
| API 限流 (429) | 等待 30 秒后重试 1 次，仍失败则标记 BLOCKED |
| SKILL.md 解析失败 | 中止测试，输出解析错误详情，请用户修复后重试 |
| TSV 文件已存在 | 提示用户选择：覆盖 / 追加 / 使用已有文件 |

详细执行指南见 [references/execution-guide.md](references/execution-guide.md)。

---

## Step 4: 生成测试报告

### 4.1 报告格式

生成飞书兼容的 Markdown 测试报告，保存至：`<skill-name>-test-report.md`

报告模板见 [references/test-report-template.md](references/test-report-template.md)。

### 4.2 报告结构

```markdown
# <Skill 名称> 测试报告

## 测试概要
| 项目 | 内容 |
|------|------|
| 测试日期 | YYYY-MM-DD |
| Skill 版本 | name version |
| 测试模型 | 当前使用的模型 |
| MCP 工具 | gateapi / 其他 |
| 测试层级 | L0-L1 / L0-L3 / 全量 |
| 测试用例总数 | N |

## L0 规范校验结果
### 校验项汇总表

## 测试结果总览
### 按模块统计表
### 按结果分类表
### 按测试层级统计表
### 调用方式统计（API vs MCP）

## 各模块详细结果
### Case N: 场景名称
- **层级**: L1
- **Prompt**: 测试 Prompt
- **测试步骤**: tool_call_1 ✅/❌ → tool_call_2 ✅/❌
- **结果**: 状态符号 状态 — 详细说明
- **调用方式**: API / MCP
- **API 验证**: 验证结果说明
- **SKILL 覆盖**: 引用 skill 定义中的具体章节

## 模型表现对比
| 模型 | 通过率 | 平均响应时间 | 工具调用准确率 | 备注 |
|------|--------|-------------|---------------|------|
| (当前模型) | xx% | - | - | 本次测试 |
| (待测模型) | - | - | - | 待填充 |

## 问题汇总与建议
### 发现的问题
### 改进建议
```

### 4.3 调用方式标记规则

在每个 Case 中标记调用方式：
- **API**: agent 直接通过 HTTP/REST 调用 API
- **MCP**: agent 通过 mcporter CLI 工具间接调用
- 在报告总览中增加调用方式统计表

### 4.4 模型表现列

报告末尾的「模型表现对比」表格：
- 当前测试填写实际使用的模型和通过率
- 其他模型列留空，标记"待填充"
- 后续可复用同一测试用例集，挂接不同模型后补充数据

#### 主流模型参考列表

| 模型 | 类型 | 建议优先级 |
|------|------|-----------|
| Claude 4 Opus / Sonnet | Anthropic | 推荐首测 |
| GPT-4o / GPT-4.1 | OpenAI | 推荐 |
| Gemini 2.5 Pro | Google | 推荐 |
| DeepSeek-V3 / R1 | DeepSeek | 建议 |
| Qwen-Max | Alibaba | 可选 |

### 4.5 精简报告模式

当用户要求"只看失败"或"精简报告"时：
- 报告开头标注 **「精简版 — 仅展示异常用例」**
- 只包含：测试概要 + L0 规范校验 + FAIL / 存疑用例详情 + 问题汇总
- 省略 PASS 用例的详细记录，仅保留统计数据

触发方式：
- `"生成精简测试报告"` / `"只看失败的用例"`
- `"简版报告"` / `"summary report"`

### 4.6 生产环境调用标记规则

测试执行过程中，若发现任何接口调用、MCP 工具调用、API 请求中包含 **Gate.io 生产环境** 相关标识，必须在报告中高亮提醒用户。

#### 检测关键词

| 类别 | 关键词/模式 |
|------|-----------|
| 域名 | `api.gateio.ws`, `gate.io`, `gateio.ws`, `www.gate.io` |
| MCP Server 名称 | `gateapi`, `gate` |
| API 路径 | 包含 `/api/v4/` 等 Gate.io 官方 API 路径 |
| MCP 工具名前缀 | `gateapi__` 开头的所有工具 |
| MCP 端点 | `api.gatemcp.ai` |

#### 标记方式

- 在每条涉及 Gate.io 的 Case 详情中，增加标记：`⚠️ 生产环境调用`
- 在报告总览区域（二、测试结果总览之后）新增 **「⚠️ 生产环境调用提醒」** 汇总区块
- 汇总表包含：涉及的 Case 编号、模块、调用的工具/接口名、操作类型（读/写）

#### 操作类型分级

| 操作类型 | 风险等级 | Case 标记 |
|---------|---------|----------|
| 写操作（下单/撤单/转账/修改设置等） | 🔴 高 | ⚠️ 生产环境 — 写操作 |
| 读操作（查询余额/行情/订单等） | 🟡 中 | ⚠️ 生产环境 — 读操作 |
| 无法判断 | 🟡 中 | ⚠️ 生产环境 — 待确认 |

#### 报告中呈现示例

```
## ⚠️ 生产环境调用提醒

> 本次测试中检测到 {gate_io_count} 条用例涉及 **Gate.io 生产环境** 调用，请核实是否为预期行为。
> 其中写操作 {write_count} 条（🔴 高风险），读操作 {read_count} 条（🟡 中风险）。

| Case | 模块 | 涉及工具/接口 | 操作类型 | 风险 |
|------|------|-------------|---------|------|
| Case 3 | 下单 | gateapi__create_spot_order | 写操作 | 🔴 |
| Case 7 | 查询 | gateapi__list_spot_accounts | 读操作 | 🟡 |
```

> **判定原则**：只要 Case 中出现上述关键词之一即标记，宁可多标不可漏标。若目标 Skill 本身就是 Gate.io 相关的（如 gate-exchange-spot），所有 Case 都会被标记，此时在提醒区块开头说明："本 Skill 为 Gate.io 业务 Skill，所有用例均涉及生产环境调用"。

---

## Step 5: 多 Session 报告合并（可选）

当测试因 session 限制分多次完成时：

### 5.1 临时报告

每个 session 结束时生成临时报告：`<skill-name>-test-report-part-N.md`
- 临时报告包含本次执行的用例范围和结果
- 记录已执行的最后一条用例编号

### 5.2 合并规则

在最后一个 session 中，执行报告合并：
1. 读取所有 `*-part-*.md` 临时报告
2. 合并用例结果，以最后一次执行结果为准（若同一用例被多次执行）
3. 重新计算统计数据（通过率、模块统计等）
4. 生成最终报告 `<skill-name>-test-report.md`
5. 提示用户是否删除临时报告

### 5.3 恢复执行

新 session 中继续测试：
- 用户说 `"继续测试 xxx skill"` 或 `"从第 N 条用例继续"`
- 读取已有的 TSV 和临时报告，确认断点
- 从未执行的用例继续

---

## 快速启动示例

### 示例 1：默认测试（L0 + L1）

用户输入：
> 帮我测试 gate-exchange-futures 这个 skill

执行流程：
1. 读取 `skills/gate-exchange-futures/SKILL.md` 及 `references/*.md`
2. 执行 L0 规范校验
3. 提取 4 个模块（开仓/平仓/撤单/改单）+ 数据查询 + 综合场景
4. 按覆盖策略生成约 60-80 条 L1 测试用例
5. 输出 `gate-exchange-futures-test-cases.tsv`
6. 逐条执行测试，记录结果
7. 输出 `gate-exchange-futures-test-report.md`

### 示例 2：含多语言测试（L0-L2）

用户输入：
> 测试 gate-exchange-futures 到 L2，包含多语言和相似问法

### 示例 3：精简报告

用户输入：
> 帮我测试 gate-exchange-futures，只输出失败的用例

### 示例 4：多模型对比

用户输入：
> 用 Claude 和 GPT 分别跑一遍 gate-exchange-futures 的测试用例

### 示例 5：带外部文档

用户输入：
> 测试 xxx skill，需求文档在这里：https://xxx.feishu.cn/docx/xxx

---

## 参考文件

- [测试用例模板与字段说明](references/test-case-template.md)
- [测试报告完整模板](references/test-report-template.md)
- [测试执行详细指南](references/execution-guide.md)
