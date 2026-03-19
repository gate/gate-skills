---
name: skill-validator
version: "2026.3.11-1"
updated: "2026-03-11"
description: 校验 Skill 是否符合标准模板规范，支持标准架构和路由式架构的识别与校验。Use this skill whenever you need to validate a skill's structure and content. Trigger phrases include "校验skill", "检查skill格式", "validate skill", or any request involving skill validation or template compliance check.
---

# Skill Validator

校验开发人员编写的 Skill 是否符合标准模板规范，检查目录结构、文件完整性、frontmatter 格式、必需章节等，并输出详细的校验报告。

## Workflow

When the user asks to validate a skill, execute the following steps.

### Step 1: 确认待校验 Skill 路径

Ask the user for the skill directory path if not provided.

Key data to extract:
- `skill_path`: Skill 目录的完整路径

### Step 2: 检查目录结构

Read the skill directory and verify required files exist.

**Required files checklist (Standard Architecture)**:
- `SKILL.md` — AI Agent 运行时指令
- `README.md` — 面向人类的说明文档
- `CHANGELOG.md` — 版本变更记录
- `references/scenarios.md` — 场景案例与 prompt 示例

**Required files checklist (Routing Architecture)**:
- `SKILL.md` — AI Agent 运行时指令
- `README.md` — 面向人类的说明文档
- `CHANGELOG.md` — 版本变更记录
- `references/*.md` — 子模块文档（场景分散在各子模块中，**不强制要求** `scenarios.md`）

For each missing file, record: `❌ 缺少文件: {filename}`

**Note**: 路由式架构中，场景可以分散在各子模块文档中（如 `open-position.md`、`close-position.md` 等），此时 `scenarios.md` 为可选。

### Step 3: 检测 Skill 架构类型

Read `SKILL.md` and first detect which architecture pattern it uses:

**Architecture Pattern Detection**:

1. **Standard Architecture** (标准单一架构):
   - SKILL.md contains complete `## Workflow` with all steps
   - All logic in one file
   
2. **Routing Architecture** (路由式架构):
   - SKILL.md contains `## Routing Rules` or `## Sub-Modules`
   - Workflow details are in `references/*.md` sub-module documents
   - Indicates complex, multi-function skill

Key data to extract:
- `architecture_type`: "standard" or "routing"
- `has_routing_rules`: boolean
- `has_sub_modules`: boolean
- `references_files`: list of files in `references/` directory

### Step 4: 校验 SKILL.md (架构感知)

Validate based on detected architecture type.

**4.1 Frontmatter 校验** (Both architectures):

**必需字段**:
| Field | Format | Validation |
|-------|--------|------------|
| `name` | `gate-{category}-{title}` | Must follow naming convention (see below) |
| `version` | `YYYY.M.DD-N` | e.g., "2026.3.4-1" |
| `updated` | `YYYY-MM-DD` | Valid date format |
| `description` | String | Must contain "Use this skill whenever" and "Trigger phrases include" |

**Name Format Convention**:

Pattern: `gate-{category}-{title}`

- All lowercase, no underscores, no hyphens in title
- `gate`: Fixed brand prefix
- `category`: Must be one of the following enums:
  - `exchange`: CEX/on-site business (trading, finance, assets, account, security, VIP, activities, etc.)
  - `dex`: Dex domain
  - `wallet`: Gate Wallet
  - `news`: Data research side (news content, market anomaly interpretation, etc.)
  - `info`: Data research side (information & research, reports, in-depth research, K-line, alerts, on-chain info, etc.)
- `title`: Lowercase official product/function name, no spaces, no underscores, no hyphens

**Valid examples**:
- `gate-exchange-market` ✅
- `gate-exchange-spot` ✅
- `gate-exchange-activitycenter` ✅
- `gate-wallet-transfer` ✅
- `gate-info-research` ✅

