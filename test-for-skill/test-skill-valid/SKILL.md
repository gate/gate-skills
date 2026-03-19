---
name: test-skill-valid
version: "2026.3.4-1"
updated: "2026-03-04"
description: 一个用于测试校验工具的示例 Skill。Use this skill whenever you need to test the skill validator. Trigger phrases include "测试skill", "test skill", or any request involving validation testing.
---

# Test Skill Valid

这是一个完全符合模板规范的测试 Skill，用于验证 skill-validator 能够正确识别合规的 skill。

## Workflow

When the user asks to test something, execute the following steps.

### Step 1: 接收输入

Receive user input and validate parameters.

Key data to extract:
- `input_data`: 用户输入数据
- `options`: 可选配置

### Step 2: 处理数据

Process the input data according to business logic.

**Pre-filter**: Only process valid input data

### Step 3: 输出结果

Generate and return results to user.

## Judgment Logic Summary

| Condition | Flag/Signal | Meaning |
|-----------|-------------|---------|
| 输入有效 | ✅ VALID | 可以继续处理 |
| 输入无效 | ❌ INVALID | 拒绝处理 |

## Report Template

```markdown
# 测试结果

**输入**: {input}
**状态**: {status}
**输出**: {output}
```
