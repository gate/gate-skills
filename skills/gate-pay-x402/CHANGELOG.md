# Changelog

## [2026.4.10-1] - 2026-04-10

### Added

- **SKILL.md**: **`## MCP host setup (discovery + payment)`** — split **payment** (`gatepay-local-mcp` stdio) vs **discovery** (optional remote HTTP MCP); Cursor-style **`mcp.json`** example; reload guidance.
- **SKILL.md**: **MCP Server Connection Detection** split into **§A Payment MCP** and **§B Discovery MCP**; separate **Setup guide — payment MCP** and **Setup guide — discovery MCP**.
- **SKILL.md**: **When `discoveryResource` is mandatory** — order intent without sufficient merchant HTTP fields → call catalog on the **discovery server** before **`x402_place_order`** / **`x402_request`** on the **payment MCP**; exclusions documented.
- **SKILL.md**: **GatePay merchant discovery** — two-MCP model (catalog may live only on discovery server); **`discoveryResource`** logical args table (`resourceDes`, `resourceType`, pagination, `tenantId`); response mapping notes; **Error handling** row for catalog failures / empty items.

### Changed

- **SKILL.md**: Frontmatter **`version` / `updated`** → **`2026.4.10-1`** / **`2026-04-10`**; **`description`** rewritten (scope, wallet rails, bilingual triggers, explicit non-use cases).
- **SKILL.md**: **General Rules** — shared runtime rules defer to the **host** (no hardcoded registry URL for rules).
- **SKILL.md**: Allowlisted **merchant discovery** — may be on a **separate** MCP; typical tool **`discoveryResource`**; scan **all** servers; invoke on the server that lists the tool.
- **SKILL.md**: **Same-server rule** clarified as **payment-only** for **`x402_*`**; discovery may use another server id. **Workflow**, **Judgment Logic**, **Cross-Skill Collaboration**, and **Data handling** updated for pay vs discovery traffic.
- **SKILL.md**: **Routing Rules** — Chinese keyword hints in the table; MCP connectivity points to **MCP host setup** then connection detection; note that **`references/scenarios.md`** is QA-only, not runtime routing.
- **SKILL.md**: **Wallet configuration procedure** — localized Quick Wallet labels (**快捷钱包**, **gate/Gate钱包**); **payment MCP** wording in auth steps; note on npm single-tool builds listing only **`x402_request`**.
- **SKILL.md**: **How to build `arguments`** — resolve tool on **correct server** (discovery vs payment).
- **SKILL.md**: Tools table — **`discoveryResource`** row with parameter summary (still **`inputSchema`-first**).
- **SKILL.md**: **`## Execution`** renamed back to **`## Execution workflow`**; steps and x402 flow diagram reference dual MCP detection and mandatory discovery path.
- **SKILL.md**: **Safety Rules** (item 6) — **`x402_gate_pay_auth`** for **centralized_payment** when listed.

### Removed

- **SKILL.md**: **Auto-Update (Session Start Only)** section (session-start fetch/overwrite of canonical `SKILL.md`).

## [2026.4.2-1] - 2026-04-02

### Added

- **README.md**: Overview, core capabilities table, architecture diagram, usage and trigger pointers.
- **CHANGELOG.md**: Version history for this skill.
- **`references/scenarios.md`**: Four QA scenarios (MCP detection, vague wallet setup, pay consent gate, merchant URL flow).
- **SKILL.md**: **`## Domain Knowledge`**, **`## Scenarios`** pointer, **`## Execution`** (renamed from Execution workflow), **`## Safety Rules`** (renamed from Security Rules; cross-refs updated).

### Changed

- **SKILL.md**: Gate Pay MCP allowlist aligned with typical **`gatepay-local-mcp`** tool set: primary HTTP tool **`x402_place_order`**; **`x402_request`** documented only when listed on the server; added **`x402_gate_pay_auth`** for centralized_payment OAuth; merchant discovery no longer uses a placeholder tool name — call only tools present on the live list.
- **SKILL.md**: **MCP Server Connection Detection** accepts any valid **`x402_*`** entry point per package docs, not only `x402_place_order` / `x402_request`.
- **SKILL.md**: **Sub-Modules** section updated to reference **README**, **CHANGELOG**, and **scenarios.md**.

### Fixed

- Package layout and documentation now match skill-validator expectations (required sibling files and scenario file present).
