#!/usr/bin/env bash
# Trigger update for one skill: compare remote vs local (version/updated), then clone+copy if needed.
# Compatibility: Bash (macOS/Linux; Windows: Git Bash / WSL). HTTP: curl first (macOS has curl by default), else wget.
# Prefers git; then ZIP+unzip; then tar.gz+tar (no unzip).
# Run with full/all permissions in sandboxed agents (e.g. Cursor) for git clone / network.
# Usage:
#   ./scripts/update-skill.sh run   <NAME>          # check → optional clone/ZIP → copy (DEST auto-derived)
#   ./scripts/update-skill.sh check <NAME>          # compare only, no download (see GATE_SKILL_UPDATE_MODE)
#   ./scripts/update-skill.sh apply <NAME>          # clone or ZIP + copy only
#   ./scripts/update-skill.sh run   <DEST> <NAME>   # legacy: explicit DEST
#
#   GATE_SKILL_UPDATE_MODE=auto — if check sees a newer remote version, apply immediately (no confirm token).
#   Without auto: optional GATE_SKILL_CHECK_STRICT=1 on check → exit 3 + two-step GATE_SKILL_CONFIRM_TOKEN for apply/run.

set -euo pipefail

REMOTE_RAW="https://raw.githubusercontent.com/gate/gate-skills/master/skills"
REPO="https://github.com/gate/gate-skills.git"
ZIP_URL="https://github.com/gate/gate-skills/archive/refs/heads/master.zip"
TAR_GZ_URL="https://github.com/gate/gate-skills/archive/refs/heads/master.tar.gz"
FETCH_REMOTE_ERR=""

# ── Colors ──────────────────────────────────────────────────────
C_RESET='\033[0m'
C_BOLD='\033[1m'
C_GREEN='\033[32m'
C_YELLOW='\033[33m'
C_RED='\033[31m'
C_CYAN='\033[36m'
C_DIM='\033[2m'

log_info()    { printf "${C_CYAN}[info]${C_RESET}  %s\n" "$*"; }
log_step()    { printf "${C_BOLD}${C_CYAN}▶${C_RESET} %s\n" "$*"; }
log_ok()      { printf "${C_GREEN}[✔ ok]${C_RESET}  %s\n" "$*"; }
log_skip()    { printf "${C_YELLOW}[skip]${C_RESET}  %s\n" "$*"; }
log_warn()    { printf "${C_YELLOW}[warn]${C_RESET}  %s\n" "$*"; }
log_fail()    { printf "${C_RED}[FAIL]${C_RESET}  %s\n" "$*"; }
log_result()  { printf "${C_BOLD}→ Result=${C_GREEN}%s${C_RESET}\n" "$1"; }
log_result_y(){ printf "${C_BOLD}→ Result=${C_YELLOW}%s${C_RESET}\n" "$1"; }
log_result_r(){ printf "${C_BOLD}→ Result=${C_RED}%s${C_RESET}\n" "$1"; }
log_dim()     { printf "${C_DIM}  %s${C_RESET}\n" "$*"; }

# One line for agents to parse from check stdout (no colors). BLOCK = ask user before skill Execution.
emit_gate_skill_agent_action() {
  printf 'GATE_SKILL_UPDATE_AGENT_ACTION=%s\n' "$1"
}

gate_skill_is_auto_mode() {
  case "${GATE_SKILL_UPDATE_MODE:-}" in
    auto|AUTO|1|true|TRUE|yes|YES) return 0 ;;
  esac
  return 1
}

# Pending apply token: strict `check` + update_available writes `.gate-skill-apply-token`;
# `apply` / `run` require GATE_SKILL_CONFIRM_TOKEN to match until success or `revoke-pending`.
gate_skill_apply_token_path() {
  printf '%s/.gate-skill-apply-token\n' "$1"
}

gate_skill_remove_apply_token() {
  rm -f "$(gate_skill_apply_token_path "$1")" 2>/dev/null || true
}

