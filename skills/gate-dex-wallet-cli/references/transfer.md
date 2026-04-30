---
name: gate-dex-wallet-cli-transfer
version: "2026.4.23-2"
updated: "2026-04-23"
description: "gate-wallet CLI transfer module. Preview-only (transfer), one-shot send, send-tx (with --hex broadcast), sol-tx (build Solana unsigned tx), sign-msg (sign 32-byte hex), sign-tx (sign raw tx), and gas estimation. GV security checkin is built in — no external binary required. Supports EVM (ERC20 + native) and Solana (SOL + SPL)."
---

# Gate Wallet CLI — Transfer

> Transfer module — gas estimation, preview, and one-shot send (GV checkin + sign + broadcast built-in). No external `tx-checkin` binary needed.

## Applicable Scenarios

- "Send ETH to 0x...", "transfer USDT", "pay someone", "move tokens"
- "Send SOL to BTYz...", "transfer SPL token"
- Preview transfer without executing
- Estimate gas fees
- Sign a 32-byte hex message (EVM or Solana)
- Sign a raw unsigned transaction hex
- Build a Solana unsigned transfer tx locally
- Broadcast a pre-signed transaction hex

---

## CLI Commands

### Preview Only (no signing)

```bash
gate-wallet transfer --chain ETH --to 0xRecipient --amount 1.0
gate-wallet transfer --chain ETH --to 0xRecipient --amount 100 --token 0xdAC17F958D2ee523a2206206994597C13D831ec7
```

Returns: estimated gas, unsigned tx details, confirm message. **Does not sign or broadcast.**

| Option | Required | Description |
|--------|----------|-------------|
| `--chain <name>` | Yes | Chain name (ETH, ARB, SOL, etc.) |
| `--to <address>` | Yes | Recipient address |
| `--amount <n>` | Yes | Human-readable amount (e.g., `0.1`, `100`) |
| `--token <contract>` | No | ERC20/SPL contract address; omit for native token |

### One-Shot Send (preview + GV checkin + sign + broadcast)

```bash
# Native token
gate-wallet send --chain ETH --to 0xRecipient --amount 0.1

# ERC20 token
gate-wallet send --chain ARB --to 0xRecipient --amount 100 \
  --token 0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9

# ERC20 with explicit decimals + symbol (optional, for display)
gate-wallet send --chain ETH --to 0xRecipient --amount 100 \
  --token 0xdAC17F958D2ee523a2206206994597C13D831ec7 \
  --token-decimals 6 --token-symbol USDT

# Solana native SOL
gate-wallet send --chain SOL --to BTYzG...bfxE --amount 0.1

# Solana SPL token
gate-wallet send --chain SOL --to BTYzG...bfxE --amount 50 \
  --token Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB \
  --token-decimals 6 --token-symbol USDT
```

| Option | Required | Description |
|--------|----------|-------------|
| `--chain <name>` | Yes | Chain name (ETH, ARB, BSC, SOL, etc.) |
| `--to <address>` | Yes | Recipient address |
| `--amount <n>` | Yes | Human-readable amount |
| `--token <contract>` | No | ERC20/SPL contract; omit for native token |
| `--token-decimals <d>` | No | Token decimals (auto-resolved if omitted) |
| `--token-symbol <sym>` | No | Display symbol (optional, for logging) |

### Gas Estimation

```bash
gate-wallet gas            # query ETH gas (default)
gate-wallet gas ETH        # specific chain gas price
gate-wallet gas SOL
gate-wallet gas ARB --from 0xFrom --to 0xTo  # include gas limit estimate
```

Alias support: `ARB`→`ARBITRUM`, `OP`→`OPTIMISM`, `AVAX`→`AVALANCHE`, `MATIC`→`POLYGON`.

| Option | Description |
|--------|-------------|
| `[chain]` | Chain name (positional or `--chain`) |
| `--from <addr>` | Sender address (required for gas limit) |
| `--to <addr>` | Recipient address (required for gas limit) |
| `--value <hex>` | Value in hex (optional) |
| `--data <data>` | Calldata hex / SOL base64 (optional) |

### sign-msg — Sign 32-byte Message

```bash
gate-wallet sign-msg <64-hex-chars> --chain ETH
gate-wallet sign-msg aabbcc...00 --chain SOL
```

`<message>` must be exactly 64 hex characters (32 bytes). GV security checkin is performed automatically. If OTP is required, the CLI prompts interactively — **do not run in non-interactive agent mode without user at keyboard**.

| Option | Default |
|--------|---------|
| `--chain <name>` | ETH |

### sign-tx — Sign Raw Transaction

