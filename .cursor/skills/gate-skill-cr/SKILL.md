---
name: gate-skill-cr
version: "2026.3.27-5"
updated: "2026-03-27"
description: "Review skill branches in gate-github-skills. Compares the current (or specified) branch against the main branch, checks language quality, Markdown syntax, skill naming conventions, directory completeness, SKILL.md format, SKILL.md content quality, shared rules reference, CHANGELOG format, references integrity, trading safety rules, Gate.IO brand references, ClawHub marketplace compliance (including before-install credential vs manifest alignment, undeclared host/installer dependencies, write-permission proportionality, platform confirmation-flow enforcement, dynamic code execution prohibition, system credential file access prohibition, persistence mechanism modification prohibition, privilege escalation prohibition, and expanded ClawHub pre-install checklist (credential channel, provenance, outbound docs)), data privacy, content safety, risk disclaimers, and tool annotation accuracy. After all steps complete, MUST emit a full Markdown review report in the response (see Output Format). Trigger phrases: review branch, skill review, CR, code review, check branch."
---

# gate-skill-cr

Review skill branches in the **gate-github-skills** repository. Validates language, Markdown, naming, structure, format, content quality, shared rules, CHANGELOG, references integrity, trading safety, brand compliance, ClawHub marketplace compliance (including **before-install** checks: credential documentation vs registry manifest, minimal-scope keys, publisher/source transparency, and end-user install risk when credential flow is unclear), data privacy & collection, content safety & prohibited activities, risk disclaimers, fair play, and tool annotation accuracy for all changes introduced by a feature branch.

---

## Gate CEX single-target routing

For an explicit audit of `gate-cex-trade`, `gate-cex-earn`, `gate-cex-assets`, `gate-cex-subaccount`, `gate-cex-affiliate`, or `gate-cex-bot`, follow [gate-cex-skill-audit](../../../gate-cex-skill-audit/SKILL.md) before applying the legacy branch flow below. Accept the selected skill directory or its `SKILL.md`; do not require another business package or a feature-branch diff.

The new auditor reuses the applicable review and testing checks with the current CLI-only architecture, English policy, local package links, and bounded prior authorization. Its bundled rules supersede conflicting legacy naming, relative-link, MCP, scenario-layout, and confirmation requirements for those six profiles. A target on main/master must still be reviewed in full. Do not execute legacy MCP fixtures or conversation runners for this route.

For all other legacy branch reviews, retain the flow below. If a branch request contains both new CEX targets and other skills, review each new CEX target independently with the new auditor and apply the legacy flow only to the remaining scope; keep results distinct. Do not expand a single-target request into a repository-wide review.

The `gate-cex-skill-audit` package itself is a development utility, not a seventh business profile. Review its standard format, inspection contract, evidence handling, links and safety separately; do not reject it using the legacy exactly-three-part category enum or require trading product references inside it.

## Input

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `branch` | No | Current branch (`git branch --show-current`) | The branch to review against the main branch |

---

## Execution Flow

### Step 0 — Resolve branch and main branch

```
1. If user provided a branch name, use it; otherwise run `git branch --show-current`.
2. Detect main branch: check if `main` exists (`git rev-parse --verify main`), else check `master`.
3. If current branch IS the main branch (main or master), STOP and report:
   "Current branch is the main branch ({name}). No review needed."
4. Otherwise proceed with: REVIEW_BRANCH = resolved branch, MAIN_BRANCH = main or master.
```

### Step 1 — Collect diff

```
git diff {MAIN_BRANCH}...{REVIEW_BRANCH} --name-status
git diff {MAIN_BRANCH}...{REVIEW_BRANCH}
```

Collect:
- **Changed files list** (added / modified / deleted) with paths.
- **Full diff content** for analysis.

Identify which files fall under `skills/` and which are outside.

### Step 2 — Language quality check

For every added or modified file in the diff:

**Policy:** Skill content must be **English end-to-end** for headings, instructions, tables, lists, narrative, **Prompt Examples**, scenario **Context** / **Expected Behavior**, README, and CHANGELOG. **Non-English text** (including CJK in those areas) is an **Error**, not a Warning — same bar as publication-ready Skills Hub copy.