**Invalid examples**:
- `gate-exchange-activity-center` ❌ (hyphens in title)
- `gate-exchange-Activity_Center` ❌ (uppercase & underscore)
- `gate-invalid-test` ❌ (invalid category)
- `exchange-market` ❌ (missing gate prefix)
- `gate-exchange` ❌ (missing title)

**Name validation checks**:
1. Must match directory name exactly
2. Must start with `gate-`
3. Must have exactly 3 parts separated by `-`
4. Second part (category) must be in the valid enum list
5. Third part (title) must be all lowercase letters, no special characters

**4.2 必需章节校验 (Standard Architecture)**:

For standard single-function skills:
- ✅ `# {Title}` — 一级标题
- ✅ `## Workflow` — 完整工作流程（包含所有步骤）
- ✅ `## Judgment Logic Summary` — 判断逻辑表格
- ✅ `## Report Template` — 报告模板

**4.3 必需章节校验 (Routing Architecture)**:

For routing-based multi-function skills:
- ✅ `# {Title}` — 一级标题
- ✅ `## Sub-Modules` or `## Routing Rules` — 子模块列表或路由规则表
- ✅ `## Execution` — 执行流程说明
- ✅ Sub-module documents exist in `references/` directory

**判断逻辑**:
- If `## Routing Rules` exists → Routing Architecture (✅ PASS, judgment logic is in routing table)
- If `## Sub-Modules` exists → Routing Architecture (✅ PASS)
- If neither exists but `## Workflow` exists → Standard Architecture (apply standard checks)
- If none exist → ❌ ERROR

**4.4 推荐章节校验**（Both architectures）:
- `## Domain Knowledge` — 领域知识（⚠️ WARNING if missing）
- `## Error Handling` — 错误处理（⚠️ WARNING if missing）
- `## Safety Rules` — 安全规则（⚠️ WARNING if missing for trading skills）

**4.5 Workflow 步骤格式校验**:

For Standard Architecture:
- Check each `### Step N:` contains:
  - `Call \`{tool_name}\` with:` — MCP tool 调用声明
  - `Key data to extract:` — 提取的关键数据

For Routing Architecture:
- Check `## Execution` describes routing and loading process
- Verify sub-module documents exist and contain detailed workflows

**4.6 品牌文字规范校验** (Both architectures):

Scan all `.md` files in the skill directory for deprecated brand names.

**Forbidden patterns** (case-insensitive):
- `Gate.io` — 已废弃，公司品牌已升级为 "Gate"
- `gate.io` — 小写形式同样禁止
- `GATE.IO` — 大写形式同样禁止

**Correct usage**:
- ✅ `Gate` — 正确的品牌名称
- ✅ `Gate Wallet` — 正确
- ✅ `Gate DEX` — 正确
- ✅ `Gate Exchange` — 正确

**Validation**:
1. Search all `.md` files for regex pattern: `/[Gg][Aa][Tt][Ee]\.[Ii][Oo]/`
2. For each match found, record:
   - File name
   - Line number
   - Context (surrounding text)
3. All matches are ❌ ERROR — must be replaced with "Gate"

### Step 5: 校验子模块文档 (Routing Architecture Only)

If routing architecture detected, validate sub-module documents in `references/`:

For each sub-module document (excluding `scenarios.md`):
- ✅ Contains `## Workflow` with detailed steps
- ✅ Contains `## Report Template`
- ✅ Workflow steps follow standard format (Call tool, Key data to extract)

**Note**: Sub-modules don't require `## Judgment Logic Summary` as routing logic is in main SKILL.md.

### Step 6: 校验 README.md

Read `README.md` and validate:

**Required sections**:
- `## Overview` — 概述
- `### Core Capabilities` — 核心能力（应包含表格）
- `## Architecture` — 架构说明

### Step 7: 校验 CHANGELOG.md

Read `CHANGELOG.md` and validate:

**Required format**:
- Version header: `## [{version}] - {YYYY-MM-DD}`
- At least one section: `### Added`, `### Changed`, `### Fixed`, or `### Audit`

