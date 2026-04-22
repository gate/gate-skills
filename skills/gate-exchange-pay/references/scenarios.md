# Scenarios

This document defines behavior-oriented scenario templates for Gate Pay payment execution.

**Scenario layout**: Each scenario uses **Context** → **Prompt Examples** → **Expected Behavior**. An **Unexpected Behavior** subsection lists anti-patterns for reviewers; it is intentionally placed after **Expected Behavior** for readability (not a gate-skill-cr required field).

## Global Execution Gate (Mandatory)

For every scenario that includes `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二):
- Verify all payment inputs (order_id, amount, currency) are complete
- Validate user has completed Gate payment authorization (guide auth flow if missing)
- Confirm user payment intent is clear (e.g., "pay", "confirm payment", "checkout")
- Optional: Display payment details for user verification
- Execute payment only after clear intent confirmation
- Output localized receipt (success) or error explanation (failure)

If confirmation is missing/ambiguous or authorization is invalid, do not execute payment.

## I. Happy Path Scenarios (1-3)

## Scenario 1: Successful Payment with Complete Inputs

**Context**: User wants to pay for a merchant order using Gate Pay. All required payment details (order ID, amount, currency) are already available, and the user has completed Gate payment authorization.

**Prompt Examples**:
- "Pay 50 USDT for order ABC123 with Gate Pay."
- "Complete payment for order #XYZ789 using my Gate account."
- "Charge 100 USDT to my Gate Pay for this order."

**Expected Behavior**:
1. Verify payment readiness: from the user's message and conversation context, extract and validate `order_id`, `amount`, and `currency` for the current turn. The three prompt lines are equivalent shapes once resolved (e.g. first line: ABC123, 50, USDT; second: #XYZ789 with amount and currency from the message or prior context; third: resolve "this order" to a concrete order id and use 100 USDT as stated).
2. Validate user has Gate payment authorization (check authorization status via context or prior confirmation).
3. Confirm user payment intent is clear from prompt ("pay", "complete payment", "charge").
4. Optional: Display payment summary using the extracted values:
   ```
   Planned charge
   Merchant order ID: {order_id}
   Amount due: {amount} {currency}
   Payment method: Gate Pay
   ```
5. Call `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with the extracted `order_id`, `amount`, and `currency`.
6. On success, output receipt in the user's language using those same values. Illustration when the first prompt shape was used (`ABC123`, `50 USDT`):
   ```
   ✅ Payment Success
   Merchant order ID: ABC123
   Amount paid: 50 USDT
   Payment status: Completed
   Payment time: 2026-03-26 18:30:00 UTC
   Payment method: Gate Pay
   ⚠️ Important: Digital asset transactions are generally irreversible. Please verify the transaction details above.
   ```

**Unexpected Behavior**:
1. Executes payment without verifying authorization status first.
2. Outputs success receipt before API call completes or fabricates payment status.
3. Does not include irreversibility warning in success receipt.

## Scenario 2: Payment After Authorization Guidance

**Context**: User wants to pay for an order, but has not completed Gate payment authorization yet. The skill guides the user through authorization first, then executes payment after authorization is complete.

**Prompt Examples**:
- "I want to pay for order #ORDER123 with Gate Pay." [Authorization not completed]
- "Charge 200 USDT for this merchant order."

**Expected Behavior**:
1. Verify payment inputs: order_id=ORDER123, amount=200, currency=USDT extracted.
2. Check authorization status: detect authorization missing or incomplete.
3. Do NOT call `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) yet.
4. Guide user to complete Gate payment authorization:
   ```
   Before proceeding with payment, you need to complete Gate payment authorization.
   Please authorize payment access for your Gate account first.
   [Provide authorization link or instructions]
   ```
5. After user completes authorization and confirms intent again (e.g., "OK, now pay"), repeat readiness checks.
6. Call `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) and output success receipt (as in Scenario 1).

