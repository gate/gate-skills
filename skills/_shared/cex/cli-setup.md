# Gate CLI Setup

Use the official [Gate CLI project](https://github.com/gate/gate-cli) and its [public releases](https://github.com/gate/gate-cli/releases). Follow the project README for current platform support and installation instructions. Do not require an internal repository, development branch, private artifact or company network.

## Reuse or install

Reuse a trusted working installation. Resolve its path and record its version:

```bash
# Inspect the selected executable without a business API call.
command -v gate-cli
gate-cli version
```

If absent from PATH, check `~/.local/bin/gate-cli` and `~/.openclaw/skills/bin/gate-cli`. Verify the selected executable and use the same absolute path throughout the task.

An existing trusted installation may report `dev`, including a local source build. That label alone is not a reason to reject it, require a release version, reinstall, or upgrade. Continue with the capability check below and the normal authentication, permission, and authorization checks. Public-release installation guidance applies when installation or an approved update is actually needed; it does not disqualify an existing trusted `dev` binary.

If installation is needed:

1. Select a public release and its asset for the host OS/architecture. Download the asset and `checksums.txt` from that same release over HTTPS.
2. Verify the asset's SHA-256 against its exact filename in `checksums.txt`, using `shasum -a 256` or `sha256sum`. Stop on a mismatch or missing checksum; extract only the verified asset.
3. On macOS/Linux, install the extracted executable as follows. On Windows, use the official project instructions for the verified Windows asset.

```bash
# Install the already verified executable for this machine's architecture.
install -d "$HOME/.local/bin"
install -m 755 ./gate-cli "$HOME/.local/bin/gate-cli"
"$HOME/.local/bin/gate-cli" version
```

4. Use that absolute path, or add the directory through the user's approved PATH setup. Do not automatically overwrite an existing executable or edit shell startup files.

Source builds, when explicitly needed, must follow the official project's default-branch build instructions and declared toolchain/dependencies. Record actual provenance for the task; this skill prescribes no branch, commit or minimum version. Do not fetch a private build to restore a missing capability.

## Capability check

Read the exact required leaf's `--help` on the trusted installation. Check command path, flags, required inputs, output options and authentication support against the selected reference. A project README, version string or locally documented action is not proof that the installed release supports it.

If a command, parameter or authentication method is absent or differs materially, stop that operation and report the mismatch. An explicitly authorized update must still use an official public release. Do not invent flags, switch to an internal checkout, silently change credentials or fall back to direct API/SDK calls.

## API environment

The default public API origin is `https://api.gateio.ws`. The CLI appends `/api/v4`; do not include that suffix or a trailing slash in the base origin. Reuse an explicitly selected profile only after verifying its effective origin. `GATE_BASE_URL` overrides the profile origin; record the effective value without exposing credentials.

Use another origin only when the user explicitly selects an officially supported environment and its matching credentials. Do not embed an internal test address or send credentials to an unverified host. Never silently change environments after a failure.

An API-origin override does not change the OAuth issuer or establish a matching resource/grant. Installation does not establish API access. Continue with [authentication](cli-auth.md) only when private access is required.
