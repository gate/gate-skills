# gate-exchange-collateralloan — Skill Validator Report

**Run**: 2026-03-18

## Summary

| Check | Result |
|-------|--------|
| Structure (SKILL, README, CHANGELOG, references/scenarios.md) | PASS |
| Routing architecture (Routing Rules, Execution, Trigger Conditions) | PASS |
| Frontmatter: `Use this skill whenever` + `Trigger phrases include` | PASS |
| Name `gate-exchange-collateralloan` | PASS |
| English-only (SKILL, README, CHANGELOG, references) | PASS |
| No relative-path Markdown links | PASS |
| Brand (no legacy domain spelling) | PASS |
| scenarios.md field order (Context → Prompt Examples → Expected Behavior) | PASS |
| MCP tools vs `user-g-d-ex` | PASS (all `cex_mcl_*` listed exist) |

## Docs change (this release)

- **REST/API mapping removed**; replaced by **`references/mcl-mcp-tools.md`** (MCP-only).
- Repay tool documented as **`cex_mcl_repay_multi_collateral_loan`**; create/operate use wrapper JSON keys **`order`**, **`repay_loan`**, **`collateral_adjust`** per MCP.