### Step 8: 校验场景文档 (架构感知)

根据架构类型选择不同的场景校验策略。

**8.1 Standard Architecture — 校验 `references/scenarios.md`**

Read `references/scenarios.md` and validate:

**Required structure per scenario** (严格格式校验):

Each scenario MUST follow this exact pattern:

```
## Scenario N: {场景名称}

**Context**: {场景上下文描述，不能为空}

**Prompt Examples**:
- "{示例 prompt 1}"
- "{示例 prompt 2}"

**Expected Behavior**:
1. {步骤 1}
2. {步骤 2}
...
```

**Strict validation rules**:

| 检查项 | 格式要求 | 状态 |
|--------|----------|------|
| Scenario 标题 | 必须是 `## Scenario N: {名称}` 格式，N 为数字，名称非空 | ❌ ERROR if missing/malformed |
| `**Context**:` | 必须紧跟场景标题，冒号后必须有非空内容 | ❌ ERROR if missing or empty |
| `**Prompt Examples**:` | 必须存在，且至少包含 1 个以 `- "` 开头的示例 | ❌ ERROR if missing or no examples |
| `**Expected Behavior**:` | 必须存在，且至少包含 1 个编号步骤 (如 `1. `) | ❌ ERROR if missing or no steps |

**Field order validation**:
- Fields MUST appear in this exact order: Context → Prompt Examples → Expected Behavior
- Missing any field or wrong order → ❌ ERROR

**Content validation**:
- `**Context**:` 后必须有实际描述文字（不能只有空白）
- `**Prompt Examples**:` 下必须有至少一行以 `- "` 或 `- '` 开头
- `**Expected Behavior**:` 下必须有至少一行以数字+点开头（如 `1. `、`2. `）

**Optional fields** (可选，但如存在需遵循格式):
- `**Unexpected Behavior**:` — 非预期行为说明

**Validation output per scenario**:

```
Scenario {N}: {场景名称}
├── Context: ✅/❌ {存在且非空 / 缺失或为空}
├── Prompt Examples: ✅/❌ {N 个示例 / 缺失或无示例}
├── Expected Behavior: ✅/❌ {N 个步骤 / 缺失或无步骤}
└── Field Order: ✅/❌ {正确 / 顺序错误}
```

**8.2 Routing Architecture — 校验子模块中的分散场景**

路由式架构中，场景分散在各子模块文档中（如 `open-position.md`、`close-position.md` 等），**不强制要求** `scenarios.md`。

**校验策略**:

1. **检查场景来源**: 
   - 如果 `references/scenarios.md` 存在 → 按 8.1 标准校验
   - 如果 `references/scenarios.md` 不存在 → 校验子模块中的场景

2. **子模块场景格式** (宽松格式，兼容多种写法):

   子模块中的场景可以使用以下任一格式：

   **格式 A — 标准 Scenario 格式**:
   ```
   ## Scenario N: {场景名称}
   **Context**: ...
   **Prompt Examples**: ...
   **Expected Behavior**: ...
   ```

   **格式 B — 简化场景格式** (推荐用于子模块):
   ```
   ## Scenario N: {场景名称}
   **Context**: ...
   **Prompt Examples**: ...
   **Expected Behavior**: ...
   **Response Template**: ...
   ```

   **格式 C — 场景驱动格式** (常见于交易类 Skill):
   ```
   ## Scenario N: {场景名称}
   
   **Context**: {场景上下文}
   
   **Prompt Examples**:
   - "..."
   
   **Expected Behavior**:
   1. ...
   
   **Response Template**:
   ```...```
   ```

3. **子模块场景校验规则** (宽松):

   | 检查项 | 要求 | 状态 |
   |--------|------|------|
   | 场景标题 | `## Scenario N:` 格式 | ✅ 存在即可 |
   | `**Context**:` | 存在且非空 | ✅ 存在即可 |
   | `**Prompt Examples**:` | 存在且有示例 | ✅ 存在即可 |
   | `**Expected Behavior**:` | 存在且有步骤 | ✅ 存在即可 |
   | `**Response Template**:` | 可选 | ⚠️ 建议有 |

