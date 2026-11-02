# 测试报告模板（Lark Markdown 兼容）

本文件定义测试报告的完整结构，生成报告时严格遵循此模板。

---

## 报告模板

````markdown
# {skill_name} 测试报告

> 测试日期: {date} | Skill 版本: {version} | 测试模型: {model_name}

---

## 一、测试概要

| 项目 | 内容 |
|------|------|
| 测试 Skill | {skill_name} |
| Skill 版本 | {version} |
| 测试日期 | {date} |
| 测试模型 | {model_name} |
| MCP Server | {mcp_server_name} (如: gateapi) |
| 测试用例总数 | {total_cases} |
| 执行用例数 | {executed_cases} |
| 测试环境 | {environment} (如: 模拟盘/实盘/沙箱) |

---

## 二、测试结果总览

### 2.1 按模块统计

| 模块 | 用例数 | ✅ PASS | ⚠️ 注意 | ❌ FAIL | 🔒 BLOCKED | ⏭ SKIP | ❓ 存疑 | 通过率 |
|------|--------|---------|---------|---------|-----------|---------|---------|--------|
| {module_1} | {n} | {pass} | {warn} | {fail} | {blocked} | {skip} | {uncertain} | {rate}% |
| {module_2} | ... | ... | ... | ... | ... | ... | ... | ... |
| **合计** | **{total}** | **{pass}** | **{warn}** | **{fail}** | **{blocked}** | **{skip}** | **{uncertain}** | **{rate}%** |

### 2.2 调用方式统计

| 调用方式 | 用例数 | 占比 | 说明 |
|---------|--------|------|------|
| MCP (mcporter CLI) | {mcp_count} | {mcp_pct}% | 通过 MCP 协议调用 Gate.io API |
| API (直接 HTTP) | {api_count} | {api_pct}% | 直接通过 REST API 调用 |
| 混合 | {mixed_count} | {mixed_pct}% | 同一用例中同时使用 MCP 和 API |

### 2.3 结果分类汇总

| 结果 | 数量 | 占比 | 典型原因 |
|------|------|------|---------|
| ✅ PASS | {n} | {pct}% | 功能正常 |
| ⚠️ PASS (有注意点) | {n} | {pct}% | 功能正常但有优化空间 |
| ❌ FAIL | {n} | {pct}% | {典型原因} |
| 🔒 BLOCKED | {n} | {pct}% | 环境限制（余额不足等） |
| ⏭ SKIP | {n} | {pct}% | 当前版本不支持 |
| ❓ 存疑 | {n} | {pct}% | 需进一步确认 |

### 2.4 ⚠️ 生产环境调用提醒

> 本次测试中检测到 {gate_io_count} 条用例涉及 **Gate.io 生产环境** 调用，请核实是否为预期行为。
> 其中写操作 {write_count} 条（🔴 高风险），读操作 {read_count} 条（🟡 中风险）。

| Case | 模块 | 涉及工具/接口 | 操作类型 | 风险 |
|------|------|-------------|---------|------|
| Case {N} | {module} | {tool_or_api} | 写操作/读操作 | 🔴/🟡 |

> 若目标 Skill 本身为 Gate.io 业务 Skill，此处说明："本 Skill 为 Gate.io 业务 Skill，所有用例均涉及生产环境调用"。
> 若无 Gate.io 相关调用，则省略本节。

---

## 三、各模块详细测试结果

### 3.1 {Module 名称}

#### Case {N}: {场景名称}
- **Prompt**: {测试 Prompt 原文}
- **测试步骤**: `{tool_1}` ✅ → `{tool_2}` ✅ → `{tool_3}` ❌
- **结果**: {状态符号} {状态} — {详细说明}
- **调用方式**: MCP / API
- **生产环境**: ⚠️ 生产环境 — 写操作/读操作（仅涉及 Gate.io 时标注）
- **API 验证**: {验证结果，如：✅ 合约查询正常，错误码正确返回}
- **SKILL 覆盖**: {引用 SKILL.md 或 references 中的具体章节，如：✅ open-position.md Scenario 1}

#### Case {N+1}: {场景名称}
...

---

## 四、模型表现对比

