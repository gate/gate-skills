# skill-tester — 自动化 Skill 测试框架

> 读取目标 Skill 定义，自动生成测试用例、执行自测、输出飞书兼容的 Markdown 测试报告。

## 功能概览

- **L0 规范校验**：自动检查 SKILL.md 的结构、YAML front-matter、必填字段
- **L1 逻辑测试**：按模块生成自然语言 Prompt，验证触发词路由、工具调用链、输出格式
- **L2 相似问法 & 多语言**：自动生成口语化/简略/英文/中英混合变体 Prompt
- **L3 业务场景端到端**：多步骤链式业务流程测试（需人工确认）
- **L4 跨 Skill 联动**：多 skill 协同场景测试（需人工确认）
- **L5 多模型对比**：同一用例集在不同 AI 模型上执行，对比通过率
- **TSV 用例管理**：生成标准 TSV 格式测试用例文件，可复用
- **飞书兼容报告**：输出 Markdown 格式测试报告，支持完整版和精简版
- **外部文档认证**：自动处理飞书/Confluence/ 文档的 401/403 认证
- **多 Session 合并**：支持分多次执行测试，自动合并报告

## 快速开始

### 默认测试（L0 + L1）

```
帮我测试 gate-exchange-futures 这个 skill
```

### 含多语言测试（L0-L2）

```
测试 gate-exchange-futures 到 L2，包含多语言和相似问法
```

### 精简报告（仅失败/存疑）

```
帮我测试 gate-exchange-futures，只输出失败的用例
```

### 多模型对比

```
用 Claude 和 GPT 分别跑一遍 gate-exchange-futures 的测试用例
```

### 带外部需求文档

```
测试 xxx skill，需求文档在这里：https://xxx.feishu.cn/docx/xxx
```

## 文件结构

```
skills/skill-tester/
├── SKILL.md                              # Skill 主定义文件
├── README.md                             # 本文件
├── CHANGELOG.md                          # 版本变更记录
└── references/
    ├── test-case-template.md             # TSV 用例模板与字段说明
    ├── test-report-template.md           # 测试报告 Markdown 模板
    └── execution-guide.md               # 测试执行详细指南
```

## 产出文件

执行测试后会在项目根目录生成：

| 文件 | 说明 |
|------|------|
| `<skill-name>-test-cases.tsv` | 测试用例集 |
| `<skill-name>-test-report.md` | 完整测试报告 |
| `<skill-name>-test-report-part-N.md` | 临时报告（多 session 时） |

## 分层测试策略

| 层级 | 名称 | 优先级 | 执行方式 |
|------|------|--------|---------|
| L0 | Skill 编写规范校验 | P0 | AI 自动 |
| L1 | 文本 / 逻辑测试 | P0 | AI 自动 |
| L2 | 相似问法 & 多语言 | P1 | AI 自动 |
| L3 | 业务场景端到端 | P1 | 人 + AI |
| L4 | 跨 Skill 联动 | P2 | 人 + AI |
| L5 | 多模型表现对比 | P2 | AI 自动 |

默认执行 L0 + L1，可通过 Prompt 指定更高层级。

## 适用范围

- 交易类 Skill（合约、现货等）
- 非交易类 Skill（文档处理、数据查询、通知等）
- 自动适配不同类型 skill 的测试维度