**Unexpected Behavior**:
1. Attempts to call payment API without authorization, resulting in API error.
2. Does not guide user to authorization flow; only reports "authorization failed" without actionable steps.
3. Charges payment after old/stale authorization without re-validating current status.

## Scenario 3: Localized Receipt (Chinese Example)

**Context**: User's conversation language is Chinese. Payment is successful. Receipt must be output in Chinese with localized field labels. Prompt examples below are English documentation parallels; the same intent may appear in Chinese (or mixed) in production.

**Prompt Examples**:
- "Pay for this order with Gate Pay."
- "Complete Gate Pay payment for order 12345, 100 USDT."

**Expected Behavior**:
1. Detect user's language is Chinese from conversation context (or the payment-turn locale).
2. Verify inputs: order_id=12345, amount=100, currency=USDT.
3. Validate authorization and confirm intent.
4. Call `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二).
5. Output receipt in Chinese:
   ```
   ✅ 支付成功
   商家订单号:12345
   支付金额:100 USDT
   支付状态:已完成
   支付时间:2026-03-26 18:30:00 UTC
   支付方式:Gate Pay
   ⚠️ 重要提示:数字资产交易通常不可撤销,请仔细核对交易详情。
   ```

**Unexpected Behavior**:
1. Outputs receipt in English even though user's language is Chinese.
2. Mixes languages in receipt (e.g., Chinese labels with English status text).
3. Does not include localized irreversibility warning.

## II. Error Handling Scenarios (4-8)

## Scenario 4: Insufficient Balance Error

**Context**: User attempts payment, but their Gate Pay account balance is insufficient for the order amount.

**Prompt Examples**:
- "Pay 1000 USDT for order #LOW_BALANCE with Gate Pay." [User balance: 50 USDT]

**Expected Behavior**:
1. Verify inputs: order_id=LOW_BALANCE, amount=1000, currency=USDT.
2. Validate authorization and confirm intent.
3. Call `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二).
4. API returns insufficient balance error.
5. Output user-friendly error message in user's language:
   ```
   ❌ Payment Failed
   Reason: Your Gate Pay balance is insufficient for this payment.
   Suggested action: Please top up your account and try again.
   ```
6. Do NOT output success receipt or fabricate payment status.

**Unexpected Behavior**:
1. Reports "payment successful" despite API error.
2. Exposes internal error code to user (e.g., "ERROR_CODE_1001: BALANCE_NOT_ENOUGH").
3. Does not suggest actionable next step (topping up account).

## Scenario 5: Authorization Expired Error

**Context**: User had completed authorization previously, but authorization has since expired. Payment API rejects the charge due to invalid authorization.

**Prompt Examples**:
- "Complete payment for order #EXPIRED_AUTH." [Authorization expired 2 hours ago]

**Expected Behavior**:
1. Verify inputs complete.
2. Attempt to call `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二).
3. API returns authorization expired/invalid error.
4. Output error explanation in user's language:
   ```
   ❌ Payment Failed
   Reason: Your Gate payment authorization has expired or is invalid.
   Suggested action: Please complete Gate account authorization again, then retry payment.
   ```
5. Guide user to re-authorize, then retry payment after new authorization.

**Unexpected Behavior**:
1. Does not detect authorization expiration before API call; only reports error after call fails.
2. Does not guide user to re-authorize; only says "authorization invalid" without next steps.
3. Retries payment automatically without user re-authorization, resulting in repeated failures.

## Scenario 6: Order Not Found Error

**Context**: User provides an order ID that does not exist or is no longer valid in merchant's system.

**Prompt Examples**:
- "Pay for order #INVALID_ORDER_ID with Gate Pay."

**Expected Behavior**:
1. Verify inputs: order_id=INVALID_ORDER_ID extracted.
2. Call `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二).
3. API returns order not found error.
4. Output error explanation:
   ```
   ❌ Payment Failed
   Reason: The order ID is invalid or no longer valid.
   Suggested action: Please verify the order details with the merchant and try again.
   ```