4. **场景覆盖度检查**:

   统计所有子模块中的场景总数，确保覆盖完整：

   ```
   场景分布统计:
   ├── {sub-module-1}.md: {N} 个场景
   ├── {sub-module-2}.md: {M} 个场景
   └── 总计: {Total} 个场景
   ```

   - 总场景数 ≥ 1 → ✅ PASS
   - 总场景数 = 0 → ❌ ERROR (路由架构必须有场景)

5. **输出格式**:

   ```
   场景校验 (路由式架构 - 分散场景)
   ├── scenarios.md: ⚠️ 不存在（路由架构可选）
   ├── 子模块场景分布:
   │   ├── open-position.md: 10 个场景 ✅
   │   ├── close-position.md: 11 个场景 ✅
   │   ├── cancel-order.md: 9 个场景 ✅
   │   └── amend-order.md: 8 个场景 ✅
   ├── 场景总数: 38 个 ✅
   └── 校验结果: ✅ PASS (场景分散在子模块中，覆盖完整)
   ```

### Step 9: 品牌文字全局扫描

Scan all `.md` files in the skill directory for brand compliance:

1. Read all `.md` files: `SKILL.md`, `README.md`, `CHANGELOG.md`, `references/*.md`
2. Search for forbidden pattern: `Gate.io` (case-insensitive)
3. Record all violations with file, line number, and context

### Step 10: MCP 工具调用校验

Validate that all MCP tool calls referenced in SKILL.md and scenario documents exist in the corresponding MCP service.

**10.1 自动发现所有 MCP 服务**

自动扫描当前工作区的 MCP 服务目录，获取所有可用服务和工具。

**MCP 服务目录位置**：
```
/Users/{user}/.cursor/projects/{workspace}/mcps/
```

**自动发现流程**：
1. 列出 `mcps/` 目录下所有子目录（每个子目录是一个 MCP 服务）
2. 对每个服务，列出 `{service}/tools/` 目录下所有 `.json` 文件
3. 构建全局工具映射表：`{tool_name} → {service_name}`

**示例目录结构**：
```
mcps/
├── user-gateapi/
│   └── tools/
│       ├── get_spot_accounts.json
│       ├── create_spot_order.json
│       └── ...
├── user-GatePre/
│   └── tools/
│       ├── market_get_kline.json
│       └── ...
└── other-service/
    └── tools/
        └── ...
```

**输出**：
- 可用 MCP 服务列表
- 全局工具清单（工具名 → 所属服务）

**10.2 提取 SKILL.md 中的工具调用**

从以下位置提取 MCP 工具名称：

| 提取来源 | 模式 |
|----------|------|
| Tool Mapping 表格 | `\`{tool_name}\`` 在表格的 Tool Calls 列 |
| Step 4: Call Tools by Scenario | `{tool_name}` 在工具列表中 |
| Case Routing Map | `{tool_name}` 在 Tool Sequence 列 |
| Workflow 步骤 | `Call \`{tool_name}\`` 或 `via \`{tool_name}\`` |

**提取规则**:
1. 使用正则表达式匹配反引号包裹的工具名：`` `([a-z_]+)` ``
2. 过滤掉非工具名的内容（如 `currency_pair`、`status=open` 等参数）
3. 工具名通常以 `get_`、`list_`、`create_`、`cancel_`、`amend_`、`update_`、`delete_` 开头

**10.3 提取场景文档中的工具调用**

根据架构类型选择提取来源：

**Standard Architecture**: 从 `scenarios.md` 提取

| 提取来源 | 模式 |
|----------|------|
| Fetch data via | `Fetch data via \`{tool_name}\`` |
| Expected Behavior 步骤 | `via \`{tool_name}\`` 或 `\`{tool_name}\`` |

