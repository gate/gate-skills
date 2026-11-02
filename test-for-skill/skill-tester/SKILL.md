---
name: skill-tester
version: "2026.11.2-1"
updated: "2026-11-02"
description: "Automated skill testing framework. Reads a target SKILL.md, generates full test cases (TSV), executes self-testing, and produces a Lark-compatible markdown test report. Supports layered testing (L0-L5), batch walkthrough for all skills, external document authentication, MCP authentication, production environment call detection (Gate.io highlighting), multi-session report merging, and multi-model performance comparison."
---

# Skill Tester — 自动化 Skill 测试框架

根据目标 Skill 定义自动生成测试用例、执行测试、输出Lark兼容的 Markdown 测试报告。
支持分层测试策略（L0-L5）、外部需求文档认证获取、多 session 报告合并、多模型对比。

## Gate CEX single-target routing

For `gate-cex-trade`, `gate-cex-earn`, `gate-cex-assets`, `gate-cex-subaccount`, `gate-cex-affiliate`, or `gate-cex-bot`, follow [gate-cex-skill-audit](../../gate-cex-skill-audit/SKILL.md), including its bundled scenario and safety protocols. Reuse the layered review, scenario/evidence, report, and synthetic fixture concepts there; no legacy directory is needed when that auditor is installed independently.

For these targets, do not execute the MCP fixture inference, credential-injection, automatic order setup/teardown, or vendor-specific conversation runner below. A private address or test-like server name is not proof of isolation. Start with one target and static inspection; record actual isolated behavior only when it was safely observed. Other legacy targets retain their existing workflow, subject to the user's current safety and authorization instructions.

## 触发条件

当用户提及以下意图时激活本 skill：
- "测试 xxx skill" / "test xxx skill"
- "生成测试用例" / "生成测试报告"
- "skill 质量评估" / "测试覆盖率"
- "skill 规范检查" / "skill 编写校验"
- "多模型对比测试" / "model comparison"
- "全量走查所有 skill" / "batch test all skills"
- "快速走查 skills 目录" / "walkthrough all skills"
- "对所有 skill 做场景走查" / "全量场景测试"

---

## 分层测试策略（L0 – L5）

skill-tester 按 6 个层级组织测试，优先级从高到低：

| 层级 | 名称 | 优先级 | 执行方式 | 说明 |
|------|------|--------|---------|------|
| **L0** | Skill 编写规范校验 | P0 | AI 自动 | 校验 SKILL.md 结构、YAML front-matter、必填字段、模块完整性 |
| **L1** | 文本 / 逻辑测试 | P0 | AI 自动 | 触发词→模块路由准确性、Prompt 理解、输出格式、工具调用链（只读工具） |
| **L1.5** | 写操作端到端（Fixture） | P0 | AI 自动 | 自动构建前置状态 → 执行写操作场景 → 校验 → 清理。仅可强制隔离的合成依赖默认可用 |
| **L2** | 相似问法 & 多语言 | P1 | AI 自动 | 同义改写、口语化表达、英文 / 中英混合 Prompt 测试 |
| **L3** | 业务场景端到端 | P1 | 人 + AI | 真实业务流程（下单→查仓→平仓）、前置状态依赖 |
| **L4** | 跨 Skill 联动 | P2 | 人 + AI | 多 skill 协同（如先用现货 skill 查价格，再用合约 skill 下单） |
| **L5** | 多模型表现对比 | P2 | AI 自动 | 同一用例集在不同模型上执行，对比通过率和调用准确率 |

### 默认执行范围

- 用户未指定时，默认执行 **L0 + L1**（P0 优先级）
- 用户可通过 Prompt 指定层级：`"测试到 L3"` / `"只跑 L0 规范检查"` / `"跑 L1.5 写操作测试"`
- **L1.5** 默认仅在可强制隔离的合成依赖执行，真实集成需单独授权；缺证据为 BLOCKED
- L3/L4 需要真实环境，自动提示用户确认

### 每层级触发示例

