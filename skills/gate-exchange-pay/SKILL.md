---
name: gate-exchange-pay
version: "2026.3.27-2"
updated: "2026-03-27"
description: "Gate Pay payment execution skill. Use when the user asks to pay with Gate Pay, complete a merchant charge, or satisfy pay-first flows (e.g. HTTP 402). Triggers on 'Gate Pay', 'complete payment', 'pay for order'. Requires prior Gate payment authorization."
---

# gate-exchange-pay — Gate Pay payment

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

## Scope and audience

This document is for end users and agents: in scenarios where payment is required first and the user has already chosen a payment method and selected Gate Pay, use this capability to complete the charge and output a receipt by calling Exchange MCP tool `cex_pay_create_ai_order_pay`.

Before invoking this Skill, the user must have completed Gate account payment-related authorization. If not, guide them through Gate account authorization before charging.

## Language

Use the user's language for receipts, pre-charge summaries, failures, and short confirmations. If the conversation mixes languages, follow the language of their payment or receipt request; keep one receipt in one language unless they switch.

## When this applies

- The user has clearly expressed intent to pay (e.g. pay, confirm payment, checkout, pay for me).
- Payment is required first (e.g. after HTTP 402 or an equivalent pay-first step when applicable), the user has selected Gate Pay as the payment method, and you are not substituting another channel.
- All information required for the payment call is present and all required arguments for `cex_pay_create_ai_order_pay` are satisfied (per MCP `inputSchema`); if anything is missing, complete it before paying.
- This capability does not cover the first visit to a protected URL solely to obtain a 402; other parts of the conversation may handle that. Once the user has chosen Gate Pay and payment inputs are ready, use this capability to charge.

## When this does not apply

- The user only pastes large raw API text and payment inputs still cannot be determined reliably → do not charge; ask the user to complete details from the order or checkout page.
- Finding merchants, comparing prices, or shopping guidance → out of scope.
- Spot, contract, deposit, or on-chain transfers unrelated to charging a specific merchant order with Gate Pay → do not handle under this capability.

## Domain Knowledge

### Gate Pay Overview

Gate Pay is Gate's digital asset payment solution that enables users to pay for merchant orders using their Gate account balance. It supports pay-first flows (HTTP 402 protocol) where payment is required before accessing resources.

### Authorization Requirements

- Users must complete Gate account payment authorization before any charge can be initiated
- Authorization includes authentication and permission grants for payment-account debiting
- If authorization is missing, expired, or invalid, guide users to complete Gate account authorization first

### Payment Flow Constraints

- Payment is irreversible once successfully executed
- Order information (order_id, amount, currency) must be complete before initiating payment
- The skill only handles the charge step; resource fetching from merchants is out of scope
- Payment voucher fields (if returned) may be used by downstream steps but should not be fabricated

### Gate Pay vs Other Payment Methods

- This skill only handles Gate Pay payments; other payment methods (bank cards, other crypto wallets) are not in scope
- Users must explicitly select Gate Pay as their payment method before this skill activates

## MCP Tools

| Tool name | Purpose | Type |
|-----------|---------|------|
| `cex_pay_create_ai_order_pay` | Debit the user's Gate Pay payment account for a merchant order | Write |

### Authentication
- API Key Required: Yes
- Additional Authorization Required: Yes, Gate Pay payment authorization must already be completed
- Note: This skill executes a private payment action through authenticated Exchange MCP tooling. Payment authorization is required in addition to the runtime's API-key-backed execution capability.

**Note**: If there is no order-status query tool available and the user only asks whether they paid, explain the limitation; do not charge again as a substitute for querying.

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this skill's Gate Pay charge workflow.

- `SKILL.md` keeps payment intent routing, product boundaries, and user-facing policy.
- `references/mcp.md` is the authoritative MCP execution layer for charge inputs, confirmation gates, and failure fallback.

## Workflow

### Step 0: Verify Payment Readiness

**Action**: Validate that all preconditions are met before proceeding.

**Key data to extract**:
- User has selected Gate Pay as payment method
- All required payment parameters are present: `order_id`, `amount`, `currency`
- User has completed Gate payment authorization (if not, halt and guide authorization)

**Decision**: If any required input is missing → ask user to provide complete details. If authorization is incomplete → guide authorization flow. Otherwise proceed to Step 1.

### Step 1: Confirm User Payment Intent

**Action**: Ensure user clearly intends to execute payment.

**Key data to extract**:
- User expresses payment intent (e.g., "pay", "confirm payment", "checkout", "pay for me")
- User has not declined or cancelled the payment

**Decision**: If user intent is unclear or negative → do not proceed with payment. If intent is clear → proceed to Step 2.