5. Do not fabricate order status or claim order exists.

**Unexpected Behavior**:
1. Reports "order paid successfully" despite order not existing.
2. Invents order status (e.g., "order is pending") without querying merchant.
3. Does not suggest user to verify order ID with merchant.

## Scenario 7: Order Expired Error

**Context**: User attempts to pay for an order whose payment window has closed (e.g., 15-minute payment deadline expired).

**Prompt Examples**:
- "Pay for order #EXPIRED_ORDER." [Order payment deadline: 30 minutes ago]

**Expected Behavior**:
1. Verify inputs: order_id=EXPIRED_ORDER.
2. Call `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二).
3. API returns order expired error.
4. Output error explanation:
   ```
   ❌ Payment Failed
   Reason: This order has expired and can no longer be paid.
   Suggested action: Please place a new order with the merchant or confirm whether a replacement order is available.
   ```

**Unexpected Behavior**:
1. Does not explain order expiration; only reports "payment failed."
2. Suggests user to retry payment for same order_id (which will continue to fail).
3. Claims order is still valid when API clearly indicates expiration.

## Scenario 8: Network/System Error

**Context**: Payment API call fails due to network timeout, temporary system unavailability, or unspecified system error.

**Prompt Examples**:
- "Pay 50 USDT for order #SYS_ERROR." [API experiences temporary outage]

**Expected Behavior**:
1. Verify inputs complete.
2. Attempt to call `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二).
3. API call times out or returns system error (non-business error).
4. Output neutral error message without exposing technical details:
   ```
   ❌ Payment Failed
   Reason: Payment failed due to a temporary system issue.
   Suggested action: Please try again in a few moments or contact support if the problem persists.
   ```
5. Do not expose stack traces, internal error codes, or API endpoint details.

**Unexpected Behavior**:
1. Exposes raw API error response to user (e.g., full JSON with internal fields).
2. Shows stack trace or technical error details (e.g., "TimeoutError at line 234").
3. Reports payment success despite system error (fabricates status).

## III. Edge Cases & Safety Scenarios (9-12)

## Scenario 9: Incomplete Payment Inputs

**Context**: User expresses payment intent, but required parameters (order ID, amount, or currency) are missing or unclear.

**Prompt Examples**:
- "Pay with Gate Pay." [No order ID or amount specified]
- "Complete payment for this order." [Order details not in conversation context]

**Expected Behavior**:
1. Detect missing required fields: order_id, amount, or currency not extracted.
2. Do NOT call `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二).
3. Ask user to provide complete payment details:
   ```
   Payment cannot be processed: Some required information is missing.
   Please provide:
   - Merchant order ID
   - Payment amount
   - Currency (e.g., USDT)
   ```
4. Wait for user to provide complete details before proceeding.

**Unexpected Behavior**:
1. Fabricates order_id or amount from unrelated conversation context.
2. Attempts payment API call with null/undefined parameters, causing API error.
3. Assumes default values (e.g., amount=0) without user confirmation.

## Scenario 10: Duplicate Payment Prevention

**Context**: User has already paid for an order in current conversation. User asks to pay again for the same order (potential duplicate charge).

**Prompt Examples**:
- "Pay for order #DUP123 with Gate Pay." [First payment]
- [Later] "Pay for order #DUP123 again."

**Expected Behavior**:
1. Detect that order_id=DUP123 was already paid in current conversation context.
2. Do NOT call `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) again.
3. Inform user:
   ```
   This order (#DUP123) has already been paid in this session.
   If you believe this is incorrect or need to verify payment status, please check your Gate payment history or contact the merchant.
   ```
4. Prevent duplicate charge for same business transaction.

**Unexpected Behavior**:
1. Executes duplicate payment without detecting prior charge in conversation.
2. Does not warn user about duplicate; charges twice for same order.
3. Assumes user wants to pay twice without confirmation.

