---
name: TestSkillBadFormat
version: "v1.0"
updated: "2026/03/04"
description: 这个描述缺少触发场景说明
---

# Test Skill Bad Format

这个 skill 故意有多个格式错误：
1. name 不是 kebab-case（使用了大写）
2. name 与目录名不匹配
3. version 格式不正确（应该是 YYYY.M.DD-N）
4. updated 日期格式不正确（应该是 YYYY-MM-DD）
5. description 缺少 "Use this skill whenever" 和 "Trigger phrases include"
6. 缺少 Judgment Logic Summary 章节
7. 缺少 Report Template 章节

## Workflow

When user asks something, do nothing.

### Step 1: 无操作

Nothing here.
