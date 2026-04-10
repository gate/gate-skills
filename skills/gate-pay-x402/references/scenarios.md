# Scenarios

Behavior-oriented templates for **gate-pay-x402**. Each block uses **Context** → **Prompt Examples** → **Expected Behavior**.

Optional **Unexpected Behavior** subsections are for reviewers only (not required by the strict scenario field order).

## Scenario 1: MCP server detection before first pay

**Context**: The user wants to complete an x402 payment. The agent has not yet verified that a Gate Pay MCP server is connected this session.

**Prompt Examples**:
- "I need to pay this 402 challenge with Gate Pay."
- "Help me finish the payment for this merchant link."

**Expected Behavior**:
1. Run **MCP Server Connection Detection** from **SKILL.md** before invoking Gate Pay write tools: locate a server exposing **`x402_*`** tools (e.g. `x402_place_order` or, if listed, `x402_request`).
2. If detection fails, show the setup guide once (stdio command, where to register MCP, optional env keys) in the user’s language.
3. If detection succeeds, record the server identifier and continue with **Workflow** (intent, rail choice, schema-first arguments).

**Unexpected Behavior**:
1. Calls `x402_sign_payment` or other pay tools without confirming the Gate Pay MCP server is available.

## Scenario 2: Vague wallet setup — first reply plain language only

**Context**: The user asks to configure or add a wallet without naming MCP Wallet, plugin wallet, or private-key rail.

**Prompt Examples**:
- "Help me set up my wallet for Gate Pay."
- "Configure my payment wallet."

**Expected Behavior**:
1. Reply in the **user’s language** with **Section 0.A** rules: three short options (MCP Wallet / plugin / private key), no env key names, no MCP tool names, no `mcp.json` paths in the **first** message.
2. Ask the user to pick one option and wait.
3. After choice (**Section 0.B**), proceed with **Wallet configuration procedure** and allowed technical detail.

**Unexpected Behavior**:
1. Dumps `PAYMENT_METHOD_PRIORITY`, `EVM_PRIVATE_KEY`, or tool names in the first vague-intent reply.

## Scenario 3: Pay consent after visible price

**Context**: The user has already received a clear price or 402 summary from the merchant or MCP. They have not yet explicitly confirmed payment.

**Prompt Examples**:
- "What happens next for this payment?" [after amount and asset were shown]
- "Go ahead" [ambiguous — not explicit pay confirmation]

**Expected Behavior**:
1. If the user’s message is **not** explicit pay confirmation, summarize **how much**, **asset/chain** (if known), and **payment method** (if known) and ask for clear consent (e.g. confirm pay) before any signing or submit tools.
2. Do **not** call `x402_sign_payment`, `x402_create_signature`, `x402_submit_payment`, `x402_centralized_payment`, or pay steps inside `x402_request` (if listed) until explicit consent after the clear price.
3. If the user explicitly confirms, proceed per **Workflow** Step 5–6 with arguments from each tool’s **`inputSchema`**.

**Unexpected Behavior**:
1. Invokes sign or pay tools on ambiguous “go ahead” without confirming payment intent.

## Scenario 4: User supplies merchant URL for place order

**Context**: Gate Pay MCP lists `x402_place_order`. The user provides an HTTPS URL (and optionally method/body) for a paid resource.

**Prompt Examples**:
- "Call the merchant at https://api.example.com/paid/resource with POST and this JSON body …"
- "Pay for this API: https://merchant.test/billable-endpoint"

**Expected Behavior**:
1. Read **`inputSchema`** for `x402_place_order` and list required fields; fill from the user message and context only — no empty or guessed probe calls.
2. Run **MCP Server Connection Detection** if not done; use the recorded Gate Pay server for all related **`x402_*`** calls (**same-server rule**).
3. After **402** or price is visible, obtain **explicit pay consent** before sign/submit tools; then call the appropriate tools per schema.
4. Summarize outcome per **Report Template** in the user’s language.

**Unexpected Behavior**:
1. Uses a different MCP server or third-party x402 tool for the same order as Gate Pay `x402_place_order` (violates same-server rule).