## Scenario 11: Payment Status Query Without Query Tool

**Context**: User asks whether they have already paid for an order. No status query tool is available in MCP.

**Prompt Examples**:
- "Did I already pay for order #STATUS_CHECK?"
- "Check if I paid for this order."

**Expected Behavior**:
1. Recognize this is a status query request, not a payment execution request.
2. Do NOT call `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) as a substitute for querying status.
3. Explain limitation:
   ```
   I cannot query payment status directly (no status query tool available).
   Please check your Gate payment history in the Gate app or website, or contact the merchant to verify whether order #STATUS_CHECK has been paid.
   ```

**Unexpected Behavior**:
1. Attempts to execute payment again to "check" if order is already paid.
2. Fabricates payment status without querying any API.
3. Reports "order paid successfully" based on assumption rather than data.

## Scenario 12: User Declines Payment

**Context**: User initially expresses payment intent but then declines or cancels before execution.

**Prompt Examples**:
- "Pay 50 USDT for order #CANCEL_ORDER."
- [Assistant displays payment summary]
- User: "Wait, cancel that. I changed my mind."

**Expected Behavior**:
1. Initial inputs verified: order_id=CANCEL_ORDER, amount=50, currency=USDT.
2. User cancels or declines before payment execution.
3. Do NOT call `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二).
4. Acknowledge cancellation:
   ```
   Payment cancelled. No charge has been made to your Gate Pay account.
   Let me know if you'd like to proceed with payment later.
   ```

**Unexpected Behavior**:
1. Executes payment despite user cancellation request.
2. Does not acknowledge cancellation; proceeds with charge silently.
3. Reports payment cancelled but still calls payment API (resulting in actual charge).

## IV. Multi-Language & Localization Scenarios (13)

## Scenario 13: Language Switching Mid-Conversation

**Context**: User starts in one language (e.g., English), then the payment turn targets another locale (e.g., Chinese). Receipt should match the payment turn locale. Prompt examples use English strings as documentation parallels; production traffic may use Chinese (or mixed) for the same intent.

**Prompt Examples**:
- [Earlier conversation in English]
- "Pay for order #LANG_SWITCH with Gate Pay for 50 USDT."

**Expected Behavior**:
1. Detect the payment-turn locale (e.g., Chinese) from the user message or conversation context, even when the documentation example prompt is English.
2. Verify inputs: order_id=LANG_SWITCH, amount=50, currency=USDT.
3. Execute payment via `cex_pay_create_ai_order_pay` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二).
4. Output receipt in Chinese when that is the payment-turn locale:
   ```
   ✅ 支付成功
   商家订单号:LANG_SWITCH
   支付金额:50 USDT
   支付状态:已完成
   支付时间:2026-03-26 18:30:00 UTC
   支付方式:Gate Pay
   ⚠️ 重要提示:数字资产交易通常不可撤销,请仔细核对交易详情。
   ```

**Unexpected Behavior**:
1. Outputs receipt in English despite the payment-turn locale being Chinese.
2. Mixes languages in receipt (e.g., Chinese labels + English values).
3. Uses the opening conversation language instead of the payment-turn locale.

## Summary

**Total scenarios**: 13
- Happy path: 3
- Error handling: 5
- Edge cases & safety: 4
- Localization: 1

**Coverage**:
- ✅ Successful payment with complete inputs
- ✅ Authorization validation and guidance
- ✅ Localized receipts (Chinese example)
- ✅ All major error types (balance, authorization, order errors, system errors)
- ✅ Incomplete inputs handling
- ✅ Duplicate payment prevention
- ✅ Status query limitation
- ✅ User cancellation handling
- ✅ Language switching

**Test validation**: Each scenario includes Context, Prompt Examples, Expected Behavior, and Unexpected Behavior fields per gate-skill-cr standard format.