```bash
gate-wallet sign-tx <raw_tx_hex> --chain ETH
gate-wallet sign-tx <raw_tx_hex> --chain ETH --to 0xAddr --amount 0.1 --token ETH
```

Signs an existing unsigned transaction hex. GV checkin built-in.

| Option | Default | Description |
|--------|---------|-------------|
| `--chain <name>` | ETH | Chain name |
| `--to <address>` | — | Recipient (used for GV intent display) |
| `--amount <n>` | — | Amount (used for GV intent display) |
| `--token <sym>` | same as chain | Token symbol (used for GV intent display) |

### send-tx — Build + Sign + Broadcast (or Broadcast Pre-signed)

```bash
# Full flow: build unsigned tx, GV checkin, sign, broadcast
gate-wallet send-tx --chain ETH --to 0xAddr --amount 0.1 --token ETH

# Broadcast a pre-signed transaction directly (skip build+sign)
gate-wallet send-tx --chain ETH --hex 0x02f8...
```

Identical to `send` in the happy path, but also supports `--hex` to broadcast an already-signed transaction without going through preview/sign steps.

| Option | Required | Description |
|--------|----------|-------------|
| `--chain <name>` | Yes | Chain name |
| `--to <address>` | Yes (unless `--hex`) | Recipient address |
| `--amount <n>` | Yes (unless `--hex`) | Human-readable amount |
| `--token <sym>` | No | Token symbol (e.g. ETH, USDT) |
| `--address <from>` | No | Sender address (auto-detected) |
| `--hex <signed_tx>` | No | Pre-signed tx hex — skip build+sign, broadcast directly |
| `--token-contract <addr>` | No | ERC20 contract address |

### sol-tx — Build Solana Unsigned Transfer Tx

```bash
gate-wallet sol-tx --to <sol_address> --amount 0.5
gate-wallet sol-tx --to <sol_address> --amount 0.5 --from <sender> --priority-fee 1000
```

Builds a native SOL transfer transaction locally using the latest blockhash from the network. Returns the unsigned transaction (base64/hex) — useful if you need to sign it separately.

| Option | Required | Description |
|--------|----------|-------------|
| `--to <address>` | Yes | Recipient Solana address |
| `--amount <n>` | Yes | Amount in SOL |
| `--from <address>` | No | Sender address (auto-detected from auth) |
| `--priority-fee <n>` | No | Priority fee in micro-lamports per CU |

---

## Internal Flow of `send` Command

The agent **does not need** to run any of these steps manually — the CLI handles them all:

```
1. Load auth from ~/.gate-wallet/auth.json
2. Display transfer preview (chain, from, to, amount, estimated gas)
3. GV security checkin (txCheckin API) — built-in, no external binary
4. Server-side signing
5. Broadcast to on-chain network
6. Print tx hash
```

**CRITICAL**: There is no `tx-checkin` binary to run. Do NOT attempt to run a checkin binary before `send`. The CLI has GV checkin built in.

---

## Agent Execution Flow

```
Step 1: Auth check
  If ~/.gate-wallet/auth.json missing → route to auth.md

Step 2: Collect parameters
  Required: to_address, amount, chain
  Optional: token contract address, token decimals, token symbol
  If chain not specified → default to Ethereum; optionally confirm with user

Step 3: Estimate balance (optional but recommended)
  Run: gate-wallet tokens --chain <CHAIN>
  Verify: token balance >= amount; native balance >= estimated gas

Step 4: Preview (optional but recommended for ERC20 / large amounts)
  Run: gate-wallet transfer --chain <c> --to <addr> --amount <n> [--token <addr>]
  Display preview to user

Step 5: User confirmation in chat (MANDATORY)
  Show: chain, from address, to address, amount, token
  Wait for explicit "confirm" reply before proceeding
  - "cancel" → abort; no transaction is sent
  - "modify" → return to Step 2

Step 6: Execute (after user confirms)
  Run: gate-wallet send --chain <c> --to <addr> --amount <n> [--token <addr>] [--token-decimals <d>] [--token-symbol <sym>]
  CLI handles GV checkin, signing, and broadcast internally

Step 7: Display result
  Show tx hash from CLI output + block explorer link
  Proactively suggest next actions
```

**NEVER run `gate-wallet send` before receiving explicit user confirmation in Step 5.**

---

## Confirmation Template

Before running `send`, display this confirmation to the user in chat:

```
========== Transfer Confirmation ==========
Chain:      {chain_name}
From:       {from_address}
To:         {to_address}
Amount:     {amount} {symbol}
Token:      {contract_address or "native"}
Gas (est.): ~{estimated_gas} {gas_symbol}
===========================================
Reply "confirm" to execute, "cancel" to abort.
```

