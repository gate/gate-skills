---
name: gate-dex-trade-cli
version: "2026.4.24-1"
updated: "2026-04-24"
description: "gate-dex CLI swap skill. One-shot DEX swap (quote → GV checkin → sign → broadcast) via the swap command. GV checkin is built in — no external binary required. Supports EVM multi-chain and Solana. Includes approve flow for ERC20."
homepage: https://git.fulltrust.link/web3/ai/gate-dex-cli
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🔄",
        "os": ["linux", "darwin"],
        "requires": {
          "bins": ["gate-dex"]
        },
        "install": [
          {
            "id": "download-linux-x64",
            "kind": "download",
            "os": ["linux"],
            "url": "https://gate-dex-cli-test.gateweb3.cc/v1.0.0/gate-dex-linux-x64",
            "bins": ["gate-dex"],
            "label": "Download gate-dex (Linux x64)"
          },
          {
            "id": "download-macos-arm64",
            "kind": "download",
            "os": ["darwin"],
            "url": "https://gate-dex-cli-test.gateweb3.cc/v1.0.0/gate-dex-darwin-arm64",
            "bins": ["gate-dex"],
            "label": "Download gate-dex (macOS arm64)"
          }
        ]
      }
  }
---

# Gate DEX CLI — Swap

> One-shot DEX swap via CLI. GV checkin + sign + broadcast are all built into the `swap` command. No external `tx-checkin` binary needed. Supports EVM and Solana.

## Skill Boundaries

| This skill | Route to other skill |
|-----------|----------------|
| Swap tokens (same-chain) | Auth / login issues → `gate-dex-wallet-cli` |
| Cross-chain bridge | Balance, address, token list → `gate-dex-wallet-cli` |
| Swap quote (preview) | Token transfers (send) → `gate-dex-wallet-cli` |
| Swap / bridge history & order detail | K-line, token info, token security → `gate-dex-market-cli` |
| Swappable & bridge token discovery | — |

---

## Applicable Scenarios

- "Swap ETH for USDT", "exchange tokens", "buy SOL", "convert", "trade"
- Get a swap quote before executing
- View swap history or a specific swap order detail
- List swappable tokens or cross-chain bridge tokens

---

## CLI Commands

### Quote (preview only, no signing)

```bash
# EVM: swap native ETH → USDT on Ethereum (chain_id = 1)
gate-dex quote --from-chain 1 --to-chain 1 --from - --to 0xdAC17F958D2ee523a2206206994597C13D831ec7 --amount 0.01

# EVM: swap USDT → USDC on Arbitrum
gate-dex quote --from-chain 42161 --to-chain 42161 \
  --from 0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9 \
  --to 0xaf88d065e77c8cC2239327C5EDb3A432268e5831 \
  --amount 100

# Solana: swap native SOL → USDC
gate-dex quote --from-chain 501 --to-chain 501 --from - \
  --to EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v --amount 0.1

# Cross-chain bridge: ETH on Ethereum → USDT on Arbitrum
gate-dex quote --from-chain 1 --to-chain 42161 --from - \
  --to 0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9 --amount 0.1 \
  --to-wallet 0xYourArbitrumAddress
```

Returns estimated output amount, price impact, route, and fee. **No signing.**

### One-Shot Swap (quote + GV checkin + sign + broadcast)

```bash
# EVM: swap native ETH → USDT
gate-dex swap --from-chain 1 --to-chain 1 --from - \
  --to 0xdAC17F958D2ee523a2206206994597C13D831ec7 --amount 0.01

# EVM: swap ERC20 with custom slippage
gate-dex swap --from-chain 42161 --to-chain 42161 \
  --from 0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9 \
  --to 0xaf88d065e77c8cC2239327C5EDb3A432268e5831 \
  --amount 100 --slippage 0.005

# Solana: swap SOL → USDC
gate-dex swap --from-chain 501 --to-chain 501 --from - \
  --to EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v --amount 0.05

# Cross-chain bridge: ETH on Ethereum → USDT on Arbitrum
gate-dex swap --from-chain 1 --to-chain 42161 --from - \
  --to 0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9 --amount 0.1 \
  --to-wallet 0xYourArbitrumAddress
```

