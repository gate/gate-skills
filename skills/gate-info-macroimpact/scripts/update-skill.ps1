#requires -Version 5.1
<#
  Trigger update for one skill on Windows without Git (built-in PowerShell + Invoke-WebRequest).
  Compares remote vs local version/updated; if differ: git clone, else ZIP+Expand-Archive, else tar.gz+tar (same order as update-skill.sh).

  Single-arg DEST: %USERPROFILE%\.cursor|\codex|\openclaw|\agents|...\skills\<NAME> if SKILL.md exists (same order as .sh), else script dir (scripts\..).
  Usage:
    powershell -ExecutionPolicy Bypass -File .\scripts\update-skill.ps1 run   "<NAME>"
    powershell -ExecutionPolicy Bypass -File .\scripts\update-skill.ps1 check "<NAME>"
    powershell -ExecutionPolicy Bypass -File .\scripts\update-skill.ps1 apply "<NAME>"
  Legacy (explicit DEST):
    powershell -ExecutionPolicy Bypass -File .\scripts\update-skill.ps1 run "<DEST>" "<NAME>"

  Use the host-approved sandbox permissions when needed.

  GATE_SKILL_UPDATE_MODE=auto — check applies newer remote without confirm token; apply/run skip token gate.
  Without auto: optional GATE_SKILL_CHECK_STRICT=1 on check → exit 3 + GATE_SKILL_CONFIRM_TOKEN for apply/run.
#>

$ErrorActionPreference = 'Stop'

$RemoteRaw = 'https://raw.githubusercontent.com/gate/gate-skills/master/skills'
$RepoGit   = 'https://github.com/gate/gate-skills.git'
$RepoZip   = 'https://github.com/gate/gate-skills/archive/refs/heads/master.zip'
$RepoTarGz = 'https://github.com/gate/gate-skills/archive/refs/heads/master.tar.gz'

# ── Logging ─────────────────────────────────────────────────────

function Log-Info   ([string]$Msg) { Write-Host "[info]  $Msg" -ForegroundColor Cyan }
function Log-Step   ([string]$Msg) { Write-Host "▶ $Msg" -ForegroundColor Cyan }
function Log-Ok     ([string]$Msg) { Write-Host "[✔ ok]  $Msg" -ForegroundColor Green }
function Log-Skip   ([string]$Msg) { Write-Host "[skip]  $Msg" -ForegroundColor Yellow }
function Log-Warn   ([string]$Msg) { Write-Host "[warn]  $Msg" -ForegroundColor Yellow }
function Log-Fail   ([string]$Msg) { Write-Host "[FAIL]  $Msg" -ForegroundColor Red }
function Log-Dim    ([string]$Msg) { Write-Host "  $Msg" -ForegroundColor DarkGray }

function Log-Result ([string]$Status, [string]$Color = 'Green') {
  Write-Host -NoNewline '→ Result='
  Write-Host $Status -ForegroundColor $Color
}

# ── Helpers ─────────────────────────────────────────────────────

function Show-Usage {
  Write-Host 'Usage: update-skill.ps1 run   <NAME>          # check -> clone or ZIP -> copy'
  Write-Host '       update-skill.ps1 check <NAME>          # compare only, no download'
  Write-Host '       update-skill.ps1 apply <NAME>          # clone or ZIP -> copy only'
  Write-Host '       update-skill.ps1 revoke-pending <NAME> # clear strict apply token'
  Write-Host '  Single-arg DEST: %USERPROFILE%\.cursor|\.codex|\.openclaw|\.agents|... \skills\<NAME> if SKILL.md exists (same order as update-skill.sh), else script dir (scripts\..).'
  Write-Host '  Legacy: update-skill.ps1 run <DEST> <NAME>  # explicit DEST still supported'
  Write-Host '  Two-arg: canonical order is DEST (skill root) then NAME; reversed order is fixed when only one path has SKILL.md.'
  exit 1
}

function Derive-Dest {
  $scriptDir = Split-Path -Parent $PSCommandPath
  return (Resolve-Path -LiteralPath (Join-Path $scriptDir '..')).Path
}

