# Scenarios

This document defines behavior-oriented scenario templates for all 14 invite-friends cases.

## Global Response Rule

For every scenario:
- Do not recommend activity cards when interpreting rules
- Include a brief description and entry guidance when recommending activities
- Do not promise specific reward amounts
- Redirect to the activity page when specific task requirements (deposit/trading volume) are involved
- When guiding users to the "Invite Friends page" or "activity page", always include the direct URL: https://www.gate.com/referral

## I. Activity Recommendation (1-3)

## Scenario 1: Recommend Activities (Earn Together Available)
**Context**: User asks about referral activities while an Earn Together campaign is currently active.
**Prompt Examples**:
- "What referral activities do you have?"
- "What rewards can I get from inviting friends?"
- "How can I earn money by inviting people?"
- "What referral programs do you have?"
**Expected Behavior**:
1. Check whether an Earn Together campaign is currently active → Yes.
2. Prioritize introducing and recommending the Earn Together campaign (recommend only 1 activity).
3. Reference response: "Here is a recommended referral activity for you. Invite friends to complete designated tasks and earn generous rewards (entry: https://www.gate.com/referral)," with a brief introduction of the Earn Together campaign.
**Unexpected Behavior**:
1. Recommends all three activities simultaneously without prioritizing based on activity status.
2. Does not check Earn Together status and directly recommends other activities.
3. Promises specific reward amounts (e.g., "You can earn XX USDT per invitation").

## Scenario 2: Recommend Activities (No Earn Together)
**Context**: User asks about referral activities while no Earn Together campaign is currently active.
**Prompt Examples**:
- "What rewards can I get from inviting friends?"
- "Are there any referral activities I can join?"
- "I want to invite friends. What benefits are there?"
**Expected Behavior**:
1. Check whether an Earn Together campaign is currently active → No.
2. Introduce and recommend both Help & Get Coupons and Super Commission.
3. Reference response: "Gate currently offers the following 2 referral programs. Choose based on your preference: [Help & Get Coupons] Invite 2 friends to complete tasks and receive platform coupon rewards. [Super Commission] A permanent referral system where you earn ongoing commission from your friends' trades."
**Unexpected Behavior**:
1. Recommends a nonexistent Earn Together campaign.
2. Only recommends one of the two activities, omitting the other.
3. Output is too brief and does not explain the core difference between the two activities.

