---
name: gate-skill-summary
version: "2026.3.26-5"
updated: "2026-03-26"
description: "Summarizes a designated Gate skill SKILL.md by adding or updating an MCP Dependencies block (required servers, tools split into Query vs Execution with empty lists omitted, Permissions list derived from tool names segment-2 + Query/Write with Write winning per key, conditional Get API Key, installation check). Use when the user asks to add MCP summary, skill summary block, gate-skill-summary, document MCP deps for a skill, or fill the MCP Dependencies template after General Rules."
---

# gate-skill-summary

Add or refresh a standardized **MCP Dependencies** section in a target `skills/<skill-name>/SKILL.md` (this repository). The block documents which MCP server the skill needs, which tools it uses, authentication expectations, and IDE installer skill names.

---

## When to run

- User names a skill directory or path under `skills/`.
- User asks to “summarize MCP / tools / installation” for a skill document.

**Do not** apply to non-skill markdown unless the user explicitly asks.

The six `gate-cex-*` business skills use CLI only. Do not add MCP dependency blocks to them; use [the top-level auditor](../../../gate-cex-skill-audit/SKILL.md) for their review rules.

---

## Step 1 — Resolve target file

1. Default: user-provided path, e.g. `skills/gate-info-coinanalysis/SKILL.md`.
2. If only a skill name is given, resolve `skills/<name>/SKILL.md`.
3. Confirm the file exists before editing.

---

## Step 2 — Map skill name prefix → `{MCP_NAME}`

Use the **first matching** prefix on the skill folder name (the segment after `skills/`, before `/SKILL.md`):

| Prefix | `{MCP_NAME}` (table cell) |
|--------|---------------------------|
| `gate-exchange-` | Gate (main) |
| `gate-dex-` | Gate-Dex |
| `gate-info-` | Gate-Info |
| `gate-news-` | Gate-News |
| `gate-growth-` | Gate (main) |
| `gate-mcp-` | **Multi-row**: list **Gate (main)**, **Gate-Dex**, **Gate-Info**, and **Gate-News** each as its own row in **Required MCP Servers** (installer skills cover the full Gate MCP set described in that skill). |

If a skill text clearly depends on an additional server (e.g. `gate-cex-pub`, `gate-cex-ex`) and the doc says so, add a short bullet under **Authentication** or after the table — do not invent servers not implied by the doc.

---

## Step 3 — Extract MCP tool names (grep)

From the target `SKILL.md` only (not `references/` unless the user asks):

1. **Backtick tool names** (primary):
   ```bash
   rg -o '`([a-z][a-z0-9_]*)`' skills/<skill>/SKILL.md
   ```
   Keep tokens that look like MCP/API tools (e.g. `cex_*`, `dex_*`, snake_case with multiple segments). Drop prose, file names, and single generic words (`coin`, `page`, `amount`).

2. **Tables** that label a column `MCP tool`, `Tool`, or similar: collect cell values that match the same pattern.

3. **Dedupe**; then **classify** each tool (see below); sort **alphabetically within each class**.

4. **Empty lists — omit the subsection**: Do **not** render a **Query Operations** heading or any bullets under it when the query list is empty. Do **not** render **Execution Operations (Write)** when the write list is empty. If **both** lists are empty after extraction, omit the entire **MCP Tools Used** section (no heading, no placeholder bullets). Flag “no tools found” for human review when both are empty.

**Read vs write classification**

- **Query Operations (Read-only)**: Tools that only fetch or list data (positions, balances, history lists, product discovery, market data, KYC status reads, etc.). Typical name hints: `_list`, `_get`, `_query`, `_find` when the doc frames them as non-mutating.
- **Execution Operations (Write)**: Tools that create, update, cancel, transfer, swap, place orders, withdraw, or otherwise change account or chain state. Typical hints: `swap`, `order`, `place`, `cancel`, `transfer`, `withdraw`, `submit`, or explicit “execute” / “trade” wording in the **Tool selection** / **Execution** sections.
- Use the skill’s own tables and safety rules as source of truth. If ambiguous, treat as **Write** when the doc requires **user confirmation** before calling the tool; otherwise default to **Query**.

For each bullet: `- {tool_name} - {description}`  
`{description}` is optional; one short clause from the same table row or adjacent sentence. If nothing clear, end after the tool name.