gate_skill_write_apply_token() {
  local DEST="$1" TOKEN="$2"
  local f
  f="$(gate_skill_apply_token_path "$DEST")"
  printf '%s\n' "$TOKEN" >"$f"
  chmod 600 "$f" 2>/dev/null || true
}

gate_skill_gen_token() {
  if command -v openssl >/dev/null 2>&1; then
    openssl rand -hex 16 2>/dev/null && return 0
  fi
  LC_ALL=C tr -dc 'a-f0-9' </dev/urandom 2>/dev/null | head -c 32
}

require_apply_token_if_pending() {
  local DEST="$1" f expected got
  if gate_skill_is_auto_mode; then
    return 0
  fi
  f="$(gate_skill_apply_token_path "$DEST")"
  [ -f "$f" ] || return 0
  expected="$(tr -d '\r\n' <"$f")"
  got="${GATE_SKILL_CONFIRM_TOKEN:-}"
  if [ -z "$got" ] || [ "$got" != "$expected" ]; then
    log_fail "apply blocked: run strict check first, then set GATE_SKILL_CONFIRM_TOKEN (from check output), or: $0 revoke-pending <NAME>"
    log_result_r "failure"
    echo "Trigger update: Result=failure; missing or wrong GATE_SKILL_CONFIRM_TOKEN (two-step gate)"
    return 2
  fi
  return 0
}

# ── Helpers ─────────────────────────────────────────────────────

usage() {
  echo "Usage: $0 run   <NAME>          # check → optional clone/ZIP → copy"
  echo "       $0 check <NAME>          # compare only, no download"
  echo "       $0 apply <NAME>          # clone or ZIP + copy only"
  echo "       $0 revoke-pending <NAME> # clear strict apply token (user declined)"
  echo "  Single-arg DEST: ~/.cursor/skills/<NAME>, ~/.codex/skills/<NAME>, ~/.openclaw/skills/<NAME>, ~/.agents/skills/<NAME>, ~/.gemini/antigravity/skills/<NAME> if SKILL.md exists (in that order), else script dir (scripts/../)."
  echo "  Legacy: $0 run <DEST> <NAME>  # explicit DEST still supported"
  echo "  Two-arg: canonical order is DEST (skill root) then NAME; reversed order is fixed when only one path has SKILL.md."
  exit 1
}

derive_dest() {
  local script_path
  script_path="$(cd "$(dirname "$0")" && pwd)"
  printf '%s\n' "$(cd "$script_path/.." && pwd)"
}

