# OpenAPI: SOP Three-Step Confirmation

> Loaded during any swap flow. All swap operations involving funds MUST pass through these three steps — they CANNOT be skipped or merged.

---

## SOP Step 1: Trading Pair Confirmation

**When**: After parameter collection, before calling quote.

**Display**:
```
========== Swap Trading Pair Confirmation ==========
  Chain: {chain_name} (chain_id: {chain_id})
  Sell: {amount_in} {from_token_symbol}
  Buy: {to_token_symbol}
  Slippage: {slippage}% ({slippage_type_text})
  Wallet: {user_wallet_short}  (0x1234...abcd)
====================================================
```

**Options**: Confirm → call quote | Modify slippage | Modify amount | Cancel

---

## SOP Step 2: Quote Details

**When**: After quote returns successfully.

**Display**:
```
========== Swap Quote Details ==========
  Sell: {amount_in} {from_token_symbol} (~ ${from_value_usd})
  Buy: ~ {amount_out} {to_token_symbol}
  Minimum receive: {min_amount_out} {to_token_symbol} (incl. {slippage}% slippage)
  Price impact: {price_impact}%
  Route: {route_display}
  Estimated Gas: Subject to build return
=======================================
```

**Route display**:
- Single hop: `UNISWAP_V3 (100%)`
- Multi-hop: `UNISWAP_V2: USDT -> WBTC -> WETH (100%)`
- Split: `UNISWAP_V3: ETH -> USDT (60%)` / `SUSHISWAP: ETH -> USDC -> USDT (40%)`

**Price impact**: `abs(1 - (amount_out * to_token_price) / (amount_in * from_token_price)) * 100`

- <= 5%: Normal flow. Options: Confirm → build | Modify amount | Cancel
- > 5%: **Mandatory risk warning**: "Price impact is {X}%, exceeding 5% safety threshold. Large impact may cause significant asset loss." Options: Accept risk | Reduce amount | Cancel

**Slippage warning**: If slippage > 5%, also display: "High slippage may expose you to MEV attacks (sandwich attacks). Consider lowering slippage."

---

## SOP Step 3: Signature Authorization

**When**: After build returns unsigned_tx.

**Display**:
```
========== Signature Authorization ==========
  Target contract: {unsigned_tx.to}
  Send amount: {unsigned_tx.value}
  Gas limit: {unsigned_tx.gas_limit}
  Chain ID: {unsigned_tx.chain_id}
  Data prefix: {first 20 chars of data}...
  Order ID: {first 10 chars of order_id}...
=============================================
```

**Options**: Confirm sign and submit | Cancel

---

## Security: Cannot Skip

Even if user says "skip confirmation", respond: "For fund security, confirmation steps are mandatory and cannot be skipped."