**Routing Architecture**: 从子模块文档提取

| 提取来源 | 模式 |
|----------|------|
| 子模块 Expected Behavior | `via \`{tool_name}\`` 或 `\`{tool_name}\`` |
| 子模块 Response Template | `\`{tool_name}\`` |
| 子模块 Workflow 步骤 | `Call \`{tool_name}\`` |

**10.4 验证工具存在性**

使用 Step 10.1 构建的全局工具映射表进行校验：

1. 对每个提取的工具名，检查是否存在于全局工具映射表中
2. 如果存在，记录所属的 MCP 服务名
3. 如果不存在于任何服务，标记为 ❌ ERROR

**验证输出格式**:

```
MCP 工具校验
├── 发现 MCP 服务: {N} 个
│   ├── {service_1}: {M} 个工具
│   ├── {service_2}: {K} 个工具
│   └── ...
├── SKILL.md 引用工具: {X} 个
│   ├── {tool_name_1}: ✅ 存在 (服务: {service_name})
│   ├── {tool_name_2}: ✅ 存在 (服务: {service_name})
│   └── {tool_name_3}: ❌ 不存在于任何 MCP 服务
├── 场景文档引用工具: {Y} 个 (来源: scenarios.md / 子模块文档)
│   ├── {tool_name_1}: ✅ 存在 (服务: {service_name})
│   └── {tool_name_2}: ❌ 不存在于任何 MCP 服务
└── 校验结果: ✅ 全部通过 / ❌ 发现 {Z} 个不存在的工具
```

**边界情况处理**:
- 如果 `mcps/` 目录不存在 → ⚠️ WARNING: 无 MCP 服务配置，跳过工具校验
- 如果 `mcps/` 目录存在但为空 → ⚠️ WARNING: 无可用 MCP 服务，跳过工具校验
- 如果 SKILL.md 未引用任何 MCP 工具 → ⚠️ WARNING: 未检测到 MCP 工具调用

**10.5 常见工具名前缀参考**

以下前缀通常表示有效的 MCP 工具名：

| 前缀 | 含义 | 示例 |
|------|------|------|
| `get_` | 获取单个资源 | `get_spot_accounts`, `get_currency_pair` |
| `list_` | 列出多个资源 | `list_spot_orders`, `list_spot_my_trades` |
| `create_` | 创建资源 | `create_spot_order`, `create_transfer` |
| `cancel_` | 取消操作 | `cancel_spot_order`, `cancel_all_spot_orders` |
| `amend_` | 修改资源 | `amend_spot_order`, `amend_futures_order` |
| `update_` | 更新资源 | `update_futures_position_leverage` |
| `delete_` | 删除资源 | `delete_sub_account_key` |
| `set_` | 设置配置 | `set_unified_mode` |

### Step 11: 生成校验报告

Compile all validation results and generate report.

## Judgment Logic Summary

