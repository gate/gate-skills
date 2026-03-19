# OpenAPI: Quote + Token Resolution

> Load after `_shared.md`. Covers parameter collection, chain inference, token address resolution, and the quote API call.

---

## Smart Chain Inference

When user doesn't specify chain:

**Can determine** (use directly): ETH→1, SOL→501, BNB→56, AVAX→43114, GT→10088, POL→137, SUI→784, TRX→195, TON→607, "on Arbitrum"→42161

**Cannot determine** (ask user): USDT, USDC, WETH, DAI etc. exist on multiple chains.

---

## Token Address Resolution

API requires contract addresses. Resolution priority:

1. **Native token?** → Use `"-"` (ETH on Ethereum, BNB on BSC, SOL on Solana, etc.)
2. **Query gate-dex-market Skill** (if available, uses same AK/SK)
3. **Common token quick reference**:

| Token | Ethereum (1) | BSC (56) | Arbitrum (42161) | Base (8453) | Solana (501) |
|-------|-------------|---------|-----------------|------------|-------------|
| USDT | 0xdAC17F958D2ee523a2206206994597C13D831ec7 | 0x55d398326f99059fF775485246999027B3197955 | 0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9 | — | Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB |
| USDC | 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 | 0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d | 0xaf88d065e77c8cC2239327C5EDb3A432268e5831 | 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 | EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v |
| WETH | 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 | — | 0x82aF49447D8a07e3bd95BD0d56f35241523fBab1 | 0x4200000000000000000000000000000000000006 | — |
| WBTC | 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599 | — | — | — | — |
| DAI | 0x6B175474E89094C44Da98b954EedeAC495271d0F | — | — | — | — |
| WBNB | — | 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c | — | — | — |
| WSOL | — | — | — | — | So11111111111111111111111111111111111111112 |

4. **Ask user** to provide contract address
5. **Confirm**: "About to trade [symbol] ([addr first6...last4]) on [chain], confirm?"

---

## Cross-Chain Detection

If user wants to swap tokens across different chains (e.g., "swap USDT on ETH for SOL on Solana"):

```
OpenAPI does not support cross-chain swaps, only same-chain Swap.
For cross-chain, please install Gate MCP service: https://github.com/gate/gate-mcp
```

**Terminate process. Do not call quote.**

---

## Action: trade.swap.quote

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| chain_id | int | Yes | Chain ID |
| token_in | string | Yes | Input token address. Native token = `"-"` |
| token_out | string | Yes | Output token address. Native token = `"-"` |
| amount_in | string | Yes | Input amount (human-readable, e.g. `"0.1"`) |
| slippage | float | Yes | Slippage, 0.01 = 1% |
| slippage_type | int | Yes | 1 = percentage, 2 = fixed |
| user_wallet | string | Yes | User wallet address |

**Call**:
```bash
python3 gate-dex-trade/scripts/gate-api-call.py "trade.swap.quote" '{"chain_id":501,"token_in":"-","token_out":"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v","amount_in":"0.001","slippage":0.05,"slippage_type":1,"user_wallet":"2ycvS9..."}'
```

**Key response fields**:
- `quote_id` — Required for build step
- `amount_out` — Estimated output
- `min_amount_out` — Minimum after slippage
- `from_token` / `to_token` — Token details (symbol, price, decimal, is_native_token)
- `protocols` — Route splits (3-level nested array)

**Error handling**: 31104 = pair not found, 31105/31503 = insufficient liquidity, 31111 = gas exceeds output, 31109 = high price impact, 31112 = cross-chain not supported.

---

## Query Actions (No Confirmation Needed)

### trade.swap.chain
```bash
python3 gate-dex-trade/scripts/gate-api-call.py "trade.swap.chain" "{}"
```
Returns all supported chains. Display as table.

### trade.swap.gasprice
```bash
python3 gate-dex-trade/scripts/gate-api-call.py "trade.swap.gasprice" '{"chain_id":56}'
```
Returns gas prices. Format varies by chain type (EVM: wei, Solana: micro-lamports, etc.). Does not support Ton.
