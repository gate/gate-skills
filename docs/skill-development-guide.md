# Gate Skill 开发与测试指南

本文档面向内部开发人员和测试人员，介绍如何基于 gate-github-skills 仓库开发、校验和测试一个符合规范的 Skill。

---

## 适用范围：先选择产品契约

| 对象 | 编写、检查与安装入口 |
|------|--------------------|
| 六个 gate-cex-* | 使用 [gate-cex-skill-audit](../gate-cex-skill-audit/SKILL.md)、专属共享规则及正式 CEX 套件；先构建独立包，不使用下文旧模板或会话执行器。 |
| Info/News | 优先复用四个 CLI primary；旧兼容入口继续按各自 Step 0 处理 fallback。 |
| DEX | 按具体 Skill 声明的 CLI/OpenAPI/MCP 方式编写，不将一种渠道强加给所有 DEX。 |
| Pay | 两个支付产品独立；保留旧 Pay 所需的 Exchange 安装，业务调用与认证按支付产品契约。 |

先检索现有 Skill 和共享能力，优先复用或扩展，再决定是否需要新入口。
本文后续旧模板与 tester 流程仅适用于其明确支持的非 CEX 目标；占位名称不是已发布 Skill。
所有外部写操作均需明确授权及可靠隔离，私有地址、HTTP 或服务器名称不能单独证明测试环境。
`test-for-skill/test_skill.py` 是旧场景格式会话执行器，仅接受其声明的旧格式；不要因目录存在就认为它能解析当前 Skill 的场景。

## 目录

### 第一部分：开发指南

