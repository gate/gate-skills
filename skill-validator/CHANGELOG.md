# Changelog

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