function Get-UserHomeDir {
  if ($env:USERPROFILE) { return $env:USERPROFILE }
  return [Environment]::GetFolderPath('UserProfile')
}

function Path-Equal([string]$A, [string]$B) {
  return [string]::Equals($A, $B, [System.StringComparison]::OrdinalIgnoreCase)
}

# Mirrors update-skill.sh resolve_dest_single_arg (Cursor, Codex, OpenClaw, .agents, Antigravity).
function Resolve-DestSingleArg([string]$Name) {
  $homeDir = Get-UserHomeDir
  $scriptDest = Derive-Dest
  $candidates = @(
    (Join-Path $homeDir (Join-Path '.cursor' (Join-Path 'skills' $Name)))
    (Join-Path $homeDir (Join-Path '.codex' (Join-Path 'skills' $Name)))
    (Join-Path $homeDir (Join-Path '.openclaw' (Join-Path 'skills' $Name)))
    (Join-Path $homeDir (Join-Path '.agents' (Join-Path 'skills' $Name)))
    (Join-Path $homeDir (Join-Path '.gemini' (Join-Path 'antigravity' (Join-Path 'skills' $Name))))
  )
  $canonScript = $scriptDest
  try { $canonScript = (Resolve-Path -LiteralPath $scriptDest).Path } catch { }

  foreach ($c in $candidates) {
    $md = Join-Path $c 'SKILL.md'
    if (-not (Test-Path -LiteralPath $md)) { continue }
    $canonC = $c
    try { $canonC = (Resolve-Path -LiteralPath $c).Path } catch {}
    if (Path-Equal $canonC $canonScript) { return $canonC }
  }
  foreach ($c in $candidates) {
    $md = Join-Path $c 'SKILL.md'
    if (Test-Path -LiteralPath $md) {
      return (Resolve-Path -LiteralPath $c).Path
    }
  }
  return $scriptDest
}

function Emit-GateSkillAgentAction([string]$Value) {
  Write-Output "GATE_SKILL_UPDATE_AGENT_ACTION=$Value"
}

function Test-GateSkillAutoMode {
  $m = $env:GATE_SKILL_UPDATE_MODE
  return ($m -eq 'auto' -or $m -eq 'AUTO' -or $m -eq '1' -or $m -eq 'true' -or $m -eq 'TRUE' -or $m -eq 'yes' -or $m -eq 'YES')
}

function Get-ApplyTokenPath([string]$Dest) {
  return (Join-Path $Dest '.gate-skill-apply-token')
}

function Remove-ApplyToken([string]$Dest) {
  $p = Get-ApplyTokenPath $Dest
  if (Test-Path -LiteralPath $p) {
    Remove-Item -LiteralPath $p -Force -ErrorAction SilentlyContinue
  }
}

function Write-ApplyToken([string]$Dest, [string]$Token) {
  [System.IO.File]::WriteAllText((Get-ApplyTokenPath $Dest), $Token)
}

function New-ApplyTokenString() {
  return [Guid]::NewGuid().ToString('N')
}

function Assert-ApplyTokenIfPending([string]$Dest) {
  if (Test-GateSkillAutoMode) { return }
  $p = Get-ApplyTokenPath $Dest
  if (-not (Test-Path -LiteralPath $p)) { return }
  $expected = ([System.IO.File]::ReadAllText($p)).Trim().TrimEnd([char]0xFEFF)
  $expected = $expected -replace "`r", '' -replace "`n", ''
  $got = $env:GATE_SKILL_CONFIRM_TOKEN
  if ([string]::IsNullOrWhiteSpace($got) -or $got -ne $expected) {
    Log-Fail 'apply blocked: run strict check first, set GATE_SKILL_CONFIRM_TOKEN from check output, or: update-skill.ps1 revoke-pending <NAME>'
    Log-Result 'failure' 'Red'
    Write-Host 'Trigger update: Result=failure; missing or wrong GATE_SKILL_CONFIRM_TOKEN (two-step gate)'
    exit 2
  }
}

