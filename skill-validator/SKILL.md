---
name: skill-validator
version: "2026.3.6-1"
updated: "2026-03-06"
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

**Required files checklist**:
- `SKILL.md` — AI Agent 运行时指令
- `README.md` — 面向人类的说明文档
- `CHANGELOG.md` — 版本变更记录
- `references/scenarios.md` — 场景案例与 prompt 示例

For each missing file, record: `❌ 缺少文件: {filename}`

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

### Step 8: 校验 references/scenarios.md

Read `references/scenarios.md` and validate:

**Required structure per scenario**:
- `## Scenario N: {场景名称}`
- `**Context**:` — 场景上下文描述
- `**Prompt Examples**:` — 示例 prompts
- `**Expected Behavior**:` — 预期行为步骤

### Step 9: 生成校验报告

Compile all validation results and generate report.

## Judgment Logic Summary

| Condition | Status | Meaning |
|-----------|--------|---------|
| All checks pass (Standard Architecture) | ✅ PASS | Skill 完全符合标准模板规范 |
| All checks pass (Routing Architecture) | ✅ PASS | Skill 符合路由式架构规范 |
| Has Routing Rules + Sub-modules exist | ✅ PASS | 路由式架构，判断逻辑在路由表中 |
| Missing required file | ❌ ERROR | 缺少必需文件，必须添加 |
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
| Missing Context in scenario | ⚠️ WARNING | scenario 缺少 Context 字段 |
| Invalid Workflow step format | ⚠️ WARNING | Workflow 步骤格式不规范 |

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
| references/scenarios.md | ✅/❌ | {说明} |
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

## scenarios.md 校验

| 检查项 | 状态 | 说明 |
|--------|------|------|
| Scenario 章节 | ✅/❌ | {N 个场景} |
| Context 字段 | ✅/⚠️ | {每个场景是否有 Context} |
| Prompt Examples | ✅/❌ | |
| Expected Behavior | ✅/❌ | |

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
