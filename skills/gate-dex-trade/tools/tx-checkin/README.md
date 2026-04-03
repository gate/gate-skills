# tx-checkin

Trade swap check-in caller.

This directory exposes a Go binary that reads the JSON returned by
`dex_tx_swap_checkin_preview`, sends the tx check-in HTTP request, and prints
the full response body to stdout.

## Usage

Use the prebuilt binary from this directory:

```bash
./swap-checkin-mac --help
# Linux: ./swap-checkin-linux --help
```

The binary only accepts command-line JSON input:

```bash
./swap-checkin-mac --preview-json '{"mcp_token":"...","user_wallet":"0x123","chain":"ethereum","chain_category":"evm","checkin_message":"...","type":"swap"}'
# Linux: ./swap-checkin-linux with the same --preview-json value
```

```powershell
# Windows (amd64): from this directory
.\swap-checkin-win.exe --preview-json '{"mcp_token":"...","user_wallet":"0x123","chain":"ethereum","chain_category":"evm","checkin_message":"...","type":"swap"}'
```

## Input Format

`--preview-json` must be a standard JSON string, not a Go struct literal.

In other words, the caller should take the full result returned by
`dex_tx_swap_checkin_preview`, serialize it to JSON text, and pass that string
into this binary. The binary will unmarshal that JSON, build the check-in
request, call the API, and print the raw response body.

## Output

Stdout is the full tx check-in response body, for example:

```json
{"code":0,"msg":"success","data":{"checkin_token":"...","need_otp":false}}
```

## Required Fields

The preview payload must contain:

- `mcp_token`
- `user_wallet`
- `chain`
- `chain_category`
- `checkin_message`

## Notes

- The only CLI input is `--preview-json`.
- Use `swap-checkin-mac` on macOS, `swap-checkin-linux` on Linux, and `swap-checkin-win.exe` on Windows (amd64).
- `checkin_path` from preview is preferred when present; otherwise `/api/v1/tx/checkin` is used.
- `mcp_token` is used directly as the `Authorization` header value; the binary does not add a `Bearer ` prefix.
- `api-timestamp` and `api-code` are generated internally by the binary.
- The request body includes `source: 3`.