function Normalize-Dest([string]$Path) {
  if (Test-Path -LiteralPath $Path) {
    return (Resolve-Path -LiteralPath $Path).Path
  }
  if ([System.IO.Path]::IsPathRooted($Path)) {
    return [System.IO.Path]::GetFullPath($Path)
  }
  return [System.IO.Path]::GetFullPath((Join-Path (Get-Location).Path $Path))
}

# Two-arg check/run/apply/revoke expect DEST then NAME; swap when only the path arg has SKILL.md (same as update-skill.sh).
function Resolve-DestTwoArg {
  param([string]$Raw1, [string]$Raw2)
  $a1 = Normalize-Dest $Raw1
  $a2 = Normalize-Dest $Raw2
  $sk1 = Join-Path $a1 'SKILL.md'
  $sk2 = Join-Path $a2 'SKILL.md'
  if (Test-Path -LiteralPath $sk1) {
    return [PSCustomObject]@{ Dest = $a1; Name = $Raw2 }
  }
  if (Test-Path -LiteralPath $sk2) {
    return [PSCustomObject]@{ Dest = $a2; Name = $Raw1 }
  }
  return [PSCustomObject]@{ Dest = $a1; Name = $Raw2 }
}

function Get-FallbackTmpDir {
  # Mirrors: mkdir -p "${TMPDIR:-/tmp}"; printf '%s\n' "${TMPDIR:-/tmp}"
  $fb = if (-not [string]::IsNullOrWhiteSpace($env:TMPDIR)) { $env:TMPDIR } elseif (-not [string]::IsNullOrWhiteSpace($env:TEMP)) { $env:TEMP } else { '/tmp' }
  try { New-Item -ItemType Directory -Force -Path $fb | Out-Null } catch { }
  return $fb
}

function Get-TmpBase([string]$Dest) {
  # Mirrors update-skill.sh choose_tmp_base: try="$(dirname "$DEST")"; try="$(cd "$try/../.." && pwd)";
  # then mkdir -p "$try/.tmp" && [ -w "$try/.tmp" ] or else fallback TMPDIR.
  $parent = Split-Path -Parent $Dest
  if ([string]::IsNullOrWhiteSpace($parent)) { return Get-FallbackTmpDir }

  $combined = [System.IO.Path]::Combine($parent, '..', '..')
  $tryTwoUp = $null
  try {
    $tryTwoUp = (Resolve-Path -LiteralPath $combined -ErrorAction Stop).Path
  } catch {
    try { $tryTwoUp = [System.IO.Path]::GetFullPath($combined) } catch { return Get-FallbackTmpDir }
  }
  if ([string]::IsNullOrWhiteSpace($tryTwoUp)) { return Get-FallbackTmpDir }

  $dotTmp = Join-Path $tryTwoUp '.tmp'
  try { New-Item -ItemType Directory -Force -Path $dotTmp | Out-Null } catch { return Get-FallbackTmpDir }
  if (-not (Test-Path -LiteralPath $dotTmp -PathType Container)) { return Get-FallbackTmpDir }
  try {
    $probe = Join-Path $dotTmp ('.gate-skills-w-' + [Guid]::NewGuid().ToString('N'))
    [System.IO.File]::WriteAllText($probe, '')
    Remove-Item -LiteralPath $probe -Force
  } catch { return Get-FallbackTmpDir }

  return $dotTmp
}

function Get-YamlField([string]$Key, [string]$FilePath) {
  if (-not (Test-Path -LiteralPath $FilePath)) { return '' }
  $lines = Get-Content -LiteralPath $FilePath -Encoding UTF8 -TotalCount 60 -ErrorAction SilentlyContinue
  foreach ($line in $lines) {
    if ($line -match ("^" + [regex]::Escape($Key) + ":\s*(.+)$")) {
      $v = $Matches[1].Trim() -replace '^"', '' -replace '"$', '' -replace "^'", '' -replace "'$", ''
      return $v.Trim()
    }
  }
  return ''
}