| 层级 | 用户 Prompt 示例 |
|------|-----------------|
| L0 | "检查 gate-info-coinanalysis 的 skill 编写规范" |
| L1 | "测试 gate-info-coinanalysis skill" |
| L1.5 | "测试 gate-dex-trade 的合成写操作场景，不发起真实交易" |
| L2 | "帮我生成 gate-info-coinanalysis 的多语言测试用例" |
| L3 | "在隔离依赖上运行 Info 查询到报告的完整流程" |
| L4 | "在隔离依赖上测试 Info 研究与 News 事件的联动" |
| L5 | "用 Claude 和 GPT 分别跑一遍测试用例对比下" |
| **Batch** | "全量走查所有 skill" / "对所有 skill 做场景走查" |

### 全量走查模式（Batch Walkthrough）

全量走查是对 `skills/` 目录下**所有 Skill** 进行 L0 + L1 快速场景走查的批量模式。与单 Skill 测试的区别：

| 维度 | 单 Skill 测试 | 全量走查 |
|------|-------------|---------|
| 对象 | 1 个指定 Skill | skills/ 下全部 Skill |
| 用例来源 | 自动生成（含参数组合/边界/异常） | 直接从 scenarios.md 的 Prompt Examples 提取 |
| TSV 文件 | 生成完整 TSV | 不生成 TSV（轻量直驱） |
| 每场景用例数 | 8-12 条（含 L2 变体） | 1 条（取第一个 Prompt Example） |
| 报告粒度 | 详细到每条用例 | 每场景一行（场景/工具/结果/摘要） |
| 输出文件 | `<skill>-test-report.md` | `all-skills-walkthrough-report.md` |

全量走查的目标是**快速验证每个场景的核心路径是否可走通**，而非深度测试。发现问题的场景后，可再用单 Skill 测试做深入排查。

详细执行指南见 [references/batch-walkthrough-guide.md](references/batch-walkthrough-guide.md)。

---

## 执行流程总览

### 单 Skill 测试流程

```
Step 0: 获取外部文档（可选）
    ↓
Step 0.5: 环境检测（Fixture 门控）
    ↓
Step 1: 解析目标 Skill
    ↓
Step 2: 生成测试用例 TSV
    ↓
Step 3: 执行测试（含 L1.5 Fixture 自动构建）
    ↓
Step 4: 生成测试报告
    ↓
Step 5: 多 session 合并（可选）
```

### Batch Walkthrough 执行流程（全量走查）

当用户触发全量走查时，执行以下流程：

```
Phase 0: 扫描 skills/ 目录 + 环境检测
    ↓
Phase 1: 逐 Skill 提取场景 Prompt + 预期行为
    ↓
Phase 2: 逐 Skill 逐场景模拟执行（核心）
    ↓
Phase 3: 汇总生成全量走查报告
```

#### Phase 0 — 扫描与环境准备

1. 列出 `skills/` 下所有含 `SKILL.md` 的子目录
2. 对每个 Skill 读取 YAML frontmatter（name / version）
3. 收集每个 Skill 的场景数（从 `references/` 中所有 `## Scenario` 标题计数）
4. 执行 Step 0.5 环境检测（判定测试/生产环境）
5. **输出走查清单表**，请用户确认后再执行

走查清单中的版本、场景数和总数必须从当前文件提取，不复制历史数字。例如：

```
| # | Skill | 版本 | 场景数 | 架构 | 状态 |
|---|-------|------|--------|------|------|
| 1 | gate-info-coinanalysis | 从 frontmatter 读取 | 按当前场景计数 | 当前入口 | 待走查 |
| 2 | gate-dex-trade | 从 frontmatter 读取 | 按当前场景计数 | 当前入口 | 待走查 |
```

用户可在此阶段排除不需要走查的 Skill（如 `"跳过 affiliate"`）。

#### Phase 1 — 逐 Skill 提取场景测试 Prompt

对每个 Skill 的每个 Scenario：

1. 从 `**Prompt Examples**` / `**Prompt examples**` 中取**第一个**作为测试 Prompt
2. 从 `**Expected Behavior**` / `**Expected behavior**` 中提取预期 MCP 工具调用链
3. 判断该场景是读操作还是写操作（写操作在生产环境标记 BLOCKED）

不生成 TSV 文件——全量走查模式为轻量直驱，直接进入 Phase 2 执行。

#### Phase 2 — 逐场景模拟执行（核心步骤）

这是全量走查的核心。对每个场景执行以下流程：