# Single-arg check/run/apply: compare & overwrite $DEST/SKILL.md. Prefer known agent install roots when
# SKILL.md exists (Cursor, Codex, OpenClaw, cross-IDE .agents, Antigravity global), else script dir (monorepo).
resolve_dest_single_arg() {
  local NAME="$1"
  local script_dest candidate
  script_dest="$(derive_dest)"
  local candidates=(
    "$HOME/.cursor/skills/$NAME"
    "$HOME/.codex/skills/$NAME"
    "$HOME/.openclaw/skills/$NAME"
    "$HOME/.agents/skills/$NAME"
    "$HOME/.gemini/antigravity/skills/$NAME"
  )
  for candidate in "${candidates[@]}"; do
    [ -f "$candidate/SKILL.md" ] || continue
    if [ "$script_dest" = "$candidate" ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  for candidate in "${candidates[@]}"; do
    if [ -f "$candidate/SKILL.md" ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  printf '%s\n' "$script_dest"
}

normalize_dest() {
  local d="$1" abs
  case "$d" in
    /*) printf '%s\n' "$d" ;;
    *)
      abs="$(cd -P "$(dirname "$d")" && pwd)/$(basename "$d")"
      printf '%s\n' "$abs"
      ;;
  esac
}

# Two-arg check/run/apply/revoke expect DEST then NAME. If agents pass NAME then DEST,
# detect via SKILL.md under normalized paths and swap.
resolve_dest_two_arg() {
  local a1 a2
  a1=$(normalize_dest "$1")
  a2=$(normalize_dest "$2")
  if [ -f "$a1/SKILL.md" ]; then
    printf '%s\n%s\n' "$a1" "$2"
    return 0
  fi
  if [ -f "$a2/SKILL.md" ]; then
    printf '%s\n%s\n' "$a2" "$1"
    return 0
  fi
  printf '%s\n%s\n' "$a1" "$2"
}

choose_tmp_base() {
  local DEST="$1" try
  try="$(dirname "$DEST")"
  try="$(cd "$try/../.." 2>/dev/null && pwd)" || try=""
  if [ -n "$try" ] && mkdir -p "$try/.tmp" 2>/dev/null && [ -w "$try/.tmp" ]; then
    printf '%s\n' "$try/.tmp"
    return
  fi
  mkdir -p "${TMPDIR:-/tmp}"
  printf '%s\n' "${TMPDIR:-/tmp}"
}

fetch_remote_skill_head() {
  local url="$1" out="$2" tmp err reason
  FETCH_REMOTE_ERR=""
  tmp="${TMPDIR:-/tmp}/update-skill-head-$$.txt"
  if command -v curl >/dev/null 2>&1; then
    log_dim "fetching via curl …"
    if ! err=$(curl -sfL "$url" -o "$tmp" 2>&1); then
      reason=$(printf '%s' "$err" | tr '
' ' ' | sed 's/[[:space:]]\+/ /g; s/^ //; s/ $//')
      FETCH_REMOTE_ERR="curl: ${reason:-unknown error}"
      rm -f "$tmp"
      return 1
    fi
    head -40 "$tmp" >"$out"
    rm -f "$tmp"
    return 0
  fi
  if command -v wget >/dev/null 2>&1; then
    log_dim "fetching via wget …"
    if ! err=$(wget -qO "$tmp" "$url" 2>&1); then
      reason=$(printf '%s' "$err" | tr '
' ' ' | sed 's/[[:space:]]\+/ /g; s/^ //; s/ $//')
      FETCH_REMOTE_ERR="wget: ${reason:-unknown error}"
      rm -f "$tmp"
      return 1
    fi
    head -40 "$tmp" >"$out"
    rm -f "$tmp"
    return 0
  fi
  FETCH_REMOTE_ERR="neither curl nor wget found in PATH"
  return 1
}

yaml_val() {
  local key="$1" file="$2"
  grep -m1 "^${key}:" "$file" 2>/dev/null | sed "s/^${key}:[[:space:]]*//; s/^[\"']//; s/[\"']\$//" | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
}

# One line per phase for logs / tooling (stdout, no color). Spaces in values unlikely; keep simple.
gate_skill_log_version_check() {
  local name="$1" rv="$2" uv="$3" lv="$4" lu="$5"
  local line="GATE_SKILL_VERSION_LOG phase=check name=${name} remote_version=${rv} remote_updated=${uv} local_version=${lv} local_updated=${lu}"
  log_info "$line"
  printf '%s\n' "$line"
}

gate_skill_log_version_after_apply() {
  local DEST="$1"
  local nv nu nm line
  nv=$(yaml_val version "$DEST/SKILL.md")
  nu=$(yaml_val updated "$DEST/SKILL.md")
  nm=$(yaml_val name "$DEST/SKILL.md")
  [ -n "$nm" ] || nm="unknown"
  line="GATE_SKILL_VERSION_LOG phase=after_apply name=${nm} local_version=${nv} local_updated=${nu} DEST=${DEST}"
  log_info "$line"
  printf '%s\n' "$line"
}

verify_and_finish() {
  local DEST="$1"
  if [ -f "$DEST/SKILL.md" ]; then
    gate_skill_remove_apply_token "$DEST"
    log_ok "overwrite complete — DEST=$DEST"
    gate_skill_log_version_after_apply "$DEST"
    log_result "success"
    echo "Trigger update: Result=success; Overwrite OK; DEST=$DEST"
    return 0
  fi
  log_fail "DEST/SKILL.md missing after copy"
  log_result_r "failure"
  echo "Trigger update: Result=failure; DEST/SKILL.md missing after copy"
  return 1
}

download_file() {
  local url="$1" dest="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -sfL -o "$dest" "$url" && return 0
  fi
  if command -v wget >/dev/null 2>&1; then
    wget -qO "$dest" "$url" && return 0
  fi
  return 1
}

copy_skill_from_src() {
  local SRC="$1" DEST="$2" NAME="$3"
  if [ ! -f "$SRC/skills/$NAME/SKILL.md" ]; then
    rm -rf "$SRC" 2>/dev/null || true
    return 1
  fi
  log_info "copying skills/$NAME/ → $DEST/"
  cp -r "$SRC/skills/$NAME/." "$DEST/"
  rm -rf "$SRC" 2>/dev/null || true
  verify_and_finish "$DEST"
}

# ── Apply ───────────────────────────────────────────────────────

do_apply() {
  local DEST="$1" NAME="$2"
  local BASE TS CLONE_DIR ok=0 SRC

  BASE=$(choose_tmp_base "$DEST")
  TS=$(date +%s)
  CLONE_DIR="$BASE/gate-skills-clone-$TS"
  SRC="$BASE/gate-skills-master"

  mkdir -p "$DEST" "$BASE"
  rm -rf "$CLONE_DIR" 2>/dev/null || true

  # ── Strategy 1: git clone ──
  log_step "Strategy 1: git clone"
  if command -v git >/dev/null 2>&1; then
    log_info "git found — cloning $REPO"
    if git clone --depth 1 "$REPO" "$CLONE_DIR" 2>/dev/null; then ok=1
    else
      log_warn "first clone attempt failed, retrying …"
      rm -rf "$CLONE_DIR" 2>/dev/null || true
      git clone --depth 1 "$REPO" "$CLONE_DIR" 2>/dev/null && ok=1 || true
    fi
  else
    log_dim "git not found, skipping"
  fi

  if [ "$ok" -eq 1 ] && [ -f "$CLONE_DIR/skills/$NAME/SKILL.md" ]; then
    log_ok "git clone succeeded"
    log_info "copying skills/$NAME/ → $DEST/"
    cp -r "$CLONE_DIR/skills/$NAME/." "$DEST/"
    rm -rf "$CLONE_DIR" 2>/dev/null || true
    verify_and_finish "$DEST"
    return $?
  fi
  rm -rf "$CLONE_DIR" 2>/dev/null || true
  [ "$ok" -eq 1 ] && log_warn "clone ok but skills/$NAME/SKILL.md not found"

  if ! command -v curl >/dev/null 2>&1 && ! command -v wget >/dev/null 2>&1; then
    log_fail "no git, no curl, no wget — cannot download"
    log_result_r "failure"
    echo "Trigger update: Result=failure; need git, or curl/wget for archive download"
    return 1
  fi

  rm -rf "$SRC" 2>/dev/null || true

  # ── Strategy 2: ZIP + unzip ──
  log_step "Strategy 2: ZIP + unzip"
  if command -v unzip >/dev/null 2>&1; then
    local ZIP="$BASE/gate-skills-$TS.zip"
    rm -f "$ZIP" 2>/dev/null || true
    log_info "downloading master.zip …"
    if download_file "$ZIP_URL" "$ZIP"; then
      log_ok "download complete"
      log_info "extracting with unzip …"
      if unzip -o -q "$ZIP" -d "$BASE" 2>/dev/null; then
        log_ok "unzip succeeded"
        rm -f "$ZIP" 2>/dev/null || true
        if copy_skill_from_src "$SRC" "$DEST" "$NAME"; then return 0; fi
        log_warn "skill directory not found in ZIP"
      else
        log_warn "unzip failed"
        rm -f "$ZIP" 2>/dev/null || true
      fi
    else
      log_warn "ZIP download failed"
    fi
    rm -rf "$SRC" 2>/dev/null || true
  else
    log_dim "unzip not found, skipping"
  fi

  # ── Strategy 3: tar.gz + tar ──
  log_step "Strategy 3: tar.gz + tar"
  rm -rf "$SRC" 2>/dev/null || true
  if command -v tar >/dev/null 2>&1; then
    local TAR_GZ="$BASE/gate-skills-$TS.tar.gz"
    rm -f "$TAR_GZ" 2>/dev/null || true
    log_info "downloading master.tar.gz …"
    if download_file "$TAR_GZ_URL" "$TAR_GZ"; then
      log_ok "download complete"
      log_info "extracting with tar …"
      if tar -xzf "$TAR_GZ" -C "$BASE" 2>/dev/null; then
        log_ok "tar extract succeeded"
        rm -f "$TAR_GZ" 2>/dev/null || true
        if copy_skill_from_src "$SRC" "$DEST" "$NAME"; then return 0; fi
        log_warn "skill directory not found in tar.gz"
      else
        log_warn "tar extract failed"
        rm -f "$TAR_GZ" 2>/dev/null || true
      fi
    else
      log_warn "tar.gz download failed"
    fi
    rm -rf "$SRC" 2>/dev/null || true
  else
    log_dim "tar not found, skipping"
  fi

  log_fail "all strategies exhausted"
  log_result_r "failure"
  echo "Trigger update: Result=failure; need git, or (curl/wget)+unzip, or (curl/wget)+tar for .tar.gz"
  return 1
}

# ── Check (compare only) ───────────────────────────────────────

cmd_check() {
  local DEST NAME
  if [ $# -eq 2 ]; then
    exec 3< <(resolve_dest_two_arg "$1" "$2")
    IFS= read -r DEST <&3
    IFS= read -r NAME <&3
    exec 3<&-
  else
    NAME="${1:?}"
    DEST=$(resolve_dest_single_arg "$NAME")
  fi
  local LOCAL="$DEST/SKILL.md"

  log_step "check: comparing remote vs local version"
  log_dim "DEST=$DEST  NAME=$NAME"

  if [ ! -f "$LOCAL" ]; then
    log_fail "local SKILL.md not found: $LOCAL"
    log_result_r "check_failed"
    echo "Trigger update: Result=check_failed; missing $LOCAL"
    emit_gate_skill_agent_action CONTINUE_SKILL_EXECUTION
    return 1
  fi

  local rf
  rf=$(mktemp "${TMPDIR:-/tmp}/gate-skills-remote.XXXXXX")
  trap "rm -f '$rf'" RETURN

  local remote_url
  remote_url="${REMOTE_RAW}/${NAME}/SKILL.md"
  log_info "fetching remote SKILL.md frontmatter …"
  if ! fetch_remote_skill_head "$remote_url" "$rf"; then
    log_warn "remote fetch failed (url=$remote_url; reason=${FETCH_REMOTE_ERR:-unknown})"
    log_result_y "check_failed"
    echo "Trigger update: Result=check_failed; remote fetch failed; url=$remote_url; reason=${FETCH_REMOTE_ERR:-unknown}"
    emit_gate_skill_agent_action CONTINUE_SKILL_EXECUTION
    return 0
  fi
  if ! grep -qE '^version:' "$rf"; then
    log_warn "remote SKILL.md has no version field"
    log_result_y "check_failed"
    echo "Trigger update: Result=check_failed; remote SKILL.md unreadable"
    emit_gate_skill_agent_action CONTINUE_SKILL_EXECUTION
    return 0
  fi
  log_ok "remote frontmatter fetched"

  local rv uv lv lu
  rv=$(yaml_val version "$rf")
  uv=$(yaml_val updated "$rf")
  lv=$(yaml_val version "$LOCAL")
  lu=$(yaml_val updated "$LOCAL")

  log_info "remote  version=$rv  updated=$uv"
  log_info "local   version=$lv  updated=$lu"
  gate_skill_log_version_check "$NAME" "$rv" "$uv" "$lv" "$lu"

  if [ -n "$rv" ] && [ "$rv" = "$lv" ] && [ -n "$uv" ] && [ "$uv" = "$lu" ]; then
    gate_skill_remove_apply_token "$DEST"
    log_skip "versions match — no update needed"
    log_result "skipped"
    echo "Trigger update: Result=skipped; version and updated unchanged"
    emit_gate_skill_agent_action CONTINUE_SKILL_EXECUTION
    return 0
  fi

  log_warn "version mismatch — update available"
  log_result_y "update_available"
  echo "Trigger update: Result=update_available; remote version=$rv updated=$uv vs local version=$lv updated=$lu"
  if gate_skill_is_auto_mode; then
    gate_skill_remove_apply_token "$DEST"
    log_info "GATE_SKILL_UPDATE_MODE=auto — applying update immediately (no user confirmation; logs only)"
    emit_gate_skill_agent_action CONTINUE_SKILL_EXECUTION
    printf '%s\n' 'GATE_SKILL_AUTO_APPLY=1'
    do_apply "$DEST" "$NAME" || return $?
    return 0
  fi
  emit_gate_skill_agent_action BLOCK_UNTIL_USER_CONFIRMS_UPDATE
  case "${GATE_SKILL_CHECK_STRICT:-}" in
    1|true|TRUE|yes|YES)
      tok="$(gate_skill_gen_token)"
      [ -n "$tok" ] || tok="$(date +%s)$RANDOM"
      gate_skill_write_apply_token "$DEST" "$tok"
      printf '%s\n' "GATE_SKILL_CONFIRM_TOKEN=$tok"
      printf '%s\n' 'GATE_SKILL_TWO_STEP_GATE=1 (export token above for apply after user confirms)'
      printf '%s\n' 'GATE_SKILL_CHECK_EXIT=3 (strict: user must confirm before apply; not a script crash)'
      return 3
      ;;
  esac
  return 0
}

# ── Run (check + auto apply) ───────────────────────────────────

cmd_run() {
  local DEST NAME
  if [ $# -eq 2 ]; then
    exec 3< <(resolve_dest_two_arg "$1" "$2")
    IFS= read -r DEST <&3
    IFS= read -r NAME <&3
    exec 3<&-
  else
    NAME="${1:?}"
    DEST=$(resolve_dest_single_arg "$NAME")
  fi
  local LOCAL="$DEST/SKILL.md"

  log_step "run: check + auto apply"
  log_dim "DEST=$DEST  NAME=$NAME"

  if [ ! -f "$LOCAL" ]; then
    log_fail "local SKILL.md not found: $LOCAL"
    log_result_r "failure"
    echo "Trigger update: Result=failure; missing $LOCAL"
    return 1
  fi

  local rf
  rf=$(mktemp "${TMPDIR:-/tmp}/gate-skills-remote.XXXXXX")
  trap "rm -f '$rf'" RETURN

  local remote_url
  remote_url="${REMOTE_RAW}/${NAME}/SKILL.md"
  log_info "fetching remote SKILL.md frontmatter …"
  if ! fetch_remote_skill_head "$remote_url" "$rf"; then
    log_warn "remote fetch failed — skipping apply (url=$remote_url; reason=${FETCH_REMOTE_ERR:-unknown})"
    log_result_y "check_failed"
    echo "Trigger update: Result=check_failed; remote fetch failed; url=$remote_url; reason=${FETCH_REMOTE_ERR:-unknown}; skipping apply (Execution may proceed)"
    return 0
  fi
  if ! grep -qE '^version:' "$rf"; then
    log_warn "remote SKILL.md unreadable — skipping apply"
    log_result_y "check_failed"
    echo "Trigger update: Result=check_failed; remote SKILL.md unreadable; skipping apply (Execution may proceed)"
    return 0
  fi
  log_ok "remote frontmatter fetched"

  local rv uv lv lu
  rv=$(yaml_val version "$rf")
  uv=$(yaml_val updated "$rf")
  lv=$(yaml_val version "$LOCAL")
  lu=$(yaml_val updated "$LOCAL")

  log_info "remote  version=$rv  updated=$uv"
  log_info "local   version=$lv  updated=$lu"
  gate_skill_log_version_check "$NAME" "$rv" "$uv" "$lv" "$lu"

  if [ -n "$rv" ] && [ "$rv" = "$lv" ] && [ -n "$uv" ] && [ "$uv" = "$lu" ]; then
    log_skip "versions match — no update needed"
    log_result "skipped"
    echo "Trigger update: Result=skipped; version and updated unchanged"
    return 0
  fi

  log_warn "version mismatch — applying update …"
  echo "Trigger update: remote differs (remote version=$rv updated=$uv vs local version=$lv updated=$lu); applying..."
  require_apply_token_if_pending "$DEST" || return $?
  do_apply "$DEST" "$NAME" || return 1
}

# ── Main ────────────────────────────────────────────────────────

main() {
  # Legacy 2-arg: <DEST> <NAME> → run
  if [ $# -eq 2 ] && [[ "${1:-}" != run && "${1:-}" != check && "${1:-}" != apply && "${1:-}" != revoke-pending ]]; then
    local __leg_d __leg_n
    exec 3< <(resolve_dest_two_arg "$1" "$2")
    IFS= read -r __leg_d <&3
    IFS= read -r __leg_n <&3
    exec 3<&-
    cmd_run "$__leg_d" "$__leg_n"
    return $?
  fi
  # 1-arg (no subcommand): <NAME> → run with auto DEST
  if [ $# -eq 1 ] && [[ "${1:-}" != run && "${1:-}" != check && "${1:-}" != apply && "${1:-}" != revoke-pending && "${1:-}" != -h && "${1:-}" != --help && "${1:-}" != help ]]; then
    cmd_run "$1"
    return $?
  fi
  case "${1:-}" in
    run)
      shift
      [ $# -ge 1 ] || usage
      cmd_run "$@"
      ;;
    check)
      shift
      [ $# -ge 1 ] || usage
      cmd_check "$@"
      ;;
    apply)
      shift
      [ $# -ge 1 ] || usage
      local DEST NAME
      if [ $# -eq 2 ]; then
        exec 3< <(resolve_dest_two_arg "$1" "$2")
        IFS= read -r DEST <&3
        IFS= read -r NAME <&3
        exec 3<&-
      else
        NAME="${1:?}"
        DEST=$(resolve_dest_single_arg "$NAME")
      fi
      log_step "apply: force download and overwrite"
      log_dim "DEST=$DEST  NAME=$NAME"
      require_apply_token_if_pending "$DEST" || exit $?
      do_apply "$DEST" "$NAME"
      ;;
    revoke-pending)
      shift
      [ $# -ge 1 ] || usage
      local rn_DEST rn_NAME
      if [ $# -eq 2 ]; then
        exec 3< <(resolve_dest_two_arg "$1" "$2")
        IFS= read -r rn_DEST <&3
        IFS= read -r rn_NAME <&3
        exec 3<&-
      else
        rn_NAME="${1:?}"
        rn_DEST=$(resolve_dest_single_arg "$rn_NAME")
      fi
      gate_skill_remove_apply_token "$rn_DEST"
      log_ok "revoke-pending: cleared apply token — DEST=$rn_DEST"
      echo "Trigger update: Result=revoke_pending_ok"
      ;;
    -h|--help|help) usage ;;
    *) usage ;;
  esac
}

main "$@"
exit $?
