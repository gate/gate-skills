# Changelog

All notable changes to the Gate Options Trading skill are documented here.

Format: date-based versioning (`YYYY.M.DD`). Each release includes a sequential suffix: `YYYY.M.DD-1`, etc.

---

## [2026.3.11-4] - 2026-03-11

### Changed (aligned with futures skill, all English)

- **SKILL.md**: Rewritten in English; structure aligned with gate-exchange-futures: routing with "Read `references/...`" and "Unclear" row, execution workflow with "Unit conversion" table (contracts / base notional / quote USDT), pre-flight checks, confirmation wording ("Reply 'confirm' to place the order"), Report template, Safety rules with Confirmation and **Errors** table (insufficient balance, order_size_min, contract not found, order not found, amend not supported). Removed all Chinese (币数, 张数).
- **references/place-order.md**: Retitled "Gate Options Place Order — Scenarios & Unit Conversion"; added Unit Conversion section with User phrase → Intent → Type table, Data sources, Base notional → contracts and Quote (USDT) → contracts formulas, Precision, Pre-Order Confirmation; Scenario 1 (market/limit) and Scenario 2 (mark IV) with Prompt Examples, Expected Behavior, Response Template. All in English.
- **references/close-position.md**: Rewritten in English with API semantics and four scenarios: Close all (one position), Partial close (half or N contracts), Close all positions / by condition (PnL filter), Limit close at price. Each with Prompt Examples, Expected Behavior, Response Template.
- **references/cancel-order.md**: Rewritten in English with API note (single vs batch cancel) and three scenarios: List orders then choose, Cancel by strike/expiry/contract, Cancel all (one-click). Each with Prompt Examples, Expected Behavior, Response Template.
- **references/amend-order.md**: Rewritten in English with three scenarios: Change price, Change size, Change both. Backend support note and response templates. All in English.
- **README.md**: Prerequisites updated to mention unit conversion (base notional / USDT → contracts) in one line.

---

## [2026.3.11-3] - 2026-03-11

### Added

- **Size: base notional / quote (USDT) → contracts**. The API accepts size only in contracts. User may say base notional (e.g. "1 BTC call", "0.1 ETH put") or quote USDT (e.g. "1000U", "half of account"). Conversion: base → contracts = base_amount / multiplier (from `get_options_contract`); quote → contracts = usdt_amount / price_per_contract. Explicit "X contracts" → use that integer. Default "X [base]" to notional and convert. Documented in `references/place-order.md` and SKILL.md execution workflow and safety.

---

## [2026.3.11-2] - 2026-03-11

### Improved

- **Close position**: Documented API semantics — full close uses `close: true`, `size: 0`; partial close uses `reduce_only: true` and size (negative for long, positive for short). Market = price `"0"`, tif `"ioc"`. Note on `order_size_min` for partial size.
- **Place order**: Added contract name format; "strike at current price" resolution via underlying ticker and nearest strike; precision (order_size_min, order_price_round) from `get_options_contract`.
- **Cancel order**: Documented single cancel by order_id vs batch cancel (DELETE with optional underlying, contract, side). Note on listing open orders first when user specifies strike/expiry without order_id.
- **Amend order**: Clarified that amend may be backend-dependent (trading-api/MCP); if unsupported, prompt user to cancel and replace. Note on price/size precision.
- **SKILL.md**: Execution workflow now includes contract format, disambiguation (expiration / strike), pre-checks (balance, order_size_min), and amend fallback. Safety rules extended with precision and amend-not-supported handling.

---

## [2026.3.11-1] - 2026-03-11

### Added

- **Case 1 — Market/limit place order**: English trigger phrases, tool sequence (list underlyings/expirations/contracts, order book, account, create_options_order), output template.
- **Case 2 — Mark IV place order**: Same resolution flow; mark IV or IV-to-price then create order; output template.
- **Case 3 — Close/reduce position**: Trigger phrases (market/limit close, half, all, by price or PnL); tool sequence (list_options_positions, filter, create_options_order for close); output template.
- **Case 4 — Cancel open orders**: Trigger phrases (cancel one by strike/expiry, cancel all by side/underlying, one-click cancel); tool sequence (list_options_orders status=open, cancel_options_order); output template.
- **Case 5 — Amend open order**: Trigger phrases (change price, halve size); tool sequence (list open orders, amend); output template.
- Reference docs: `references/place-order.md`, `references/close-position.md`, `references/cancel-order.md`, `references/amend-order.md`.
- SKILL.md: routing table, module overview, tool mapping, execution workflow, response templates, safety rules (all in English).

---

## [0.0.1] - 2026-03-11

### Added

- Template structure (SKILL.md, README.md, CHANGELOG.md, references/)