| Condition | Status | Meaning |
|-----------|--------|---------|
| All checks pass (Standard Architecture) | ✅ PASS | Skill 完全符合标准模板规范 |
| All checks pass (Routing Architecture) | ✅ PASS | Skill 符合路由式架构规范 |
| Has Routing Rules + Sub-modules exist | ✅ PASS | 路由式架构，判断逻辑在路由表中 |
| Routing + scenarios in sub-modules | ✅ PASS | 路由式架构，场景分散在子模块中（不要求 scenarios.md） |
| Routing + no scenarios.md + sub-module scenarios ≥ 1 | ✅ PASS | 路由架构场景覆盖完整 |
| Routing + no scenarios.md + sub-module scenarios = 0 | ❌ ERROR | 路由架构必须有场景（在 scenarios.md 或子模块中） |
| Missing required file (Standard) | ❌ ERROR | 标准架构缺少必需文件，必须添加 |
| Missing required file (Routing, excl. scenarios.md) | ❌ ERROR | 路由架构缺少必需文件（scenarios.md 除外） |
| Missing frontmatter field | ❌ ERROR | frontmatter 缺少必需字段 |
| Invalid frontmatter format | ❌ ERROR | frontmatter 格式不正确 |
| name 格式不符合 `gate-{category}-{title}` | ❌ ERROR | name 必须符合命名规范 |
| name 未以 `gate-` 开头 | ❌ ERROR | 必须以 gate 品牌前缀开头 |
| name 的 category 不在枚举列表 | ❌ ERROR | category 必须是: exchange/dex/wallet/news/info |
| name 的 title 包含大写/下划线/短横线 | ❌ ERROR | title 必须全小写，无下划线无短横线 |
| name 部分数量不是 3 个 | ❌ ERROR | 必须是 gate-{category}-{title} 三部分 |
| Standard: Missing Workflow/Judgment/Report | ❌ ERROR | 标准架构缺少必需章节 |
| Routing: Missing Routing Rules/Sub-modules | ❌ ERROR | 路由架构缺少路由规则或子模块 |
| Missing recommended section | ⚠️ WARNING | 缺少推荐章节，建议添加 |
| name 与目录名不匹配 | ❌ ERROR | name 必须与目录名一致 |
| Invalid Workflow step format | ⚠️ WARNING | Workflow 步骤格式不规范 |
| Scenario 标题格式错误 | ❌ ERROR | 必须是 `## Scenario N: {名称}` 格式 |
| Scenario 缺少 Context | ❌ ERROR | 每个场景必须有 `**Context**:` 字段 |
| Scenario Context 内容为空 | ❌ ERROR | Context 后必须有实际描述内容 |
| Scenario 缺少 Prompt Examples | ❌ ERROR | 每个场景必须有 `**Prompt Examples**:` 字段 |
| Prompt Examples 无示例条目 | ❌ ERROR | 必须至少有一个以 `- "` 开头的示例 |
| Scenario 缺少 Expected Behavior | ❌ ERROR | 每个场景必须有 `**Expected Behavior**:` 字段 |
| Expected Behavior 无编号步骤 | ❌ ERROR | 必须至少有一个编号步骤（如 `1. `） |
| Scenario 字段顺序错误 | ❌ ERROR | 必须按 Context → Prompt Examples → Expected Behavior 顺序 |
| 文档中出现 "Gate.io" | ❌ ERROR | 品牌已升级为 "Gate"，禁止使用 "Gate.io" |
| MCP 工具不存在 | ❌ ERROR | SKILL.md 或场景文档中引用的 MCP 工具在任何服务中都不存在 |
| mcps 目录不存在或为空 | ⚠️ WARNING | 无 MCP 服务配置，跳过工具校验 |
| 未检测到 MCP 工具调用 | ⚠️ WARNING | SKILL.md 中未引用任何 MCP 工具 |
| 所有 MCP 工具存在 | ✅ PASS | 所有引用的 MCP 工具在可用服务中都存在 |

## Report Template

