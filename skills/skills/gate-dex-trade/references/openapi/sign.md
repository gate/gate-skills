# OpenAPI: Transaction Signing

> Load after build confirmed. Covers wallet address derivation and multi-chain transaction signing.

---

## Get Wallet Address

Guide user to provide private key, then derive address. **Always display this security notice first**:

```
Security Notice:
Private key is only used locally for signing. It will NOT be uploaded to any server or API.
Private key is discarded after signing — not retained or stored.
```

---

## Sign Unsigned Transaction

### EVM Signing (All EVM Chains)

**Use the helper script** — do NOT hand-write signing code:

```bash
echo "0xPRIVATE_KEY" | python3 gate-dex-trade/scripts/sign-tx-evm.py '<unsigned_tx_json>' '<rpc_url>'
```

Example:
```bash
echo "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80" | \
  python3 gate-dex-trade/scripts/sign-tx-evm.py \
  '{"to":"0x459E945e...","data":"0x140a50ef...","value":"0","gas_limit":314090,"chain_id":1}' \
  'https://eth.llamarpc.com'
```

Output:
```json
{
  "signed_tx_string": "[\"0x02f8b2...\"]",
  "wallet_address": "0xABC...",
  "tx_hash": "0x..."
}
```

The `signed_tx_string` is already in the JSON array format required by the submit API.

**Key**: EVM must use EIP-1559 Type 2 format (starts with `0x02`). Legacy format (`0xf8`/`0xf9`) will be rejected.

**If approve is also needed**: Sign approve first (nonce=N), then swap (nonce=N+1). Run the script twice with appropriate unsigned_tx for each.

Requirements: `pip3 install web3`

### Solana Signing

**Use the helper script**:

```bash
echo "BASE58_PRIVATE_KEY" | node gate-dex-trade/scripts/sign-tx-sol.js '<unsigned_tx_base64>' '<rpc_url>'
```

Output: `{"signed_tx_string": "[\"base58...\"]", "wallet_address": "..."}`

The script automatically refreshes `recentBlockhash` (validity ~60-90s).

Requirements: `npm install @solana/web3.js bs58`

### SUI Signing

For SUI transactions, sign using `@mysten/sui.js`:

- unsigned_tx.data is base64 encoded TransactionBlock
- SUI signature format: flag(1 byte, 0x00) + signature(64 bytes) + pubkey(32 bytes), Base64 encoded
- signed_tx_string format: **JSON array string**, internal elements are Base64 encoded

```javascript
import { Ed25519Keypair } from "@mysten/sui.js/keypairs/ed25519";
import { TransactionBlock } from '@mysten/sui.js/transactions';
import { hexToBytes } from '@noble/hashes/utils';
import { SuiClient } from '@mysten/sui.js/client';

const keypair = Ed25519Keypair.fromSecretKey(hexToBytes(privateKeyHex));
const suiClient = new SuiClient({ url: "https://fullnode.mainnet.sui.io" });
const tx = TransactionBlock.from(Buffer.from(unsignedTxData, 'base64').toString());
tx.setSenderIfNotSet(keypair.toSuiAddress());
const txBytes = await tx.build({ client: suiClient });
const { signature, bytes } = await keypair.signTransactionBlock(txBytes);
const signedTxBase64 = Buffer.from(bytes).toString('base64');

// Key: submit interface requires signed_tx_string to be JSON array format string
const signedTxString = JSON.stringify([signedTxBase64]);  // '["base64..."]'
```

Output format: `signed_tx_string = '["base64_encoded_tx"]'`

Requirements: `npm install @mysten/sui.js @noble/hashes`

### Ton Signing

For Ton transactions, sign using `@ton/ton`:

- unsigned_tx contains `to`, `value`, `data` (contains body and sendMode)
- Need to get seqno via RPC
- signed_tx_string format: **JSON array string**, internal elements are BOC's Base64 encoding

```javascript
import { TonClient, WalletContractV4 } from '@ton/ton';

const publicKey = getPublicKeyFromPrivateKey(privateKeyHex);
const wallet = WalletContractV4.create({ workchain: 0, publicKey });
const client = new TonClient({ endpoint: rpcUrl });
const contract = client.open(wallet);
const seqno = await contract.getSeqno();

const txInfo = {
    messages: [{
        address: unsignedTx.to,
        amount: unsignedTx.value,
        payload: unsignedTx.data?.body,
        sendMode: unsignedTx.data?.sendMode
    }]
};

const transfer = await createTonConnectTransfer(seqno, contract, txInfo, keypair.secretKey);
const bocBase64 = externalMessage(contract, seqno, transfer).toBoc({ idx: false }).toString("base64");

// Key: submit interface requires signed_tx_string to be JSON array format string
const signedTxString = JSON.stringify([bocBase64]);  // '["base64..."]'
```

Output format: `signed_tx_string = '["base64_boc"]'`

Requirements: `npm install @ton/ton`

---

## Critical: signed_tx_string Format

The submit API requires `signed_tx_string` to be a **JSON array format string**:

| Chain | Format | Example |
|-------|--------|---------|
| EVM | Hex in array | `'["0x02f8b2..."]'` |
| Solana | Base58 in array | `'["5K8j..."]'` |
| SUI | Base64 in array | `'["base64..."]'` |
| Ton | Base64 BOC in array | `'["base64..."]'` |

**Raw hex will cause error 50005** (`invalid character 'x' after top-level value`).

---

## Private Key Sources

Agent handles flexibly:
1. Ask user to paste (after showing security notice)
2. Ask for file path (keystore, .env with PRIVATE_KEY)
3. Read from existing workspace files if found

**After signing**: Do NOT retain private key. Prompt user: "Signing complete. Recommend clearing private key from conversation history."