### Step 2: Present Payment Details (Optional)

**Action**: Display key charge details for user verification. This is informational and does not require an explicit forced confirmation step. It does **not** replace Step 1: calling the payment tool still requires the clear payment intent established there (see **Safety Rules**).

**Key data to extract**:
- Merchant order ID
- Amount and currency
- Payment method (Gate Pay)

**Output format**:
```
Planned charge
Merchant order ID: {order_id}
Amount due: {amount} {currency}
Payment method: Gate Pay
```

**Decision**: Proceed to Step 3 after displaying details when Step 1's payment-intent gate is satisfied; the optional display is for transparency only.

### Step 3: Execute Payment

**Action**: Call Exchange MCP tool `cex_pay_create_ai_order_pay` with validated parameters.

**Call `cex_pay_create_ai_order_pay` with**:
- `order_id`: Merchant order identifier
- `amount`: Payment amount
- `currency`: Payment currency
- Other required fields per MCP `inputSchema`

**Key data to extract**:
- Payment status (success/failure)
- Transaction timestamp
- Payment confirmation details (order_id, amount, status)
- Voucher fields (if applicable, e.g., prepayId) for downstream use

**Decision**: If payment succeeds → proceed to Step 4 with success receipt. If payment fails → proceed to Step 4 with failure handling.

### Step 4: Output Result

**Action**: Report payment result to user in their language (per Language section).

**Success path**: Output receipt using Report Template format (see Report Template section).

**Failure path**: Provide user-friendly error explanation without exposing internal error codes or stack traces (see Error Handling section).

## Judgment Logic Summary

| Condition | Status | Meaning |
|-----------|--------|---------|
| Payment inputs complete + user selected Gate Pay + user intent clear + authorization valid | Execute | Proceed with payment execution via `cex_pay_create_ai_order_pay` |
| Missing order_id, amount, or currency | Block | Ask user to provide complete payment details from merchant order page |
| User has not selected Gate Pay | Block | This skill does not apply; other payment methods are out of scope |
| User intent unclear or user declines | Block | Do not initiate payment; wait for clear confirmation or handle cancellation |
| Authorization missing, expired, or invalid | Block | Guide user to complete Gate account payment authorization first |
| User only asks payment status (no query tool available) | Inform | Explain limitation; do not charge again to infer status |
| Payment API returns success | Report | Output success receipt with transaction details (localized) |
| Payment API returns failure | Report | Output failure explanation in user's language with actionable guidance |

## Report Template

### Success Receipt

Use field labels in the user's language (see Language section). Template shape (English labels shown as reference):

```
✅ Payment Success

Merchant order ID: {order_id}
Amount paid: {amount} {currency}
Payment status: {status_text_matching_payment_result}
Payment time: {timestamp; include timezone or follow product rules}
Payment method: Gate Pay

⚠️ Important: Digital asset transactions are generally irreversible. Please verify the transaction details above.
```

**Voucher handling**: If the successful payment response includes voucher-style fields (final names per spec, e.g., prepayId), downstream steps may use them to fetch resources from the merchant. This skill does not fetch resources; voucher fields should be preserved for external use if applicable.

### Failure Explanation

Use the user's language (see Language section). Provide specific, actionable guidance based on error type:

**Template**:
```
❌ Payment Failed

Reason: {user_friendly_explanation}
Suggested action: {actionable_next_step}
```

**Do not**: Expose internal error codes, stack traces, or raw API responses to the user.

## Runtime rules

Before calling any payment-related tools, follow the Agent and MCP usage rules shipped with this product, and comply with [exchange-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/exchange-runtime-rules.md).

## Scenarios

Reviewer-oriented scenario templates (happy path, errors, localization, and safety edges) live in `references/scenarios.md` in this skill directory. Use that file for parity checks against this SKILL; do not treat the path as a Skills Hub hyperlink.

## Error Handling

| Error Type | Condition | User Message (Template) | Recommended Action |
|------------|-----------|-------------------------|-------------------|
| Insufficient balance | Payment API returns balance insufficient error | "Payment failed: Your Gate Pay balance is insufficient for this payment. Please top up your account and try again." | Guide user to deposit funds or use alternative payment method |
| Authorization expired/invalid | API indicates authorization is missing, expired, or invalid | "Payment failed: Your Gate payment authorization has expired or is invalid. Please complete Gate account authorization again." | Guide user through Gate account payment authorization flow |
| Order not found | API indicates order_id does not exist or cannot be found | "Payment failed: The order ID is invalid or no longer valid. Please verify the order details with the merchant and try again." | Ask user to obtain valid order information from merchant |
| Order expired | API indicates order has expired or payment window closed | "Payment failed: This order has expired and can no longer be paid. Please place a new order with the merchant." | Suggest user to create new order or contact merchant for replacement |
| Duplicate payment | Business logic detects duplicate charge attempt for same order | "This order has already been paid. Please check your payment history or contact support if you believe this is incorrect." | Do not initiate duplicate charge; explain limitation |
| Invalid parameters | Missing required fields or invalid format | "Payment cannot be processed: Some required information is missing or invalid. Please provide complete order details (order ID, amount, currency)." | Ask user to provide complete and valid payment parameters |
| Network/system error | API timeout, connection failure, or unspecified system error | "Payment failed due to a temporary system issue. Please try again in a few moments or contact support if the problem persists." | Suggest retry later; do not expose technical error details |

