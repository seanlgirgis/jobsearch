# job-chatgpt-check.ps1
# ChatGPT pipeline step 1: duplicate check only (no scoring, no shell creation yet).
#
# Usage:
#   .\job-chatgpt-check.ps1
#   .\job-chatgpt-check.ps1 "intake\intake.md"

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$IntakeFile = "intake\intake.md"
)

Set-Location $PSScriptRoot
. .\env_setter.ps1

if (-not (Test-Path -LiteralPath $IntakeFile)) {
    Write-Host "ERROR: File not found: $IntakeFile" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== CHATGPT PIPELINE: STEP 1 / DUPLICATE CHECK ===" -ForegroundColor Cyan
python scripts\00_check_applied_before.py $IntakeFile
if ($LASTEXITCODE -ne 0) {
    Write-Host "Duplicate detected or check failed. Stopping." -ForegroundColor Red
    exit $LASTEXITCODE
}

$cache = @{
    pipeline = "chatgpt"
    intake_file = $IntakeFile
    duplicate_checked = $true
    duplicate_checked_at = (Get-Date).ToString("s")
    accepted = $false
    documents_ready = $false
    applied = $false
}
$cache | ConvertTo-Json | Set-Content -LiteralPath ".job_cache_chatgpt.json"

Write-Host ""
Write-Host "Duplicate check passed." -ForegroundColor Green
Write-Host "Next: .\job-chatgpt-accept.ps1" -ForegroundColor Yellow