function Get-YamlFieldFromText([string]$Key, [string]$Text) {
  foreach ($line in ($Text -split "`r?`n")) {
    if ($line -match ("^" + [regex]::Escape($Key) + ":\s*(.+)$")) {
      $v = $Matches[1].Trim() -replace '^"', '' -replace '"$', '' -replace "^'", '' -replace "'$", ''
      return $v.Trim()
    }
  }
  return ''
}

function Write-GateSkillVersionLogCheck([string]$Name, [string]$Rv, [string]$Uv, [string]$Lv, [string]$Lu) {
  $line = "GATE_SKILL_VERSION_LOG phase=check name=$Name remote_version=$Rv remote_updated=$Uv local_version=$Lv local_updated=$Lu"
  Log-Info $line
  Write-Host $line
}

function Write-GateSkillVersionLogAfterApply([string]$Dest) {
  $md = Join-Path $Dest 'SKILL.md'
  if (-not (Test-Path -LiteralPath $md)) { return }
  $nv = Get-YamlField 'version' $md
  $nu = Get-YamlField 'updated' $md
  $nn = Get-YamlField 'name' $md
  if ([string]::IsNullOrWhiteSpace($nn)) { $nn = 'unknown' }
  $line = "GATE_SKILL_VERSION_LOG phase=after_apply name=$nn local_version=$nv local_updated=$nu DEST=$Dest"
  Log-Info $line
  Write-Host $line
}

# ── Apply ───────────────────────────────────────────────────────