```
读取场景的 Prompt Example
    ↓
Agent 按目标 Skill 定义处理该 Prompt：
    ├─ 判断意图，路由到正确模块
    ├─ 调用预期的 MCP 工具链（实际调用 MCP）
    ├─ 检查返回数据是否合理
    └─ 写操作场景：验证是否要求用户确认
    ↓
对比实际行为 vs 预期行为（Expected Behavior）：
    ├─ 工具调用顺序是否匹配？
    ├─ 关键参数是否正确？
    └─ 写操作是否要求了用户确认？
    ↓
判定结果：PASS / FAIL / BLOCKED
    ↓
记录摘要（1-2 行，如 "BTC 100920 USDT, 5 档深度正常"）
```

**执行约束**：
- 写操作场景在走查模式下**不实际执行写入**，仅验证 Agent 是否正确构建了调用参数并要求用户确认，然后标记为 `PASS (逻辑校验)`
- 读操作场景**实际调用 MCP 工具**，验证返回数据是否合理
- 每个 Skill 完成后输出该 Skill 的小结行，便于用户追踪进度
- 连续 5 个场景 BLOCKED 时暂停，提示用户确认

**分批策略**：总场景数超过 50 时，建议分 Session 执行，每 Session 走查 3-5 个 Skill。每个 Session 结束时生成临时报告 `all-skills-walkthrough-report-part-N.md`。

#### Phase 3 — 生成全量走查报告

报告保存至项目根目录：`all-skills-walkthrough-report.md`

报告结构参照 [references/batch-walkthrough-guide.md](references/batch-walkthrough-guide.md) 中的模板：

1. **走查概要**：日期 / 环境 / Skill 数 / 场景总数 / 汇总统计表
2. **L0 规范校验汇总**：所有 Skill 的 9 项校验简表
3. **全场景走查大表**：每 Skill 一个子表，每行一个场景（#/场景名/MCP 工具/结果/实际数据摘要）
4. **BLOCKED 场景分析**：按原因分类汇总
5. **问题汇总与建议**：P0/P1/P2 分级

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

## Step 0.5: Fixture 隔离与授权门禁

完整执行 [Fixture isolation and authorization contract](references/fixture-safety.md)。
自动 Fixture 仅使用可强制隔离的合成依赖；真实集成须另有明确授权，覆盖端点、账号、
权限、数据及 Setup/Execute/Verify/Teardown。地址、HTTP、端口和 server 名都不授予写入权限。
任一证据缺失时写场景 BLOCKED，零业务写入；静态推演与合成事件分别记录。

---

## L1.5: 写操作端到端测试（Fixture 机制）

### 核心概念

Fixture（测试夹具）是指在测试目标场景前，**自动构建所需的前置状态**，测试完成后**自动清理**。

```
[Fixture Setup]   自动创建前置状态（如挂一个远离市价的限价单）
       ↓
[Execute]          执行目标场景（如撤单、改单）
       ↓
[Verify]           校验结果（订单是否被撤销、价格是否修改）
       ↓
[Teardown]         清理残留状态（如撤掉未使用的订单）
```

### Fixture 自动推断

skill-tester **自动分析** Skill 定义，为任何业务域的写操作场景构建 Fixture，无需 Skill 开发者做额外配置：

```
自动推断流程：
  1. 提取 SKILL.md 中所有 MCP 工具引用 → 按前缀分类读/写
  2. 对每个写工具，读 MCP 工具 JSON Schema → 分析必填参数依赖
  3. 自动识别 Pattern（A/B/C/D）
  4. 自动构建 Setup 参数（安全价格、最小金额等）
  5. 自动匹配 Teardown 工具
```

### 通用 Fixture 模式（Pattern）

每个 Fixture 属于以下 4 种模式之一，详见 [references/fixture-templates.md](references/fixture-templates.md)：

| Pattern | 名称 | 自动识别条件 | 适用场景 |
|---------|------|-------------|---------|
| A | Resource Lifecycle | 写工具需要另一个 create 工具的产出 | 撤单/改单/还贷/平仓 |
| B | Instant Execution | 写工具不依赖其他写工具的产出 | 闪兑/市价单/DEX Swap |
| C | State Transition | 工具为 set_*/update_* 且操作配置类字段 | 杠杆/模式/抵押设置 |
| D | Multi-Step Pipeline | Workflow 中有链式调用关系 | DEX Transfer/DApp |