```markdown
# Skill 校验报告

**校验路径**: {skill_path}
**校验时间**: {timestamp}
**架构类型**: {Standard / Routing}
**校验结果**: {PASS / FAIL / PASS with WARNINGS}

## 架构检测

| 项目 | 结果 |
|-----|------|
| 架构类型 | {Standard / Routing} |
| 路由规则 | {✅ 存在 / ❌ 不存在} |
| 子模块数量 | {N} |
| 子模块列表 | {list of sub-modules} |

## 目录结构检查

| 文件 | 状态 | 说明 |
|------|------|------|
| SKILL.md | ✅/❌ | {说明} |
| README.md | ✅/❌ | {说明} |
| CHANGELOG.md | ✅/❌ | {说明} |
| references/scenarios.md | ✅/❌/⚠️ | {说明，路由架构可选} |
| references/{sub-module}.md | ✅/❌ | {如果是路由架构} |

## SKILL.md 校验

### Frontmatter

| 字段 | 状态 | 当前值 | 问题 |
|------|------|--------|------|
| name | ✅/❌ | {value} | {issue or "OK"} |
| version | ✅/❌ | {value} | {issue or "OK"} |
| updated | ✅/❌ | {value} | {issue or "OK"} |
| description | ✅/❌ | {truncated} | {issue or "OK"} |

### Name Format Validation

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 格式 `gate-{category}-{title}` | ✅/❌ | {是否符合三部分结构} |
| `gate-` 前缀 | ✅/❌ | {是否以 gate- 开头} |
| Category 枚举 | ✅/❌ | {当前: {category}, 是否在 exchange/dex/wallet/news/info 中} |
| Title 格式 | ✅/❌ | {是否全小写，无下划线，无短横线} |
| 与目录名匹配 | ✅/❌ | {name 是否与目录名完全一致} |

### 必需章节 (Standard Architecture)

| 章节 | 状态 |
|------|------|
| # Title | ✅/❌ |
| ## Workflow | ✅/❌ |
| ## Judgment Logic Summary | ✅/❌ |
| ## Report Template | ✅/❌ |

### 必需章节 (Routing Architecture)

| 章节 | 状态 | 说明 |
|------|------|------|
| # Title | ✅/❌ | |
| ## Sub-Modules / ## Routing Rules | ✅/❌ | 路由规则表或子模块列表 |
| ## Execution | ✅/❌ | 执行流程说明 |
| Sub-module documents | ✅/❌ | {N} 个子模块文档存在 |

### 推荐章节

| 章节 | 状态 | 说明 |
|------|------|------|
| ## Domain Knowledge | ✅/⚠️ | {存在/缺少，建议添加领域知识} |
| ## Error Handling | ✅/⚠️ | {存在/缺少，建议添加错误处理} |
| ## Safety Rules | ✅/⚠️ | {存在/缺少，交易类建议添加} |

### Workflow 步骤格式

| 检查项 | 状态 | 说明 |
|--------|------|------|
| Step 声明 | ✅/⚠️ | {N 个步骤} |
| MCP Tool 调用 | ✅/⚠️ | {格式是否正确} |
| Key data to extract | ✅/⚠️ | {是否声明提取数据} |

## 子模块文档校验 (Routing Architecture Only)

{For each sub-module:}

### {sub-module-name}.md

| 检查项 | 状态 |
|--------|------|
| ## Workflow | ✅/❌ |
| ## Report Template | ✅/❌ |
| Workflow 步骤格式 | ✅/⚠️ |

**Note**: 子模块不要求独立的 Judgment Logic Summary（路由逻辑在主 SKILL.md 中）

## README.md 校验

| 章节 | 状态 |
|------|------|
| ## Overview | ✅/❌ |
| ### Core Capabilities | ✅/❌ |
| ## Architecture | ✅/❌ |

## CHANGELOG.md 校验

| 检查项 | 状态 |
|--------|------|
| 版本标题格式 | ✅/❌ |
| 变更章节 | ✅/❌ |

## 场景校验

{根据架构类型显示不同内容}

### Standard Architecture — scenarios.md 校验

#### 场景概览

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 场景总数 | ✅/❌ | {N 个场景} |
| 场景格式完整性 | ✅/❌ | {N/M 个场景格式完整} |

#### 各场景详细校验

{For each scenario:}

**Scenario {N}: {场景名称}**

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 标题格式 | ✅/❌ | `## Scenario N: {名称}` |
| `**Context**:` | ✅/❌ | {存在且非空 / 缺失 / 内容为空} |
| `**Prompt Examples**:` | ✅/❌ | {N 个示例 / 缺失 / 无示例条目} |
| `**Expected Behavior**:` | ✅/❌ | {N 个步骤 / 缺失 / 无编号步骤} |
| 字段顺序 | ✅/❌ | {正确 / 顺序错误: 实际为 X→Y→Z} |