| Option | Required | Description |
|--------|----------|-------------|
| `--from-chain <id>` | Yes | Source chain ID |
| `--to-chain <id>` | No | Destination chain ID (defaults to same as from-chain) |
| `--from <token>` | Yes | Source token contract; use `-` for native token (ETH/SOL/BNB) |
| `--to <token>` | Yes | Destination token contract |
| `--amount <n>` | Yes | Human-readable input amount |
| `--slippage <n>` | No | Slippage tolerance as decimal (default 0.03 = 3%) |
| `--native-in <0\|1>` | No | `1` if source token is native (ETH/SOL); default `0` |
| `--native-out <0\|1>` | No | `1` if destination token is native; default `0` |
| `--wallet <addr>` | No | Source wallet address (auto-detected from auth) |
| `--to-wallet <addr>` | No | Destination wallet address (required for cross-chain bridge) |

### Swap History

```bash
gate-dex swap-history
```

### Swap Order Detail

```bash
gate-dex swap-detail <order_id>
```

### List Swappable Tokens

```bash
gate-dex swap-tokens
gate-dex swap-tokens --chain eth
gate-dex swap-tokens --chain sol --search USDC
```

Use `--search` to look up a token address by symbol.

### List Cross-Chain Bridge Tokens

```bash
gate-dex bridge-tokens
gate-dex bridge-tokens --src-chain eth --dest-chain arb
```

---

## Internal Flow of `swap` Command

The agent **does not run any of these steps manually** — the CLI handles everything:

```
EVM same-chain flow:
1. Load auth; fetch wallet address
2. Get quote
3. Check if ERC20 approve is needed → auto-approve if needed (GV checkin for approve)
4. Re-quote after approve
5. Build swap transaction
6. GV security checkin (built-in) for swap tx
7. Server-side signing
8. Broadcast
9. Print tx hash + order ID

EVM cross-chain bridge flow (from-chain ≠ to-chain):
1. Load auth; fetch wallet address
2. Get cross-chain bridge quote (--from-chain / --to-chain / --to-wallet required)
3. Check if ERC20 approve is needed on source chain → auto-approve if needed
4. Build bridge transaction on source chain
5. GV security checkin (built-in)
6. Server-side signing
7. Broadcast on source chain
8. Print source tx hash + order ID (destination arrival is async, monitor via swap-detail)

Solana flow:
1. Load auth; fetch Solana address
2. Get quote
3. Build transaction (base64 → base58 conversion handled internally)
4. GV security checkin (built-in, includes priority fee)
5. Server-side signing
6. Broadcast via Solana mainnet RPC
7. Print tx hash + order ID
```

**CRITICAL**: There is no `tx-checkin` binary to run. Do NOT attempt to run a checkin binary before `swap`. The CLI has GV checkin built in.

---

## Chain IDs

| Chain | ID | Native Token |
|-------|----|-------------|
| Ethereum | 1 | ETH |
| BSC | 56 | BNB |
| Polygon | 137 | MATIC |
| Arbitrum | 42161 | ETH |
| Optimism | 10 | ETH |
| Avalanche | 43114 | AVAX |
| Base | 8453 | ETH |
| Solana | 501 | SOL |

**Native token address**: Use `-` as the token address for native tokens (ETH, SOL, BNB, etc.).

---

## Slippage Guidelines

| Token type | Recommended slippage |
|------------|----------------------|
| Stablecoins (USDT ↔ USDC) | 0.005 (0.5%) |
| Major tokens (ETH, BTC, SOL) | 0.01–0.03 (1%–3%) |
| Mid-cap tokens | 0.03 (3%) |
| Meme / low-liquidity tokens | 0.05–0.10 (5%–10%) |

---

## Common Token Addresses

| Chain | USDT | USDC |
|-------|------|------|
| Ethereum (1) | `0xdAC17F958D2ee523a2206206994597C13D831ec7` | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` |
| Arbitrum (42161) | `0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9` | `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` |
| BSC (56) | `0x55d398326f99059fF775485246999027B3197955` | `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d` |
| Solana (501) | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |

---

## Agent Execution Flow

```
Step 1: Auth check
  If not logged in → run gate-dex login

