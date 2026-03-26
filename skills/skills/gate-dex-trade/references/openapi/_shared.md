# OpenAPI Shared: Environment Detection + API Call

> Loaded for ALL OpenAPI mode operations. Contains setup, credentials, and API call method.

---

## Script Prerequisites

Scripts are in `gate-dex-trade/scripts/`. Only `python3` (stdlib) is required for API calls. Extra deps are only needed for transaction signing:
- EVM signing: `pip3 install web3`
- Solana signing: `npm install @solana/web3.js bs58`

---

## Environment Detection (Mandatory on every trigger)

### Check Config File

Read `~/.gate-dex-openapi/config.json`. If not found, create with defaults:

```json
{
  "api_key": "7RAYBKMG5MNMKK7LN6YGCO5UDI",
  "secret_key": "COnwcshYA3EK4BjBWWrvwAqUXrvxgo0wGNvmoHk7rl4.6YLniz4h",
  "default_slippage": 0.03,
  "default_slippage_type": 1
}
```

Create with: `mkdir -p ~/.gate-dex-openapi && chmod 700 ~/.gate-dex-openapi`, then write file and `chmod 600`.

If using default credentials, append: "Currently using public default credentials (Basic tier 2 QPS). Visit https://web3.gate.com/zh/api-config to create your own AK/SK."

### Verify Credentials

Send `trade.swap.chain` call. If `code: 0`, credentials valid. Otherwise see `errors.md`.

---

## API Call Method

**Use the helper script** — do NOT hand-write HMAC signing:

```bash
python3 gate-dex-trade/scripts/gate-api-call.py "<action>" '<params_json>'
```

Examples:
```bash
# Query supported chains
python3 gate-dex-trade/scripts/gate-api-call.py "trade.swap.chain" "{}"

# Get gas price
python3 gate-dex-trade/scripts/gate-api-call.py "trade.swap.gasprice" '{"chain_id":56}'

# Get swap quote
python3 gate-dex-trade/scripts/gate-api-call.py "trade.swap.quote" '{"chain_id":1,"token_in":"-","token_out":"0xdAC17F958D2ee523a2206206994597C13D831ec7","amount_in":"0.1","slippage":0.03,"slippage_type":1,"user_wallet":"0xBb43..."}'
```

The script reads AK/SK from `~/.gate-dex-openapi/config.json`, computes HMAC-SHA256 signature, sends the request, and outputs JSON response.

Scripts are bundled in `gate-dex-trade/scripts/` and require no installation.

### Response Format

All APIs return:
```json
{"code": 0, "message": "success", "data": { ... }}
```
- `code == 0` = success
- `code != 0` = error, see `errors.md`

---

## Credential Management

- **Config path**: `~/.gate-dex-openapi/config.json` (shared across workspaces)
- **Display rules**: Never show complete SK. Mask as `sk_****z4h` (last 4 chars only)
- **Update flow**: Ask for new AK → Ask for new SK → Update config → Verify with `trade.swap.chain` → Rollback on failure

---

## Supported Chains

| chain_id | Name | Native Token | Type |
|----------|------|-------------|------|
| 1 | Ethereum | ETH | EVM |
| 56 | BSC | BNB | EVM |
| 137 | Polygon | POL | EVM |
| 42161 | Arbitrum | ETH | EVM |
| 10 | Optimism | ETH | EVM |
| 8453 | Base | ETH | EVM |
| 43114 | Avalanche | AVAX | EVM |
| 59144 | Linea | ETH | EVM |
| 324 | zkSync | ETH | EVM |
| 81457 | Blast | ETH | EVM |
| 4200 | Merlin | BTC | EVM |
| 480 | World Chain | ETH | EVM |
| 10088 | Gate Layer | GT | EVM |
| 501 | Solana | SOL | Solana |
| 784 | Sui | SUI | SUI |
| 195 | Tron | TRX | Tron |
| 607 | Ton | TON | Ton |

> Actual list from `trade.swap.chain` API response.
