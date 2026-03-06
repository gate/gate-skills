# Changelog

All notable changes to the Gate-Exchange-Market skill are documented here.  
本文档记录 Gate-Exchange-Market 技能的所有变更。

Format: date-based versioning (`YYYY.M.DD`). Each release includes a sequential suffix: `YYYY.M.DD-1`, `YYYY.M.DD-2`, etc.  
版本格式：`YYYY.M.DD-N`。

---

## [2026.3.5-7] - 2026-03-05

### Changed
- **Bilingual documentation (中英双语文档):** SKILL.md and README.md support both English and 中文 in a single document. Section headers use "EN / 中文" or "Title / 中文标题"; key paragraphs and tables include both languages. Reports default to 中文 with English technical terms.
- **description:** Trigger phrases now include 中文 examples (e.g. 流动性, 深度, 滑点, 动能, 爆仓, 套利, 基差, 操控, 订单簿).

---

## [2026.3.5-1] - 2026-03-05

### Added
- Initial release (market tape analysis, seven scenarios) 首次发布（行情分析，七大场景）
- Routing-based SKILL.md with document loading from `references/scenarios.md`
- **Seven analysis modules 七大分析模块:** Liquidity 流动性, Momentum 动能, Liquidation 爆仓, Funding arbitrage 费率套利, Basis 基差, Manipulation risk 操控风险, Order book explainer 订单簿解读
- Smart spot/futures market detection (perpetual/contract keywords) 现货/合约识别（永续、合约等关键词）
- MCP call order and Report Template defined in `references/scenarios.md`
- Domain knowledge and safety rules 领域知识与安全规则
