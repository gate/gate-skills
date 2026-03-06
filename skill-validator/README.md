# Skill Validator

## Overview

An AI Agent skill that validates whether a skill conforms to the standard template specification. It checks directory structure, file completeness, frontmatter format, required sections, and outputs a detailed validation report.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **目录结构校验** | 检查必需文件是否存在 | "校验 my-skill 是否有完整的文件结构" |
| **命名规范校验** | 检查 skill 名称是否符合 `gate-{category}-{title}` 格式 | "检查 gate-exchange-market 命名是否规范" |
| **Frontmatter 校验** | 检查 SKILL.md 的 frontmatter 格式 | "检查 name、version、description 是否正确" |
| **章节完整性校验** | 检查各文件是否包含必需/推荐章节 | "校验 SKILL.md 是否有 Workflow 章节" |
| **Workflow 格式校验** | 检查 MCP tool 调用格式 | "Call \`{tool}\` with: 格式是否正确" |
| **Scenario Context 校验** | 检查场景是否有 Context 字段 | "scenarios.md 每个场景是否有 Context" |
| **校验报告生成** | 输出详细的校验结果 | "生成 markdown 格式的校验报告" |

## Architecture

```
skill-validator/
├── SKILL.md              # 校验逻辑和工作流程
├── README.md             # 本文档
├── CHANGELOG.md          # 版本记录
└── references/
    └── scenarios.md      # 使用场景示例
```

### 校验规则

**目录结构要求**:
```
{skill-name}/
├── SKILL.md              # [必须] AI Agent 运行时指令
├── README.md             # [必须] 面向人类的说明文档
├── CHANGELOG.md          # [必须] 版本变更记录
└── references/
    └── scenarios.md      # [必须] 场景案例与 prompt 示例
```

**SKILL.md Frontmatter 要求**:
```yaml
---
name: gate-{category}-{title}   # 必须符合命名规范
version: "{YYYY.M.DD-N}"        # 日期版本格式
updated: "{YYYY-MM-DD}"         # 最后更新日期
description: ...                # 必须包含触发场景说明
---
```

**Name Format Convention**:
- Pattern: `gate-{category}-{title}`
- All lowercase, no underscores, no hyphens in title
- `gate`: Fixed brand prefix
- `category`: Must be one of:
  - `exchange`: CEX/on-site business (trading, finance, assets, account, etc.)
  - `dex`: Dex domain
  - `wallet`: Gate Wallet
  - `news`: Data research (news content, market anomaly interpretation)
  - `info`: Data research (information & research, reports, K-line, alerts)
- `title`: Lowercase official product/function name, no spaces/underscores/hyphens

**Valid examples**:
- `gate-exchange-market` ✅
- `gate-exchange-activitycenter` ✅
- `gate-wallet-transfer` ✅

**Invalid examples**:
- `gate-exchange-activity-center` ❌ (hyphens in title)
- `gate-invalid-test` ❌ (invalid category)
- `exchange-market` ❌ (missing gate prefix)

**SKILL.md 必需章节**:
- `# {Title}` — 一级标题
- `## Workflow` — 工作流程
- `## Judgment Logic Summary` — 判断逻辑
- `## Report Template` — 报告模板

**SKILL.md 推荐章节**（操作类 Skill）:
- `## Domain Knowledge` — 领域知识
- `## Error Handling` — 错误处理
- `## Safety Rules` — 安全规则

**Workflow 步骤格式**:
```markdown
### Step N: {步骤名}

Call `{mcp_tool_name}` with:
- `param1`: value1
- `param2`: value2

Key data to extract:
- {数据点1}
- {数据点2}

**Pre-filter**: {筛选条件}
```

**scenarios.md 结构要求**:
```markdown
## Scenario N: {场景名称}

**Context**: {场景上下文描述}

**Prompt Examples**:
- "{示例 prompt 1}"
- "{示例 prompt 2}"

**Expected Behavior**:
1. {步骤1}
2. {步骤2}
```

### 校验结果状态

| 状态 | 含义 |
|------|------|
| ✅ PASS | 全部校验通过 |
| ✅ PASS with WARNINGS | 通过但有建议项 |
| ❌ FAIL | 有必须修复的错误 |

| 标记 | 含义 |
|------|------|
| ✅ | 检查通过 |
| ❌ ERROR | 必须修复的问题 |
| ⚠️ WARNING | 建议修复的问题 |

## Usage

1. 加载此 skill
2. 提供待校验 skill 的路径
3. AI 会读取文件并输出校验报告

**示例 prompt**:
- "帮我校验 .cursor/skills/my-skill/ 是否符合模板规范"
- "validate skill at path/to/skill"
- "校验skill"
