# Gate Pay Payment Skill

## Overview

An AI-powered payment execution skill for Gate Pay transactions. This skill enables users to complete merchant order payments using their Gate account balance in pay-first scenarios (such as HTTP 402 payment-required flows). The skill handles payment authorization validation, transaction execution via Exchange `gate-cli`, and localized receipt generation.

### Core Capabilities

| Capability | Description | User Examples |
|------------|-------------|---------------|
| Payment execution | Execute Gate Pay charges for merchant orders after user confirmation | "Pay with Gate Pay", "Complete this payment", "Charge my Gate Pay account" |
| Authorization validation | Verify user has completed Gate payment authorization before executing charge | Automatically checks authorization status; guides user through auth flow if needed |
| Localized receipts | Generate payment success/failure messages in user's language | Outputs receipts in English, Chinese, or conversation language |
| Error handling | Provide user-friendly explanations for payment failures without exposing internal errors | Maps API errors to actionable user guidance (insufficient balance, expired order, etc.) |
| Payment readiness check | Validate all required parameters (order ID, amount, currency) are present before execution | Blocks payment if inputs incomplete; prompts user for missing details |
| Irreversibility warning | Remind users that digital asset transactions cannot be undone | Includes disclaimer in success receipts and pre-payment displays |

## Execution Guardrail (Mandatory)

Before executing payment via `cex_pay_create_ai_order_pay` (no `gate-cli` mapping; see `gate-cli/cmd/cex/MCP_LEGACY_TOOL_RESOLUTION.md` §二), the assistant must:

1. **Verify payment readiness**: All required parameters (order_id, amount, currency) are present and valid
2. **Confirm user intent**: User has clearly expressed payment intent (e.g., "pay", "confirm payment", "checkout")
3. **Validate authorization**: User has completed Gate payment authorization (guide auth flow if missing)
4. **Optional details display**: May show payment details for user verification (not a forced confirmation step)
5. **Execute only after clear intent**: Do not initiate payment without explicit user payment intent

**Hard gate rules**:
- NEVER call `cex_pay_create_ai_order_pay` (no `gate-cli` mapping; see `gate-cli/cmd/cex/MCP_LEGACY_TOOL_RESOLUTION.md` §二) without clear user payment intent in the current or immediately previous user turn
- If parameters change (amount, order ID, merchant), re-confirm intent is required
- If user asks "did I pay?" without query tool available, explain limitation—do not charge again to infer status
- Authorization missing/expired → halt payment, guide auth flow first

## Architecture

```
gate-exchange-pay/
├── SKILL.md                    # AI agent runtime instructions
├── README.md                   # Human-readable documentation (this file)
├── CHANGELOG.md                # Version history
└── references/
    └── scenarios.md            # Behavior-oriented test scenarios
```

**Design pattern**: Standard single-function skill architecture
- All workflow logic in one SKILL.md file
- No sub-modules (payment flow is straightforward and linear)
- Scenarios documented in `references/scenarios.md` for testing

## Usage Examples

```
User: "Pay 50 USDT for order #ABC123 with Gate Pay."
Assistant: [Verifies inputs complete, validates authorization]
          Planned charge:
          Merchant order ID: ABC123
          Amount due: 50 USDT
          Payment method: Gate Pay
          [Calls cex_pay_create_ai_order_pay]
          ✅ Payment Success
          Merchant order ID: ABC123
          Amount paid: 50 USDT
          Payment time: 2026-03-26 18:30:00 UTC
          ⚠️ Important: Digital asset transactions are generally irreversible.

User: "Complete payment for this order" [after seeing 402 payment page]
Assistant: [Extracts order details from context, validates authorization]
          [Displays payment summary, executes charge, outputs receipt]

User: "Did I already pay for order #XYZ789?"
Assistant: "I cannot query payment status directly (no status query tool available).
           Please check your Gate payment history or contact the merchant to verify."
```

## Trigger Phrases

- pay / payment / checkout / complete payment
- Gate Pay / pay with Gate Pay / charge Gate Pay
- confirm payment / proceed with payment / pay for me
- pay for this order / complete this order / finish payment

## Data Privacy & Security

**Data handling**:
- This skill processes order information (order ID, amount, currency) and user payment authorization credentials
- All data is transmitted exclusively to Gate API endpoints via `gate-cli`—no third-party services involved
- No user data is stored locally; payment records are maintained by Gate's infrastructure per platform policy
- All transmissions use encrypted channels compliant with Gate's security standards

**Age restriction**: This skill is intended for users aged 18 or above with full civil capacity.

## Risk Disclaimers

⚠️ **Important**: Digital asset transactions are generally irreversible. Please verify all payment details before confirming.

- This skill provides payment execution functionality only and does not constitute investment, financial, tax, or legal advice.
- Users must comply with applicable laws and regulations in their jurisdiction when using Gate Pay.
- Gate is not responsible for merchant products, services, delivery, refunds, or disputes. Verify merchant legitimacy before paying.

## Support & Contact

For issues or questions about this skill:
- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
- **Support**: Submit issues via GitHub repository or contact Gate customer support

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
- **License**: Proprietary (Gate.com)