function Invoke-Apply {
  param([string]$Dest, [string]$Name)

  $base = Get-TmpBase $Dest
  $ts = [int64]([DateTimeOffset]::UtcNow.ToUnixTimeSeconds())
  $cloneDir = Join-Path $base "gate-skills-clone-$ts"

  New-Item -ItemType Directory -Force -Path $Dest | Out-Null
  New-Item -ItemType Directory -Force -Path $base | Out-Null

  Assert-ApplyTokenIfPending $Dest

  # ── Strategy 1: git clone ──
  Log-Step 'Strategy 1: git clone'
  $usedGit = $false
  if (Get-Command git -ErrorAction SilentlyContinue) {
    Log-Info "git found — cloning $RepoGit"
    try {
      Remove-Item -LiteralPath $cloneDir -Recurse -Force -ErrorAction SilentlyContinue
      & git clone --depth 1 $RepoGit $cloneDir 2>$null
      if ((Test-Path -LiteralPath (Join-Path $cloneDir (Join-Path 'skills' (Join-Path $Name 'SKILL.md'))))) {
        $usedGit = $true
        Log-Ok 'git clone succeeded'
      }
    } catch {
      Log-Warn "git clone failed: $($_.Exception.Message)"
    }
  } else {
    Log-Dim 'git not found, skipping'
  }

  if ($usedGit) {
    Log-Info "copying skills/$Name/ → $Dest/"
    $skillSrcGit = Join-Path $cloneDir (Join-Path 'skills' $Name)
    Copy-Item -Path (Join-Path $skillSrcGit '*') -Destination $Dest -Recurse -Force
    Remove-Item -LiteralPath $cloneDir -Recurse -Force -ErrorAction SilentlyContinue
    if (Test-Path -LiteralPath (Join-Path $Dest 'SKILL.md')) {
      Remove-ApplyToken $Dest
      Log-Ok "sync complete — DEST=$Dest"
      Write-GateSkillVersionLogAfterApply $Dest
      Log-Result 'success'
      Write-Host "Trigger update: Result=success; Overwrite OK; DEST=$Dest"
      return
    }
    throw 'Copy after git failed'
  }

  Remove-Item -LiteralPath $cloneDir -Recurse -Force -ErrorAction SilentlyContinue

  # ── Strategy 2: ZIP + Expand-Archive ──
  Log-Step 'Strategy 2: ZIP + Expand-Archive'
  $zipPath = Join-Path $base "gate-skills-$ts.zip"
  $extractRoot = Join-Path $base "gate-skills-extract-$ts"
  $srcRoot = Join-Path $extractRoot 'gate-skills-master'
  Remove-Item -LiteralPath $zipPath -Force -ErrorAction SilentlyContinue
  Remove-Item -LiteralPath $extractRoot -Recurse -Force -ErrorAction SilentlyContinue

  $zipOk = $false
  try {
    Log-Info 'downloading master.zip …'
    Invoke-WebRequest -Uri $RepoZip -OutFile $zipPath -UseBasicParsing
    Log-Ok 'download complete'
    Log-Info 'extracting with Expand-Archive …'
    New-Item -ItemType Directory -Force -Path $extractRoot | Out-Null
    Expand-Archive -LiteralPath $zipPath -DestinationPath $extractRoot -Force
    $skillSrc = Join-Path $srcRoot (Join-Path 'skills' $Name)
    if (Test-Path -LiteralPath (Join-Path $skillSrc 'SKILL.md')) {
      Log-Ok 'unzip succeeded'
      Log-Info "copying skills/$Name/ → $Dest/"
      Copy-Item -Path (Join-Path $skillSrc '*') -Destination $Dest -Recurse -Force
      $zipOk = $true
    } else {
      Log-Warn "skill directory not found in ZIP"
    }
  } catch {
    Log-Warn "ZIP strategy failed: $($_.Exception.Message)"
    $zipOk = $false
  } finally {
    Remove-Item -LiteralPath $zipPath -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $extractRoot -Recurse -Force -ErrorAction SilentlyContinue
  }

  if ($zipOk -and (Test-Path -LiteralPath (Join-Path $Dest 'SKILL.md'))) {
    Remove-ApplyToken $Dest
    Log-Ok "sync complete — DEST=$Dest"
    Write-GateSkillVersionLogAfterApply $Dest
    Log-Result 'success'
    Write-Host "Trigger update: Result=success; Overwrite OK; DEST=$Dest"
    return
  }

  # ── Strategy 3: tar.gz + tar ──
  Log-Step 'Strategy 3: tar.gz + tar'
  $tarPath = Join-Path $base "gate-skills-$ts.tar.gz"
  $extractTar = Join-Path $base "gate-skills-extract-tar-$ts"
  $srcTar = Join-Path $extractTar 'gate-skills-master'
  Remove-Item -LiteralPath $tarPath -Force -ErrorAction SilentlyContinue
  Remove-Item -LiteralPath $extractTar -Recurse -Force -ErrorAction SilentlyContinue

  if (-not (Get-Command tar -ErrorAction SilentlyContinue)) {
    Log-Fail 'ZIP failed and tar.exe not found for .tar.gz fallback'
    Log-Result 'failure' 'Red'
    Write-Host 'Trigger update: Result=failure; ZIP path failed and tar.exe not found for .tar.gz fallback'
    exit 1
  }

  $tarOk = $false
  try {
    Log-Info 'downloading master.tar.gz …'
    Invoke-WebRequest -Uri $RepoTarGz -OutFile $tarPath -UseBasicParsing
    Log-Ok 'download complete'
    Log-Info 'extracting with tar …'
    New-Item -ItemType Directory -Force -Path $extractTar | Out-Null
    & tar -xzf $tarPath -C $extractTar
    $skillSrc = Join-Path $srcTar (Join-Path 'skills' $Name)
    if (Test-Path -LiteralPath (Join-Path $skillSrc 'SKILL.md')) {
      Log-Ok 'tar extract succeeded'
      Log-Info "copying skills/$Name/ → $Dest/"
      Copy-Item -Path (Join-Path $skillSrc '*') -Destination $Dest -Recurse -Force
      $tarOk = $true
    } else {
      Log-Warn 'skill directory not found in tar.gz'
    }
  } catch {
    Log-Warn "tar.gz strategy failed: $($_.Exception.Message)"
    $tarOk = $false
  } finally {
    Remove-Item -LiteralPath $tarPath -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $extractTar -Recurse -Force -ErrorAction SilentlyContinue
  }

  if ($tarOk -and (Test-Path -LiteralPath (Join-Path $Dest 'SKILL.md'))) {
    Remove-ApplyToken $Dest
    Log-Ok "sync complete — DEST=$Dest"
    Write-GateSkillVersionLogAfterApply $Dest
    Log-Result 'success'
    Write-Host "Trigger update: Result=success; Overwrite OK; DEST=$Dest"
    return
  }

  Log-Fail 'all strategies exhausted'
  Log-Result 'failure' 'Red'
  Write-Host 'Trigger update: Result=failure; need git, or (curl/wget)+unzip, or (curl/wget)+tar for .tar.gz'
  exit 1
}

