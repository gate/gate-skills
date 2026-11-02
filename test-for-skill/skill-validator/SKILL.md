---
name: skill-validator
version: "2026.11.2-1"
updated: "2026-11-02"
description: |
  校验 Skill 是否符合标准模板规范，支持标准架构和路由式架构的识别与校验；
  同时包含 ClawHub 合规检查（Purpose & Capability 一致性、引用文件完整性、工具命名、权限说明、发布包完整性）；
  以及与官方 gate/gate-skills 仓库 master 分支下 skills 目录中全部 Skill 的意图冲突扫描（路由重叠与互斥指引检测）。
  Use this skill whenever you need to validate a skill's structure, content, or ClawHub compliance.
  Trigger phrases include "校验skill", "检查skill格式", "validate skill", "ClawHub 合规检查", "check skill for ClawHub", "intent conflict", "skills 意图冲突", "gate-skills 意图冲突", or any request involving skill validation or template compliance check.
---

# Skill Validator

校验开发人员编写的 Skill 是否符合标准模板规范，检查目录结构、文件完整性、frontmatter 格式、必需章节等，并输出详细的校验报告。

## Gate CEX single-target routing

For `gate-cex-trade`, `gate-cex-earn`, `gate-cex-assets`, `gate-cex-subaccount`, `gate-cex-affiliate`, or `gate-cex-bot`, use [gate-cex-skill-audit](../../gate-cex-skill-audit/SKILL.md) as the current inspection contract. Review the selected directory or `SKILL.md` and its declared dependencies without requiring the other five packages.

For these six profiles, its bundled rules replace the legacy three-part category enum, mandatory README/CHANGELOG/scenarios, blanket relative-link prohibition, MCP-tool validation, and global pairwise scan below. Preserve the adapted structure, language, coverage and reference checks through that auditor. Do not run a repository-wide scan or legacy runner for a single-target request. Other legacy targets retain the workflow below.

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

**4.0 Frontmatter 语法完整性校验** (Both architectures, must run FIRST):

Before parsing any frontmatter fields, verify that the YAML frontmatter block itself is syntactically valid. This catches structural defects that would silently break all downstream parsing.

**4.0.1 文件首行必须是 `---`**

The very first line of `SKILL.md` (line 1, zero content before it) must be exactly `---` (three hyphens, no leading spaces, no trailing content).

Validation:
1. Read line 1 of `SKILL.md`
2. Strip trailing whitespace, then compare to `---`
3. If line 1 is NOT `---`:
   - ❌ **CRITICAL ERROR**: Frontmatter 未从文件首行开始
   - Record what line 1 actually contains
   - Common causes: developer added a paragraph, comment, or blank line before the frontmatter block

**4.0.2 Frontmatter 闭合标记 `---` 必须存在**

After the opening `---` on line 1, there must be a second `---` line that closes the YAML block. The closing `---` must appear before any Markdown heading (`# ...`).

Validation:
1. Starting from line 2, scan forward for a line that is exactly `---` (stripped of trailing whitespace)
2. Also scan for the first Markdown heading line (starts with `# `)
3. Rules:
   - If a closing `---` is found before any heading → ✅ PASS
   - If a heading is found before any closing `---` → ❌ **CRITICAL ERROR**: Frontmatter 缺少闭合标记 `---`
   - If end-of-file is reached with no closing `---` → ❌ **CRITICAL ERROR**: Frontmatter 缺少闭合标记 `---`

**4.0.3 Frontmatter 内不允许空行中断 YAML**

Between the opening and closing `---`, blank lines are tolerated by some parsers but are a strong signal of a malformed block (e.g., the developer forgot the closing `---` and the blank line is actually separating frontmatter from body).

Validation:
1. If a completely blank line (zero non-whitespace characters) appears between the opening and closing `---`, record:
   - ⚠️ **WARNING**: Frontmatter 块内有空行（第 {N} 行），可能导致解析异常

**4.0.4 Frontmatter YAML 键值格式校验**

Each non-blank line between the opening and closing `---` must be either:
- A YAML key-value line matching pattern `{key}: {value}` where key is `[a-zA-Z_][a-zA-Z0-9_]*`
- A **continuation line** of a multi-line quoted value: starts with whitespace (spaces or tabs) and is part of an unclosed quoted string from a previous line

