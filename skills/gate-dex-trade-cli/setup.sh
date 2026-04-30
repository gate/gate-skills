#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
#  Gate Wallet CLI — GateClaw setup script (PROD)
#
#  Runs inside the GateClaw Pod (node user, no sudo, no TTY, idempotent).
#  Downloads the pre-built Linux binary into the GateClaw skills bin dir.
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SKILL_BIN_DIR="/home/node/.openclaw/skills/bin"
BINARY_NAME="gate-dex"

# Version is the source of truth; align with cli/package.json on every release.
VERSION="1.0.0"

DOWNLOAD_URL="https://gate-dex-cli.gateweb3.cc/v${VERSION}/gate-dex-linux-x64"

BIN_PATH="$SKILL_BIN_DIR/$BINARY_NAME"

mkdir -p "$SKILL_BIN_DIR"

# ── Idempotency: skip if same version already installed ──────────────────────
if [ -x "$BIN_PATH" ]; then
  current="$("$BIN_PATH" --version 2>/dev/null | tr -d '[:space:]' || true)"
  if [ "$current" = "$VERSION" ]; then
    echo "[gate-dex-cli] already at v${VERSION}, skipping."
    exit 0
  fi
  echo "[gate-dex-cli] found v${current:-unknown}, upgrading to v${VERSION} ..."
fi

# ── Atomic download: write to temp, chmod, then mv ───────────────────────────
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

echo "[gate-dex-cli] downloading from $DOWNLOAD_URL ..."
curl -fsSL "$DOWNLOAD_URL" -o "$tmp"
chmod +x "$tmp"
mv "$tmp" "$BIN_PATH"

installed="$("$BIN_PATH" --version 2>/dev/null | tr -d '[:space:]' || echo unknown)"
echo "[gate-dex-cli] installed: v${installed} at ${BIN_PATH}"
