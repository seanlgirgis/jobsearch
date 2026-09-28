# job-v2-shell.ps1
# Manual-v2 step 1: duplicate check + create job shell (no LLM generation).
#
# Usage:
#   .\job-v2-shell.ps1 .\intake\intake.md
#   .\job-v2-shell.ps1 .\intake\intake.md -SkipDuplicateCheck
#   .\job-v2-shell.ps1 .\intake\intake.md -AllowDuplicate

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$IntakeFile = "intake\intake.md",
    [switch]$SkipDuplicateCheck,
    [switch]$AllowDuplicate,
    [switch]$MoveIntake
)

Set-Location $PSScriptRoot
. .\env_setter.ps1

if (-not (Test-Path -LiteralPath $IntakeFile)) {
    Write-Host "ERROR: File not found: $IntakeFile" -ForegroundColor Red
    exit 1
}

$argsList = @("scripts_v2\00_create_job_shell.py", $IntakeFile)
if ($SkipDuplicateCheck) { $argsList += "--skip-duplicate-check" }
if ($AllowDuplicate) { $argsList += "--allow-duplicate" }
if ($MoveIntake) { $argsList += "--move-intake" }

python @argsList
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if (-not (Test-Path -LiteralPath ".job_cache_v2.json")) {
    Write-Host "ERROR: .job_cache_v2.json not created." -ForegroundColor Red
    exit 1
}

$cache = Get-Content -LiteralPath ".job_cache_v2.json" | ConvertFrom-Json

Write-Host ""
Write-Host "Manual-v2 shell ready." -ForegroundColor Green
Write-Host "Job ID    : $($cache.job_id)"
Write-Host "UUID short: $($cache.uuid_short)"
Write-Host "Folder    : $($cache.job_folder)"
Write-Host ""
Write-Host "Next in ChatGPT Project:"
Write-Host "1) MODE_ID: B1  (score report)"
Write-Host "2) MODE_ID: C1  (tailored_data_v1.yaml + resume_intermediate_v1.json)"
Write-Host "3) MODE_ID: D1  (cover_intermediate_v1.json)"
Write-Host ""
Write-Host "Then run: .\job-v2-render.ps1" -ForegroundColor Yellow