Validation:
1. Track whether we are inside an unclosed quoted string (a line with `key: "...` or `key: '...` where the closing quote has not appeared yet)
2. If inside an unclosed quote, lines starting with whitespace are legal continuation lines — skip them
3. A line that contains the closing quote (`"` or `'`) ends the multi-line value
4. Lines that are NOT a key-value start and NOT a valid continuation → ❌ ERROR: Frontmatter 包含非法行

**Output format**:

```
Frontmatter 语法完整性校验
├── 首行检查: ✅ 首行为 `---` / ❌ 首行不是 `---`（实际: "{line_1_content}"）
├── 闭合标记: ✅ 找到闭合 `---`（第 {N} 行） / ❌ 缺少闭合 `---`
├── 空行检查: ✅ 无空行 / ⚠️ 第 {N} 行有空行
├── YAML 格式: ✅ 所有行格式正确 / ❌ 第 {N} 行格式异常
└── 校验结果: ✅ PASS / ❌ CRITICAL ERROR (后续字段校验不可靠)
```

**CRITICAL ERROR handling**: If 4.0 reports any CRITICAL ERROR, the validator must:
1. Still continue with all remaining checks (collect as many issues as possible)
2. Mark the entire frontmatter section as unreliable in the final report
3. Recommend fixing structural issues first before re-running validation

**4.1 Frontmatter 校验** (Both architectures):

**必需字段**:
| Field | Format | Validation |
|-------|--------|------------|
| `name` | `gate-{category}-{title}` (3 parts) or `gate-{category}-{a}-{b}` (4 parts) | Must follow naming convention (see below) |
| `version` | `YYYY.M.DD-N` | e.g., "2026.3.4-1" |
| `updated` | `YYYY-MM-DD` | Valid date format |
| `description` | String | Must contain "Use this skill whenever" and "Trigger phrases include" |

**Name Format Convention**:

Pattern (3 parts): `gate-{category}-{title}`  
Pattern (4 parts): `gate-{category}-{title-segment1}-{title-segment2}` — compound title; each segment follows the same rules as `title` below (lowercase letters only; use 4 parts only when the official name is a compound of two such segments).

- All lowercase, no underscores; no extra hyphens inside a title segment (a 4-part name has exactly one hyphen between the two title segments, for four `-`-separated parts total)
- `gate`: Fixed brand prefix
- `category`: Must be one of the following enums:
  - `exchange`: Existing legacy Pay identity only; the six CEX skills use the dedicated auditor.
  - `dex`: Dex domain
  - `wallet`: Gate Wallet
  - `news`: Data research side (news content, market anomaly interpretation, etc.)
  - `info`: Data research side (information & research, reports, in-depth research, K-line, alerts, on-chain info, etc.)
- `title` / title segments: Lowercase official product/function name; no spaces, no underscores, no hyphens within a segment

**Valid examples**:
- `gate-exchange-pay` ✅ (existing payment identity)
- `gate-wallet-transfer` ✅
- `gate-info-research` ✅
- `gate-info-deep-research` ✅ (4 parts, compound title)

**Invalid examples**:
- `gate-exchange-activity-center` ❌ (hyphens in title)
- `gate-exchange-Activity_Center` ❌ (uppercase & underscore)
- `gate-invalid-test` ❌ (invalid category)
- `exchange-market` ❌ (missing gate prefix)
- `gate-exchange` ❌ (missing title)
- `gate-info-deep-research-extra` ❌ (5 parts; only 3 or 4 parts allowed)

**Name validation checks**:
1. Must match directory name exactly
2. Must start with `gate-`
3. Must have **3 or 4** parts separated by `-` (not 2, not 5+)
4. Second part (category) must be in the valid enum list
5. **3-part names**: Third part (title) must be all lowercase letters, no special characters. **4-part names**: Third and fourth parts must each be all lowercase letters, no special characters (compound title)

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

### Step 10: 相对路径链接校验（Broken Link Prevention）

Scan all `.md` files in the skill directory for relative Markdown links that will 404 on the Skills Hub page.

**Background**: Skill files are hosted on GitHub, where relative links like `[text](./references/openapi.md)` resolve correctly. However, when rendered on `https://www.gate.com/skills-hub/detail/{skill-name}`, these relative links break and produce 404 errors.