# ── Check (compare only) ───────────────────────────────────────

function Invoke-Check {
  param([string]$Dest = '', [string]$Name)

  if (-not [string]::IsNullOrWhiteSpace($Dest) -and -not [string]::IsNullOrWhiteSpace($Name)) {
    $pair = Resolve-DestTwoArg -Raw1 $Dest -Raw2 $Name
    $Dest = $pair.Dest
    $Name = $pair.Name
  } elseif ([string]::IsNullOrWhiteSpace($Dest)) {
    $Dest = Resolve-DestSingleArg -Name $Name
  }
  $Dest = Normalize-Dest $Dest
  $localMd = Join-Path $Dest 'SKILL.md'

  Log-Step 'check: comparing remote vs local version'
  Log-Dim "DEST=$Dest  NAME=$Name"

  if (-not (Test-Path -LiteralPath $localMd)) {
    Log-Fail "local SKILL.md not found: $localMd"
    Log-Result 'check_failed' 'Red'
    Write-Host "Trigger update: Result=check_failed; missing $localMd"
    Emit-GateSkillAgentAction 'CONTINUE_SKILL_EXECUTION'
    exit 1
  }

  $url = "$RemoteRaw/$Name/SKILL.md"
  Log-Info 'fetching remote SKILL.md frontmatter …'
  try {
    $resp = Invoke-WebRequest -Uri $url -UseBasicParsing
    $head = ($resp.Content -split "`r?`n")[0..39] -join "`n"
  } catch {
    $reason = ''
    try { $reason = (($_.Exception.Message) -replace '\s+', ' ').Trim() } catch { $reason = 'unknown error' }
    if ([string]::IsNullOrWhiteSpace($reason)) { $reason = 'unknown error' }
    Log-Warn "remote fetch failed (url=$url; reason=$reason)"
    Log-Result 'check_failed' 'Yellow'
    Write-Host "Trigger update: Result=check_failed; remote fetch failed; url=$url; reason=$reason"
    Emit-GateSkillAgentAction 'CONTINUE_SKILL_EXECUTION'
    exit 0
  }

  if ($head -notmatch '(?m)^version:') {
    Log-Warn 'remote SKILL.md has no version field'
    Log-Result 'check_failed' 'Yellow'
    Write-Host 'Trigger update: Result=check_failed; remote SKILL.md unreadable'
    Emit-GateSkillAgentAction 'CONTINUE_SKILL_EXECUTION'
    exit 0
  }
  Log-Ok 'remote frontmatter fetched'

  $rv = Get-YamlFieldFromText 'version' $head
  $uv = Get-YamlFieldFromText 'updated' $head
  $lv = Get-YamlField 'version' $localMd
  $lu = Get-YamlField 'updated' $localMd

  Log-Info "remote  version=$rv  updated=$uv"
  Log-Info "local   version=$lv  updated=$lu"
  Write-GateSkillVersionLogCheck $Name $rv $uv $lv $lu

  if ($rv -and ($rv -eq $lv) -and $uv -and ($uv -eq $lu)) {
    Remove-ApplyToken $Dest
    Log-Skip 'versions match — no update needed'
    Log-Result 'skipped'
    Write-Host 'Trigger update: Result=skipped; version and updated unchanged'
    Emit-GateSkillAgentAction 'CONTINUE_SKILL_EXECUTION'
    exit 0
  }

  Log-Warn 'version mismatch — update available'
  Log-Result 'update_available' 'Yellow'
  Write-Host "Trigger update: Result=update_available; remote version=$rv updated=$uv vs local version=$lv updated=$lu"
  if (Test-GateSkillAutoMode) {
    Remove-ApplyToken $Dest
    Log-Info 'GATE_SKILL_UPDATE_MODE=auto — applying update immediately (no user confirmation; logs only)'
    Emit-GateSkillAgentAction 'CONTINUE_SKILL_EXECUTION'
    Write-Host 'GATE_SKILL_AUTO_APPLY=1'
    Invoke-Apply -Dest $Dest -Name $Name
    exit 0
  }
  Emit-GateSkillAgentAction 'BLOCK_UNTIL_USER_CONFIRMS_UPDATE'
  $strict = $env:GATE_SKILL_CHECK_STRICT
  if ($strict -eq '1' -or $strict -eq 'true' -or $strict -eq 'TRUE' -or $strict -eq 'yes' -or $strict -eq 'YES') {
    $tok = New-ApplyTokenString
    Write-ApplyToken $Dest $tok
    Write-Host "GATE_SKILL_CONFIRM_TOKEN=$tok"
    Write-Host 'GATE_SKILL_TWO_STEP_GATE=1 (set env above for apply after user confirms)'
    Write-Host 'GATE_SKILL_CHECK_EXIT=3 (strict: user must confirm before apply; not a script crash)'
    exit 3
  }
  exit 0
}

