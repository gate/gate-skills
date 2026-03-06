# Skill Validator — Scenarios & Prompt Examples

## Scenario 1: 校验新创建的 Skill

**Context**: 开发人员刚创建了一个新的 skill，想检查是否符合模板规范。

**Prompt Examples**:
- "帮我校验 .cursor/skills/my-new-skill/ 是否符合模板规范"
- "validate the skill at .cursor/skills/my-new-skill/"
- "检查我写的 skill 格式对不对"

**Expected Behavior**:
1. Read skill directory structure
2. Check all required files exist
3. Validate SKILL.md frontmatter and sections
4. Validate README.md sections
5. Validate CHANGELOG.md format
6. Validate scenarios.md structure
7. Output detailed validation report

---

## Scenario 2: 修复后重新校验

**Context**: 开发人员根据上次校验报告修复了问题，想再次校验确认。

**Prompt Examples**:
- "再帮我校验一次 my-skill"
- "我修好了，重新检查下 skill 格式"
- "re-validate my skill"

**Expected Behavior**:
1. Read updated skill files
2. Re-run all validation checks
3. Compare with previous issues
4. Output new validation report showing fixed items

---

## Scenario 3: 只校验特定文件

**Context**: 开发人员只修改了 SKILL.md，想快速检查这个文件。

**Prompt Examples**:
- "只检查 my-skill 的 SKILL.md 格式"
- "validate only SKILL.md in my-skill"
- "帮我看看 SKILL.md 的 frontmatter 对不对"

**Expected Behavior**:
1. Read only SKILL.md file
2. Validate frontmatter fields
3. Validate required sections
4. Output focused validation report for SKILL.md only

---

## Scenario 4: 批量校验多个 Skill

**Context**: 项目中有多个 skill，想一次性校验所有。

**Prompt Examples**:
- "校验 .cursor/skills/ 下所有的 skill"
- "validate all skills in the skills directory"
- "批量检查所有 skill 格式"

**Expected Behavior**:
1. List all skill directories
2. Run validation on each skill
3. Output summary report with pass/fail status for each skill
4. Detail issues for failed skills

---

## Scenario 5: 校验操作类 Skill（含推荐章节）

**Context**: 开发人员创建了一个交易操作类 skill，需要检查是否包含领域知识、错误处理等推荐章节。

**Prompt Examples**:
- "校验我的 gate-futures-open-position skill"
- "检查 trading skill 是否完整"
- "validate my trading skill thoroughly"

**Expected Behavior**:
1. Run standard validation checks
2. Check recommended sections: Domain Knowledge, Error Handling, Safety Rules
3. Check Workflow step format: `Call \`{tool}\` with:`, `Key data to extract:`
4. Check scenarios.md has Context field for each scenario
5. Output report with warnings for missing recommended items

**Response Template**:
```
校验结果: ✅ PASS with WARNINGS

⚠️ 警告:
- 缺少 ## Safety Rules 章节，交易类 skill 建议添加安全规则
- Scenario 3 缺少 **Context**: 字段

建议:
1. 添加 Safety Rules 章节，说明风险提示、金额限制等
2. 为 Scenario 3 补充 Context 描述
```