**Detection rule**:
- Use regex pattern to detect Markdown links with relative paths: `/\[([^\]]+)\]\((?!https?:\/\/|#)([^)]+)\)/`
- This matches `[link text](path)` where `path` does NOT start with `http://`, `https://`, or `#` (anchor)

**Examples of broken patterns**:
- `[references/openapi.md](./references/openapi.md)` — ❌ relative path
- `[scenarios](references/scenarios.md)` — ❌ relative path
- `[detail](../other-skill/SKILL.md)` — ❌ relative parent path

**Allowed patterns**:
- `[Gate DEX](https://www.gatedex.com)` — ✅ absolute URL
- `[section](#architecture)` — ✅ anchor link within same page
- `` `references/openapi.md` `` — ✅ inline code (not a clickable link)

**Validation process**:

1. Read each `.md` file line by line
2. For each line, test against the relative link regex
3. If a match is found, record:
   - File name
   - Line number
   - The full matched link: `[text](path)`
   - Suggested fix: replace with inline code `` `path` `` or absolute GitHub URL
4. All matches are ❌ ERROR

**Output format**:

```
相对路径链接校验 (Broken Link Prevention)
├── SKILL.md: ✅ 无相对链接 / ❌ 发现 {N} 处相对链接
│   ├── Line {X}: [references/openapi.md](./references/openapi.md)
│   │   └── 建议: 改为 `references/openapi.md` 或绝对 URL
│   └── Line {Y}: [detail](../other/file.md)
│       └── 建议: 改为 `../other/file.md` 或绝对 URL
├── README.md: ✅ / ❌
├── references/{file}.md: ✅ / ❌
└── 校验结果: ✅ 无相对链接 / ❌ 发现 {Total} 处相对路径链接（将在 Skills Hub 页面 404）
```

### Step 11: 语言规范校验（English Only）

Scan all `.md` files in the skill directory to ensure content is written in English. Chinese characters are forbidden.

**Scope**: `SKILL.md`, `README.md`, `CHANGELOG.md`, `references/*.md`

**Detection rule**:
- Use regex pattern to detect Chinese characters: `/[\u4e00-\u9fff\u3400-\u4dbf]/`
- This covers CJK Unified Ideographs and Extension A