# ── Run (check + auto apply) ───────────────────────────────────

function Invoke-Run {
  param([string]$Dest = '', [string]$Name)

  if (-not [string]::IsNullOrWhiteSpace($Dest) -and -not [string]::IsNullOrWhiteSpace($Name)) {
    $pair = Resolve-DestTwoArg -Raw1 $Dest -Raw2 $Name
    $Dest = $pair.Dest
    $Name = $pair.Name
  } elseif ([string]::IsNullOrWhiteSpace($Dest)) {
    $Dest = Resolve-DestSingleArg -Name $Name
  }
  $Dest = Normalize-Dest $Dest
  $localMd = Join-Path $Dest 'SKILL.md'

  Log-Step 'run: check + auto apply'
  Log-Dim "DEST=$Dest  NAME=$Name"

  if (-not (Test-Path -LiteralPath $localMd)) {
    Log-Fail "local SKILL.md not found: $localMd"
    Log-Result 'failure' 'Red'
    Write-Host "Trigger update: Result=failure; missing $localMd"
    exit 1
  }

  $url = "$RemoteRaw/$Name/SKILL.md"
  Log-Info 'fetching remote SKILL.md frontmatter …'
  try {
    $resp = Invoke-WebRequest -Uri $url -UseBasicParsing
    $head = ($resp.Content -split "`r?`n")[0..39] -join "`n"
  } catch {
    $reason = ''
    try { $reason = (($_.Exception.Message) -replace '\s+', ' ').Trim() } catch { $reason = 'unknown error' }
    if ([string]::IsNullOrWhiteSpace($reason)) { $reason = 'unknown error' }
    Log-Warn "remote fetch failed — skipping apply (url=$url; reason=$reason)"
    Log-Result 'check_failed' 'Yellow'
    Write-Host "Trigger update: Result=check_failed; remote fetch failed; url=$url; reason=$reason; skipping apply (Execution may proceed)"
    exit 0
  }

  if ($head -notmatch '(?m)^version:') {
    Log-Warn 'remote SKILL.md unreadable — skipping apply'
    Log-Result 'check_failed' 'Yellow'
    Write-Host 'Trigger update: Result=check_failed; remote SKILL.md unreadable; skipping apply (Execution may proceed)'
    exit 0
  }
  Log-Ok 'remote frontmatter fetched'

  $rv = Get-YamlFieldFromText 'version' $head
  $uv = Get-YamlFieldFromText 'updated' $head
  $lv = Get-YamlField 'version' $localMd
  $lu = Get-YamlField 'updated' $localMd

  Log-Info "remote  version=$rv  updated=$uv"
  Log-Info "local   version=$lv  updated=$lu"
  Write-GateSkillVersionLogCheck $Name $rv $uv $lv $lu

  if ($rv -and ($rv -eq $lv) -and $uv -and ($uv -eq $lu)) {
    Log-Skip 'versions match — no update needed'
    Log-Result 'skipped'
    Write-Host 'Trigger update: Result=skipped; version and updated unchanged'
    exit 0
  }

  Log-Warn 'version mismatch — applying update …'
  Write-Host "Trigger update: remote differs (remote version=$rv updated=$uv vs local version=$lv updated=$lu); applying..."

  try {
    Invoke-Apply -Dest $Dest -Name $Name
    exit 0
  } catch {
    Log-Fail $_.Exception.Message
    Log-Result 'failure' 'Red'
    Write-Host "Trigger update: Result=failure; $($_.Exception.Message)"
    exit 1
  }
}