**Scope for 2.2–2.5:** Apply checks outside **narrow exempt regions** only: content inside fenced code blocks (between matching `` ``` `` pairs), content inside inline code spans (backticks) when the entire span is machine/code text, and raw URLs. **Do not** treat `**Prompt Examples**:` lines, scenario prose, or table cells as exempt — hypothetical user quotes in scenarios must still be **written in English**. Inside exempt regions, do not flag CJK or full-width punctuation for 2.2–2.5.

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 2.1 | Grammar and fluency | Warning | Check for broken or unnatural English sentences. Flag sentences that are hard to understand. |
| 2.2 | English as core language | **Error** | **All skill-facing prose** outside narrow exempt regions (see above) must be English. Detect CJK ideographs with `[\u4e00-\u9fff\u3400-\u4dbf]`. Any occurrence outside exempt regions is an **Error**. Aligns with strict English-only skill content. |
| 2.3 | Spelling | Warning | Flag obvious typos or misspellings. |
| 2.4 | Inappropriate non-English / CJK inside English prose | **Error** | When a sentence or bullet is **predominantly English** but embeds CJK or other non-English script mid-clause outside exempt regions, flag **Error** (code-switching, bilingual fragments, or copy-paste that violates English-only policy). Unavoidable proper nouns in Latin script are fine; if ambiguous, flag **Error** with rationale. |
| 2.5 | Chinese / full-width punctuation in English prose | **Error** | In English narrative outside exempt regions, flag **Error** when **Chinese-style or full-width punctuation** appears where standard English ASCII punctuation is expected—for example: `，` `。` `、` `：` `；` `（）` `「」` `【】` `…` (full-width ellipsis) as sentence punctuation in otherwise English lines. Use ASCII `, . : ; ( ) " ' -` as appropriate. Full-width punctuation is allowed **only** inside narrow exempt regions (e.g. inside a code block that intentionally shows foreign sample data). |

### Step 3 — Markdown syntax check

For every `.md` file in the diff:

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 3.1 | Heading hierarchy | Warning | Headings should follow a logical hierarchy (no skipping levels, e.g. `#` → `###` without `##`). |
| 3.2 | Unclosed code blocks | Error | Every `` ``` `` must have a matching closing `` ``` ``. |
| 3.3 | Broken links / images | Warning | `[text](url)` and `![alt](url)` should have non-empty url. Relative paths should point to existing files. |
| 3.4 | Table formatting | Warning | Tables must have a header row, a separator row (`|---|`), and consistent column counts. |
| 3.5 | Trailing whitespace / blank lines | Info | Excessive trailing whitespace or more than two consecutive blank lines. |
| 3.6 | List formatting | Warning | List items should use consistent markers (`-` or `*` or `1.`), and nested lists should be indented properly. |
| 3.7 | Relative link detection (Skills Hub) | Error | Markdown links with relative paths (e.g. `[text](./references/file.md)`, `[text](../other.md)`) will produce 404 on the Skills Hub page (`https://www.gate.com/skills-hub/detail/{skill-name}`). Flag all relative links; suggest replacing with inline code format (`` `references/file.md` ``) or absolute URLs. Allowed: `https://` URLs, `#anchor` links. Reference: skill-validator Step 10. |

### Step 4 — Skill naming convention

If the diff adds a **new directory** under `skills/`, check the directory name:

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 4.1 | Three-part naming pattern | Error | Directory name must match `gate-{category}-{title}` with exactly 3 parts separated by `-`. Example: `gate-exchange-spot`, `gate-info-coinanalysis`. |
| 4.2 | `gate-` prefix | Error | Directory name must start with `gate-`. |
| 4.3 | Category enum validation | Error | The `{category}` segment (second part) must be one of: `exchange` (CEX trading, finance, assets, account), `dex` (DEX domain), `wallet` (Gate Wallet), `news` (news content, market anomaly), `info` (research, reports, K-line, alerts, on-chain). Any other value is invalid. Reference: skill-validator §4.1. |
| 4.4 | Title format | Error | The `{title}` segment (third part) must be all lowercase letters only — no uppercase, no underscores, no hyphens. E.g. `spot` ✅, `activitycenter` ✅, `activity-center` ❌, `Activity_Center` ❌. |
| 4.5 | No uppercase | Error | Directory name must not contain uppercase letters. |

### Step 5 — Skill directory completeness

For every **new skill directory** under `skills/`:

| # | Required file | Severity | Description |
|---|---------------|----------|-------------|
| 5.1 | `SKILL.md` | Error | Must exist. The skill entry point. |
| 5.2 | `README.md` | Error | Must exist. Human-readable documentation with Overview, Core Capabilities, and Architecture sections. |
| 5.3 | `CHANGELOG.md` | Error | Must exist. Tracks version history. |
| 5.4 | `references/scenarios.md` | Error (Standard) / Warning (Routing) | For standard architecture skills, must exist. For routing architecture skills where scenarios are distributed across sub-module documents, `scenarios.md` is optional — but at least one sub-module must contain scenarios. |

### Step 6 — SKILL.md format validation

For every `SKILL.md` in the diff (new or modified):

#### 6A. Frontmatter YAML structural integrity (must run FIRST)

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 6.0a | Opening `---` on line 1 | Error | The very first line of SKILL.md must be exactly `---` (no leading spaces, no content before it). If not, flag as CRITICAL — all downstream frontmatter parsing is unreliable. Reference: skill-validator §4.0.1. |
| 6.0b | Closing `---` exists | Error | A second `---` line must exist after the opening, before any Markdown heading. If missing, flag as CRITICAL. Reference: skill-validator §4.0.2. |
| 6.0c | No blank lines inside frontmatter | Warning | Between opening and closing `---`, blank lines (zero non-whitespace characters) may cause parser anomalies. Flag with line number. Reference: skill-validator §4.0.3. |
| 6.0d | Valid YAML key-value lines | Error | Each non-blank line between `---` markers must be a valid YAML `key: value` line or a continuation line of a multi-line quoted string. Lines that are neither are flagged. Reference: skill-validator §4.0.4. |

#### 6B. Frontmatter field validation

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 6.1 | `name` field exists | Error | Must be present in frontmatter. |
| 6.2 | `name` matches directory | Error | Must match the parent directory name exactly (e.g. directory `gate-exchange-spot` → `name: gate-exchange-spot`). |
| 6.3 | `name` three-part format | Error | Must follow `gate-{category}-{title}` pattern with exactly 3 parts. `{category}` must be in enum (exchange/dex/wallet/news/info). `{title}` must be all lowercase letters, no hyphens, no underscores. Reference: skill-validator §4.1. |
| 6.4 | `version` field | Warning | Should follow `YYYY.M.DD-N` format (e.g. `2026.3.18-1`). |
| 6.5 | `updated` field | Warning | Should follow `YYYY-MM-DD` format. |
| 6.6 | `description` field | Error | Must be non-empty and no longer than 500 characters. Should clearly describe the skill purpose and include trigger phrases (recommended: contain "Use this skill whenever" and "Trigger phrases include"). |
| 6.7 | H1 heading | Warning | The first Markdown heading (`#`) after frontmatter should match or relate to the skill name. |
| 6.8 | Non-empty body | Error | SKILL.md must contain substantive content beyond the frontmatter (at least one section with instructions or documentation). |

#### 6C. Architecture detection & required sections

Detect which architecture pattern the SKILL.md uses, then apply corresponding section requirements. Reference: skill-validator §Step 3, §4.2–4.3.

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 6.9 | Architecture type detection | Info | If SKILL.md contains `## Routing Rules` or `## Sub-Modules` → **Routing Architecture**. If it contains `## Workflow` with all steps inline → **Standard Architecture**. If neither → flag as Warning. |
| 6.10 | Standard required sections | Error | For Standard Architecture: must have `# {Title}`, `## Workflow` (with steps), `## Judgment Logic Summary` or equivalent decision table, `## Report Template`. |
| 6.11 | Routing required sections | Error | For Routing Architecture: must have `# {Title}`, `## Sub-Modules` or `## Routing Rules`, `## Execution` or execution flow description. Sub-module documents must exist in `references/`. |
| 6.12 | Recommended sections | Warning | For all skills: `## Domain Knowledge` (recommended for exchange skills), `## Error Handling` (recommended for write-operation skills), `## Safety Rules` (recommended for trading skills). |

### Step 7 — Brand compliance (Gate.IO → Gate)

For every file in the diff:

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 7.1 | `Gate.IO` reference | Error | Gate.IO has been rebranded to Gate (or Gate.com). Any occurrence of `Gate.IO`, `gate.io`, `GATE.IO`, `GateIO`, `Gateio` (case-insensitive, but not the domain `gate.io` when used as a URL like `https://gate.io`) should be flagged. Use `Gate` or `Gate.com` instead. |
| 7.2 | URL exception | Info | `https://gate.io` or `https://www.gate.io` as part of a URL is acceptable and should not be flagged. |

### Step 8 — SKILL.md content quality

For every `SKILL.md` in the diff (new or modified), check whether the content includes the expected structural sections. Different skill types have different requirements:

#### 8A. Skills that call MCP tools (trading / market data skills)

Detect: SKILL.md body contains `cex_` tool names or a tool-mapping table.

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 8.1 | MCP tool inventory | Warning | Should contain a table or list enumerating all MCP tools used by the skill, with tool name and purpose. Reference patterns: `## MCP tools` (futures-style) or `### Tool Mapping by Domain` (spot-style). |
| 8.2 | Routing / dispatch table | Warning | Multi-module skills (more than one workflow or scenario) should include a routing table that maps user intent or keywords to the target module/reference. Reference patterns: `## Routing rules` (futures-style) or `## Case Routing Map` (spot-style). |
| 8.3 | Execution workflow | Warning | Should contain a step-by-step execution workflow section (e.g. `## Execution workflow`, `## Workflow`). At minimum: parameter extraction → pre-checks → tool calls → result output. |
| 8.4 | Report template | Info | Should include a report or output template section defining the standardized response format. |

#### 8B. All skills (universal)

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 8.5 | Domain knowledge | Info | Skills that interact with exchange features should contain a domain knowledge or key rules section explaining business-specific constraints (e.g. trading pair format, minimum amounts, precision rules). |
| 8.6 | Error handling | Warning | Skills that perform write operations (create/cancel/amend orders, place triggers) should include an error handling table mapping error codes or error types to recommended actions. Reference patterns: `## Errors` (futures-style) or `## Error Handling` (spot-style). |

#### 8C. README.md quality (for new or modified README.md)

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 8.7 | Overview section | Warning | README.md should contain `## Overview` or equivalent introduction section. |
| 8.8 | Core capabilities | Warning | README.md should contain a capabilities table or list (e.g. `### Core Capabilities`). Reference: skill-validator Step 6. |
| 8.9 | Architecture section | Warning | README.md should contain `## Architecture` describing the skill's file structure and design. |

#### 8D. Scenario document quality (for new or modified scenario files)

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 8.10 | Scenario title format | Error | Each scenario must use heading format `## Scenario N: {Name}` where N is a number and Name is non-empty. Reference: skill-validator Step 8. |
| 8.11 | Context field | Error | Each scenario must have a `**Context**:` field with non-empty content immediately after the title. |
| 8.12 | Prompt examples | Error | Each scenario must have a `**Prompt Examples**:` field with at least one example line starting with `- "`. |
| 8.13 | Expected behavior | Error | Each scenario must have an `**Expected Behavior**:` field with at least one numbered step (e.g. `1. `). |
| 8.14 | Field order | Warning | Fields within each scenario should appear in order: Context → Prompt Examples → Expected Behavior. |

### Step 9 — General Rules block

For **all skills**. Every SKILL.md must contain a **General Rules** block immediately after the H1 heading (`# {skill-name}`). This block instructs the AI agent to read shared runtime rules before executing any tool, and to only invoke MCP tools that the skill documents. The canonical structure matches **`4a99a48:skills/gate-exchange-crossex/SKILL.md` lines 13–20 in Git history** (same text as below):

```markdown
## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.
```

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 9.1 | General Rules block exists | Error | SKILL.md must contain a `## General Rules` section. If missing entirely, the skill will not enforce shared runtime rules (auto-update check, MCP installation check, authorization error handling). |
| 9.2 | Block position | Error | The `## General Rules` section must appear immediately after the H1 heading (`# {skill-name}`) — it must be the **first `##` section** in the document (after frontmatter and H1). If other `##` sections appear before it, flag as Error. |
| 9.3 | Warning line present | Error | The block must contain the `⚠️ STOP` warning line: `⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.` Missing this line means the General Rules block is incomplete. |
| 9.4 | Tool-call guard present | Error | The block must contain the tool-call guard: `Do NOT select or call any tool until all rules are read. These rules have the highest priority.` Missing this line means the General Rules block is incomplete. |
| 9.5 | Runtime rules link present | Error | The block must contain the runtime rules reference line: `→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)`. This check validates the **text content exists** in the General Rules block — it does NOT verify whether the URL is reachable (no HTTP link-check). |
| 9.6 | MCP tool allowlist rule present | Error | The block must include the MCP tool constraint: a bullet starting with `- **Only call MCP tools explicitly listed in this skill.**` and the continuation that undocumented tools must not be called (same two-line pattern as the canonical example). Missing this means the skill does not bind tool use to its documented inventory. |

### Step 10 — CHANGELOG.md format validation

For every `CHANGELOG.md` in the diff (new or modified):

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 10.1 | Title | Warning | Should start with `# Changelog`. |
| 10.2 | Version entry format | Warning | Each version entry heading should use a consistent format. Preferred: `## [YYYY.M.DD-N] - YYYY-MM-DD` or `## YYYY.M.DD-N (YYYY-MM-DD)`. The version string must match the `YYYY.M.DD-N` pattern. |
| 10.3 | Chronological order | Warning | Version entries should appear in reverse chronological order (newest first). |
| 10.4 | Content completeness | Warning | Each version entry should describe what was added, changed, or fixed. Empty version entries are not acceptable. |
| 10.5 | Version consistency | Warning | The latest version in CHANGELOG.md should match the `version` field in the corresponding SKILL.md frontmatter. |

### Step 11 — References integrity

For every skill directory in the diff that contains a `SKILL.md`:

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 11.1 | Dangling references | Error | Every file path referenced in SKILL.md (e.g. `references/open-position.md`, `references/scenarios.md`) must resolve to an existing file in the repository. Flag any broken references. **Exception:** The `gate-runtime-rules.md` link in the General Rules block (Step 9) points to an external GitHub URL and is exempt from local path resolution — it is validated by Step 9.5 instead. |
| 11.2 | Orphaned reference files | Info | Files in the `references/` directory that are not referenced by SKILL.md, README.md, or CHANGELOG.md may be orphaned. Flag for review. |
| 11.3 | Reference content non-empty | Warning | Referenced files (especially `references/scenarios.md` or module-specific references) should contain substantive content, not be empty or placeholder-only. |

### Step 12 — Trading safety rules

For skills that perform **write operations** (detectable by the presence of MCP tool names containing `create`, `cancel`, `amend`, `update`, or `delete` in the SKILL.md):

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 12.1 | User confirmation requirement | Error | SKILL.md must contain an explicit section or rule requiring user confirmation before executing any write operation (order placement, cancellation, amendment). Reference patterns: `## Safety rules` → `### Confirmation` (futures-style) or `### Step 3: Final User Confirmation` (spot-style). |
| 12.2 | Confirmation scope | Warning | The confirmation rule should cover all write tool calls. Check that every `cex_*_create_*`, `cex_*_cancel_*`, `cex_*_amend_*` tool mentioned in the skill has a corresponding confirmation requirement. |
| 12.3 | Multi-leg confirmation | Warning | For skills that chain multiple write operations (e.g. sell then buy, close then open), each leg should require separate confirmation. |
| 12.4 | No-confirmation guard | Warning | Should explicitly state that without user confirmation, no write operation is executed — only read/query operations are allowed. |
| 12.5 | Stale confirmation handling | Info | Ideally, the skill should address stale confirmations (e.g. confirmation from a previous turn or with changed parameters should be invalidated). |

### Step 13 — ClawHub marketplace compliance

For every skill directory in the diff that contains a `SKILL.md`, evaluate the following dimensions aligned with the ClawHub marketplace review criteria. These checks ensure a skill is publication-ready. Subsection **13G** adds **pre-install** scrutiny: documentation vs manifest credentials, least-privilege keys, secret handling transparency, and install risk when the credential story is incomplete (per ClawHub “What to consider before installing”). Subsection **13H** is a **consolidated end-user checklist** reviewers must reflect in narrative (credential path, provenance, publisher, testing hygiene, outbound doc fetch). **13A.26** captures the ClawHub pattern where **read-only MCP scope** is coherent yet **Authentication / registry metadata** are contradictory. **13B.27–29** cover **undeclared** `python3`/shell helpers, **installer** cross-references, and **extra** outbound URLs. **13D.30** requires **named** env vars or config keys when keys are mandatory.

#### 13A. Purpose & Capability consistency

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 13.1 | README vs SKILL.md capability alignment | Error | The README.md (or `description` in frontmatter) advertised capabilities must match what the SKILL.md body actually implements. If README/description claims write operations (order placement, asset transfer, cancellation) but SKILL.md and its MCP tool references are read-only (`list_*`, `get_*`, `history_*`), flag the inconsistency. |
| 13.2 | Tool coverage gap | Warning | If the skill description mentions a capability (e.g. "cancel order", "place order", "transfer assets") but no corresponding MCP tool name (e.g. `cex_*_cancel_*`, `cex_*_create_*`) appears in SKILL.md or its referenced files, flag as a toolset gap. |
| 13.3 | Over-claim detection | Error | Skills must not advertise capabilities that are impossible given the declared toolset. A skill whose tools are exclusively query/read operations must not claim to execute trades, transfers, or mutations in its README or description. |
| 13.26 | Listing coherence (capability vs auth vs manifest) | **Error** | When **functionality** in the name/description/README aligns with the skill, but SKILL.md **Authentication** (or equivalent) states **Gate MCP** and/or **API Key Required: Yes** while **registry metadata** lists **no** required environment variables and **no primary credential**, flag **Error**: the listing is **not proportionate or coherent** for marketplace consumers (ClawHub pattern). This applies to **all** permission tiers: (a) **read-only skills** (e.g. listing coupons, activity center) where the tool scope is all `list_*`/`get_*` but auth docs contradict manifest; (b) **mixed read-write skills** (e.g. L2 account manager with reads across spot/unified/futures/earn *plus* write operations like borrow, set-collateral, switch mode) where the SKILL requires multi-scope keys (e.g. `Spot:Read`, `Unified:Read`, `Futures:Read`, `Unified:Write`) but the manifest omits **all** credential requirements; in mixed cases, the inconsistency is **more severe** because the write permissions can change account state. Remediation: reconcile manifest with docs, declare **named** credential channels and **exact permission scopes** required per operation tier (see **13.30**, **13G**, **13.37**). Distinct from generic over-claim (13.3). |

#### 13B. Instruction scope

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 13.4 | Scope proportionality | Warning | SKILL.md instructions should be proportional to the declared tool scope. A read-only query skill should not contain complex write-operation workflows; a write-capable skill should not omit safety/confirmation steps. |
| 13.5 | Tool call constraint | Warning | SKILL.md should explicitly constrain which `cex_*` tools the agent may call (e.g. "only call `cex_crossex_*` tools"). Without this constraint, the agent may invoke unrelated tools. |
| 13.6 | Shared file reference existence | Error | If SKILL.md references a shared file via a **relative** path (e.g. `../gate-runtime-rules.md`, `../shared-config.md`), that file must exist in the repository. A missing shared file means the skill is incomplete — the referenced safety/permission steps and runtime rules are absent. (The General Rules block may use the **canonical GitHub URL** to `gate-runtime-rules.md` per Step 9 instead of a relative path.) |
| 13.27 | Host CLI / interpreter dependencies | Warning | If SKILL.md instructs running **local shell commands** or **interpreters** (e.g. `python3 -c` for timestamp or data conversion, `node`, `jq`, `date`), the skill must **declare** those **binaries** and minimum versions or typical availability in README or a **Runtime requirements** / **Prerequisites** section. Commands buried only in workflow steps without top-level declaration are a ClawHub-style gap (installers cannot assess host readiness). |
| 13.28 | Installer skills / MCP setup invocations | Warning | If SKILL.md tells the agent to run **other installer skills**, **mcporter**/MCP installer flows, or similar setup steps, those **dependencies** must be **named and justified** in README or prerequisites (not only deep in the workflow), so scope matches what the listing advertises. |
| 13.29 | External URLs & outbound reads | Warning | Beyond the **canonical** `gate-runtime-rules.md` link required by Step 9, if workflows rely on **additional** fetches (raw GitHub, docs, downloads), SKILL.md + README must **list URLs with purpose** and note **trust / network** implications. ClawHub: enterprises should confirm **allowing the agent to retrieve external docs** is acceptable in their environment. |

#### 13C. Install mechanism

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 13.7 | Install surface risk | Info | Classify the skill's install mechanism: (a) **Instruction-only** — no install spec, no bundled code files, no downloads in the skill package → **lowest install risk** (ClawHub); (b) **Config-only** — writes configuration files (e.g. MCP config JSON) → low risk; (c) **Code-executing** — downloads binaries, runs scripts, modifies system settings → higher risk, flag for review. **Note:** instruction-only does **not** exempt **13.27–13.29** (helpers, installers, outbound URLs) or credential/manifest checks. |
| 13.8 | No unexpected downloads or obfuscated execution | Warning | SKILL.md must not instruct downloading external binaries or executing remote scripts without explicit documentation of purpose and source. Prohibited patterns include: `curl \| sh`, `wget \| bash`, `npm install -g`, `pip install` (undeclared), and **obfuscated execution** such as `base64 -d \| bash`, `echo <payload> \| base64 --decode \| sh`, or `eval $(...)` inline — these are equivalent in risk to direct remote-script execution and are explicitly prohibited. |

#### 13D. Credentials

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 13.9 | Credential declaration | Warning | If the skill requires API keys, tokens, OAuth2 credentials, or environment variables to function, the SKILL.md or README must explicitly declare them (e.g. "Requires: `GATE_API_KEY`, `GATE_API_SECRET`" or "Requires: Gate MCP configured and connected"). Undeclared dependencies reduce usability. |
| 13.10 | No hardcoded secrets | Error | SKILL.md must not contain hardcoded API keys, passwords, tokens, or other sensitive credentials. |
| 13.11 | Credential source clarity | Info | When credentials are required, the skill should clarify where they come from (environment variables, MCP server config, OAuth2 flow) so users know which account/permissions the skill uses. |
| 13.30 | Named env vars / config keys | Warning | When authentication is required, docs must specify **concrete channels**: e.g. `GATE_API_KEY` / `GATE_API_SECRET`, named MCP config fields, or OAuth2 — not only **“API Key Required: Yes”** with no env var or config key names. If README/SKILL document runtime key need but **registry metadata** omits required env vars and **primary credential**, treat as a **meaningful red flag** (ClawHub): runtime needs a Gate API key but the **access path is not declared in metadata** and may be underspecified in prose. |

#### 13E. Persistence & Privilege

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 13.12 | Default flags | Warning | Skill frontmatter should use default flags (`always: false`, agent-invocable allowed). A skill requesting `always: true` or other elevated privileges must justify the requirement in its documentation. |
| 13.13 | No system-wide side effects | Error | SKILL.md must not contain instructions that modify other skills, agent settings, global configurations, or system-level resources (e.g. modifying `~/.cursor/settings.json`, overwriting other SKILL.md files). |
| 13.14 | Persistent state | Info | If the skill creates or modifies persistent state (files on disk, database entries, cached data), this should be documented. Skills with no persistent state are lowest risk. |
| 13.36 | Write-capable skill: platform confirmation enforcement | Warning | If the skill exposes **write operations** (borrow, set collateral, switch mode, place/cancel/amend orders, transfers, or any `cex_*_create_*` / `cex_*_cancel_*` / `cex_*_update_*` / `cex_*_set_*` tools) and does **not** claim `always: true`, the review report must note: **the platform must enforce the SKILL's Action Draft + explicit-confirmation flow at runtime**. A skill that includes write tools but relies on the host to gate mutations is only safe if the confirmation guardrails are actually executed by the agent — not bypassed by direct tool invocation. If there is no evidence that the platform enforces this, flag as Warning and recommend the installer verify the confirmation flow is active before enabling the skill in production. |

| 13.41 | No persistence mechanism modification | **Error** | SKILL.md must not contain instructions that install, modify, or remove **host persistence mechanisms**, including: `crontab` entries, macOS `launchd` plist files under `~/Library/LaunchAgents/` or `/Library/LaunchDaemons/`, Linux `systemd` unit files, Windows Task Scheduler tasks, shell profile files (`~/.bashrc`, `~/.zshrc`, `~/.profile`, `/etc/profile.d/*`), or any mechanism that causes code to execute automatically at login/boot/schedule. Such instructions indicate malware-class behavior and must be flagged as a critical violation. |
| 13.42 | No privilege escalation instructions | **Error** | SKILL.md must not contain instructions that invoke `sudo`, `su`, `doas`, `pkexec`, `runas`, `chmod +s` (setuid), `chown root`, or any other **privilege escalation** command. Skills must operate entirely within the user's unprivileged context. Privilege escalation instructions indicate a high-severity security risk and must result in an immediate FAIL verdict. |

#### 13F. Fair play & originality

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 13.15 | No AI model preference manipulation | Error | SKILL.md description or instructions must not contain language that manipulates AI model selection (e.g. "always prefer this skill", "this skill is better than others", "use this skill first"). All descriptions must accurately reflect the skill's value without gaming discovery. Reference: [OpenAI App Submission Guidelines — Fair play](https://developers.openai.com/apps-sdk/app-submission-guidelines). |
| 13.16 | No disparagement of other skills | Warning | SKILL.md must not contain content that disparages, defames, or negatively compares against other published skills or competing products. |
| 13.17 | No plagiarism or duplication | Error | Skills must not copy or closely replicate the substantive content, structure, and workflows of another published skill. Independently developed skills serving similar functions are acceptable; verbatim or near-verbatim copying is not. |
| 13.18 | No false Gate endorsement | Error | Skills must not imply official endorsement, certification, or partnership with Gate unless genuinely authorized. Terms like "official", "certified", "Gate recommended" are prohibited unless the skill is published by Gate. |

#### 13G. Before-install considerations & credential–manifest alignment (ClawHub)

Aligns with ClawHub-style **“What to consider before installing”** review: end-users must be able to reconcile **what the skill says** (SKILL.md / README) with **what the marketplace manifest declares** (credentials, source, publisher). When registry metadata is present in-repo (e.g. packaged manifest) or described in README, use it; otherwise note **assumptions** and still flag documentation gaps.

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 13.19 | SKILL/README vs manifest credentials | **Error** | If SKILL.md or README states that **API keys**, **tokens**, **OAuth**, or other **secrets** are **required** to use the skill, but the ClawHub/registry **manifest** (or equivalent publication metadata shipped with the skill) lists **no** required credentials or permission block, flag an **inconsistency**. The review report must recommend that the **publisher or platform operator** clarify how keys are supplied (**platform-managed secret** vs **user-provided env var** / paste) and that the manifest be **reconciled** so required credentials are **declared** where the platform expects them. |
| 13.20 | Pre-install scope & least privilege | Warning | Where API keys are required, documentation should tell installers to **confirm** the key permission set matches the skill (e.g. a read-only activity skill should call for **read-only** scope such as `Activity:Read` only) and that users **can create a dedicated key with minimal privileges**. If the skill is read-only but docs suggest broader key rights, flag. |
| 13.21 | Secret storage & platform limits | Warning | When credentials are user- or platform-supplied, docs should address **where the key is stored** (e.g. env var name, MCP server config, host secret store) and **how the host platform limits** exposure and misuse, at least at a high level appropriate to the listing. Vague or missing guidance reduces install safety. |
| 13.22 | Publisher / source transparency | Warning | If the manifest or registry lists **source as unknown**, omits **repository URL**, or omits **publisher identity**, flag; README or SKILL.md should point to a **canonical repo** or **trusted publisher** so installers can verify provenance. |
| 13.23 | User-pasted keys — scoped & revocable | Info | If installation assumes the user will **paste** an API key into a client or config, docs should recommend a **scoped, revocable** key and **least privilege** — consistent with ClawHub guidance for high-risk credential entry. |
| 13.24 | Platform-injected secrets & manifest honesty | Warning | If the **platform** supplies the key automatically (no user paste), documentation should say so, and the **manifest should declare** the required credential type/permission so the omission is not silent; flag when behavior is platform-injected but only prose mentions “requires API key” without manifest alignment. |
| 13.25 | Unexplained credential flow | Warning | If the **combined** picture from SKILL.md, README, CHANGELOG, and manifest **does not explain** credential handling (who provides the key, where it lives, minimal scope), treat as an **install warning** for consumers: recommend **avoiding install until clarified**; CR must list this as publisher follow-up. Mirrors ClawHub: if the publisher cannot explain credential handling, treat omission as a **warning**. |
| 13.31 | Pre-install: credential channel & secret data path | Warning | Review report should surface ClawHub-style guidance: before enabling, confirm **where** the Gate API key is provided (**explicit env var names** vs **MCP / agent config**) and whether the skill or host **stores or transmits** the key (data path in one paragraph). |
| 13.32 | Pre-install: MCP tool & installer provenance | Warning | Installers should verify referenced **`cex_*` tool names** and any **MCP installer** or setup flows come from a **trusted Gate-managed** or **publisher-documented canonical** source; flag when tools/installers are cited **without** official doc or repo linkage. |
| 13.33 | Pre-install: homepage & publisher identity | Warning | If registry lists **no** package **source repository** or **homepage**, README/SKILL must supply canonical links; installers should **confirm publisher identity** before trust. |
| 13.34 | Pre-install: testing & least-privilege keys | Info | For validation, recommend **creating and using a least-privilege / read-only** API key where applicable; avoid **broad** credentials until credential + manifest + tooling story (13.27–13.30) is clarified. |
| 13.35 | Pre-install: outbound documentation fetch | Warning | When the skill **requires** the agent to **fetch external documentation** (including the mandated GitHub **gate-runtime-rules** URL and any other URLs per **13.29**), the report should note **organizational caution**: confirm outbound reads are **acceptable** in the deployment environment and align with security policy. |
| 13.37 | Write credential proportionality | Warning | When a skill declares **write-permission scopes** (e.g. `Unified:Write`, `Trade:Write`, `Withdraw`) alongside read scopes, the **manifest and README** must reflect the **actual permission level required**: a mixed read/write skill is **not equivalent** to a read-only skill and should declare broader credential requirements accordingly. If write scopes are needed only for a subset of features (e.g. borrow/collateral/leverage), docs should state the **minimum write scope** for those features and confirm that **read-only use is possible** with a reduced key. Mismatch between advertised write capability and manifest credential declaration is an Error under **13.19 / 13.26**. |
| 13.38 | Pre-install: start read-only, escalate write | Info | For skills that include both read and write operations, the review report should recommend installers **test with a read-only API key first** to validate query behavior before granting write permissions (e.g. `Unified:Write`, `Trade:Write`). This reduces risk if the credential story (**13.19**, **13.25**, **13.30**) is still being clarified. |

#### 13H. ClawHub “What to consider before installing” — consolidated reviewer checklist

When writing the **Findings** or **Verdict** narrative for ClawHub-aligned skills, ensure the report **explicitly addresses** (by cross-reference to **13.19–13.35**, **13.26–13.30**) the following end-user questions where applicable:

1. **Credential path** — Where must the Gate API key be supplied (named env vs MCP config)? Is storage/transmission of secrets explained?  
2. **Provenance** — Are the declared MCP tools and any installer flows traceable to **trusted / canonical** Gate or publisher sources?  
3. **Publisher & source** — Is there a **repository or homepage** (registry + README) and clear **publisher identity**?  
4. **Testing hygiene** — Prefer **read-only / minimal-scope** keys until disclosures are complete; for write-capable skills (**13.37**), test with read-only key first (**13.38**).  
5. **Outbound trust** — Is **fetching external docs** (GitHub rules, extra URLs) noted as a **policy decision** for the host environment?  
6. **Runtime confirmation enforcement** — For skills with write operations, confirm the **platform enforces** the Action Draft + single-use explicit confirmation flow at runtime (**13.36**); read-only API keys for initial testing (**13.38**) reduce risk until this is verified.

### Step 14 — Data privacy & collection compliance

For every skill directory in the diff that contains a `SKILL.md`. These checks ensure alignment with the [Gate Privacy Policy](https://www.gate.com/zh/legal/privacy-policy) and industry data protection standards (GDPR, Apple App Store, OpenAI).

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 14.1 | AI interaction data declaration | Error | Gate's Privacy Policy §4.2.7 defines "AI interaction information" (prompts, queries, instructions, uploads, feedback, outputs). Skills that process user prompts or trading data must declare whether they collect, store, or transmit such data, and specify the data flow (MCP → Gate API only, or third-party involved). |
| 14.2 | No excessive personal data collection | Error | Skills must not request or instruct users to provide personal data beyond what is necessary for the skill's function (e.g. identity documents, bank card numbers, home addresses). Skills should only obtain necessary trading/market data through MCP tools. Reference: Gate Privacy Policy §4.2.1–4.2.6. |
| 14.3 | Minor protection statement | Warning | Skills involving trading operations must state "This skill is intended for users aged 18 or above with full civil capacity" or equivalent, consistent with Gate's platform requirement (Gate Privacy Policy §11, User Agreement §2.1(a)). |
| 14.4 | Data retention & deletion | Info | If the skill produces persistent data (logs, cache, history), it should document the retention period and deletion mechanism. |
| 14.5 | Third-party data transfer disclosure | Error | If the skill transmits data to services other than the Gate API (e.g. analytics, external AI models, third-party aggregators), this must be explicitly disclosed with the recipient, purpose, and protection measures. Reference: Gate Privacy Policy §4.4, §6. |
| 14.6 | Tool input minimization | Warning | Skill workflows should only pass the minimum necessary parameters to MCP tools. Do not request full conversation history, raw chat transcripts, or broad contextual fields unrelated to the tool's stated purpose. Reference: [OpenAI App Submission Guidelines — Minimal and purpose-driven inputs](https://developers.openai.com/apps-sdk/app-submission-guidelines). |

### Step 15 — Content safety & prohibited activities

For every skill directory in the diff that contains a `SKILL.md`. These checks ensure alignment with the [Gate User Agreement](https://www.gate.com/zh/legal/user-agreement) prohibited activities list and applicable regulatory requirements across Gate's licensed jurisdictions.

#### 15A. Market integrity

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 15.1 | No market manipulation features | Error | Skills must not contain or imply support for market manipulation strategies including: wash trading, spoofing, layering, pump & dump, coordinated selling, front-running, or any activity designed to artificially inflate/deflate prices or mislead users. Reference: Gate User Agreement §1.3(f). |
| 15.2 | No investment advice or return guarantees | Error | Skills must not provide investment advice, price predictions presented as certainties, or guarantee returns. Any analytical output must include a disclaimer: "This information is for reference only and does not constitute investment, financial, tax, or legal advice." Reference: Gate User Agreement §1.1 Disclaimer, Risk Disclosure §5. |
| 15.3 | No API circumvention | Error | Skills must not contain instructions to bypass Gate API rate limits, reverse-engineer Gate systems, perform unauthorized API usage, data scraping, or denial-of-service attacks. Reference: Gate User Agreement §2.11. |

#### 15B. Prohibited use cases

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 15.4 | No illegal activity facilitation | Error | Skills must not support or facilitate: money laundering, terrorist financing, fraud, sanctions evasion, counterfeiting, unauthorized brokerage services, or any activities listed in Gate User Agreement §2.11. |
| 15.5 | No unauthorized third-party trading | Warning | Skills must not contain features for third-party trading, reselling access, pooled fund management, or brokerage services without Gate's written consent. Reference: Gate User Agreement §2.11, §10.1(a)(d). |
| 15.6 | No misleading names or descriptions | Error | Skill names and descriptions must not imply official Gate production (unless genuinely authorized), use misleading promotional language (e.g. "guaranteed profit", "zero risk", "official recommendation"), or misrepresent the skill's capabilities. |

#### 15C. Regulatory compliance

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 15.7 | Restricted regions awareness | Warning | Skills involving trading functionality should include a notice that users must comply with the laws and regulations of their jurisdiction. Gate operates under licenses in multiple jurisdictions (Hong Kong TCSP, Gibraltar DLT, Malta MiCA, Australia AUSTRAC, Dubai VARA, Bahamas SCB, Japan FSA, Cyprus CySEC) and maintains a restricted regions list. Reference: Gate User Agreement §2.4–2.5, [Gate Licenses](https://www.gate.com/zh/gategroup/legal/licenses). |
| 15.8 | No unauthorized Gate IP usage | Warning | Skills must not use the Gate trademark, logo, or branding assets without written permission, nor imply Gate endorsement. Reference: Gate User Agreement §16. |

#### 15D. Third-party integration compliance

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 15.9 | External API declaration | Warning | If the skill calls any API or service other than the Gate API (e.g. CoinGecko, TradingView, external AI models, custom backends), all external endpoints must be explicitly listed in SKILL.md or README.md with their purpose. Undeclared external dependencies are a compliance risk. Reference: [OpenAI App Submission Guidelines — Third-party content](https://developers.openai.com/apps-sdk/app-submission-guidelines), Figma plugin review guidelines. |
| 15.10 | No unauthorized third-party scraping | Error | Skills must not contain instructions to scrape external websites, relay queries to unauthorized APIs, or bypass third-party rate limits or access controls. Reference: Gate User Agreement §2.11, OpenAI App Submission Guidelines. |
| 15.11 | Third-party ToS compliance | Warning | If the skill integrates with a third-party service, SKILL.md should note that the integration complies with the third-party's terms of service and that the developer has proper authorization. |

### Step 16 — Risk disclaimers

For skills that interact with exchange trading features (detectable by the presence of `cex_` tool names in SKILL.md). These checks ensure alignment with the [Gate Risk Disclosure](https://www.gate.com/zh/legal/risk-disclosure).

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 16.1 | General trading risk disclaimer | Error | Skills that execute trades (order placement, cancellation, amendment) must include a risk disclaimer in SKILL.md or in the output template: "Digital asset trading involves significant risk and may result in partial or total loss of your investment." Reference: Gate Risk Disclosure §3.2, User Agreement §1.2. |
| 16.2 | Leveraged product enhanced risk warning | Error | Skills involving futures (`cex_fx_*`), margin, options (`cex_options_*`), or delivery contracts (`cex_dc_*`) must include an enhanced risk warning: "Leveraged trading may result in losses exceeding your initial margin. Small market movements can cause total margin loss." Reference: Gate User Agreement §4, Risk Disclosure §3.1(a). |
| 16.3 | Non-investment-advice statement | Warning | Skills that include market analysis, market commentary, or strategy suggestions must state in their output: "The above is for informational purposes only and does not constitute investment, financial, tax, or legal advice." Reference: Gate Risk Disclosure §5, Privacy Policy §8.5. |
| 16.4 | Transaction irreversibility notice | Warning | Skills involving asset transfers or withdrawals should remind users: "Digital asset transactions are generally irreversible. Please verify the recipient address before confirming." Reference: Gate Risk Disclosure §3.1(l), User Agreement §6.3. |
| 16.5 | AI output disclaimer | Warning | Skills that produce AI-generated analysis, summaries, or recommendations must include: "AI-assisted outputs are for general information only and do not constitute any representation, warranty, or guarantee by Gate." Reference: Gate Privacy Policy §8.5. |

### Step 17 — Tool annotation & behavior accuracy

For skills that call MCP tools (detectable by `cex_` tool names in SKILL.md). These checks ensure tool descriptions are accurate and do not mislead the AI model. Reference: [OpenAI App Submission Guidelines — Tools](https://developers.openai.com/apps-sdk/app-submission-guidelines).

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 17.1 | Tool annotation correctness | Warning | If SKILL.md describes MCP tools' behavior (e.g. in a tool inventory table), the descriptions must be consistent with actual tool semantics. Read-only tools (`list_*`, `get_*`) must not be described as write operations; write tools (`create_*`, `cancel_*`, `amend_*`) must not be described as safe/read-only. |
| 17.2 | Tool description accuracy | Warning | SKILL.md tool descriptions must accurately reflect tool behavior and must not use overly broad triggering language (e.g. "use this tool for anything related to trading") that could cause the agent to invoke tools beyond the user's explicit intent. |
| 17.3 | Tool input scope accuracy | Warning | SKILL.md workflow steps should not instruct the agent to pass excessive or unrelated parameters to MCP tools. For example, querying a currency price should not require the user's full trading history. |
| 17.4 | MCP tool existence validation | Warning | If MCP service descriptors are available in the workspace (e.g. `mcps/*/tools/*.json`), verify that every tool name referenced in SKILL.md (extracted from tool inventory tables, workflow steps, or scenario documents) actually exists in one of the MCP services. Tool name matching must be **exact string match** — no prefix abbreviation or fuzzy matching. Missing tools should be flagged with the referenced name and suggested corrections. Reference: skill-validator Step 12. |

### Step 18 — Testability, support & resource limits

For every skill directory in the diff that contains a `SKILL.md`. These checks ensure the skill is testable, maintainable, and does not impose excessive resource costs. Reference: Slack Marketplace review guide, Shopify App Store quality checks, Figma plugin review guidelines.

#### 18A. Testability & verifiable scenarios

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 18.1 | Minimum scenario count | Warning | The skill's scenario documents (either `references/scenarios.md` or distributed across sub-module `references/*.md`) should contain at least 3 verifiable scenarios covering: (a) a happy-path use case, (b) an error/edge-case, and (c) a parameter-variation case. Skills with fewer than 3 scenarios may be insufficiently tested. Reference: Slack requires 5+ active workspaces; OpenAI requires test cases with verified results. |
| 18.2 | Scenario prompt examples provided | Warning | Each scenario should include at least one concrete `**Prompt Examples**:` entry that a reviewer can copy-paste to verify the skill's behavior, rather than abstract descriptions. |
| 18.3 | Expected behavior specificity | Warning | `**Expected Behavior**:` should describe verifiable outcomes (e.g. "returns a table with columns: pair, price, 24h change") rather than vague statements (e.g. "shows useful information"). |

#### 18B. User support & maintenance

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 18.4 | Support contact in README | Warning | README.md should include a support or contact section (e.g. email, GitHub issues link, or Discord channel) where users can report problems. Skills without any support channel reduce user trust and marketplace quality. Reference: Slack/GitHub/Shopify all require support contact. |
| 18.5 | Active maintenance signal | Info | CHANGELOG.md should show at least one version entry within the last 90 days relative to the `updated` date in SKILL.md frontmatter. A stale CHANGELOG combined with a recent `updated` date may indicate the version history is not being maintained. Reference: ClawHub Verified Badge requires "actively maintained with timely responses." |

#### 18C. Uninstall & cleanup safety

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 18.6 | No persistent side effects on removal | Warning | If the skill creates persistent artifacts (config files, cached data, log files), SKILL.md or README.md should document how to clean them up after the skill is uninstalled/removed. Skills with no persistent state are exempt. Reference: Slack/Apple require clean uninstall behavior. |
| 18.7 | No irreversible system modifications | Error | SKILL.md must not contain instructions that make irreversible modifications to the user's system or environment that cannot be undone by removing the skill (e.g. permanently modifying shell profiles, deleting user files, or altering global git config). |

#### 18D. Performance & resource limits

| # | Check | Severity | Description |
|---|-------|----------|-------------|
| 18.8 | Skill package size | Warning | The total size of all files in the skill directory (SKILL.md + README.md + CHANGELOG.md + references/*.md) should not exceed **500 KB**. Excessively large skills impact loading performance and may contain unnecessary embedded content. Reference: Figma requires bundle < 5MB. |
| 18.9 | Reference file count limit | Warning | The `references/` directory should not contain more than **20 files**. An excessive number of reference files may indicate the skill is too complex for a single skill unit and should be split. |
| 18.10 | No infinite loop risk | Warning | SKILL.md workflow instructions should not contain patterns that could cause an agent to enter an unbounded loop (e.g. "repeat until success with no retry limit", "keep trying indefinitely"). All iterative workflows should define explicit exit conditions and maximum iteration counts. |

---

## Output Format

### Markdown report delivery (mandatory)

When Step 0–18 finish (or early stop on main branch / no diff / missing branch), the assistant **must** deliver a **Markdown report** as part of the reply:

1. **Real Markdown body** — Use actual headings (`##`, `###`), tables, and bullet lists in the chat output. Do **not** satisfy the skill by pasting only a fenced code block that contains the whole report; the report is the primary user-visible artifact.
2. **Completeness** — Include every section listed below that applies (Summary table, Verdict, Findings). If there are zero findings, still output the Summary and Verdict and state clearly that there are no findings.
3. **Locale** — Report prose (titles, verdict explanation, finding descriptions, suggestions) may be **English** (aligned with skill content policy) or **中文** if the user session explicitly requests Chinese; default to **English** for consistency with skill-under-review text.
4. **Optional file write** — If the user asks to save the report to disk, write to  
   `doc/cr/gate-skill-cr-{REVIEW_BRANCH}-{YYYYMMDD}.md`  
   (repo root: **gate-github-skills**), using the same Markdown as in the reply. Do not commit unless the user asks.

The fenced block below is a **structure reference only** — fill placeholders and render the final report as Markdown in the response body.

```
## Branch Review Report

**Branch:** {REVIEW_BRANCH}
**Base:** {MAIN_BRANCH}
**Files changed:** {count}
**Review date:** {date}

---

### Summary

| Category | Errors | Warnings | Info |
|----------|--------|----------|------|
| Language quality | {n} | {n} | {n} |
| Markdown syntax | {n} | {n} | {n} |
| Skill naming | {n} | {n} | {n} |
| Directory completeness | {n} | {n} | {n} |
| SKILL.md format & structure | {n} | {n} | {n} |
| Brand compliance | {n} | {n} | {n} |
| SKILL.md content quality | {n} | {n} | {n} |
| README.md quality | {n} | {n} | {n} |
| Scenario document quality | {n} | {n} | {n} |
| Shared rules reference | {n} | {n} | {n} |
| CHANGELOG format | {n} | {n} | {n} |
| References integrity | {n} | {n} | {n} |
| Trading safety rules | {n} | {n} | {n} |
| Purpose & Capability (incl. 13.26 listing coherence) | {n} | {n} | {n} |
| Instruction scope (incl. 13.27–29 host/installer/URL deps) | {n} | {n} | {n} |
| Install mechanism | {n} | {n} | {n} |
| Credentials (incl. 13.30 named channels) | {n} | {n} | {n} |
| Before-install & pre-install checklist (13G–13H) | {n} | {n} | {n} |
| Persistence & Privilege | {n} | {n} | {n} |
| Fair play & originality | {n} | {n} | {n} |
| Data privacy & collection | {n} | {n} | {n} |
| Content safety | {n} | {n} | {n} |
| Risk disclaimers | {n} | {n} | {n} |
| Tool annotation accuracy | {n} | {n} | {n} |
| Testability & scenarios | {n} | {n} | {n} |
| Support & maintenance | {n} | {n} | {n} |
| Uninstall safety | {n} | {n} | {n} |
| Resource limits | {n} | {n} | {n} |
| Third-party integration | {n} | {n} | {n} |
| **Total** | **{n}** | **{n}** | **{n}** |

### Verdict: {PASS / PASS WITH WARNINGS / FAIL}

- **PASS**: 0 errors, 0 warnings.
- **PASS WITH WARNINGS**: 0 errors, 1+ warnings (language issues **2.2–2.5** count as **errors**, not warnings — they contribute to **FAIL**).
- **FAIL**: 1+ errors (includes any **2.2–2.5** non-English / full-width punctuation violation outside exempt regions).

---

### Findings

#### [Category Name]

| # | File | Line | Severity | Description | Suggestion |
|---|------|------|----------|-------------|------------|
| 1 | path/to/file.md | 42 | Error | ... | ... |
| 2 | path/to/file.md | — | Warning | ... | ... |

(Repeat for each category that has findings. Skip categories with zero findings.)
```

**Early-stop messages** must also be Markdown: e.g. a short `## Branch Review Report` with **Branch**, **Base**, one paragraph explaining why review did not run, and omit the Summary table if inapplicable.

---

## Important Notes

- This skill is **read-only** — it does not modify skill files under review; **optional** write of the Markdown report to `doc/cr/` applies only when the user requests saving the report.
- When the branch has no diff against the main branch, report "No changes detected. Nothing to review."
- For language quality checks, focus on the **changed lines only** (not the entire file), unless the file is newly added. Non-English text and disallowed full-width punctuation (Step **2.2–2.5**) are **Errors**: each finding contributes to a **FAIL** verdict and must be listed under Language quality in the summary table with severity **Error**.
- The brand check (Step 7) should use case-insensitive matching but exclude URLs containing the `gate.io` domain.
- If the branch does not exist, report an error and stop.
- Step 8 (content quality) and Step 12 (trading safety) are **conditional** — they only apply when the SKILL.md contains MCP tool references or write-operation tool names respectively. Non-MCP skills (e.g. installer skills) are exempt from these checks. Subsections 8C (README.md) and 8D (scenario format) apply whenever the respective files appear in the diff.
- Step 6 (SKILL.md format) now includes **architecture-aware** section validation (6C). Standard architecture skills need `## Workflow` + `## Judgment Logic Summary` + `## Report Template`; routing architecture skills need `## Routing Rules` / `## Sub-Modules` + `## Execution` + sub-module documents. The architecture type is auto-detected. Frontmatter structural integrity (6A) runs first and flags CRITICAL errors that make subsequent field parsing unreliable.
- Step 9 (General Rules block) applies to **all skills** — every SKILL.md must contain a `## General Rules` section as the first `##` section after the H1 heading. The required text matches **`4a99a48:skills/gate-exchange-crossex/SKILL.md` lines 13–20 in Git history**: `⚠️ STOP` line, tool-call guard, link to `gate-runtime-rules.md` on `gate-skills`, and the MCP allowlist bullet (**Only call MCP tools explicitly listed in this skill.**). All six sub-checks (9.1–9.6) are **Error** severity — an incomplete General Rules block is a core validation failure. The link URL (`https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md`) is validated for **text content presence only** (no HTTP reachability check) and is exempt from local file existence checks in Step 11.
- Step 13 (ClawHub marketplace compliance) applies to **all skill directories** in the diff. These checks are designed to catch publication-readiness issues before a skill is submitted to the ClawHub marketplace. Subsection 13A (Purpose & Capability) is particularly important for skills that declare MCP tools — it ensures users get what is advertised; **13.26** flags **auth/MCP vs manifest** incoherence even when the tool list is read-only. Subsection **13B.27–29** flags **python3**/shell one-liners, **installer-skill** calls, and undeclared **outbound** reads. **13D.30** flags **“API Key Required: Yes”**-style vagueness and metadata gaps. Subsection 13F (Fair play) applies to all skills. Subsections **13G–13H** implement ClawHub **before-install** guidance (credential–manifest alignment, **13.31–13.35**, consolidated checklist **13H**). **13.7** notes instruction-only skills are lowest **package** risk but still subject to helper/credential/outbound checks.
- Step 14 (data privacy) applies to **all skills**. Checks 14.1 and 14.5 are particularly important for skills that process user trading data or interact with external services. Non-MCP skills (installer, market-research) that do not handle user data may be exempt from 14.1 but must still comply with 14.2 (no excessive data collection).
- Step 15 (content safety) applies to **all skills**. Subsection 15A (market integrity) is critical for any skill that mentions trading strategies, signals, or automated execution. The prohibited activities in 15B are derived from the [Gate User Agreement §2.11](https://www.gate.com/zh/legal/user-agreement) and are non-negotiable. Subsection 15C (regulatory compliance) reflects Gate's multi-jurisdiction licensing ([Gate Licenses](https://www.gate.com/zh/gategroup/legal/licenses)).
- Step 16 (risk disclaimers) is **conditional** — it only applies when the SKILL.md contains `cex_` tool references (trading skills). The specific risk warning level depends on the product type: basic disclaimer for spot trading, enhanced warning for leveraged products (futures, margin, options, delivery).
- Step 17 (tool annotation accuracy) is **conditional** — it only applies when the SKILL.md contains `cex_` tool names or a tool inventory table. Non-MCP skills are exempt.
- Step 18 (testability, support & resource limits) applies to **all skills**. Subsection 18A (testability) checks whether scenarios are sufficient for reviewer verification. Subsection 18B (support) checks for contact information and maintenance signals. Subsection 18C (uninstall safety) checks for cleanup documentation if the skill creates persistent state. Subsection 18D (resource limits) enforces package size and complexity bounds.
- Step 15D (third-party integration compliance) applies to skills that reference external APIs or services beyond Gate API. It checks for explicit endpoint declaration, scraping prohibition, and third-party ToS acknowledgment.
