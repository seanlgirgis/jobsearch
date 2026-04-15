# job-reject.ps1 — Reject the current scored job and clear the cache
# Usage: .\job-reject.ps1 [-Reason "your reason"]

param(
    [string]$Reason = "User rejected after reviewing score"
)

Set-Location $PSScriptRoot
. .\env_setter.ps1

if (-not (Test-Path .job_cache.json)) {
    Write-Host "ERROR: No cache found. Run .\job-check.ps1 first." -ForegroundColor Red
    exit 1
}

$cache = Get-Content .job_cache.json | ConvertFrom-Json
$uuid  = $cache.uuid_short

if (-not $uuid) {
    Write-Host "ERROR: No UUID in cache. Run .\job-score.ps1 first." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== REJECTING JOB ===" -ForegroundColor Yellow
Write-Host "UUID  : $uuid"
Write-Host "Reason: $Reason"
Write-Host ""

python -m scripts.02_decide_job --uuid $uuid --reject --reason $Reason
if ($LASTEXITCODE -ne 0) { exit 1 }

# Clear cache — done with this job
Remove-Item .job_cache.json -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Job rejected. Cache cleared — ready for the next one." -ForegroundColor Yellow
