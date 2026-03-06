# Changelog

All notable changes to the **gate-market-tape** (Market Tape Intelligence) skill are documented in this file.

## [2026.3.5-5] - 2026-03-05

### Changed (Case 6: Manipulation risk)
- **Trigger words**: Explicitly added "这个币深度和成交比怎么样" / "容易操控吗" in SKILL and scenarios.
- **Tools**: Spot path remains `list_order_book` → `list_tickers` → `list_trades`. When user says **perpetual/contract** (永续、合约), use **futures** path: `list_futures_order_book` → `list_futures_tickers` → `list_futures_trades`.
- **Judgment logic** (unchanged, clarified): Top 10 depth total / 24h volume < 0.5% → "thin depth" (深度薄); 24h trades have consecutive same-direction large orders → "possible manipulation" (可能有主力在控盘).
- **scenarios.md**: Case 6 MCP Call Spec table now has separate spot vs futures columns; added Scenario 6.3 for futures manipulation query (e.g. "BTC永续容易操控吗").
- **README**: Case 6 row in MCP call order table updated to show spot vs futures branch.

---

## [2026.3.5-4] - 2026-03-05

### Changed
- **references/scenarios.md**: Fully translated to English; format and style aligned with `gate-market/references/scenarios.md`.
- Title set to "Gate Market Tape Intelligence — Scenarios & MCP Call Specs"; intro and overview table in English.
- Each Case (1–7): "MCP Call Spec" tables (Step, MCP Tool, Parameters, Required Fields), "Calculation & judgment", and "Output" requirements in English.
- All sub-scenarios (e.g. 1.1, 1.2, 2.1–2.3, 3.1–3.2, 4.1–4.2, 5.1–5.2, 6.1–6.2, 7.1–7.2) use **Context**, **Prompt examples** (EN + 中文 where useful), **Expected behavior**, and **Output** blocks in English.
- Report templates and example outputs (tables, labels, risk notices) translated; structure unchanged for implementation consistency.

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