### 自动推断核心逻辑

**1. 参数依赖分析** — 读取写工具的 JSON Schema，识别参数来源：

| 参数名模式 | 推断依赖 |
|-----------|---------|
| `order_id` | 需要先 `create_*_order` |
| `trigger_order_id` | 需要先 `create_*_triggered_order` |
| `contract` + `size`（平仓） | 需要先开仓 |
| 无资源 ID 依赖 | 可直接执行 |

**2. 安全参数自动构建** — 从同 Skill 的读工具获取安全值：

| 参数类型 | 安全策略 |
|---------|---------|
| 价格 | 偏离市价 ≥30%（buy: ×0.7, sell: ×1.3） |
| 数量/金额 | 使用交易规则中的最小允许值 |
| 触发价 | 偏离市价 ≥50% |
| 交易对 | 使用 Skill 最常引用的（如 BTC_USDT） |

**3. Teardown 自动匹配** — 根据 create 工具找对应 cancel/delete 工具：

| 创建工具模式 | 自动匹配清理工具 |
|-------------|----------------|
| `create_*_order` | `cancel_*_order` |
| `create_*_batch_orders` | `cancel_*_batch_orders` |
| `create_*_triggered_order` | `cancel_*_triggered_order` |
| 开仓 (size > 0) | 反向平仓 (size < 0) |
| `set_*` / `update_*` | 同工具，参数恢复为原始值 |

详细推断规则和示例见 [references/fixture-templates.md](references/fixture-templates.md)。

### Fixture 安全约束

| 约束 | 规则 |
|------|------|
| 环境限制 | 仅合成依赖默认自动执行；真实集成需单独授权（见 Step 0.5） |
| 金额限制 | 使用交易对允许的最小金额（如 `min_quote_amount`） |
| 价格策略 | 限价单价格偏离市价 ≥30%，仅是合成输入，不能证明真实订单不会成交 |
| Teardown 强制 | 每个 Fixture 登记合成清理；真实清理只在授权且状态明确时执行，未知结果停止并记录残留 |
| ID 传播 | Fixture 创建的资源 ID（order_id 等）自动注入到后续测试步骤 |
| 超时保护 | 单个 Fixture 超过 30 秒未完成则标记 BLOCKED |

### Fixture 到 MCP 工具的自动映射

自动推断时，skill-tester 根据目标 Skill 中引用的 MCP 工具自动选择 Fixture 使用的工具：

| Fixture 动作 | 工具选择规则 |
|-------------|-------------|
| 创建资源 | Skill 中的 `create_*` 工具（读 JSON Schema 确定参数） |
| 清理资源 | 自动匹配对应的 `cancel_*` / `delete_*` 工具 |
| 查询状态 | Skill 中的 `get_*` / `list_*` 工具 |
| 查询行情 | Skill 中的 `get_*_tickers` 工具 |
| 查询规则 | Skill 中的 `get_*_currency_pair` 或 `get_*_contract` 工具 |

### L1.5 执行流程

```
Step 0.5 通过隔离与逐项授权门禁
    ↓
提取目标 Skill 的所有 MCP 工具引用 → 分类读/写
    ↓
对每个写操作工具，读取 JSON Schema → 分析参数依赖
    ↓
自动识别 Pattern（A/B/C/D）→ 构建 Setup + Teardown
    ↓
遍历所有场景，匹配所需的写工具和对应的 Fixture
    ↓
按 Fixture 类型分组，相同 Fixture 可复用
    ↓
对每个场景：
    1. Fixture Setup（自动调用前置工具，创建前置状态）
    2. 记录产出变量（资源 ID 等）
    3. 执行目标场景（注入产出变量）
    4. 校验结果
    5. Teardown（自动清理残留状态）
    ↓
汇总 L1.5 测试结果
```

### L1.5 结果状态

