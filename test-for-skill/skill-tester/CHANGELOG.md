# Changelog

本文件记录 skill-tester 的版本变更历史。

## [2026.3.9-5] - 2026-03-09

### 新增
- **生产环境调用检测与标记**：新增 SKILL.md 4.6 节，测试执行过程中自动检测 Gate.io 生产环境调用
  - 检测关键词：域名（`api.gateio.ws`、`gate.io` 等）、MCP Server（`gateapi`）、API 路径（`/api/v4/`）、工具名前缀（`gateapi__`）、MCP 端点（`api.gatemcp.ai`）
  - 操作分级：写操作标为 🔴 高风险，读操作标为 🟡 中风险
  - 报告中新增「⚠️ 生产环境调用提醒」汇总区块（2.4 节）
  - Gate.io 业务 Skill 特殊处理：整体声明避免逐条冗余标注
- **execution-guide.md 新增「生产环境调用检测指南」**：定义检测时机、关键词、操作类型判定规则和标记方式
- **test-report-template.md 新增「2.4 ⚠️ 生产环境调用提醒」**：报告模板中增加生产环境调用汇总表和检测逻辑说明

### 变更
- SKILL.md 版本升级至 2026.3.9-5
- SKILL.md description 增加 "production environment call detection (Gate.io highlighting)"
- test-report-template.md Case 详情区增加「生产环境」标注字段

## [2026.3.9-4] - 2026-03-09

### 新增
- **MCP 认证处理流程**：新增 Step 0.3，支持 MCP Server 返回 401/403 时的完整认证处理
  - 自动检测：通过 `mcporter list <server-name>` 探测认证状态
  - 自动认证：尝试 `mcporter auth <server-name>` 自动完成认证
  - 手动认证：认证失败时向用户展示详细的 Token/Cookie 获取步骤（浏览器 F12 → Network → 请求头）
  - 凭证注入：通过 `mcporter config add --header` 注入 Bearer Token 或 Cookie
  - 安全原则：凭证不写入报告/日志，测试完成后提示用户清理

### 变更
- SKILL.md 版本升级至 2026.3.9-4
- 原 Step 0.3（文档内容解析）重编号为 Step 0.4
- 异常处理表（3.4）新增 MCP 认证失败（401/403）处理条目，引用 Step 0.3 流程

## [2026.3.9-3] - 2026-03-09

### 新增
- **变更操作二次确认校验**：L0 规范校验新增第 9 项，要求涉及资金/账户/用户数据变更的操作必须在 SKILL 中定义用户二次确认环节（🔴 高严重级别）
- **L1 变更操作确认验证**：PASS/FAIL 判定条件扩展，涵盖资金变更、账户设置变更、用户信息变更、授权变更四大类操作的确认步骤校验
- **变更操作范围定义**：明确列出需要二次确认校验的操作类别（下单/转账/提现、修改杠杆/密码、修改绑定信息、API Key 管理等）

### 变更
- SKILL.md L0 校验表从 8 项扩展至 9 项
- execution-guide.md L0 校验清单同步更新
- execution-guide.md L1 PASS/FAIL 判定标准从"交易操作"扩展到所有"变更操作"
- 非交易类 Skill 的二次确认校验项可标记为 N/A

## [2026.3.9-2] - 2026-03-09

### 新增
- **分层测试策略（L0-L5）**：按优先级组织测试，支持 L0 规范校验到 L5 多模型对比
- **L0 Skill 编写规范校验**：自动检查 YAML front-matter、触发条件、执行流程等 8 项规范
- **L2 相似问法 & 多语言 Prompt 生成**：自动生成口语化/简略/英文/中英混合/同义替换变体
- **外部文档认证处理**：支持飞书、Confluence、GitHub 文档的 401/403 认证流程
- **多 Session 报告合并**：支持分多次执行测试，自动合并临时报告为最终报告
- **精简报告模式**：支持只展示失败/存疑用例的简化报告
- **异常处理与容错**：MCP 不可用、超时、API 限流等场景的处理策略
- **非交易类 Skill 适配**：针对非交易 skill 调整测试维度和校验重点
- **TSV 新增 `测试层级` 列**：标识每条用例所属的测试层级（L0-L5）

### 变更
- 重构 SKILL.md，整合所有新功能到完整的执行流程（Step 0-5）
- 更新 execution-guide.md，增加分层执行策略和多 session 执行指南
- 更新 test-case-template.md，增加 L2 变体生成规则和非交易 skill 适配
- 模型表现对比表增加主流模型参考列表（Claude、GPT、Gemini、DeepSeek、Qwen）

### 文档
- 新增 README.md
- 新增 CHANGELOG.md

## [2026.3.9-1] - 2026-03-09

### 初始版本
- 基础测试框架：读取 SKILL.md → 生成 TSV 用例 → 执行测试 → 输出报告
- 测试用例 TSV 格式定义
- 飞书兼容 Markdown 测试报告模板
- API vs MCP 调用方式标记
- 测试执行指南
