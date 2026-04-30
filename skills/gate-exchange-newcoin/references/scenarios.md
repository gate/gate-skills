# Scenarios

Behavior-oriented scenario templates for **`gate-exchange-newcoin`**. All write paths require **Action Draft** + explicit **Y** per `SKILL.md`.

## Global execution gate (mandatory)

For any scenario that ends in **`gate-cli cex spot order`** or **`gate-cli cex alpha order place`**:

1. Complete the read-phase union for activated signals **S1–S4**.
2. Present **Action Draft** with risk disclosure.
3. Obtain **Y** / **N** on that draft only.
4. Execute writes only after **Y**; treat confirmation as single-use.

---

## Scenario 1: Screen recent listings for safety and heat

**Context**: User wants newly listed coins, filtered by basic safety and attention, and may later ask to buy.

**Prompt Examples**:

- "What listed recently on Gate that is not an obvious scam and has buzz?"
- "Pull new listings from the last few days and flag higher-risk ones."

**Expected Behavior**:

1. Run **`gate-cli news feed get-exchange-announcements`** with listing-oriented filters supported by the CLI plus **`gate-cli news feed search-news`** as needed.
2. Extract symbols; for each candidate run **`gate-cli info compliance check-token-security`**, **`gate-cli info coin get-coin-info`**, **`gate-cli news feed get-social-sentiment`** in parallel batches.
3. Summarize trade-offs; **do not** place orders unless **`buy_intent=true`** **and** **Y** confirmation follows a fresh Action Draft.

---

## Scenario 2: Pre-listing diligence only

**Context**: User expects an upcoming listing and wants fundamentals and risk **without** placing orders.

**Prompt Examples**:

- "Coin XYZ is rumored to list soon — summarize project, tokenomics, and risks."
- "Due diligence only on ABC before it goes live."

**Expected Behavior**:

1. Query **`gate-cli news feed get-exchange-announcements`** with keyword coverage when helpful.
2. Run **`gate-cli info coin get-coin-info`** and **`gate-cli info compliance check-token-security`** for the named asset.
3. Deliver a structured report; **no** write CLIs.

---

## Scenario 3: Rapid rally with scam concerns plus optional chase

**Context**: User worries about scams or rugs after a sharp move and may request a small chase trade.

**Prompt Examples**:

- "TOKEN pumped 80% after listing — rug risk? Can I chase a tiny spot amount?"
- "Is this pump manipulated? If clean, I might buy $50."

**Expected Behavior**:

1. Parallel **`gate-cli news events get-latest-events`**, **`gate-cli info compliance check-token-security`**, **`gate-cli info coin get-coin-info`**.
2. If user supplied an address, add **`gate-cli info onchain get-address-info`** with explicit chain context.
3. Explain attribution cautiously; if **`buy_intent=true`**, produce Action Draft with **liquidity/slippage** warnings **before** **`gate-cli cex spot order buy`**.

---

## Scenario 4: Weekly launchpool-style calendar

**Context**: User wants a calendar of launch-oriented programs with rough risk labels, not immediate orders.

**Prompt Examples**:

- "Build this week’s launchpool calendar with risk labels and staking notes."
- "Summarize LaunchPool announcements for the next 7 days."

**Expected Behavior**:

1. **`gate-cli news feed get-exchange-announcements`** with launchpool-oriented filters **and** **`gate-cli cex launch projects`**.
2. For each project coin, **`gate-cli info coin get-coin-info`** + **`gate-cli info compliance check-token-security`** (batch when possible).
3. Output schedule table plus qualitative risk tiers; **no** writes unless user later confirms execution intent.

---

## Scenario 5: Narrative sector token with optional starter buy

**Context**: User mixes thesis research with possible small first spot buy.

**Prompt Examples**:

- "Review this NFT-sector listing for fundamentals and tape; if sane, I might buy $100 spot."
- "Check this AI meme coin narrative and quote me a cautious entry."

**Expected Behavior**:

1. **`gate-cli info coin get-coin-info`**, **`gate-cli news feed search-news`**, **`gate-cli cex spot market ticker`** (add **`gate-cli cex spot market orderbook`** if depth matters).
2. If **`buy_intent=true`**, finish Action Draft including **fee** and **volatility** notes **before** spot order CLI.

---

## Scenario 6: Track listing tape and place first limit

**Context**: User monitors post-listing price and wants a limit first order when conditions match.

**Prompt Examples**:

- "Watch SYMBOL after listing; if ask dips below X, draft a limit buy for Y USDT notional."
- "Alert me when SYMBOL tape looks sane and prep a limit buy."

**Expected Behavior**:

1. **`gate-cli news feed get-exchange-announcements`** for listing context **and** **`gate-cli cex spot market ticker`** (poll responsibly without infinite loops; cap iterations or ask user to rerun).
2. When user commits to a limit with explicit parameters, output Action Draft with **limit price**, **size**, **est. fee**.
3. Call **`gate-cli cex spot order buy`** (limit) **only** after **Y**.

---

## Scenario 7: Missing symbol edge case

**Context**: User expresses urgent buy desire but does not name an instrument.

**Prompt Examples**:

- "Buy the hottest new coin now with 200 USDT."
- "Market buy something that just listed without telling you which pair."

**Expected Behavior**:

1. Refuse writes; ask for **pair** or **symbol** and intended market (spot vs Alpha).
2. Optionally suggest running **Scenario 1** reads to produce candidates.
3. **Never** guess a pair for market orders without user confirmation of the exact **currency_pair**.