### Routing Architecture — 分散场景校验

#### 场景来源

| 检查项 | 状态 | 说明 |
|--------|------|------|
| scenarios.md | ✅/⚠️ | {存在 / 不存在（路由架构可选）} |
| 场景分布方式 | - | {集中在 scenarios.md / 分散在子模块中} |

#### 子模块场景分布

| 子模块 | 场景数 | 状态 |
|--------|--------|------|
| {sub-module-1}.md | {N} | ✅ |
| {sub-module-2}.md | {M} | ✅ |
| ... | ... | ... |
| **总计** | **{Total}** | ✅/❌ |

#### 场景覆盖度

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 场景总数 | ✅/❌ | {Total} 个场景 (≥1 为 PASS) |
| 场景格式 | ✅/⚠️ | {宽松校验，子模块场景格式灵活} |

**Note**: 路由式架构中，场景分散在各子模块文档中，不强制要求 `scenarios.md`。只要子模块中有场景且格式基本正确即可。

## 品牌文字规范校验

| 文件 | 状态 | 问题详情 |
|------|------|----------|
| SKILL.md | ✅/❌ | {无问题 / 第 N 行发现 "Gate.io"} |
| README.md | ✅/❌ | {无问题 / 第 N 行发现 "Gate.io"} |
| CHANGELOG.md | ✅/❌ | {无问题 / 第 N 行发现 "Gate.io"} |
| references/*.md | ✅/❌ | {无问题 / {文件名}第 N 行发现 "Gate.io"} |

**品牌规范说明**: 公司品牌已升级，所有文档中禁止使用 "Gate.io"，应使用 "Gate"。

## MCP 工具校验

### MCP 服务发现

| 检查项 | 状态 | 说明 |
|--------|------|------|
| mcps 目录 | ✅/⚠️ | {存在 / 不存在或为空} |
| 发现 MCP 服务 | - | {N} 个服务 |
| 全局可用工具 | - | {M} 个工具 |

**已发现的 MCP 服务**:

| 服务名 | 工具数量 |
|--------|----------|
| {service_1} | {N} |
| {service_2} | {M} |

### 工具引用校验

| 检查项 | 状态 | 说明 |
|--------|------|------|
| SKILL.md 引用工具 | ✅/❌ | {M 个工具，N 个不存在} |
| 场景文档引用工具 | ✅/❌ | {K 个工具，J 个不存在} (来源: scenarios.md / 子模块) |

### SKILL.md 工具匹配详情

| 工具名称 | 状态 | 所属服务 |
|----------|------|----------|
| {tool_name_1} | ✅ | {service_name} |
| {tool_name_2} | ❌ | 不存在于任何服务 |

### 场景文档工具匹配详情

| 工具名称 | 状态 | 所属服务 | 来源 |
|----------|------|----------|------|
| {tool_name_1} | ✅ | {service_name} | {scenarios.md / sub-module.md} |
| {tool_name_2} | ❌ | 不存在于任何服务 | {来源文件} |

### 未使用的 MCP 工具（仅供参考）

以下工具在 MCP 服务中可用但 Skill 未使用，可按需扩展：

| 工具名称 | 分类 | 说明 |
|----------|------|------|
| {unused_tool_1} | {category} | 可用于 {potential_use_case} |

## 问题汇总

### ❌ 错误（必须修复）

{列出所有 ❌ 项目}

### ⚠️ 警告（建议修复）

{列出所有 ⚠️ 项目}

## 架构评估

{If Routing Architecture:}
- ✅ 路由式架构设计合理，适合复杂多功能 Skill
- ✅ 职责分离：SKILL.md 负责路由，子模块负责执行
- ✅ 易于维护和扩展

{If Standard Architecture:}
- ✅ 标准单一架构，适合简单功能 Skill
- ✅ 所有逻辑集中在一个文件，便于理解

## 修复建议

{针对每个问题给出具体修复建议}
```