| 状态 | 符号 | 判定标准 |
|------|------|---------|
| **PASS** | ✅ | Fixture Setup 成功 + 场景执行成功 + 结果校验通过 + Teardown 成功 |
| **PASS (Teardown 失败)** | ⚠️ | 场景本身通过但 Teardown 清理失败（需人工检查） |
| **FAIL** | ❌ | 场景执行结果与预期不符 |
| **FIXTURE_FAIL** | 🔧 | Fixture Setup 失败，场景未能执行 |
| **BLOCKED** | 🔒 | 非测试环境或 MCP 不可用 |

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
编号	模块	测试层级	测试场景	Fixture类型	测试 Prompt	预期行为（Expected Behavior）	预期输出 / 关键校验点	涉及 MCP 工具	状态
```

各列说明见 [references/test-case-template.md](references/test-case-template.md)。

> 相比原版新增 `测试层级` 列（取值 L0–L5）和 `Fixture类型` 列（取值见 [fixture-templates.md](references/fixture-templates.md)，无需 Fixture 时填 `none`）。

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

### 3.3.1 失败/阻塞用例 — MCP 调用详情记录

当用例结果为 **❌ FAIL**、**🔒 BLOCKED** 或 **🔧 FIXTURE_FAIL** 时，必须在该 Case 的详细结果中额外记录完整的 MCP 调用请求和返回值，便于快速定位问题根因。

**记录内容**：

| 记录项 | 说明 |
|--------|------|
| **MCP 工具名** | 调用的工具全名，如 `cex_tradfi_query_mt5_account_info` |
| **请求参数** | 传入的 arguments JSON（无参数时记录 `{}` ） |
| **HTTP 状态码** | API 返回的 HTTP status，如 `400`、`401`、`500` |
| **响应体** | 完整的 response body JSON（包含 label、message、data） |
| **响应头（关键字段）** | `content-type`、`x-gate-trace-id` 等便于追踪的 header |

**报告中呈现格式**（在 Case 详情中追加）：

```markdown
- **MCP 调用详情**：
  - 工具：`{tool_name}`
  - 请求参数：
    ```json
    { ... }
    ```
  - 响应状态：{status_code}
  - 响应体：
    ```json
    { "label": "...", "message": "...", "data": ... }
    ```
  - Trace ID：`{x-gate-trace-id}`
```

**规则**：
1. ✅ PASS 用例仅记录返回值摘要（关键字段），不展示完整响应体，避免报告冗长
2. ❌ FAIL / 🔒 BLOCKED / 🔧 FIXTURE_FAIL 用例**必须**展示完整请求和响应，便于问题排查
3. ⚠️ PASS（有注意点）用例可选择性展示，当注意点与 API 响应相关时展示
4. 响应体中如有敏感信息（API Key、Token 等），用 `***` 脱敏处理
5. 如果单次用例涉及多个 MCP 调用，只展示失败的那个调用的详情；若多个均失败，全部展示

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

报告采用 **场景驱动** 的组织方式：用例按场景分组，场景归属于模块。

```markdown
# <Skill 名称> 测试报告

## 测试概要
| 项目 | 内容 |
|------|------|
| 测试日期 | YYYY-MM-DD |
| Skill 版本 | name version |
| 测试模型 | 当前使用的模型 |
| MCP 服务 | 服务名称（环境说明）|
| 测试层级 | L0-L1 / L0-L3 / 全量 |
| 场景总数 | M |
| 用例总数 | N |

## L0 规范校验结果
### 校验项汇总表

## 测试结果总览

### 按场景统计
| # | 模块 | 场景 | 用例数 | ✅ | ❌ | 通过率 |
|---|------|------|--------|----|----|--------|
| S1 | 模块名 | 场景名 | n | p | f | xx% |
| ... | ... | ... | ... | ... | ... | ... |
| | **合计** | **M 个场景** | **N** | **P** | **F** | **xx%** |

### 按模块统计
| 模块 | 场景数 | 用例数 | ✅ 通过 | ❌ 失败 | 通过率 |
|------|--------|--------|---------|---------|--------|

### 按测试层级统计
| 层级 | 用例数 | 通过 | 失败 |
|------|--------|------|------|

## 各场景详细结果

### 模块 X：模块名称（M 个场景，N 条用例）

#### 场景 S1：场景名称（n 条用例）

**MCP 工具**：`tool_name`
**SKILL 来源**：references/xxx.md → Scenario N