---

## Address Formats

| Chain | Format | Example |
|-------|--------|---------|
| EVM (eth/bsc/arb/...) | `0x` + 40 hex (42 chars) | `0xdAC17F958D2ee523a2206206994597C13D831ec7` |
| Solana | Base58, 32–44 chars | `BTYzGSzMYpH4VoYRHRRv2mALEEqB3AhPJa6bfxE` |

Validation failure → reject with correct format guidance.

---

## Chain Reference

| Chain Name | Chain ID | Gas Token | Block Explorer |
|------------|----------|-----------|----------------|
| `eth` | 1 | ETH | etherscan.io |
| `bsc` | 56 | BNB | bscscan.com |
| `polygon` | 137 | MATIC | polygonscan.com |
| `arbitrum` / `arb` | 42161 | ETH | arbiscan.io |
| `optimism` / `op` | 10 | ETH | optimistic.etherscan.io |
| `avax` | 43114 | AVAX | snowtrace.io |
| `base` | 8453 | ETH | basescan.org |
| `sol` | 501 | SOL | solscan.io |

---

## Common Stablecoin Addresses

| Chain | USDT | USDC |
|-------|------|------|
| Ethereum | `0xdAC17F958D2ee523a2206206994597C13D831ec7` | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` |
| Arbitrum | `0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9` | `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` |
| BSC | `0x55d398326f99059fF775485246999027B3197955` | `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d` |
| Solana | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |

---

## Conversation Examples

**Example 1 (Happy Path): Send ETH**
User: "Send 0.1 ETH to 0xDEF...5678"
Agent:
1. Check auth; get `evm_address` from `gate-wallet address`.
2. Run `gate-wallet tokens --chain ETH` to verify ETH >= 0.1 + gas.
3. Show confirmation: chain ETH, from own EVM address, to `0xDEF...5678`, amount 0.1 ETH.
4. User replies "confirm".
5. Run `gate-wallet send --chain ETH --to 0xDEF...5678 --amount 0.1`.
6. Display tx hash + etherscan link.

**Example 2 (Happy Path): Send USDT on Arbitrum**
User: "Send 100 USDT to 0xABC...1234 on Arbitrum"
Agent:
1. Check auth.
2. Run `gate-wallet tokens --chain ARB` → verify USDT >= 100 AND ETH (gas) balance.
3. Show confirmation template with ERC20 contract address.
4. User confirms → run `gate-wallet send --chain ARB --to 0xABC... --amount 100 --token 0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9`.
5. Display tx hash + arbiscan link.

**Example 3 (Happy Path): Send SOL**
User: "Send 0.5 SOL to BTYz...bfxE"
Agent:
1. Get Solana address from `gate-wallet address` → `sol_address`.
2. Check `gate-wallet tokens --chain SOL` → SOL balance >= 0.5 + gas.
3. Confirm with user → run `gate-wallet send --chain SOL --to BTYz...bfxE --amount 0.5`.
4. Display tx hash + solscan link.

**Example 4 (Edge Case): Insufficient balance**
User: "Send 1000 USDT on Ethereum"
Agent:
1. Check token balance → USDT is 800.
2. Abort: "Insufficient USDT balance. You have 800 USDT but need 1000. Please reduce the amount or top up first."

---

## Post-Transfer Suggestions

```
Transfer broadcast successfully!
Tx Hash: {hash}
Explorer: https://{explorer}/tx/{hash}

You can:
- Check updated balance: gate-wallet balance
- View transaction: gate-wallet tx-detail {hash}
- Make another transfer
- Swap tokens
```

---

## Error Handling

| Error | Handling |
|-------|----------|
| `Not logged in` | Route to auth.md |
| Insufficient token balance | Abort; show shortfall; suggest top-up or smaller amount |
| Insufficient gas | Abort; show gas shortfall; suggest acquiring gas token |
| Invalid recipient address | Reject; show correct format |
| Same sender/recipient | Warn user; ask confirmation of intent |
| GV checkin failed (built-in) | CLI displays error; suggest retry |
| Broadcast failed | CLI displays error with code; do not auto-retry |
| User cancels | Abort immediately; no transaction is sent |

---

## Security Rules

1. **Confirm before send**: Always get explicit user confirmation in chat before running `gate-wallet send`.
2. **Preview recommended**: Run `gate-wallet transfer` first for unfamiliar tokens or large amounts.
3. **No tx-checkin binary**: Do not run any external checkin binary — it is not needed.
4. **Address validation**: Validate recipient format before execution.
5. **No auto-retry**: On failure, display the error; do not retry automatically.