**Allowed exceptions**:
- Content inside frontmatter `description` field is **NOT** exempt — must also be English
- File paths or directory names containing Chinese are exempt (e.g., referencing external docs)
- Code blocks (``` fenced blocks) are **NOT** exempt — all content must be English

**Validation process**:

1. Read each `.md` file line by line
2. For each line, test against the Chinese character regex
3. If a match is found, record:
   - File name
   - Line number
   - The matched Chinese text (first 50 chars of the line)
   - Full line content for context
4. All matches are ❌ ERROR

**Output format**:

```
语言规范校验 (English Only)
├── SKILL.md: ✅ 无中文 / ❌ 发现 {N} 处中文
│   ├── Line {X}: "{matched_text}..."
│   └── Line {Y}: "{matched_text}..."
├── README.md: ✅ / ❌
├── CHANGELOG.md: ✅ / ❌
├── references/{file}.md: ✅ / ❌
└── 校验结果: ✅ 全部英文 / ❌ 发现 {Total} 处中文内容
```

### Step 12: MCP 工具调用校验

Validate that all MCP tool calls referenced in SKILL.md and scenario documents exist in the corresponding MCP service.

**12.1 自动发现所有 MCP 服务**

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

**12.2 提取 SKILL.md 中的工具调用**

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

**12.3 提取场景文档中的工具调用**

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

**12.4 验证工具存在性**

Use Step 12.1 构建的全局工具映射表进行校验：

**匹配规则（强制）**: 提取的工具名必须与 MCP 工具映射表中的 key **完全一致**（exact string match）。不允许前缀省略、后缀匹配、子串匹配或任何形式的模糊匹配。例如 `get_unified_accounts` 与 `cex_unified_get_unified_accounts` 视为 ❌ 不匹配。

1. 对每个提取的工具名，检查是否与全局工具映射表中某个 key 完全相等
2. 如果完全相等，记录所属的 MCP 服务名
3. 如果不与任何 key 完全相等，标记为 ❌ ERROR

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

**12.5 常见工具名前缀参考**

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

### Step 13: ClawHub 合规检查

Execute ClawHub compliance checks to prevent skill rejection or "suspicious" flagging on ClawHub.

**13.1 Purpose & Capability consistency**

- Extract claimed features from README and SKILL frontmatter `description` (keywords: order placement, transfer, convert, cancel, close position, trading)
- Extract declared tools from SKILL MCP Tools table (`create_*`, `cancel_*`, `update_*`, `close_*`, `*_transfer`, `*_convert`)
- If claimed write operations but tools only have `list_*`, `get_*`, `*_history` → ❌ ERROR

**13.2 Referenced file completeness**

- Search SKILL.md (and sub-module docs) for file references: `../`, `references/`, `gate-runtime-rules.md`, `*.md`
- For each path, resolve relative to skill root and check file existence
- Missing referenced file → ❌ ERROR

**13.3 Tool naming consistency**

- Extract tool prefix from SKILL (e.g. `cex_crx`, `cex_crossex`)
- If MCP tools directory available, compare doc prefix vs actual MCP prefix
- Mismatch → ❌ ERROR

**13.4 Credentials and permissions clarity**

- Search README for "API Key", "permission", "CrossEx", "read-only", "trade", "MCP"
- README should state which permissions the MCP/API Key needs
- Missing → ⚠️ WARNING

**13.5 Package completeness (for publish)**

- Parse SKILL Routing Rules or Module Overview for declared modules
- Map modules to reference files (Spot→spot-trading.md, Margin→margin-trading.md, etc.)
- Verify each file exists in `references/`
- Missing → ⚠️ WARNING

Key data to extract:
- clawhub_purpose_capability: pass/fail, mismatch detail
- clawhub_referenced_files: list, missing_files
- clawhub_tool_naming: pass/fail
- clawhub_credentials: pass/warning
- clawhub_package_completeness: pass/warning, missing_module_files

### Step 14: 跨 Skill 意图冲突扫描（官方 `gate/gate-skills` 全量 pairwise）

检测被测 Skill 与 **[gate/gate-skills](https://github.com/gate/gate-skills/tree/master) `master` 分支**下 **`skills/`** 目录中**除自身以外每一个** Skill 之间是否存在**路由级意图冲突**：用户一句自然语言或共享的触发表述可能同时激活两个 Skill，或两个 Skill 对同类用户目标给出互斥、竞争性的「何时使用本 Skill」指引。

**Peer 目录来源（权威目录）**：以 GitHub 上公开仓库 **`https://github.com/gate/gate-skills`** 的 **`master`** 分支、路径 **`skills/`** 为**唯一** peer 技能目录（与 [仓库根布局](https://github.com/gate/gate-skills/tree/master) 一致）。**不得**再以当前工作区本地 `repo_root/skills/` 作为 peer 集合——除非下文 **14.1** 判定当前仓库即为 `gate/gate-skills` 且已同步 `master`（此时本地 `skills/` 即该权威目录的副本）。

**强制执行规则**：

1. **必须全量遍历**：对 **14.1 解析得到的 `peer_catalog_root`** 下每个含 `SKILL.md` 的一级子目录逐一对比，**禁止抽样、禁止因数量多而跳过**。
2. **逐 Skill 扫描**：对列表中的每个 peer，完成「提取意图触达文本 → 判定冲突」的完整流程；不得将多个 peer 合并为一次模糊判断而省略某个目录。
3. **无关则标通过（仅内部判定）**：与某一 peer 无意图冲突时，内部可记通过；**最终校验报告不得**罗列「与每个 peer 无冲突」的逐项列表、逐 peer 通过表或全部 peer 名称——PASS 时见 14.5。
4. **冲突则告警**：若与任一 peer 存在意图冲突，在报告中**仅**输出发生冲突的项：必须**明确列出**每一个**发生冲突的 peer Skill**（`name` + 相对 **`gate/gate-skills` 的路径** `skills/{dir}`）及**每条**对应的**具体冲突提示词/触发语原文**（尽量逐字来自文档），并标明来源（被测 A / peer B）。**不得**在「意图冲突」小节混入无冲突 peer 的罗列。

**14.1 解析权威 peer 目录 `peer_catalog_root`**

目标：得到与 [gate/gate-skills `master` / `skills`](https://github.com/gate/gate-skills/tree/master/skills) 一致的 **`skills/`** 根路径，供枚举全部 peer。

1. **优先：浅克隆官方仓库（推荐）**  
   在可写目录执行（需网络与 `git`）：  
   `git clone --depth 1 --branch master https://github.com/gate/gate-skills.git`  
   然后设 **`peer_catalog_root` = `{clone_root}/gate-skills/skills`**（若克隆目录名不同，则为 `{clone_root}/<repo-name>/skills`）。  
   若 `master` 不存在，尝试 `main` 并在报告中注明所用分支。

2. **若当前工作区就是 `gate/gate-skills` 克隆**（例如 `origin` URL 含 `gate/gate-skills`）：可先 `git fetch origin master && git checkout master && git pull`，再设 **`peer_catalog_root` = `{repo_root}/skills`**。

3. **用户显式覆盖**：若用户提供 **`GATE_SKILLS_CATALOG`** 或等效路径，指向已存在的 **`.../skills`** 目录且用户声明其与官方 `master` 一致，可使用该路径作为 `peer_catalog_root`，并在报告中写明「peer 目录来源：用户指定」。

4. **失败则 SKIP**：若无法得到可读、且含至少一个子目录的 `peer_catalog_root`：⚠️ **WARNING**，记录「无法获取 gate/gate-skills 权威 `skills/` 目录，跳过意图冲突扫描」，本 Step **SKIP**（整体校验不因本项 alone 判 FAIL）。

**14.2 枚举 peer 列表并排除自身**

1. 列出 **`peer_catalog_root`** 下一级子目录中所有包含 `SKILL.md` 的路径，得到 `peer_skills`。
2. 从被测 Skill 的 `SKILL.md` 读取 frontmatter `name`（若暂不可用，则用 `skill_path` 的目录 basename）。
3. **排除与「被测 Skill 为同一包」的项**（满足任一即跳过该 peer）：
   - `peer` 目录的绝对路径与被测 `skill_path` 的绝对路径相同；或
   - 被测 Skill 位于 `skills/` 下且 `peer` 目录名等于被测 `name`；或
   - `peer/SKILL.md` 的 frontmatter `name` 等于被测 `name`。
4. 若被测 Skill **不在**官方目录树内（例如位于 `test-for-skill/`），仍对 **`peer_catalog_root` 下全部**其他包执行对比，**仅**按 `name` 相同排除（与官方目录中同名 Skill 视为同一 Skill，不与之做冲突对比）。
5. 若排除后列表为空（例如目录仅有自身）：本 Step ✅ PASS，说明「无其他 Skill 需对比」。

**14.3 提取「意图触达文本」（被测与每个 peer 均需做）**

从下列来源收集可供路由匹配的原文片段，每条注明 **文件路径** 与 **摘录**（保留触发语、用户表述类示例的原文）：

| 来源 | 提取要点 |
|------|----------|
| `SKILL.md` frontmatter | 完整 `description`（含 Trigger phrases 段落） |
| `SKILL.md` 正文 | 写明触发条件、激活场景、与其它 Skill 边界的段落 |
| `references/**/*.md` | `**Prompt Examples**:`（及同类列表）下所有 `- "` 条目；子模块中的用户问法示例 |
| `README.md` | 「When to use」「Trigger」「Core Capabilities」等面向**何时选用本 Skill** 的列表或表格中的用户向表述 |

汇总为 `intent_excerpts[]`，供 pairwise 判定使用。

**14.4 Pairwise 意图冲突判定提示词（对每个 peer 各执行一次）**

对 `peer_skills` 中**每一个**未排除的目录 `B`，读取其 `SKILL.md`（及 README、`references/` 中与前表相关部分），按 14.3 得到 `intent_excerpts_B`。然后由执行校验的 Agent **基于以下英文判定锚点完成推理**（不得省略某个 peer；不得仅输出「大概不冲突」而无逐项对比）：

```text
You are validating Gate Agent Skills for routing safety (intent conflict).

Skill under test (A):
- name: {name_A}
- path: {path_A}
- Intent-bearing excerpts (quoted from A's SKILL/README/references):
{list_A}

Peer skill from the gate/gate-skills master branch skills/ catalog (B):
- name: {name_B}
- path: {path_B}
- Intent-bearing excerpts (quoted from B's SKILL/README/references):
{list_B}

DEFINITION — INTENT CONFLICT (answer YES only if at least one holds):
- The same or near-duplicate user prompts / trigger phrases would reasonably cause BOTH skills to claim the invocation; OR
- Both skills assert primary ownership of the same user goal without a clear, documented boundary; OR
- For the same user scenario, the "when to use" guidance is contradictory or mutually exclusive.

NOT a conflict when:
- Clear domain or capability split (e.g., read-only research vs execution, different products with disambiguated triggers); OR
- One is an obvious subset and triggers defer to the other; OR
- Overlap is only generic words with materially different scoped intent.

TASK:
1. Conflict: YES or NO for this pair (A vs B).
2. If YES: list EVERY specific conflicting user-facing string — quote the minimal faithful substring from A or B's documents (trigger phrase or Prompt Example line). For each, label which skill (A or B) it comes from.
3. If YES: one line identifying B: name + path.

If NO: output only "Conflict: NO" for this pair.
```

**14.5 输出与总判定**

- 对每个 peer：内部记录 `Conflict: NO` / `YES`；`YES` 时保存冲突字符串列表与 `name_B`、`path_B`。
- **写入最终校验报告（本 Step）的规则**：
  - **✅ PASS**（全部 peer 无意图冲突，或无 peer）：**只写一行**总判定即可，例如：「与 [gate/gate-skills](https://github.com/gate/gate-skills) `master` 下其余 Skill 均未发现意图冲突（已扫描 peer 数：{N}）」；**禁止**在报告中列出每个 peer 的通过状态、禁止「分项结果」表逐行列出 ✅。
  - **⚠️ WARNING（意图冲突告警）**：**仅**输出「意图冲突」小节：用表格或列表**只包含**存在冲突的 peer；**必须**写清**发生冲突的 Skill**（每个 peer 的 `name` 与 `skills/{dir}`，相对官方仓库）以及**每条**冲突的**具体提示词/触发语原文**（及来源 A/B）。禁止用冗长列表重复「无冲突」的 peer。
- **无法获取** `gate/gate-skills` 权威 `skills/` 所致 SKIP：⚠️ WARNING，并在「问题汇总」中说明未执行全量 pairwise。

**报告措辞要求（必须遵守）**：

- 有意图冲突时，报告开头或本小节首句须**明确说明**存在意图冲突，并指向下列明细（例如：「以下 Skill 与当前被测 Skill 存在意图冲突，冲突提示词如下：」）。
- **禁止**在 PASS 情形下把「通过的 peer」全部罗列出来。

Key data to extract:

- `intent_conflict_catalog`: 固定为 `https://github.com/gate/gate-skills/tree/master/skills`（权威说明）
- `intent_conflict_peer_catalog_root`: 解析得到的本地 `peer_catalog_root`（绝对路径）及获取方式（clone / 当前仓库 / 用户指定）
- `intent_conflict_peer_total`: 排除自身后的 peer 数量
- `intent_conflict_pairs_resolved`: 已完成判定的 pairwise 次数（须等于 `peer_total`）
- `intent_conflict_result`: pass | warning | skip
- `intent_conflict_details`: `[ { peer_name, peer_path, conflicting_prompts: [ { text, from_skill } ], notes } ]`

### Step 15: 生成校验报告

Compile all validation results (Steps 1–14, including ClawHub 与跨 Skill 意图冲突扫描) and generate report.

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
| Frontmatter 首行不是 `---` | ❌ CRITICAL ERROR | SKILL.md 第一行必须是 `---`，可能有人在 frontmatter 前加了其他内容 |
| Frontmatter 缺少闭合 `---` | ❌ CRITICAL ERROR | 开头 `---` 后没有配对的闭合 `---`，YAML 解析将失败 |
| Frontmatter 块内有空行 | ⚠️ WARNING | 开闭 `---` 之间不应有完全空行，可能导致解析异常 |
| Frontmatter 包含非法行 | ❌ ERROR | 开闭 `---` 之间的行必须是合法 YAML key-value 格式 |
| Missing frontmatter field | ❌ ERROR | frontmatter 缺少必需字段 |
| Invalid frontmatter format | ❌ ERROR | frontmatter 格式不正确 |
| name 格式不符合 `gate-{category}-{title}`（或合法四段式 compound title） | ❌ ERROR | name 必须符合命名规范 |
| name 未以 `gate-` 开头 | ❌ ERROR | 必须以 gate 品牌前缀开头 |
| name 的 category 不在枚举列表 | ❌ ERROR | category 必须是: exchange/dex/wallet/news/info |
| name 的 title（或各 title 段）包含大写/下划线/段内短横线 | ❌ ERROR | title 段必须全小写，无下划线；段内无短横线 |
| name 部分数量不是 3 或 4 个 | ❌ ERROR | 必须为 gate-{category}-{title} 三段，或 gate-{category}-{a}-{b} 四段 |
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
| 文档中出现中文字符 | ❌ ERROR | Skill 文档必须全部使用英文，禁止出现中文 |
| 所有文档均为英文 | ✅ PASS | 所有 .md 文件中未检测到中文字符 |
| 文档中存在相对路径链接 | ❌ ERROR | 相对链接在 Skills Hub 页面会 404，必须改为 inline code 或绝对 URL |
| 无相对路径链接 | ✅ PASS | 所有 .md 文件中未检测到相对路径链接 |
| ClawHub: Purpose & Capability mismatch | ❌ ERROR | README 宣称写操作但 SKILL 只有 read-only 工具 |
| ClawHub: 引用文件缺失 | ❌ ERROR | SKILL 引用的文件不在 skill 包内 |
| ClawHub: 工具命名不一致 | ❌ ERROR | 文档工具前缀与 MCP 实际不一致 |
| ClawHub: 无权限说明 | ⚠️ WARNING | README 未说明 API Key 所需权限 |
| ClawHub: 发布包不完整 | ⚠️ WARNING | 声明的模块缺少对应 reference 文件 |
| 无法获取 gate/gate-skills 权威 `skills/`，跳过意图冲突扫描 | ⚠️ WARNING | 无法与官方目录内 Skill 做 pairwise 对比（见 Step 14.1） |
| 与 gate/gate-skills `master` 下全部 peer 均无意图冲突 | ✅ PASS | 内部全量 pairwise 无冲突；**报告**仅一行总判定（可含已扫描 peer 数），**不得**罗列逐 peer 通过项 |
| 与至少一个官方目录中的 peer 存在意图冲突 | ⚠️ WARNING | **报告**须明确说明存在冲突，且**仅**列出发生冲突的 Skill、`skills/{dir}`、**每条**冲突提示词原文；**不得**罗列无冲突 peer |

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

### Frontmatter 语法完整性

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 首行为 `---` | ✅/❌ | {首行为 `---` / 首行不是 `---`（实际: "{line_1_content}"）} |
| 闭合 `---` 存在 | ✅/❌ | {找到闭合 `---`（第 {N} 行） / 缺少闭合 `---`} |
| 无空行中断 | ✅/⚠️ | {无空行 / 第 {N} 行有空行} |
| YAML 行格式 | ✅/❌ | {所有行格式正确 / 第 {N} 行格式异常} |

### Frontmatter 字段

| 字段 | 状态 | 当前值 | 问题 |
|------|------|--------|------|
| name | ✅/❌ | {value} | {issue or "OK"} |
| version | ✅/❌ | {value} | {issue or "OK"} |
| updated | ✅/❌ | {value} | {issue or "OK"} |
| description | ✅/❌ | {truncated} | {issue or "OK"} |

### Name Format Validation

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 格式 `gate-{category}-{title}` 或四段 compound | ✅/❌ | {是否符合三段或四段结构} |
| `gate-` 前缀 | ✅/❌ | {是否以 gate- 开头} |
| Category 枚举 | ✅/❌ | {当前: {category}, 是否在 exchange/dex/wallet/news/info 中} |
| Title 格式 | ✅/❌ | {第三段（及第四段若存在）是否全小写，无下划线，段内无短横线} |
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

## 语言规范校验 (English Only)

| 文件 | 状态 | 中文出现次数 | 问题详情 |
|------|------|-------------|----------|
| SKILL.md | ✅/❌ | {N} | {无中文 / 第 X 行: "..."} |
| README.md | ✅/❌ | {N} | {无中文 / 第 X 行: "..."} |
| CHANGELOG.md | ✅/❌ | {N} | {无中文 / 第 X 行: "..."} |
| references/{file}.md | ✅/❌ | {N} | {无中文 / 第 X 行: "..."} |

**语言规范说明**: Skill 所有文档必须使用英文编写，禁止出现中文字符。

## 相对路径链接校验 (Broken Link Prevention)

| 文件 | 状态 | 相对链接数 | 问题详情 |
|------|------|-----------|----------|
| SKILL.md | ✅/❌ | {N} | {无相对链接 / 第 X 行: `[text](./path)`} |
| README.md | ✅/❌ | {N} | {无相对链接 / 第 X 行: `[text](path)`} |
| references/{file}.md | ✅/❌ | {N} | {无相对链接 / 第 X 行: `[text](path)`} |

**链接规范说明**: Skill 文档中禁止使用相对路径的 Markdown 链接（如 `[text](./file.md)`），因为在 Skills Hub 页面会产生 404。应改为 inline code 格式（如 `` `references/openapi.md` ``）或绝对 URL。

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

## ClawHub 合规检查

| 检查项 | 状态 | 说明 |
|--------|------|------|
| Purpose & Capability | ✅/❌ | README 宣称 vs SKILL 工具一致性 |
| 引用文件完整性 | ✅/❌ | 所有引用文件在包内 |
| 工具命名一致性 | ✅/❌ | 文档前缀 vs MCP 实际 |
| 凭证与权限说明 | ✅/⚠️/❌ | README 是否说明 API Key 权限 |
| 发布包完整性 | ✅/⚠️/❌ | 模块与 reference 文件对应 |

**ClawHub 说明**: 发布到 [ClawHub](https://clawhub.ai) 前建议修复所有 ❌。

## 跨 Skill 意图冲突扫描（官方 [gate/gate-skills](https://github.com/gate/gate-skills/tree/master) `master` / `skills` 全量 pairwise）

| 项目 | 结果 |
|------|------|
| 权威目录说明 | [gate/gate-skills `master` / `skills`](https://github.com/gate/gate-skills/tree/master/skills) |
| 本地 peer 目录 `peer_catalog_root` | {绝对路径}（来源：浅克隆 / 当前仓库为 gate-skills / 用户指定 `GATE_SKILLS_CATALOG`） |
| 排除自身后 peer 数 | {N} |
| 已完成 pairwise 次数 | {须等于 N / SKIP 说明} |
| **总判定** | ✅ PASS / ⚠️ WARNING（意图冲突告警）/ ⚠️ SKIP（无法获取权威 `skills/`） |

**报告写法（强制）**：

- **若 ✅ PASS**：本小节**仅保留**上表 + **一句**总判定（可含「已扫描 peer 数：{N}」）；**不要**增加「分项结果」表，**不要**逐行列出每个 peer 为 ✅。
- **若 ⚠️ WARNING**：**不要**写「分项结果」；**必须**写明：本被测 Skill 与下列 **{K} 个** Skill 存在**意图冲突**，并**列出**每一个发生冲突的 Skill 与对应提示词。

**意图冲突明细**（**仅当** ⚠️ WARNING 时填写；**只含**有冲突的 peer；无冲突 peer 不写）：

| 发生冲突的 Skill | 路径 | 冲突提示词原文 | 来源（被测 A / peer B） |
|------------------|------|----------------|----------------|
| `{name_B}` | `skills/{dir}` | `"..."`（逐字自文档） | A 或 B |

**说明行（⚠️ 时必填）**：例如「与当前被测 Skill 存在意图冲突的 Skill 共 **{K}** 个；上表列出各 Skill 与对应冲突提示词。」

---

若 ✅ PASS：除上表外，**仅一句**「与 [gate/gate-skills](https://github.com/gate/gate-skills) `master` 目录下其余 Skill 均未发现意图冲突（已扫描 peer：{N}）」——**不要**罗列通过的 peer 名称或逐 peer 表。

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