| # | 层级 | Prompt | 测试步骤 | 结果 | 说明 |
|---|------|--------|----------|------|------|
| 1 | L1 | 测试 Prompt | `tool_call(params)` | ✅/❌ | 摘要说明 |

**❌ 用例 N 失败详情**（仅 ❌/🔒/🔧 时展示）:
- **MCP 调用详情**：
  - 工具：`tool_name`
  - 请求参数：`{ ... }`
  - 响应状态：{status_code}
  - 响应体：`{ "label": "...", "message": "...", "data": ... }`
  - Trace ID：`{x-gate-trace-id}`
- **问题说明**：具体错误原因分析

#### 场景 S2：...
（同上格式，每个场景重复）

## 模型表现对比
| 模型 | 场景通过率 | 用例通过率 | 工具调用准确率 | 备注 |
|------|-----------|-----------|---------------|------|
| (当前模型) | xx% | xx% | - | 本次测试 |
| (待测模型) | — | — | — | 待填充 |

## 问题汇总
### ❌ 错误（必须修复）
### ⚠️ 观察项

## 改进建议
### Skill 改进建议
### 测试环境改进建议

## 结论
```

### 4.3 场景驱动组织规则

报告按 **模块 → 场景 → 用例** 三级层次组织：
- 每个**模块**对应 Skill 中的一个子模块（或路由/跨模块等特殊类别）
- 每个**场景**对应子模块中的一个 Scenario 或一类完整用户意图
- 每个场景下包含 1-N 条具体测试**用例**，以表格呈现
- 场景头部标注 MCP 工具和 SKILL 来源（精确到 references 文档的 Scenario 编号）
- 失败/阻塞用例在场景表格下方补充详细的 MCP 调用详情
- 测试概要中需包含「场景总数」和「用例总数」两个维度
- 按场景统计表是报告总览的首要维度，按模块统计表是汇总维度

### 4.4 模型表现列

报告末尾的「模型表现对比」表格：
- 当前测试填写实际使用的模型、场景通过率和用例通过率
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

> **判定原则**：只要 Case 中出现上述关键词之一即标记，宁可多标不可漏标。若目标 Skill 本身就是 Gate.io 相关的（按目标声明的实际业务端点判定），所有 Case 都会被标记，此时在提醒区块开头说明："本 Skill 为 Gate.io 业务 Skill，所有用例均涉及生产环境调用"。

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
> 帮我测试 gate-info-coinanalysis 这个 skill

执行流程：
1. 读取 `skills/gate-info-coinanalysis/SKILL.md` 及 `references/*.md`
2. 执行 L0 规范校验
3. 提取当前入口的研究维度、CLI 委派/fallback 与降级场景
4. 按实际产品边界生成最小充分用例，不沿用历史固定数量
5. 输出 `gate-info-coinanalysis-test-cases.tsv`
6. 逐条执行测试，记录结果
7. 输出 `gate-info-coinanalysis-test-report.md`

### 示例 2：含多语言测试（L0-L2）

用户输入：
> 测试 gate-info-coinanalysis 到 L2，包含多语言和相似问法

### 示例 3：精简报告

用户输入：
> 帮我测试 gate-info-coinanalysis，只输出失败的用例

### 示例 4：多模型对比

用户输入：
> 用 Claude 和 GPT 分别跑一遍 gate-info-coinanalysis 的测试用例

### 示例 5：带外部文档

用户输入：
> 测试 xxx skill，需求文档在这里：https://xxx.feishu.cn/docx/xxx

### 示例 6：全量走查

用户输入：
> 全量走查所有 skill

执行流程：
1. 扫描 `skills/` 下所有 Skill 目录，输出走查清单表（Skill 名、版本、场景数）
2. 用户确认走查范围
3. 逐 Skill 逐场景模拟执行：取每个场景的第一个 Prompt Example 作为用户输入，实际调用 MCP 工具，对比 Expected Behavior
4. 汇总输出 `all-skills-walkthrough-report.md`（含全场景走查大表 + 问题汇总）

---

## 参考文件

- [测试用例模板与字段说明](references/test-case-template.md)
- [测试报告完整模板](references/test-report-template.md)
- [测试执行详细指南](references/execution-guide.md)
- [Fixture 模板定义](references/fixture-templates.md)
- [全量走查执行指南](references/batch-walkthrough-guide.md)
