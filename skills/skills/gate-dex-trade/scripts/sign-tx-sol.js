#!/usr/bin/env node
/**
 * Solana transaction signing.
 * Signs a VersionedTransaction from the Gate DEX build API response.
 *
 * Usage:
 *   echo "<private_key_base58>" | node sign-tx-sol.js '<unsigned_tx_base64>' '<rpc_url>'
 *
 * Input:
 *   unsigned_tx_base64: The base64-encoded transaction from build response
 *   rpc_url: Solana RPC endpoint
 *
 * Output (JSON to stdout):
 *   { "signed_tx_string": "[\"base58_signed_tx\"]", "wallet_address": "..." }
 *
 * Requirements: npm install @solana/web3.js bs58
 */

const { Connection, Keypair, VersionedTransaction } = require("@solana/web3.js");
const bs58 = require("bs58");
const readline = require("readline");

async function main() {
  if (process.argv.length < 4) {
    console.error(
      'Usage: echo "<private_key>" | node sign-tx-sol.js \'<unsigned_tx_base64>\' \'<rpc_url>\''
    );
    process.exit(1);
  }

  const unsignedTxBase64 = process.argv[2];
  const rpcUrl = process.argv[3];

  // Read private key from stdin
  const rl = readline.createInterface({ input: process.stdin });
  const privateKey = await new Promise((resolve) => {
    rl.on("line", (line) => {
      resolve(line.trim());
      rl.close();
    });
  });

  try {
    const keypair = Keypair.fromSecretKey(bs58.decode(privateKey));
    const connection = new Connection(rpcUrl, "confirmed");

    // Deserialize the unsigned transaction
    const txBuffer = Buffer.from(unsignedTxBase64, "base64");
    const tx = VersionedTransaction.deserialize(txBuffer);

    // Refresh blockhash for latest validity
    const { blockhash } = await connection.getLatestBlockhash("confirmed");
    tx.message.recentBlockhash = blockhash;

    // Sign
    tx.sign([keypair]);

    // Encode signed transaction as base58
    const signedBytes = tx.serialize();
    const signedBase58 = bs58.encode(signedBytes);

    // Format as JSON array string (required by Gate submit API)
    const signedTxString = JSON.stringify([signedBase58]);

    console.log(
      JSON.stringify({
        signed_tx_string: signedTxString,
        wallet_address: keypair.publicKey.toBase58(),
      })
    );
  } catch (e) {
    console.log(JSON.stringify({ error: e.message }));
    process.exit(1);
  }
}

main();
