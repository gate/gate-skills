# Changelog

## [2026.3.30-2] - 2026-03-30

### Changed
- **Invalid examples**：增加五段 `name` 不规范样例（`gate-info-deep-research-extra`）；README 同步。

## [2026.3.30-1] - 2026-03-30

### Changed
- **Name validation**：`name` 允许 **3 段或 4 段**（`-` 分隔），四段式为 compound title（第三、四段规则与单段 title 一致）。同步更新 Name Format Convention、Name validation checks、Judgment Logic、Report Template「Name Format Validation」及 README 能力说明。

## [2026.3.26-3] - 2026-03-26

### Changed
- **跨 Skill 意图冲突扫描（Step 14）peer 来源**：由「当前工作区仓库根下 `skills/`」**改为**官方 **[gate/gate-skills](https://github.com/gate/gate-skills/tree/master) `master` 分支**下的 **`skills/`** 全量 Skill（与公开目录一致）。优先通过浅克隆官方仓库解析 `peer_catalog_root`；若当前仓库即为 `gate/gate-skills` 且已同步 `master`，可用本地 `{repo_root}/skills`；支持用户通过 `GATE_SKILLS_CATALOG` 等显式指定等价路径。无法获取权威目录时 SKIP 并说明。
- Report Template、Judgment Logic、frontmatter `description` / Trigger phrases 已同步上述约定。

## [2026.3.26-2] - 2026-03-26

### Changed
- **跨 Skill 意图冲突扫描（Step 14）报告规则**：最终报告 **PASS** 时仅保留一行总判定 + 汇总表，**禁止**罗列每个 peer 的通过项或「分项结果」逐行表；**WARNING** 时 **仅**列出**存在意图冲突**的 Skill，并**必须**明确写出各 Skill 与**每条**冲突提示词原文，**禁止**混入无冲突 peer 的罗列。
- Report Template「跨 Skill 意图冲突扫描」章节与 Judgment Logic 对应行已同步上述写法。

## [2026.3.26-1] - 2026-03-26

### Added
- **跨 Skill 意图冲突扫描** (Step 14)：
  - 以仓库根下 `skills/`（@skills）为目录，**排除自身后**对其余**每一个**含 `SKILL.md` 的一级子目录做 **pairwise** 语义比对，禁止抽样或跳过。
  - 从 `description`、Trigger phrases、`Prompt Examples`、README 中何时使用本 Skill 等提取「意图触达文本」，使用 SKILL 内嵌英文判定锚点识别路由重叠、主职责争夺或互斥指引。
  - 全部 peer 无意图冲突 → ✅ PASS；任一对冲突 → ⚠️ WARNING，并在报告中列出**冲突提示词原文**与**对方 Skill**（name + `skills/{dir}`）。
- Step 15：生成校验报告（由原 Step 14 顺延）。
- Report Template 与 Judgment Logic Summary 增加「跨 Skill 意图冲突扫描」章节与判定行。
- frontmatter `description` / 触发短语补充意图冲突相关说明。

### Changed
- Workflow 自 14 步增至 15 步。
- Step 13.2 引用文件完整性：搜索关键词由 `exchange-runtime-rules` 改为 `gate-runtime-rules.md`（与仓库共享运行时规则文件名一致）。

## [2026.3.19-1] - 2026-03-19

### Added
- **ClawHub 合规检查** (Step 13):
  - 整合原 clawhub-check 技能，校验时自动执行 ClawHub 检查
  - 13.1 Purpose & Capability 检查：SKILL.md 明确技能目的与能力边界
  - 13.2 引用文件完整性：references 下文件存在且可访问
  - 13.3 工具命名一致性：MCP 工具命名与 MCP 服务保持一致
  - 13.4 凭证与权限说明：API key / OAuth 等凭证获取与权限说明
  - 13.5 发布包完整性：README、CHANGELOG、使用说明完整
- Report Template 新增「ClawHub 合规检查」章节
- Judgment Logic Summary 新增 5 条 ClawHub 相关判断规则

### Changed
- Workflow 步骤从 12 步增加到 14 步（新增 Step 13 ClawHub 合规检查，原生成报告顺延为 Step 14）
- description 与触发词补充 ClawHub 相关说明

### Removed
- 删除独立 clawhub-check 技能目录，功能已整合至 skill-validator
- 删除 `references/clawhub-usage-guide.md`：使用说明已精简至本 CHANGELOG 与 SKILL.md

### Audit
- ✅ ClawHub 检查与标准模板校验同步执行
- ✅ 支持 ClawHub 发布前预检与「suspicious」问题排查

## [2026.3.7-1] - 2026-03-07

### Added
- **MCP 工具调用校验** (Step 10):
  - 自动检测关联的 MCP 服务（如 `user-gateapi`）
  - 从 SKILL.md 提取工具调用（Tool Mapping 表格、Case Routing Map、Workflow 步骤）
  - 从 scenarios.md 提取工具调用（Fetch data via、Expected Behavior 步骤）
  - 验证所有引用的工具是否存在于 MCP 服务中
  - 输出不存在的工具列表和未使用的可用工具参考
- Report Template 新增「MCP 工具校验」章节：
  - 关联 MCP 服务信息
  - SKILL.md 工具匹配详情
  - scenarios.md 工具匹配详情
  - 未使用的 MCP 工具参考
- Judgment Logic Summary 新增 4 条 MCP 工具校验规则

### Changed
- Workflow 步骤从 10 步增加到 11 步（新增 MCP 工具校验）

### Audit
- ✅ MCP 工具校验覆盖 SKILL.md 和 scenarios.md
- ✅ 支持自动推断关联 MCP 服务
- ✅ 提供详细的工具匹配报告

## [2026.3.6-1] - 2026-03-06

### Added
- **Skill 命名规范校验**:
  - 新增 `gate-{category}-{title}` 命名格式检查
  - 验证 `gate-` 品牌前缀
  - 验证 category 枚举值（exchange/dex/wallet/news/info）
  - 验证 title 格式（全小写，无下划线，无短横线）
  - 验证三部分结构（必须是 3 个部分，用 `-` 分隔）
- Report Template 新增「Name Format Validation」章节
- Judgment Logic Summary 新增 5 条命名规范相关校验规则

### Changed
- Frontmatter 校验中的 name 字段从 `kebab-case` 更新为 `gate-{category}-{title}` 格式
- README.md 核心能力表新增「命名规范校验」
- README.md 新增详细的命名规范说明和示例

### Audit
- ✅ 命名规范校验覆盖所有要求
- ✅ 错误提示明确具体
- ✅ 向后兼容现有校验逻辑

## [2026.3.5-2] - 2026-03-05

### Added
- **路由式架构支持** (Routing Architecture):
  - 新增架构类型检测（Standard / Routing）
  - 路由架构识别规则：检测 `## Routing Rules` 或 `## Sub-Modules` 章节
  - 路由架构特定校验：验证子模块文档存在性和完整性
  - 子模块文档校验：验证 Workflow 和 Report Template
- Judgment Logic Summary 更新：
  - 路由架构的判断逻辑可以在 `## Routing Rules` 表中
  - 子模块文档不要求独立的 Judgment Logic Summary
- Report Template 增强：
  - 新增「架构检测」部分
  - 新增「子模块文档校验」部分
  - 新增「架构评估」部分

### Changed
- Workflow 步骤从 7 步增加到 9 步（新增架构检测和子模块校验）
- 必需章节校验根据架构类型区分：
  - Standard Architecture: 需要 Workflow, Judgment Logic Summary, Report Template
  - Routing Architecture: 需要 Routing Rules/Sub-Modules, Execution, 子模块文档
- 校验逻辑更灵活：路由式架构不会因缺少标准章节而报错

### Audit
- ✅ 支持两种架构模式：标准架构和路由架构
- ✅ 路由架构校验逻辑完整
- ✅ 向后兼容：标准架构的校验规则不变

## [2026.3.5-1] - 2026-03-05

### Added
- scenarios.md 新增 `**Context**:` 字段校验
- SKILL.md 新增推荐章节校验：
  - `## Domain Knowledge` — 领域知识
  - `## Error Handling` — 错误处理
  - `## Safety Rules` — 安全规则
- SKILL.md 新增 Workflow 步骤格式校验：
  - `Call \`{tool}\` with:` 格式
  - `Key data to extract:` 声明
  - `**Pre-filter**:` 前置条件
- Report Template 新增推荐章节和 Workflow 格式检查表格
- 校验结果新增 `PASS with WARNINGS` 状态

### Changed
- 问题汇总分为「错误」和「警告」两部分
- scenarios.md 校验新增 Context 字段检查列

## [2026.3.4-1] - 2026-03-04

### Added
- 初始版本
- 目录结构校验（SKILL.md, README.md, CHANGELOG.md, references/scenarios.md）
- SKILL.md frontmatter 校验（name, version, updated, description）
- SKILL.md 必需章节校验（Workflow, Judgment Logic Summary, Report Template）
- README.md 章节校验（Overview, Core Capabilities, Architecture）
- CHANGELOG.md 格式校验
- scenarios.md 结构校验
- 详细校验报告模板

### Audit
- ✅ 校验规则覆盖所有模板必需项
- ✅ 报告模板清晰易读
- ✅ 错误提示具有可操作性
