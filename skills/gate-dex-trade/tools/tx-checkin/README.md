# tx-checkin

HTTP caller for the **swap tx check-in** step: it accepts the JSON shape produced by **`dex_tx_swap_checkin_preview`**, builds the signed POST request, calls the Gate Web3 GV API, and writes the **raw response body** to stdout.

Use this when you have preview JSON (for example from Gate Wallet MCP) and need to run check-in **outside** the MCP runtime—for local debugging, CI, or a custom agent pipeline.

**Gateway (baked into this binary):** `https://api.web3gate.io/api/web/v1/web3-gv-api`. For the **test** GV host, use the `swap-checkin-*` build from your **installed** `gate-dex-trade-test` skill (`<SKILL_ROOT>/tools/tx-checkin/`), not a path inside an unrelated repo.

Only **prebuilt executables** live in this directory (under the **installed** `gate-dex-trade` skill root) alongside this README.

**Agents (staged swap):** Follow the mandatory workflow in **[`references/mcp.md` §4.3.1 Agent canonical check-in procedure](../references/mcp.md)** — preview JSON via **file + `jq -c`** (bash/zsh) or the PowerShell pattern documented there, **`checkin_token` from stdout only**, **no** one-off scripts that reimplement `api-sign`. The Quick start below is for tiny payloads only.

---

## Prebuilt binaries (by platform)

Shipped names in this directory (same flags for all):

| OS | File |
|----|------|
| macOS (`darwin`, Apple Silicon + Intel) | `swap-checkin-mac` |
| Linux (`linux`, amd64) | `swap-checkin-linux` |
| Windows (`windows`, amd64) | `swap-checkin-win.exe` |

Agents and users should run **only** the binary that matches the current machine.

---

## Quick start

Use the copy of this folder under your **installed** `gate-dex-trade` skill (`<SKILL_ROOT>/tools/tx-checkin/`). Either `cd` there or call the binary by full path.

```bash
./swap-checkin-mac --preview-json '{"user_wallet":"0x...","chain":"bsc","chain_category":"ethereum","checkin_message":"..."}'
# or ./swap-checkin-linux / swap-checkin-win.exe with the same flag
```

---

## Credential (`Authorization` header)

Same rules as **gate-dex-wallet** [`references/tx-checkin.md`](../../gate-dex-wallet/references/tx-checkin.md) § Credential: the binary sends the **bare** MCP session token (no `Bearer ` prefix) as HTTP `Authorization`.

| Priority | Source |
|----------|--------|
| 1 | Preview JSON field `mcp_token` (if non-empty after trim; a leading `Bearer ` is stripped). |
| 2 | Environment **`MCP_TOKEN`** (bare token). |
| 3 | **`~/.cursor/mcp.json`**: read `mcpServers.*.headers.Authorization`, strip `Bearer `. Multiple servers: prefer a name matching `gate`, `wallet`, `dex`, or `mcp`; set **`TX_CHECKIN_MCP_SERVER=<key>`** to pick one server entry explicitly. |
| 4 | **`CURSOR_MCP_JSON=/path/to/mcp.json`** instead of the default path above. |

If both preview `mcp_token` and env resolution are empty, the program exits with an error. **Do not paste tokens into chat** — use Cursor MCP config or `MCP_TOKEN` locally.

---

## CLI

| Flag | Required | Description |
|------|----------|-------------|
| `--preview-json` | Yes | Single JSON object string: the serialized preview payload (valid JSON text). |

There are no other flags or positional arguments.

---

## Input: preview JSON

Pass the **full** object you get from `dex_tx_swap_checkin_preview`, serialized to one line (or minified JSON). The program unmarshals it into the following fields.

### Required (validated)

| Field | Role |
|-------|------|
| `user_wallet` | Mapped to request body `wallet_address`. |
| `chain` | Request body `chain`. |
| `checkin_message` | Request body `message`. |

### Optional

| Field | Role |
|-------|------|
| `mcp_token` | If set, used as `Authorization` (see **Credential**). If omitted or empty, the binary resolves the token from **`MCP_TOKEN`** / **`~/.cursor/mcp.json`** like gate-dex-wallet `tx-checkin`. |
| `chain_category` | Request body `chain_category` (may be empty if omitted). |
| `type` | Request body `type` (omitted in JSON if empty after trim). |
| `checkin_path` | HTTP path (must start with `/`). If empty, `/api/v1/tx/checkin` is used. |

---

## HTTP request (what the binary sends)

- **Method:** `POST`
- **URL:** `{defaultGatewayBaseURL}{checkin_path or /api/v1/tx/checkin}`  
  Example path: `/api/v1/tx/checkin`
- **Headers:**
  - `Content-Type`: `application/json; charset=utf-8`
  - `api-timestamp`: Unix seconds (set by the binary)
  - `api-code`: random positive 31-bit integer (set by the binary)
  - `api-sign`: HMAC-less digest derived from method, path+query, body, timestamp, and `api-code` (see below)
  - `Authorization`: resolved **Credential** (preview `mcp_token` or env / `mcp.json`)
- **Body:** JSON object

```json
{
  "wallet_address": "<user_wallet>",
  "chain": "<chain>",
  "chain_category": "<chain_category>",
  "message": "<checkin_message>",
  "type": "<type if non-empty>",
  "source": 3
}
```

`source` is always **`3`** (AI agent) in this binary.

---

## Signing (`api-sign`)

The binary computes:

1. `encodedPath` — path segments path-escaped; query string re-encoded with `url.Values.Encode()` when a `?` is present.
2. `bodyForSign` — the exact JSON string used as the request body, or `{}` if it would be empty after trim.
3. Preimage: `METHOD|encodedPath|bodyForSign|api-timestamp|api-code` (method uppercased).
4. `api-sign` = hex encoding of the **last 8 bytes** of `SHA256(preimage)`.

This matches the gateway’s expectations for the Web3 GV check-in route.

---

## Output

- **Success:** stdout is the **full response body** from the server (typically JSON). A trailing newline is ensured.
- **Failure:** stderr is a single JSON line: `{"ok":false,"error":"..."}`.

Non-zero exit codes:

| Code | Typical cause |
|------|----------------|
| `1` | Missing/invalid `--preview-json`, JSON parse error, or missing required preview fields |
| `2` | Internal error (marshal, signing path encode, stdout write, etc.) |
| `3` | HTTP or network error talking to the gateway |

---

## Example success response

Shape depends on the API version; stdout is passed through unchanged. For example:

```json
{"code":0,"msg":"success","data":{"checkin_token":"...","need_otp":false}}
```

---

## Security notes

- Treat `mcp_token` like a secret: avoid logging full `--preview-json` in shared terminals or CI artifacts.
- The binary does not store tokens; it only forwards them in the `Authorization` header.

---

## See also

- Parent index: [../README.md](../README.md)
- Test gateway copy: `gate-dex-trade-test/tools/tx-checkin/`
