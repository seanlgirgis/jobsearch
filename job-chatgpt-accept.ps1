# job-chatgpt-accept.ps1
# ChatGPT pipeline step 2: accept job, create UUID + folder shell, copy intake, mark ACCEPTED.
#
# Usage:
#   .\job-chatgpt-accept.ps1
#   .\job-chatgpt-accept.ps1 -MoveIntake
#   .\job-chatgpt-accept.ps1 -IntakeFile "intake\intake.md" -SkipCheckRequirement

param(
    [string]$IntakeFile = "",
    [switch]$MoveIntake,
    [switch]$SkipCheckRequirement
)

Set-Location $PSScriptRoot
. .\env_setter.ps1

$chatCachePath = ".job_cache_chatgpt.json"

if (-not $IntakeFile) {
    if (Test-Path -LiteralPath $chatCachePath) {
        $existing = Get-Content -LiteralPath $chatCachePath | ConvertFrom-Json
        $IntakeFile = $existing.intake_file
    } else {
        $IntakeFile = "intake\intake.md"
    }
}

if (-not (Test-Path -LiteralPath $IntakeFile)) {
    Write-Host "ERROR: Intake file not found: $IntakeFile" -ForegroundColor Red
    exit 1
}

if (-not $SkipCheckRequirement) {
    if (-not (Test-Path -LiteralPath $chatCachePath)) {
        Write-Host "ERROR: No chatgpt cache found. Run .\job-chatgpt-check.ps1 first." -ForegroundColor Red
        exit 1
    }
    $pre = Get-Content -LiteralPath $chatCachePath | ConvertFrom-Json
    if (-not $pre.duplicate_checked) {
        Write-Host "ERROR: duplicate_checked=false. Run .\job-chatgpt-check.ps1 first." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "=== CHATGPT PIPELINE: STEP 2 / ACCEPT + SHELL CREATE ===" -ForegroundColor Cyan
Write-Host "Intake: $IntakeFile"

$argsList = @("scripts_v2\00_create_job_shell.py", $IntakeFile, "--skip-duplicate-check")
if ($MoveIntake) { $argsList += "--move-intake" }

python @argsList
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create job shell." -ForegroundColor Red
    exit $LASTEXITCODE
}

if (-not (Test-Path -LiteralPath ".job_cache_v2.json")) {
    Write-Host "ERROR: .job_cache_v2.json not found after shell creation." -ForegroundColor Red
    exit 1
}

$v2 = Get-Content -LiteralPath ".job_cache_v2.json" | ConvertFrom-Json
$uuid = $v2.uuid_short
if (-not $uuid) {
    Write-Host "ERROR: Missing uuid_short in .job_cache_v2.json" -ForegroundColor Red
    exit 1
}

$reason = "Accepted in chatGpt pipeline (manual artifacts, no Grok scoring)"
python -m scripts.02_decide_job --uuid $uuid --accept --reason $reason
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Could not set ACCEPTED decision." -ForegroundColor Red
    exit $LASTEXITCODE
}

# Mark metadata pipeline mode as chatgpt for explicit tracking.
python -c "from pathlib import Path; import yaml; p=Path(r'$($v2.job_folder)')/'metadata.yaml'; d=yaml.safe_load(p.read_text(encoding='utf-8')) or {}; d['pipeline_mode']='chatgpt'; p.write_text(yaml.safe_dump(d, sort_keys=False, allow_unicode=True), encoding='utf-8')"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to set pipeline_mode=chatgpt in metadata." -ForegroundColor Red
    exit $LASTEXITCODE
}

$chatCache = @{
    pipeline = "chatgpt"
    intake_file = $IntakeFile
    duplicate_checked = $true
    duplicate_checked_at = (Get-Date).ToString("s")
    job_id = $v2.job_id
    uuid = $v2.uuid
    uuid_short = $v2.uuid_short
    job_folder = $v2.job_folder
    created_at = $v2.created_at
    accepted = $true
    documents_ready = $false
    applied = $false
}
$chatCache | ConvertTo-Json | Set-Content -LiteralPath $chatCachePath

Write-Host ""
Write-Host "Accepted and shell created." -ForegroundColor Green
Write-Host "Job ID    : $($chatCache.job_id)"
Write-Host "UUID short: $($chatCache.uuid_short)"
Write-Host "Folder    : $($chatCache.job_folder)"
Write-Host ""
Write-Host "Now place ChatGPT files into generated/:" -ForegroundColor Yellow
Write-Host "- resume_intermediate_v1.json"
Write-Host "- cover_intermediate_v1.json"
Write-Host ""
Write-Host "Next: .\job-chatgpt-render.ps1" -ForegroundColor Yellow
