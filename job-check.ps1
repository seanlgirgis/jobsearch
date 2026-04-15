# job-check.ps1 — Step 1: Duplicate check on a new intake file
# Usage: .\job-check.ps1 "intake\intake.md"

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$IntakeFile
)

Set-Location $PSScriptRoot
. .\env_setter.ps1

if (-not (Test-Path $IntakeFile)) {
    Write-Host "ERROR: File not found: $IntakeFile" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== STEP 1: Duplicate Check ===" -ForegroundColor Cyan
python scripts\00_check_applied_before.py $IntakeFile
if ($LASTEXITCODE -ne 0) {
    Write-Host "Duplicate detected or check failed. Stopping." -ForegroundColor Red
    exit 1
}

# Save intake file path to cache
@{ intake_file = $IntakeFile } | ConvertTo-Json | Set-Content .job_cache.json
Write-Host ""
Write-Host "OK — no duplicate. Run .\job-score.ps1 next." -ForegroundColor Green