1. [获取仓库权限与分支管理](#1-获取仓库权限与分支管理)
2. [配置本地 MCP 环境](#2-配置本地-mcp-环境)
3. [拉取 skill-validator 到自己的分支](#3-拉取-skill-validator-到自己的分支)
4. [根据 skill-validator 规范开发 Skill](#4-根据-skill-validator-规范开发-skill)
5. [使用 skill-validator 校验 Skill](#5-使用-skill-validator-校验-skill)
6. [使用 skill-tester 进行自动化测试（可选）](#6-使用-skill-tester-进行自动化测试可选)

### 第二部分：测试指南

7. [获取测试仓库与环境准备](#7-获取测试仓库与环境准备)
8. [拉取待测 Skill 代码](#8-拉取待测-skill-代码)
9. [使用 skill-tester 进行自动化测试](#9-使用-skill-tester-进行自动化测试)
10. [辅助手工测试检查](#10-辅助手工测试检查)
11. [测试完成与报告输出](#11-测试完成与报告输出)

---

## 1. 获取仓库权限与分支管理

### 1.1 获取仓库权限

向管理员申请 [gate-github-skills](https://bitbucket.org/gateio/gate-github-skills/src) 仓库的读写权限。

### 1.2 克隆仓库

```bash
git clone https://bitbucket.org/gateio/gate-github-skills.git
cd gate-github-skills
```

### 1.3 创建个人开发分支

从 `test` 分支拉出自己的开发分支，命名规范为 `feature/<skill-name>`：

```bash
git checkout test
git pull origin test
git checkout -b feature/gate-info-yourskill
```

---

## 2. 配置本地 MCP 环境

本章仅适用于所选非 CEX Skill 明确声明的 MCP 依赖。
CEX 使用 Gate CLI，参考 [gate-cli-installer](../skills/gate-cli-installer/SKILL.md)，不执行本章配置。

### 2.1 配置 MCP Server

使用 [gate-mcp-installer](../skills/gate-mcp-installer/SKILL.md) 选择当前客户端和所需服务。
Exchange 连接模式保留给旧 Pay；DEX、Info、News 按产品说明选择。
不要在聊天或文档中填写真实密钥，也不要从安装完成推断已经获得业务写入授权。

### 2.2 测试凭据与环境

默认使用本地合成响应或明确隔离的 mock 服务。确需外部集成时，先确认目标端点、
账号、权限、数据和清理范围并取得相应授权。密钥只通过产品支持的安全渠道配置。

### 2.3 验证连接

先核对客户端暴露的工具名称及 schema；只执行已授权的只读验证。
工具不存在时停止或按产品约定降级，不为了测试新建订单、转账或付款。

---

## 3. 拉取 skill-validator 到自己的分支

[skill-validator](https://bitbucket.org/gateio/gate-github-skills/src/test/test-for-skill/skill-validator/) 是 Skill 规范校验工具，定义了 Skill 的标准模板和校验规则。开发前需要将其拉取到自己分支。

```bash
# 确保在自己的开发分支上
git checkout feature/gate-info-yourskill

# 从 test 分支拉取 skill-validator 和 skill-tester
git checkout origin/test -- test-for-skill/
```

拉取后，确认以下路径存在：

```
test-for-skill/
├── skill-validator/
│   └── SKILL.md          # 校验规范定义
└── skill-tester/
    └── SKILL.md          # 自动化测试框架（可选）
```

---

## 4. 根据 skill-validator 规范开发 Skill

### 4.1 让 AI 读取规范

开发 Skill 时，首先让 AI 读取 skill-validator 的规范，然后在其指导下进行开发。在 AI IDE 中输入：

```
请读取 test-for-skill/skill-validator/SKILL.md，然后根据该规范帮我开发一个新的 Skill。
我要开发的 Skill 功能描述如下：
[在这里用自然语言描述你的 Skill 功能]
```

**描述示例**：

> 先检查现有 Info/News Skill 是否已覆盖所需研究任务。
> 如需独立的新入口，声明精确触发意图、公开数据来源、只读范围与失败降级；
> 使用所选产品的现行契约编写，不复制交易或支付授权规则。

AI 会根据 skill-validator 的规范自动生成符合格式要求的 Skill 文件。

### 4.2 目录结构要求

业务 Skill 使用独立目录。以下是非 CEX 旧模板；六个 CEX 的最小入口与文件清单由专属 auditor 规定：

```
skills/gate-info-yourskill/
├── SKILL.md                    # [必需] AI Agent 运行时指令
├── README.md                   # [必需] 面向人类的说明文档
├── CHANGELOG.md                # [必需] 版本变更记录
└── references/
    └── scenarios.md            # [必需] 场景案例与 Prompt 示例
```

### 4.3 命名规范

先遵守 Agent Skills 的名称与目录一致规则；现有非 CEX 旧模板采用 `gate-{category}-{title}`。六个 CEX、安装器及开发审计工具使用各自已登记的身份，不套用此枚举。

| 部分 | 规则 | 说明 |
|------|------|------|
| `gate` | 固定前缀 | 品牌标识 |
| `category` | 枚举值 | `dex` / `wallet` / `news` / `info`；已有 `gate-exchange-pay` 保留身份，不新增旧 CEX 类别 |
| `title` | 全小写英文，无特殊字符 | 产品/功能名称 |

**现存示例**：`gate-dex-market`、`gate-info-coinanalysis`、`gate-news-briefing`；CEX 使用 `gate-cex-trade` 等六个已登记名称。

**名称检查**：目录名与 frontmatter 不一致、大小写或下划线不合规范应报错；不能仅因名称多于三段就否定现有已登记 Skill。

### 4.4 SKILL.md 编写要求

#### Frontmatter（必需）

```yaml
---
name: gate-info-yourskill
version: "2026.3.11-1"
updated: "2026-03-11"
description: "功能描述。Use this skill whenever ... Trigger phrases include '...', '...'"
---
```

- `name`：必须与目录名完全一致
- `version`：格式 `YYYY.M.DD-N`
- `description`：必须包含 `Use this skill whenever` 和 `Trigger phrases include`

#### 架构选择

根据 Skill 复杂度选择架构类型：

**标准架构**（单一功能，逻辑简单）：

SKILL.md 中必须包含：
- `# {Title}` — 一级标题
- `## Workflow` — 完整工作流（含所有步骤）
- `## Judgment Logic Summary` — 判断逻辑表格
- `## Report Template` — 报告模板

**路由架构**（多功能，逻辑复杂）：

SKILL.md 中必须包含：
- `# {Title}` — 一级标题
- `## Sub-Modules` 或 `## Routing Rules` — 路由规则
- `## Execution` — 执行流程说明
- `references/` 下的子模块文档

#### 推荐章节

以下章节强烈建议添加（缺少会产生 WARNING）：
- `## Domain Knowledge` — 领域知识（工具映射、业务规则等）
- `## Error Handling` — 错误处理
- `## Safety Rules` — 安全规则（交易类 Skill 必须添加）

#### Workflow 步骤格式

每个步骤应包含：

```markdown
### Step N: 步骤描述

Call `{tool_name}` with:
- param1: 说明
- param2: 说明

Key data to extract:
- `field_1`: 描述
- `field_2`: 描述
```

### 4.5 scenarios.md 编写要求

每个场景必须严格遵循以下格式：

```markdown
## Scenario N: {场景名称}

**Context**: {场景上下文描述，不能为空}

**Prompt Examples**:
- "{示例 prompt 1}"
- "{示例 prompt 2}"

**Expected Behavior**:
1. {步骤 1}
2. {步骤 2}
```

字段顺序必须为：Context → Prompt Examples → Expected Behavior（不可乱序）。

### 4.6 README.md 编写要求

必须包含以下章节：
- `## Overview` — 概述
- `### Core Capabilities` — 核心能力（含表格）
- `## Architecture` — 架构说明

### 4.7 CHANGELOG.md 编写要求

```markdown
## [2026.3.11-1] - 2026-03-11

### Added
- 初始版本，支持 xxx 功能
```

### 4.8 品牌规范

所有文档中**禁止使用 `Gate.io`**，公司品牌已升级为 **`Gate`**。

- ✅ 正确：`Gate`、`Gate Wallet`、`Gate Exchange`
- ❌ 错误：`Gate.io`、`gate.io`、`GATE.IO`

---

## 5. 使用 skill-validator 校验 Skill

Skill 开发完成后，使用 skill-validator 进行规范校验。

### 5.1 触发校验

在 AI IDE 中输入：

```
请校验 skills/gate-info-yourskill 这个 skill
```

或：

```
帮我检查 skills/gate-info-yourskill 是否符合 skill 规范
```

### 5.2 校验覆盖范围

skill-validator 会依次检查：

| 步骤 | 检查项 | 说明 |
|------|--------|------|
| 1 | 目录结构 | SKILL.md / README.md / CHANGELOG.md / scenarios.md 是否存在 |
| 2 | 架构类型检测 | 自动识别标准架构或路由架构 |
| 3 | Frontmatter 校验 | name / version / updated / description 格式 |
| 4 | 命名规范 | `gate-{category}-{title}` 格式校验 |
| 5 | 必需章节 | 根据架构类型检查必要章节 |
| 6 | Workflow 格式 | 步骤格式、MCP 工具调用声明 |
| 7 | scenarios.md 格式 | 场景结构严格校验（Context / Prompt / Expected Behavior） |
| 8 | README / CHANGELOG 格式 | 必需章节和版本格式 |
| 9 | 品牌文字规范 | 全局扫描禁止 `Gate.io` |
| 10 | MCP 工具校验 | 验证引用的 MCP 工具在 MCP 服务中是否存在 |

### 5.3 处理校验结果

- **❌ ERROR**：必须修复，否则 Skill 不符合规范
- **⚠️ WARNING**：建议修复，提高 Skill 质量
- **✅ PASS**：已通过校验

修复所有 ERROR 后重新运行校验，直到通过为止。

---

## 6. 使用 skill-tester 进行自动化测试（可选）

通过校验后，可以使用 skill-tester 进行更深入的自动化测试。

### 6.1 测试层级

| 层级 | 名称 | 说明 | 执行方式 |
|------|------|------|---------|
| L0 | 规范校验 | SKILL.md 结构与格式 | AI 自动 |
| L1 | 文本/逻辑测试 | 触发词路由、Prompt 理解、工具调用链 | AI 自动 |
| L2 | 相似问法 & 多语言 | 同义改写、口语化、英文/中英混合 | AI 自动 |
| L3 | 业务端到端 | 真实业务流程（需测试环境） | 人 + AI |
| L4 | 跨 Skill 联动 | 多 Skill 协同 | 人 + AI |
| L5 | 多模型对比 | 不同模型执行同一用例集 | AI 自动 |

### 6.2 触发测试

```
帮我测试 gate-info-yourskill 这个 skill
```

默认执行 L0 + L1。如需更多层级：

```
测试 gate-info-yourskill 到 L3
```

### 6.3 测试产出

- `<skill-name>-test-cases.tsv` — 测试用例文件
- `<skill-name>-test-report.md` — 测试报告（飞书兼容 Markdown）

---

## 完整开发流程总览

```
获取仓库权限 & 拉分支
        ↓
配置本地 MCP（测试环境）
        ↓
拉取 skill-validator 到自己分支
        ↓
让 AI 读取 skill-validator 规范
        ↓
用自然语言描述 Skill 功能 → AI 生成 Skill 文件
        ↓
使用 skill-validator 校验 → 修复 ERROR → 重新校验
        ↓
（可选）使用 skill-tester 自动化测试
```

---

---

# 第二部分：测试指南

本部分面向测试人员，介绍如何拉取开发提测的 Skill 代码，并使用 skill-tester 进行自动化测试和手工辅助检查。

---

## 7. 获取测试仓库与环境准备

### 7.1 获取仓库权限

向管理员申请 [gate-github-skills test 分支](https://bitbucket.org/gateio/gate-github-skills/src/test/) 的读写权限。

### 7.2 克隆仓库并切换到 test 分支

```bash
git clone https://bitbucket.org/gateio/gate-github-skills.git
cd gate-github-skills
git checkout test
git pull origin test
```

### 7.3 配置本地 MCP 环境

先按开头的产品表选择执行契约。仅 MCP 目标参考[第 2 章](#2-配置本地-mcp-环境)；
CEX 直接运行正式离线套件。不要把旧会话执行器或真实交易当作 CEX 的默认验证。

### 7.4 确认测试工具已就绪

确保 `test-for-skill/` 目录下包含以下工具：

```
test-for-skill/
├── skill-validator/
│   └── SKILL.md          # 规范校验工具
└── skill-tester/
    └── SKILL.md          # 自动化测试框架
```

如果缺失，从 `test` 分支拉取：

```bash
git checkout origin/test -- test-for-skill/
```

---

## 8. 拉取待测 Skill 代码

开发完成后，开发人员会将 Skill 提测到 `develop` 分支或个人特性分支。测试人员需要将待测代码拉取到本地。

### 8.1 方式一：从 develop 分支拉取（推荐）

当开发已合并到 `develop` 分支时，使用以下命令拉取指定 Skill：

```bash
# 更新远程分支信息
git fetch origin

# 从 develop 分支拉取 skills/ 目录下的所有 skill
git checkout origin/develop -- skills/
```

如果只需拉取某个特定 Skill：

```bash
# 仅拉取指定 skill，例如 gate-info-yourskill
git checkout origin/develop -- skills/gate-info-yourskill/
```

### 8.2 方式二：从开发的特性分支拉取

当开发尚未合并到 `develop`，而是提供了特性分支名时：

```bash
# 更新远程分支信息
git fetch origin

# 从开发的特性分支拉取指定 skill
git checkout origin/feature/gate-info-yourskill -- skills/gate-info-yourskill/
```

### 8.3 验证拉取结果

拉取完成后，确认 Skill 文件完整：

```bash
ls -la skills/gate-info-yourskill/
```

应至少包含以下文件：

```
skills/gate-info-yourskill/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    └── scenarios.md
```

---

## 9. 使用 skill-tester 进行自动化测试

skill-tester 是 AI 驱动的自动化测试框架，能够根据 Skill 定义自动生成测试用例、执行测试并输出报告。

### 9.1 触发自动化测试

在 AI IDE（Cursor / Claude 等）中输入：

```
请读取 test-for-skill/skill-tester/SKILL.md，然后帮我测试 skills/gate-info-yourskill 这个 skill
```

AI 会自动执行以下流程：

```
Step 1: 解析目标 Skill（读取 SKILL.md 和 references/）
    ↓
Step 2: 生成测试用例 TSV
    ↓
Step 3: 逐条执行测试
    ↓
Step 4: 生成测试报告
```

### 9.2 指定测试层级

默认执行 **L0（规范校验）+ L1（逻辑测试）**。可根据需要指定更高层级：

| 指令示例 | 执行范围 |
|---------|---------|
| `测试 gate-info-yourskill` | L0 + L1（默认） |
| `检查 gate-info-yourskill 的 skill 编写规范` | 仅 L0 |
| `测试 gate-info-yourskill 到 L2，包含多语言` | L0 + L1 + L2 |
| `端到端跑一下 gate-info-yourskill 的完整流程` | L0 ~ L3 |
| `只看失败的用例` | 生成精简报告 |

### 9.3 测试层级说明

| 层级 | 名称 | 优先级 | 执行方式 | 适用场景 |
|------|------|--------|---------|---------|
| **L0** | 规范校验 | P0 | AI 自动 | SKILL.md 结构、YAML frontmatter、必填字段、二次确认机制 |
| **L1** | 文本/逻辑测试 | P0 | AI 自动 | 触发词路由准确性、Prompt 理解、工具调用链、输出格式 |
| **L2** | 相似问法 & 多语言 | P1 | AI 自动 | 同义改写、口语化、英文/中英混合 Prompt |
| **L3** | 业务端到端 | P1 | 人 + AI | 业务入口到最终结果；默认使用合成依赖，真实外部写操作需单独授权 |
| **L4** | 跨 Skill 联动 | P2 | 人 + AI | 多 Skill 协同（现货查价 + 合约下单） |
| **L5** | 多模型对比 | P2 | AI 自动 | 同一用例集在不同模型上执行，对比通过率 |

### 9.4 测试产出物

| 文件 | 说明 |
|------|------|
| `<skill-name>-test-cases.tsv` | 测试用例文件（含编号、模块、层级、Prompt、预期行为、MCP 工具、状态） |
| `<skill-name>-test-report.md` | 飞书兼容的 Markdown 测试报告 |

### 9.5 结果状态定义

| 状态 | 符号 | 含义 |
|------|------|------|
| PASS | ✅ | API 调用成功 + 业务逻辑正确 + 输出格式符合预期 |
| PASS (有注意点) | ⚠️ | API 成功但存在优化空间 |
| FAIL | ❌ | 行为与预期不符 / 调用链错误 / 输出缺失关键信息 |
| BLOCKED | 🔒 | 因环境限制无法执行（余额不足/无持仓等） |
| SKIP | ⏭ | 当前版本不支持的功能 |
| 存疑 | ❓ | API 语义待确认 / 行为需进一步验证 |

---

## 10. 辅助手工测试检查

自动化测试完成后，建议结合手工检查覆盖以下方面：

### 10.1 L0 规范手工复核

对照 skill-validator 校验报告，重点确认：

| 检查项 | 关注点 |
|--------|--------|
| 命名规范 | `gate-{category}-{title}` 是否正确，与目录名是否一致 |
| description | 是否包含 `Use this skill whenever` 和 `Trigger phrases include` |
| 品牌用语 | 全文搜索确认无 `Gate.io`，均使用 `Gate` |
| 安全确认机制 | 交易类 Skill 是否要求用户二次确认后才执行变更操作 |

### 10.2 场景覆盖度检查

对照 `references/scenarios.md`，确认：

- 每个场景都有 Context、Prompt Examples、Expected Behavior
- Prompt 示例覆盖了核心业务路径
- Expected Behavior 中的 MCP 工具调用链与 SKILL.md 的工具映射一致
- 异常场景（余额不足、参数错误、无持仓等）有覆盖

### 10.3 关键业务流程手工验证

对于 L3 级别的端到端场景，建议手工在 AI IDE 中逐步执行：

```
1. 使用自然语言向 AI 发出操作指令
2. 观察 AI 是否正确识别意图并路由到对应模块
3. 确认 MCP 工具调用参数正确
4. 确认交易类操作是否弹出用户确认
5. 确认输出报告格式与 Report Template 一致
```

**重点验证场景**：

| 场景类型 | 验证要点 |
|---------|---------|
| 交易下单 | 是否要求确认？参数（币对/数量/价格/方向）是否正确传递？ |
| 异常处理 | 余额不足时是否给出友好提示？错误码是否被正确解读？ |
| 边界条件 | 最小下单量、价格精度、杠杆范围是否正确校验？ |
| 模糊输入 | "买点 BTC" 这类模糊 Prompt 能否正确理解？ |

### 10.4 生产环境调用检查

测试报告中会自动标记涉及 Gate 生产环境的调用。手工复核时注意：

- 外部调用必须属于已确认的隔离环境与授权范围；仅凭地址或 server 名不能判定安全
- 如果报告中出现 `⚠️ 生产环境调用` 标记，需确认是否为误报

---

## 11. 测试完成与报告输出

### 11.1 汇总测试结果

测试完成后，整合自动化测试报告和手工测试记录：

| 产出物 | 来源 | 说明 |
|--------|------|------|
| `<skill-name>-test-report.md` | skill-tester 自动生成 | 含 L0 规范校验 + L1/L2 逻辑测试结果 |
| `<skill-name>-test-cases.tsv` | skill-tester 自动生成 | 完整测试用例与执行状态 |
| 手工测试记录 | 测试人员补充 | L3 端到端、边界条件、模糊输入等 |

### 11.2 缺陷反馈

对于测试中发现的问题，按严重程度分类反馈给开发：

| 级别 | 说明 | 示例 |
|------|------|------|
| 🔴 严重 | 功能不可用或安全风险 | 交易操作未要求用户确认、工具调用链错误 |
| 🟡 一般 | 功能有偏差但不阻塞 | 输出格式不符合 Report Template、缺少错误处理 |
| 🟢 建议 | 可优化项 | 缺少 Domain Knowledge、Prompt 覆盖面不足 |

### 11.3 回归测试

开发修复问题后，测试人员重新拉取代码并复测：

```bash
# 重新拉取修复后的代码
git fetch origin
git checkout origin/develop -- skills/gate-info-yourskill/

# 重新运行自动化测试
# 在 AI IDE 中输入：
# "帮我测试 skills/gate-info-yourskill"
```

---

## 完整测试流程总览

```
获取仓库权限 & 切换到 test 分支
        ↓
配置本地 MCP（测试环境）
        ↓
拉取待测 Skill 代码（从 develop 或特性分支）
        ↓
skill-tester 自动化测试（L0 + L1，可扩展到 L2/L3）
        ↓
手工辅助检查（规范复核 + 业务流程验证）
        ↓
输出测试报告 & 反馈缺陷
        ↓
开发修复 → 回归测试 → 测试通过
```

---

## 附录：现有 Skill 参考

开发前建议参考以下已有的 Skill 实现：

| Skill | 架构类型 | 路径 | 参考价值 |
|-------|---------|------|---------|
| gate-cex-trade | CLI 业务入口 | `skills/gate-cex-trade/` | 当前 CEX 路由与共享规则，使用专属 auditor |
| gate-cex-bot | CLI 策略入口 | `skills/gate-cex-bot/` | 当前机器人边界与独立包 |
| gate-dex-market | 只读查询 | `skills/gate-dex-market/` | 非 CEX 产品契约 |
| gate-info-research | CLI primary | `skills/gate-info-research/` | Info/News 研究与 playbook 路由 |