---

## Step 4 — Authentication

**Branch on whether the skill depends on a CEX / API key** (per `SKILL.md` and runtime rules):

1. **No API key dependency** (public MCP, Dex/Info/News-only, or doc states no API key): Under **Authentication**, output **only**:
   - `- API Key Required: No`  
   Do **not** add **Permissions** or **Get API Key** lines in this branch.

2. **API key or authenticated exchange MCP applies**:
   - **API Key Required**: `Yes`, plus a short qualifier when needed (local `gate-mcp` vs remote OAuth, etc.). Use `See skill doc` only when the doc is ambiguous.
   - **Permissions** (`{list}`): **Comma-separated `K:V` pairs** (e.g. `Spot:Read`, `Futures:Write`). **`V`** is **only** `Read` or `Write`. Build `{list}` **after** you have filled **`{tool_query_*}`** and **`{tool_write_*}`** (same tool names as under **MCP Tools Used**), using the rules below.

**How to build `{list}` from tools**

1. **Format**: `K:V` for each distinct **K**, comma-separated, e.g. `Spot:Read, Futures:Write`.

2. **Derive `K` from each tool name** (every `{tool_query_*}` and `{tool_write_*}`): split the token on **`_`**. Take the **second segment** (the segment after the first `_`; 1-based “第2个” = second field). Use that string as the business-permission key. **Display**: capitalize for readability — **first letter uppercase**, rest lowercase (e.g. `spot` → `Spot`, `earn` → `Earn`, `coin` → `Coin`). If a token has **fewer than two** segments after extraction, skip it or derive **K** from the skill doc / adjacent table (do not invent keys).

3. **Derive `V` per tool, then merge per `K`**:
   - If the tool appears under **Execution Operations (Write)** → that tool contributes **`V = Write`** for its `K`.
   - If the tool appears under **Query Operations (Read-only)** → that tool contributes **`V = Read`** for its `K` **only for merging**; the final `V` for that `K` is chosen in step 4.

4. **Deduplicate by `K`; `Write` wins**: For each distinct `K`, there must be **exactly one** pair `K:V`. If any tool mapped to `K` is **Write**, the final **`V` is `Write`**. If **no** Write tool maps to `K` but at least one Query tool does, **`V` is `Read`**. Do **not** output both `K:Read` and `K:Write` for the same `K` — output **`K:Write`** only when both kinds exist.

5. **Sort**: List pairs in **ascending order by `K`** (string order) unless the target skill already groups domains in a fixed order for readability — prefer consistent ordering across skills.

6. **Get API Key**: Include **only** when the **Permissions** line is present (at least one `K:V` pair). Use `https://www.gate.io/myaccount/profile/api-key/manage` when API-key management applies; use `N/A` (or a one-line reason) when the doc says keys are not used or not applicable for that skill.

If **Permissions** would be empty (no `K:V` pairs — e.g. no tools listed under **MCP Tools Used**), **omit** both the **Permissions** line and the **Get API Key** line; leave only **API Key Required** (and optional qualifier) under **Authentication**.

**Filled example — public / no API key**

```markdown
### Authentication
- API Key Required: No
```

**Filled example — authenticated (`K:V` Permissions)**

*Illustration:* `cex_earn_asset_list` / `cex_earn_find_coin` → Query; `cex_earn_swap_staking_coin` → Write. Second segment `earn` → **K** = `Earn`. Write present → **Earn:Write** (not `Earn:Read` and `Earn:Write`). If `cex_wallet_get_total_balance` is Query-only → **Wallet:Read**.

```markdown
### Authentication
- API Key Required: Yes (local **gate-mcp**); or Gate OAuth when using remote exchange MCP — see runtime rules and MCP deployment
- Permissions: Earn:Write, Wallet:Read
- Get API Key: https://www.gate.io/myaccount/profile/api-key/manage
```

---

## Step 5 — Block template (exact structure)

Insert **once**. If `## MCP Dependencies` already exists, **replace** that section through the end of **Installation Check** (up to but not including the next `##` heading at the same level as `## MCP Dependencies`).

Use this template (fill variables):