## Scenario 3: How to Get Referral Link
**Context**: User asks how to invite friends or obtain a referral link.
**Prompt Examples**:
- "How do I invite friends?"
- "Where can I get my referral link?"
- "How do I share my referral code?"
- "How do I get my referral link?"
**Expected Behavior**:
1. Explain the steps to obtain the referral link: go to the Invite Friends page (https://www.gate.com/referral) → copy the exclusive link or QR code.
2. Briefly explain the process for friends to register via the link.
3. Guide the user to the Invite Friends page (https://www.gate.com/referral) to proceed.
**Unexpected Behavior**:
1. Provides an incorrect page path or nonexistent feature entry.
2. Skips guidance and directly generates a link (AI does not have this capability).
3. Does not mention the QR code sharing option.

## II. Rule Interpretation (4-7)

## Scenario 4: Explain Earn Together Rules
**Context**: User asks about the specific rules and mechanics of the Earn Together campaign.
**Prompt Examples**:
- "How does Earn Together work?"
- "What is Earn Together?"
- "What are the Earn Together rules?"
**Expected Behavior**:
1. Explain the Earn Together participation flow in detail: inviter shares link → invitee registers → completes tasks → both parties receive random rewards.
2. Describe the activity characteristics: time-limited, exclusive (only one at a time), random rewards.
3. Note important caveats: task requirements vary by region; rewards are subject to risk-control review.
4. After the explanation, ask: "Is there anything else you'd like to know?"
5. Do not recommend activity cards.
**Unexpected Behavior**:
1. Recommends activity cards while interpreting the rules.
2. Provides specific deposit amounts or trading volume requirements.
3. Promises specific reward amounts.
4. Does not mention the randomness of rewards and risk-control review.

## Scenario 5: Explain Help & Get Coupons Rules
**Context**: User asks about the specific rules and mechanics of Help & Get Coupons.
**Prompt Examples**:
- "How does Help & Get Coupons work?"
- "What is the coupon campaign?"
- "How can I get trial vouchers?"
**Expected Behavior**:
1. Explain the Help & Get Coupons participation flow in detail: share link → invite 2 new users to register → new users complete deposit and trading tasks → receive coupon rewards.
2. Describe the reward format: coupon rewards (e.g., 200 USDT position trial voucher; rewards may be adjusted based on actual conditions).
3. Note important caveats: rewards are distributed to the Coupon Center, valid for 5 days, subject to usage rules and restrictions.
4. Do not recommend activity cards.
**Unexpected Behavior**:
1. Recommends activity cards while interpreting the rules.
2. Describes coupon rewards as cash rewards.
3. Does not mention the coupon validity period and usage rule restrictions.
4. Provides specific deposit and trading volume requirements.

## Scenario 6: Explain Super Commission Rules
**Context**: User asks about the specific rules and mechanics of Super Commission.
**Prompt Examples**:
- "How does Super Commission work?"
- "How does the commission rebate work?"
- "How can I earn ongoing passive income?"
- "How does the commission rebate work?"
**Expected Behavior**:
1. Explain the Super Commission participation flow in detail: share link → friend registers → friend trades → both parties receive trading fee rebates.
2. List the covered trading types: Spot, Alpha, Futures, TradFi, etc.
3. Highlight the key feature: permanently effective with continuous passive income.
4. Note important caveats: commission rates vary by trading type; check the activity page for detailed rules.
5. Do not recommend activity cards.
**Unexpected Behavior**:
1. Provides specific commission rate percentages.
2. Describes the commission as a one-time reward rather than an ongoing benefit.
3. Does not mention that commission rates vary by trading type.

## Scenario 7: Can I Join Multiple Activities
**Context**: User asks whether all three activities can be joined simultaneously.
**Prompt Examples**:
- "Can I join all three activities at the same time?"
- "Can I participate in both Earn Together and Super Commission?"
- "Can I join all referral programs at once?"
**Expected Behavior**:
1. Clearly confirm that all three activities can be joined simultaneously.
2. Emphasize the exclusivity constraint: referral relationships created through Super Commission cannot earn rewards from other activities; users invited through other activities cannot earn commission rebates.
3. Reference response: "Yes, you can participate in all three activities simultaneously. However, please note: referral relationships created through Super Commission cannot earn rewards from other activities, and users invited through other activities cannot earn commission rebates."
**Unexpected Behavior**:
1. Simply answers "Yes" without explaining the exclusivity constraint.
2. Incorrectly states that simultaneous participation is not allowed.
3. Misinterprets the exclusivity rule (e.g., "All activity rewards can be stacked").

## III. Personalized Recommendation (8-10)

## Scenario 8: Quick Cash Reward Recommendation
**Context**: User wants quick cash rewards and needs the best-matching activity recommended.
**Prompt Examples**:
- "I want to earn money quickly. Which activity do you recommend?"
- "Is there an activity that gives rewards fast?"
- "Which program gives the fastest reward?"
**Expected Behavior**:
1. Based on the "quick cash" need, recommend the Earn Together campaign.
2. Explain the recommendation rationale: both parties receive random cash vouchers, claimable after task completion.
3. Briefly describe the participation steps and important notes.
4. If no Earn Together campaign is currently active, inform the user and recommend Help & Get Coupons as an alternative.
**Unexpected Behavior**:
1. Recommends Super Commission (commission is long-term income, not quick earnings).
2. Promises specific cash reward amounts.
3. Does not consider whether an Earn Together campaign is currently active.

## Scenario 9: Coupon/Voucher Recommendation
**Context**: User wants trial vouchers or discount coupons.
**Prompt Examples**:
- "I want trial vouchers."
- "Are there any discount coupons I can claim?"
- "How do I get a position trial voucher?"
**Expected Behavior**:
1. Based on the "get trial vouchers" need, recommend the Help & Get Coupons activity.
2. Explain the recommendation rationale: invite 2 friends to complete tasks to receive platform coupon rewards.
3. Briefly describe the participation steps and coupon usage notes (5-day validity, etc.).
**Unexpected Behavior**:
1. Recommends Earn Together or Super Commission (does not match user need).
2. Equates coupon rewards with cash rewards in the description.
3. Does not mention the coupon validity period restriction.

## Scenario 10: Long-term Passive Income Recommendation
**Context**: User wants long-term passive income.
**Prompt Examples**:
- "Is there a way to earn money long-term?"
- "I want ongoing passive income."
- "How can I earn passive income from referrals?"
**Expected Behavior**:
1. Based on the "long-term passive income" need, recommend Super Commission.
2. Explain the recommendation rationale: permanently effective; you earn ongoing rebates from your friends' trades.
3. Briefly describe the participation steps and the trading types covered by the rebate.
**Unexpected Behavior**:
1. Recommends Earn Together (a time-limited event, not long-term).
2. Promises specific commission rate percentages.
3. Does not mention the "permanently effective" key feature.

## IV. FAQ and Boundaries (11-14)

## Scenario 11: Why Different Reward Amounts
**Context**: User is confused about why they and their friend received different reward amounts.
**Prompt Examples**:
- "Why did my friend and I get different amounts?"
- "Why are the reward amounts different?"
- "Why did my friend get a different reward?"
**Expected Behavior**:
1. Clearly explain the random reward generation mechanism: rewards are randomly generated, and the amount may differ for each invitation.
2. Use a friendly tone to assure the user that this is normal behavior, not a system error.
**Unexpected Behavior**:
1. Implies a system error or suggests contacting customer support.
2. Provides misleading numbers such as "typically XX USDT."
3. Does not clearly explain the random mechanism.

## Scenario 12: When Will Reward Arrive
**Context**: User asks when the reward will be credited.
**Prompt Examples**:
- "When will my reward arrive?"
- "Why haven't I received my reward yet?"
- "When will I receive my referral reward?"
**Expected Behavior**:
1. Explain that rewards are subject to a risk-control review process.
2. Inform the user that rewards are typically reviewed and distributed within 14 business days after the activity ends.
3. Use a reassuring tone to confirm this is the standard process.
**Unexpected Behavior**:
1. States that rewards are credited immediately.
2. Provides inaccurate arrival times.
3. Suggests the user contact customer support to expedite (standard review process does not require this).

## Scenario 13: Specific Task Requirements
**Context**: User asks about specific deposit amounts or trading volume requirements.
**Prompt Examples**:
- "How much do I need to deposit to get rewards?"
- "How much do I need to trade to complete the task?"
- "What's the minimum deposit to qualify?"
**Expected Behavior**:
1. Explain that specific deposit amounts and trading volume requirements vary by regional policy.
2. Guide the user to check the activity page for detailed requirements.
3. Do not provide specific numbers directly.
**Unexpected Behavior**:
1. Provides specific deposit amounts (e.g., "Deposit 100U").
2. Provides specific trading volume requirements.
3. Does not guide the user to check the activity page.

## Scenario 14: Query Activity Data / Reward Progress
**Context**: User wants to check activity data or reward progress.
**Prompt Examples**:
- "How many people have I invited?"
- "How much reward have I earned so far?"
- "Can you check my invitation progress?"
- "How many friends have I successfully invited?"
**Expected Behavior**:
1. Inform the user that activity data queries via conversation are not currently supported.
2. Guide the user to the Invite Friends page to view detailed data.
3. Reference response: "Activity data queries via conversation are not currently supported. Please visit the Invite Friends page (https://www.gate.com/referral) to view detailed data."
**Unexpected Behavior**:
1. Fabricates activity data (e.g., "You have invited 5 people").
2. Attempts to call a nonexistent API to query data.
3. Does not guide the user to the activity page.
