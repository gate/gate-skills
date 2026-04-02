# Gate Auto-Invest — Rules, compliance, funding source

Static product rules and compliance-facing replies. **Often no MCP write** is required—answer from policy below and forward API errors faithfully.

## Workflow

1. **Classify the question**: Investment currency limits, funding source / Simple Earn, post-stop holdings, region restriction, generic compliance, or create-plan compliance failure.
2. **Answer from policy**: Use the sections below; do not invent product rules. Do not call write tools unless the user also requests a plan lifecycle action (then route to `autoinvest-plans.md`).
3. **Optional read-only context**: If the user asks where funds are debited from, optionally use `cex_spot_get_spot_accounts` or `cex_earn_list_user_uni_lends` for balance context only, per **Funding source** section.
4. **API-aligned wording**: For compliance failures, prefer MCP/API messages; use **Report Template** samples when they match the situation.

## Report Template

**Region restriction (adapt to actual API message)**:

```
This service is not available in your region at the moment. Please try again later or contact customer support.
```

**Investment currency (USDT/BTC only)** — short reply:

```
Only USDT or BTC are supported as the investment currency (the amount debited each period). You can still choose other assets as purchase targets.
```

## Investment currency (hard rule)

- **Only USDT or BTC** may be used as the **investment currency** (the currency debited each period).
- Users may still **target** other coins (e.g. buy ETH with USDT).
- If the user asks to use **ETH** (or any non-USDT/BTC) as investment currency: reply clearly that this product only supports **USDT or BTC** as invest currency; suggest using USDT/BTC to DCA **into** their desired coin.

**Prompt Examples**:
- "Can I use ETH to fund my DCA?"

**Expected Behavior**: No create call; explain rule in English.

---

## Funding source: spot vs Simple Earn

**Prompt Examples**:
- "Is DCA debited from spot or Simple Earn?"
- "Does it take from Simple Earn?"

**Expected Behavior**:
1. Default: **spot** for debits unless the plan explicitly uses Simple Earn / Uni participation.
2. If user enabled Simple Earn linkage, state that when visible from **plan detail** or product copy.
3. Optionally cite `cex_spot_get_spot_accounts` vs `cex_earn_list_user_uni_lends` for **balance context** only—not as legal guarantee.

---

## Fund flow: post-purchase destination (API `fund_flow`)

**Policy** (aligns with `SKILL.md` → **Fund Flow**):

- **`earn`** → Simple Earn / flexible earn (exact app label may vary by locale).
- **`auto_invest`** → spot account (default).

When users refer to Simple Earn (flexible earn) or spot account in any language, map to `earn` or `auto_invest` for create/update MCP calls.

---

## After stopping a plan

**Prompt Examples**:
- "Where is my money after I stop DCA?"
- "Do I need to redeem?"

**Expected Behavior**:
- Stopping ends **future** debits.
- **Purchased assets** typically remain in **spot** / trading account; no extra "redeem auto-invest" if holdings are normal spot.
- If user had **Simple Earn** auto-transfer, mention possible product-specific redemption paths per app—no step-by-step circumvention.

---

## Compliance scenarios

### Region restriction

**Prompt Examples**:
- "Can I use this in [country]?"

**Action**: Rely on API/compliance responses when attempting actions; short message that service may be unavailable in the user’s region—no circumvention advice.

### Generic compliance failure

**Prompt Examples**:
- "Compliance check failed."

**Action**: Summarize MCP/API message; list possible reasons (region, enterprise restrictions, risk) **without** inventing specific codes.

### Create plan failed — compliance validation

**Prompt Examples**:
- "My auto-invest plan creation failed; it says compliance validation failed."
- "I tried to create a DCA plan but got a compliance error."

**Logic**:
- A **compliance validation** failure can stem from **multiple causes** (e.g. restricted region, enterprise-account restrictions, risk controls). Do **not** invent an internal error code.
- When the underlying reason is a **restricted region** (or the API message clearly indicates regional unavailability), **state that reason plainly** to the user—do not imply KYC or other causes unless the API says so.

**Sample output (English)** — region case:

```
This service is not available in your region at the moment. Please try again later or contact customer support.
```

(Adapt wording to match the actual MCP/API message when it is more specific.)

---

## Error summary

| Situation | Response pattern |
|-----------|-------------------|
| Region | Service may be unavailable; no circumvention |
| Create plan — compliance validation failed | Prefer API/MCP wording; if region: use sample output above |
| Generic | Summarize API message |
| Auth | [`exchange-runtime-rules.md`](../../exchange-runtime-rules.md) |