**General rules**:
- Use the user's language for all error messages (see Language section)
- Do not expose internal error codes, stack traces, or raw API responses
- Provide actionable next steps for each error type
- If error type is unclear, provide neutral guidance to retry or contact support

## Data Privacy & Collection

This skill processes user payment data through the Gate MCP. All data is transmitted directly to the Gate API for payment execution. 

**Data handling statement**:
- **Data collection**: This skill collects order information (order ID, amount, currency) and user payment authorization credentials as required for payment execution
- **Data storage**: No user data is stored locally by this skill. All payment transactions are processed and recorded by Gate's secure payment infrastructure
- **Data transmission**: Payment data is transmitted exclusively to Gate API endpoints. No third-party services are involved
- **Data protection**: All data transmission uses encrypted channels compliant with Gate's security standards
- **User control**: Users can view their payment history through Gate's official platform. Transaction records are maintained per Gate's data retention policy

**Age restriction**: This skill is intended for users aged 18 or above with full civil capacity, consistent with Gate's platform requirements.

## Risk Disclaimers

⚠️ **Important notices for Gate Pay users**:

1. **Risk of loss**: Paying with digital assets involves financial risk; you may lose the amounts debited if the order or merchant context is wrong. Verify every detail before authorizing a charge.

2. **Transaction irreversibility**: Digital asset transactions are generally irreversible. Once a Gate Pay payment is successfully executed, it cannot be undone. Please carefully verify all order details (merchant, amount, currency) before confirming payment.

3. **Not investment advice**: This skill provides payment execution functionality only. Any payment decisions are the user's sole responsibility. This does not constitute investment, financial, tax, or legal advice.

4. **Regulatory compliance**: Users must ensure their use of Gate Pay complies with applicable laws and regulations in their jurisdiction. Gate operates under licenses in multiple jurisdictions. Users are responsible for understanding and complying with local payment and digital asset regulations.

5. **Merchant responsibility**: Gate Pay facilitates payment to third-party merchants. Gate is not responsible for merchant products, services, delivery, refunds, or disputes. Users should verify merchant legitimacy before making payments.

6. **AI output disclaimer**: AI-assisted payment processing is for convenience only and does not constitute any representation, warranty, or guarantee by Gate regarding payment success, merchant reliability, or transaction outcomes.

## Safety Rules

### Confirmation Requirements

This skill follows a streamlined confirmation model for payment execution:

1. **User intent confirmation**: The user must clearly express payment intent (e.g., "pay", "confirm payment", "checkout")
2. **Parameter verification**: Payment details (order ID, amount, currency) may be displayed for user verification, but no additional forced confirmation step is required beyond clear payment intent
3. **Single-use confirmation**: Each payment intent is single-use. If parameters or merchant details change, re-confirm intent is required
4. **No execution without intent**: Without clear user payment intent, the skill operates in query/information mode only

### Authorization Guards

- **Pre-execution check**: Before calling `cex_pay_create_ai_order_pay`, verify user has completed Gate payment authorization
- **Authorization validation**: If authorization is missing, expired, or invalid, halt payment and guide user through authorization flow
- **No bypass**: Payment execution must not bypass authorization requirements under any circumstances

### Duplicate Payment Prevention

- **Transaction tracking**: Do not charge the same order_id twice within a conversation context
- **Status query limitation**: If user asks "did I pay?", explain query limitation rather than initiating a duplicate charge to infer status

## Security Requirements

1. Do not fabricate order information, payment status, timestamps, or payment vouchers.
2. Do not initiate a charge when inputs are incomplete or the user did not select Gate Pay for this payment.
3. If the charge did not succeed, do not output a success receipt or claim payment succeeded.
4. Do not charge twice for the same business transaction.
5. Do not invent voucher fields that the payment API did not return.
6. Do not expose sensitive data (API keys, internal error codes, system architecture details) in user-facing messages.
7. Validate all input parameters before calling payment API to prevent injection or malformed data attacks.
