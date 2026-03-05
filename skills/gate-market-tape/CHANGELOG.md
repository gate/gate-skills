# Changelog

All notable changes to the **gate-market-tape** (Market Intelligence) skill are documented in this file.

## [2026.3.5-2] - 2026-03-05

### Changed
- **README**: 标题与技能名统一为 gate-market-tape；增加 Prerequisites（Gate MCP）、MCP 调用规范速查表、File Structure；架构图更新为 list_* MCP 工具名并指向 scenarios.md
- **SKILL.md**: name 改为 gate-market-tape，version 2026.3.5-2；增加前置条件与「MCP 调用速查」表；Case 6 明确 currency_pair 与 24h 成交额(quote)；深度比公式注明 USDT 口径
- **Scenarios**（references/scenarios.md）: 全场景已含 MCP 调用规范，本文档仅记录技能层优化

### Added
- README 中「MCP 调用规范速查」表，便于实现与文档一致

---

## [2026.3.5-1] - 2026-03-05

### Added
- Initial release of Market Intelligence skill (gate-market-tape)
- 7 analysis scenarios:
  - Case 1: Liquidity analysis (流动性分析)
  - Case 2: Momentum analysis (动能判断)
  - Case 3: Liquidation monitoring (爆仓监控)
  - Case 4: Funding rate arbitrage (费率套利)
  - Case 5: Basis monitoring (基差监控)
  - Case 6: Manipulation risk (操控风险)
  - Case 7: Order book explanation (订单簿解读)
- Smart spot/futures market detection
- MCP 调用规范与 Report Template（references/scenarios.md + SKILL.md）
- Domain knowledge and safety rules