Step 2: Collect parameters
  Required: from-chain, to-chain, from-token, to-token, amount
  Optional: slippage
  If token address unknown → run gate-dex swap-tokens --search <symbol>

Step 3: Get quote (show to user)
  Run: gate-dex quote --from-chain <id> --to-chain <id> --from <token> --to <token> --amount <n>
  Display: estimated output, price impact, route, fee

Step 4: User confirmation in chat (MANDATORY)
  Show: from chain/token/amount → to chain/token, estimated output, slippage
  Wait for explicit "confirm" reply
  - "cancel" → abort
  - "modify" → return to Step 2

Step 5: Execute (after user confirms)
  Run: gate-dex swap --from-chain <id> --to-chain <id> --from <token> --to <token> --amount <n> [--slippage <n>]
  CLI handles GV checkin, signing, and broadcast internally

Step 6: Display result
  Show tx hash + block explorer link + order ID
  Suggest next actions
```

**NEVER run `gate-dex swap` before receiving explicit user confirmation in Step 4.**

---

## Swap Confirmation Template

```
========== Swap Confirmation ==========
From:     {amount} {from_symbol} on {from_chain}
To:       ~{estimated_out} {to_symbol} on {to_chain}
Slippage: {slippage}%
Route:    {route_path}
Fee:      {fee_usd} USD
========================================
Reply "confirm" to execute, "cancel" to abort.
```

---

## Conversation Examples

**Example 1: Swap ETH → USDT on Ethereum**
User: "Swap 0.01 ETH for USDT on Ethereum"
1. `gate-dex quote --from-chain 1 --to-chain 1 --from - --to 0xdAC17... --amount 0.01`
2. Show quote to user; wait for "confirm".
3. `gate-dex swap --from-chain 1 --to-chain 1 --from - --to 0xdAC17... --amount 0.01`
4. Display tx hash + etherscan link + order ID.

**Example 2: Swap SOL → USDC**
User: "Swap 0.1 SOL for USDC"
1. `gate-dex quote --from-chain 501 --to-chain 501 --from - --to EPjFWdd5... --amount 0.1`
2. Show quote; user confirms.
3. `gate-dex swap --from-chain 501 --to-chain 501 --from - --to EPjFWdd5... --amount 0.1`
4. Display tx hash + solscan link.

**Example 3: Unknown token symbol**
User: "Swap 10 USDT for ARB on Arbitrum"
1. `gate-dex swap-tokens --chain arb --search ARB` → get ARB contract address.
2. Proceed with quote and swap using the resolved address.

**Example 4: Cross-chain bridge ETH (Ethereum) → USDT (Arbitrum)**
User: "Bridge 0.1 ETH from Ethereum to USDT on Arbitrum"
1. `gate-dex bridge-tokens --src-chain eth --dest-chain arb` → confirm the token pair is supported.
2. `gate-dex quote --from-chain 1 --to-chain 42161 --from - --to 0xFd086bC7... --amount 0.1 --to-wallet 0xYourAddress`
3. Show quote to user; wait for "confirm".
4. `gate-dex swap --from-chain 1 --to-chain 42161 --from - --to 0xFd086bC7... --amount 0.1 --to-wallet 0xYourAddress`
5. Display source chain tx hash; note that destination arrival is async — user can track via `gate-dex swap-detail <order_id>`.

---

## Error Handling

| Error | Handling |
|-------|----------|
| `Not logged in` | Run `gate-dex login` |
| Insufficient balance | Abort; show shortfall |
| Quote expired | CLI re-quotes automatically before signing |
| Slippage too low | Suggest higher slippage (0.05 for volatile tokens) |
| GV checkin failed (built-in) | CLI displays error; suggest retry |
| Broadcast failed | Display error code; do not auto-retry |
| User cancels | Abort immediately |

---

## Security Rules

1. **Confirm before swap**: Always get explicit user confirmation before running `gate-dex swap`.
2. **Show quote first**: Always run `quote` first so the user can see estimated output.
3. **No tx-checkin binary**: CLI handles GV checkin internally — do not run any external binary.
4. **Audit unfamiliar tokens**: Recommend `gate-dex token-risk` before swapping unknown tokens.