```markdown
## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| {MCP_NAME} | ✅ Required |

### MCP Tools Used

Include **Query Operations** only if there is at least one query tool; include **Execution Operations (Write)** only if there is at least one write tool. If both lists are empty, omit the whole **MCP Tools Used** section.

**Query Operations (Read-only)** *(omit this block if the query list is empty)*

- {tool_query_1}
- {tool_query_2}

**Execution Operations (Write)** *(omit this block if the write list is empty)*

- {tool_write_1}
- {tool_write_2}

### Authentication

- **If no API key dependency:** only `- API Key Required: No`
- **If API key applies:** `- API Key Required: Yes` (optional qualifier). Add `- Permissions: {list}` where **`{list}`** = comma-separated **`K:V`** built from **`{tool_query_*}`** / **`{tool_write_*}`** (second `_` segment → **K**; merge per **K** with **Write** over **Read**). Add `- Get API Key: {URL_or_N/A}` **only** when **Permissions** is present. If `{list}` is empty, omit **both** Permissions and Get API Key.

### Installation Check
- Required: {MCP_NAME}
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`
```

**Variable rules**

- `{MCP_NAME}`: only **Gate (main)** / **Gate-Dex** / **Gate-Info** / **Gate-News** (see Step 2). For multiple rows, repeat the table row pattern for each required server.
- `{tool_query_*}` / `{tool_write_*}` / `{description}`: from Step 3 after read/write split; omit entire **Query** or **Execution** subsections when that list is empty; delete spare bullets and unused placeholder lines.
- **`{list}` / Permissions**: From **all** `{tool_query_*}` and `{tool_write_*}`: **K** = second `_`-delimited segment (capitalized); **V** = `Write` if the tool is listed under **Execution Operations (Write)**, else `Read` if only under **Query**; **one pair per K**, final **V** = **Write** if any tool for that **K** is Write. After `:` only `Read` or `Write`.
- `{URL_or_N/A}`: Only when Permissions is shown (Step 4).
- **Authentication formatting**: Follow Step 4 branches and **Filled examples**; for API-key skills without a Permissions mapping, only the **API Key Required** line appears under **Authentication**.

**Installation Check**

- Keep wording exactly as in the template (uniform across skills).
- Line 1 under **Installation Check**: repeat the same `{MCP_NAME}` text as in **Required** (for multi-server skills, use a comma-separated list on one line: `Required: Gate (main), Gate-Dex, Gate-Info, Gate-News`).

---

## Step 6 — Insertion position

1. Locate `## General Rules` in the target `SKILL.md`.
2. Find the **end** of that section: the content through an optional following `---` and blank lines, **stopping before** the next top-level `##` (e.g. `## Module overview`, `## Domain Knowledge`, `## Resources`).
3. Insert a blank line if needed, then the filled **## MCP Dependencies** block.
4. Preserve existing content order: **General Rules** → **MCP Dependencies** → rest of document.

If **General Rules** is missing, insert **MCP Dependencies** immediately after the frontmatter `#` title block (after the first H1 section intro) and before the next `##`, then flag for human review.

---

## Step 7 — Human review and acceptance

After editing:

1. **Diff check**: MCP block present once; no duplicate `## MCP Dependencies`.
2. **Prefix vs content**: If the skill text explicitly names a different MCP than the prefix mapping, prefer the doc and adjust the table (leave a short note in review for the maintainer).
3. **Tools**: Spot-check classification (read vs write) and 2–3 tool names against the skill’s tool tables / execution sections.
4. **Installers**: Four IDE skill names must appear exactly as listed in the template.

Hand off to the user for final approval before merge.

---

## Quick checklist (copy for the agent)

```
Task Progress:
- [ ] 1. Resolve path to skills/<name>/SKILL.md
- [ ] 2. Map skill folder prefix → MCP_NAME (multi-row for gate-mcp-*)
- [ ] 3. Grep / table extract → dedupe → split Query vs Execution → sort within each → omit empty Query/Execution blocks (omit whole MCP Tools Used if both empty)
- [ ] 4. Fill Authentication (No API key: only API Key Required: No; else API Key Required + `Permissions: {list}` from tools — `K` = 2nd `_` segment, `V` = Read/Write with Write winning per `K` + Get API Key only when `{list}` non-empty)
- [ ] 5. Paste template; set Installation Check + Required line
- [ ] 6. Insert immediately after General Rules (before next ##)
- [ ] 7. Human review + acceptance
```
