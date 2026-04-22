# Scenarios

This document defines behavior-oriented scenario templates for gate-exchange-transfer. All transfer operations require **explicit user confirmation** before execution.

## Global Execution Gate (Mandatory)

For every scenario that includes `gate-cli cex wallet transfer create`, `gate-cli cex wallet transfer to-sub`, or `gate-cli cex wallet transfer sub-to-sub`:
- Verify source balance first
- Present Transfer Draft (currency, amount, from, to)
- Require explicit confirmation from the immediately previous user turn
- Treat confirmation as single-use
- Re-confirm whenever parameters or intent change

If confirmation is missing/ambiguous/stale, do not execute any transfer.

## I. Main Account Transfers (1-4)

## Scenario 1: Spot to Futures
**Context**: User wants to transfer funds from spot to futures account.
**Prompt Examples**:
- "Transfer 1000 USDT from spot to futures."
- "Move my USDT to futures for trading."
**Expected Behavior**:
1. Call `get_spot_accounts` `currency=USDT` to verify available balance.
2. If balance >= amount, output `Transfer Draft`: currency=USDT, amount, from=spot, to=futures, settle=USDT.
3. Wait for user confirmation.
4. Call `gate-cli cex wallet transfer create` with from=spot, to=futures, settle=USDT.
5. Output `Transfer Result Report`.
**Unexpected Behavior**:
1. Executes without balance check.
2. Executes without user confirmation.
3. Omits settle for futures (causes API error).

## Scenario 2: Futures to Spot
**Context**: User wants to transfer funds from futures to spot.
**Prompt Examples**:
- "Transfer 500 USDT from futures to spot."
- "Move my futures balance back to spot."
**Expected Behavior**:
1. Call `get_futures_accounts` or equivalent to verify futures balance.
2. Output `Transfer Draft` with from=futures, to=spot, settle=USDT.
3. Wait for confirmation.
4. Call `gate-cli cex wallet transfer create`.
5. Output `Transfer Result Report`.
**Unexpected Behavior**:
1. Transfers without verifying futures balance.
2. Executes without confirmation.
3. Uses wrong settle currency.

## Scenario 3: Spot to Margin
**Context**: User wants to transfer to margin account for leveraged trading.
**Prompt Examples**:
- "Transfer 200 USDT to margin."
- "Move funds to margin for BTC_USDT."
**Expected Behavior**:
1. Call `get_spot_accounts` to verify balance.
2. Determine `currency_pair` (e.g. BTC_USDT) from user intent or ask.
3. Output `Transfer Draft` with from=spot, to=margin, currency_pair.
4. Wait for confirmation.
5. Call `gate-cli cex wallet transfer create` with currency_pair.
6. Output `Transfer Result Report`.
**Unexpected Behavior**:
1. Omits currency_pair (required for margin).
2. Executes without confirmation.
3. Uses invalid currency pair.

## Scenario 4: Margin to Spot
**Context**: User wants to transfer from margin back to spot.
**Prompt Examples**:
- "Transfer 200 USDT from margin to spot."
- "Move margin balance to spot."
**Expected Behavior**:
1. Output `Transfer Draft` with from=margin, to=spot, currency_pair.
2. Wait for confirmation.
3. Call `gate-cli cex wallet transfer create`.
4. Output `Transfer Result Report`.
**Unexpected Behavior**:
1. Omits currency_pair.
2. Executes without confirmation.

## II. Sub-Account Transfers (5-7)

## Scenario 5: Main to Sub-Account
**Context**: User wants to transfer from main account to a sub-account.
**Prompt Examples**:
- "Transfer 1000 USDT to sub-account 12345."
- "Send 500 USDT to my sub-account."
**Expected Behavior**:
1. Call `get_spot_accounts` to verify main account balance.
2. Output `Transfer Draft`: currency, amount, direction=to, sub_account.
3. Wait for confirmation.
4. Call `gate-cli cex wallet transfer to-sub` with direction=to.
5. Output `Transfer Result Report`.
**Unexpected Behavior**:
1. Executes without sub_account UID.
2. Executes without confirmation.
3. Transfers more than available balance.

## Scenario 6: Sub-Account to Main
**Context**: User wants to transfer from sub-account back to main.
**Prompt Examples**:
- "Transfer 500 USDT from sub-account to main."
- "Move sub-account balance to main."
**Expected Behavior**:
1. Call `gate-cli cex wallet balance sub` to verify sub-account balance.
2. Output `Transfer Draft` with direction=from, sub_account.
3. Wait for confirmation.
4. Call `gate-cli cex wallet transfer to-sub` with direction=from.
5. Output `Transfer Result Report`.
**Unexpected Behavior**:
1. Executes without verifying sub-account balance.
2. Executes without confirmation.
3. Uses wrong sub_account UID.

## Scenario 7: Sub-Account to Sub-Account
**Context**: User wants to transfer between two sub-accounts.
**Prompt Examples**:
- "Transfer 100 USDT from sub-account A to sub-account B."
- "Move funds between my sub-accounts."
**Expected Behavior**:
1. Call `gate-cli cex wallet balance sub` to verify source sub-account balance.
2. Output `Transfer Draft`: currency, amount, sub_account_from, sub_account_to, types.
3. Wait for confirmation.
4. Call `gate-cli cex wallet transfer sub-to-sub`.
5. Output `Transfer Result Report`.
**Unexpected Behavior**:
1. Executes without both sub_account_from and sub_account_to.
2. Executes without confirmation.
3. Omits sub_account_from_type or sub_account_to_type.

## III. Status Query (8)

## Scenario 8: Transfer Status Query
**Context**: User wants to check status of a main-sub transfer.
**Prompt Examples**:
- "Check my transfer status."
- "What's the status of my last transfer?"
**Expected Behavior**:
1. Call `gate-cli cex wallet transfer status` with client_order_id or tx_id if user provides.
2. Output `Transfer Status Report`.
**Unexpected Behavior**:
1. Executes a new transfer instead of querying.
2. Returns wrong transfer when multiple exist (ask user to specify).