# ── Main ────────────────────────────────────────────────────────

$argsList = @($args)

# 1-arg (no subcommand): <NAME> → run with auto DEST
if ($argsList.Count -eq 1 -and $argsList[0] -notin @('run','check','apply','revoke-pending','-h','--help','help')) {
  Invoke-Run -Name $argsList[0]
}

# Legacy 2-arg: <DEST> <NAME> → run
if ($argsList.Count -eq 2 -and $argsList[0] -notin @('run','check','apply','revoke-pending')) {
  $leg = Resolve-DestTwoArg -Raw1 $argsList[0] -Raw2 $argsList[1]
  Invoke-Run -Dest $leg.Dest -Name $leg.Name
}

if ($argsList.Count -lt 2) { Show-Usage }

$cmd = $argsList[0]

# subcommand + 1 arg (NAME, auto DEST) or subcommand + 2 args (DEST, NAME)
if ($argsList.Count -eq 2) {
  $nameArg = $argsList[1]
  $destArg = ''
} elseif ($argsList.Count -ge 3) {
  $destArg = $argsList[1]
  $nameArg = $argsList[2]
} else {
  Show-Usage
}

switch ($cmd.ToLowerInvariant()) {
  'run'   { Invoke-Run -Dest $destArg -Name $nameArg; exit $LASTEXITCODE }
  'check' { Invoke-Check -Dest $destArg -Name $nameArg; exit $LASTEXITCODE }
  'apply' {
    Log-Step 'apply: force download and sync files'
    if (-not [string]::IsNullOrWhiteSpace($destArg) -and -not [string]::IsNullOrWhiteSpace($nameArg)) {
      $ap = Resolve-DestTwoArg -Raw1 $destArg -Raw2 $nameArg
      $destArg = $ap.Dest
      $nameArg = $ap.Name
    } elseif ([string]::IsNullOrWhiteSpace($destArg)) {
      $destArg = Resolve-DestSingleArg -Name $nameArg
    }
    $destArg = Normalize-Dest $destArg
    Log-Dim "DEST=$destArg  NAME=$nameArg"
    try {
      Invoke-Apply -Dest $destArg -Name $nameArg
      exit 0
    } catch {
      Log-Fail $_.Exception.Message
      Log-Result 'failure' 'Red'
      Write-Host "Trigger update: Result=failure; $($_.Exception.Message)"
      exit 1
    }
  }
  'revoke-pending' {
    if (-not [string]::IsNullOrWhiteSpace($destArg) -and -not [string]::IsNullOrWhiteSpace($nameArg)) {
      $rp = Resolve-DestTwoArg -Raw1 $destArg -Raw2 $nameArg
      $destArg = $rp.Dest
      $nameArg = $rp.Name
    } elseif ([string]::IsNullOrWhiteSpace($destArg)) {
      $destArg = Resolve-DestSingleArg -Name $nameArg
    }
    $destArg = Normalize-Dest $destArg
    Remove-ApplyToken $destArg
    Log-Ok "revoke-pending: cleared apply token — DEST=$destArg"
    Write-Host 'Trigger update: Result=revoke_pending_ok'
    exit 0
  }
  default { Show-Usage }
}
