# Gate Pay x402 Skill

## Overview

An AI agent skill for **Gate Pay x402** flows through **`gatepay-local-mcp`**: MCP server discovery, wallet rail configuration (MCP Wallet, plugin wallet, local private key), merchant HTTP and **402 Payment Required** handling, explicit pay consent before signing, and optional routing to **Gate Exchange** MCP when the user selects the **`gate_exchange` rail**. All tool arguments must follow each tool’s live **`inputSchema`**.

### Core Capabilities

| Capability | Description | User examples |
|------------|-------------|----------------|
| MCP connectivity | Detect Gate Pay MCP, surface setup guidance when missing | "Gate Pay MCP not working", "tools not found" |
| Wallet setup | Plain-language rail choice, then env and tool-driven auth | "Configure wallet", "add Quick Wallet", "PAYMENT_METHOD_PRIORITY" |
| x402 payment | Place order / handle 402, confirm price, then sign or submit per server tools | "Pay this 402", "x402", "sign payment" |
| Schema-first orchestration | Build `arguments` only from `inputSchema` | (implicit in all flows) |
| Safety | No private keys in chat; consent before write tools | (guardrails across flows) |

## Architecture

```
gate-pay-x402/
├── SKILL.md                 # Agent runtime: routing, workflow, tools, safety
├── README.md                # Human-readable overview (this file)
├── CHANGELOG.md             # Version history
└── references/
    └── scenarios.md         # QA scenarios (Context → Prompt Examples → Expected Behavior)
```

**Design pattern:** Single-file **routing** architecture — procedural logic and **Routing Rules** live in **`SKILL.md`**. **`references/scenarios.md`** is for testing and review, not a runtime submodule.

## Usage

1. Register **`gatepay-local-mcp`** (or your vendor package) in the host’s MCP settings.
2. Load this skill so the agent follows **SKILL.md** (including shared **gate-runtime-rules**).
3. User requests wallet setup or x402 pay; the agent reads the **live** tool list and **`inputSchema`** for each call.

For detailed workflows, tool allowlisting, and error handling, see **SKILL.md**.

## Trigger phrases

See **SKILL.md** frontmatter `description` and **Trigger Scenarios** — e.g. x402, 402 payment, wallet configuration, merchant discovery, `PAYMENT_METHOD_PRIORITY`, Gate Exchange pay.

## Auto-update

**SKILL.md** may self-check against the registry URL in **Auto-Update (Session Start Only)** inside **SKILL.md**; mirror URL changes here when publishing from a different org/branch.