| 模型 | 通过率 | BLOCKED 率 | FAIL 率 | 工具调用准确率 | 意图理解准确率 | 平均工具调用次数 | 备注 |
|------|--------|-----------|---------|---------------|---------------|-----------------|------|
| {当前模型} | {pass_rate}% | {blocked_rate}% | {fail_rate}% | {tool_accuracy}% | {intent_accuracy}% | {avg_tool_calls} | 本次测试 |
| {待测模型 A} | - | - | - | - | - | - | 待填充 |
| {待测模型 B} | - | - | - | - | - | - | 待填充 |

### 模型评估维度说明

| 维度 | 计算方式 |
|------|---------|
| 通过率 | PASS / (PASS + FAIL) × 100% (不含 BLOCKED/SKIP) |
| 工具调用准确率 | 实际调用链与预期调用链的匹配度 |
| 意图理解准确率 | 正确识别用户意图的用例占比 |
| 平均工具调用次数 | 每个 PASS 用例的平均 MCP 工具调用数 |

---

## 五、问题汇总与建议

### 5.1 发现的问题

| # | 严重级别 | 模块 | 问题描述 | 关联 Case | 建议 |
|---|---------|------|---------|----------|------|
| 1 | 🔴 高 | {module} | {description} | Case {N} | {suggestion} |
| 2 | 🟡 中 | {module} | {description} | Case {N} | {suggestion} |
| 3 | 🟢 低 | {module} | {description} | Case {N} | {suggestion} |

### 5.2 Skill 改进建议

- {建议 1}
- {建议 2}

### 5.3 测试覆盖空白

| 未覆盖场景 | 原因 | 优先级 |
|-----------|------|--------|
| {场景} | {原因} | P{0-3} |

---

## 六、附录

### 测试用例文件
- TSV 文件: `{skill_name}-test-cases.tsv`
- 报告文件: `{skill_name}-test-report.md`

### 测试执行环境
- Agent: {agent_name}
- MCP Server 版本: {mcp_version}
- 运行时间: {start_time} — {end_time}
````

---

## 模板使用说明

### 占位符替换规则

所有 `{xxx}` 格式的占位符在生成报告时替换为实际值：
- `{skill_name}` → 目标 skill 名称
- `{version}` → SKILL.md 中的 version 字段
- `{date}` → 测试执行日期 (YYYY-MM-DD)
- `{model_name}` → 当前使用的 AI 模型标识
- `{mcp_server_name}` → 使用的 MCP server 名称

### 调用方式判定逻辑

| 场景 | 标记 |
|------|------|
| Agent 通过 MCP 协议调用 `gateapi` 等 MCP Server | **MCP** |
| Agent 直接发起 HTTP 请求调用 API | **API** |
| 同一 Case 中两种方式都有 | **混合** |
| 无法判断（如仅做格式输出） | **N/A** |

### 生产环境调用检测逻辑

在生成报告时，扫描每条 Case 的工具调用和 API 请求，检测是否命中以下关键词：

| 类别 | 关键词/模式 |
|------|-----------|
| 域名 | `api.gateio.ws`, `gate.io`, `gateio.ws`, `www.gate.io` |
| MCP Server | `gateapi`, `gate` |
| API 路径 | `/api/v4/` |
| 工具名前缀 | `gateapi__` |
| MCP 端点 | `api.gatemcp.ai` |

命中规则：
- 命中任一关键词即标记
- 写操作（create/update/delete/cancel/transfer）标为 🔴 高风险
- 读操作（list/get/query）标为 🟡 中风险
- 无法判断的标为 🟡 待确认
- 若 Skill 本身即 Gate.io 业务 Skill，在 2.4 区块开头说明，避免逐条标注冗余

### Lark兼容性注意事项

- 使用标准 Markdown 表格语法（`|` 分隔）
- emoji 使用 Unicode 标准 emoji（✅ ❌ ⚠️ 🔒 ⏭ ❓ 🔴 🟡 🟢）
- 避免使用 HTML 标签
- 代码块使用 ` `` ` 包裹，不使用 ``` 代码块（Lark渲染差异）
- 标题层级不超过 4 级
