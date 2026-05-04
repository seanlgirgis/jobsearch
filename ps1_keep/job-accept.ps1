# job-accept.ps1 — Step 3: Accept or reject the scored job
# Usage: .\job-accept.ps1 [-Reject] [-Reason "your reason"]

param(
    [switch]$Reject,
    [string]$Reason = ""
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
Write-Host "=== STEP 3: Decision ===" -ForegroundColor Cyan

if ($Reject) {
    $decision = "--reject"
    $defaultReason = "User rejected after reviewing score"
    Write-Host "Decision: REJECT" -ForegroundColor Red
} else {
    $decision = "--accept"
    $defaultReason = "User accepted after reviewing score"
    Write-Host "Decision: ACCEPT" -ForegroundColor Green
}

if (-not $Reason) { $Reason = $defaultReason }

python -m scripts.02_decide_job --uuid $uuid $decision --reason $Reason
if ($LASTEXITCODE -ne 0) { exit 1 }

if ($Reject) {
    Remove-Item .job_cache.json -ErrorAction SilentlyContinue
    Write-Host "Job rejected. Cache cleared." -ForegroundColor Yellow
    exit 0
}

# Update cache
$cache | Add-Member -NotePropertyName accepted -NotePropertyValue $true -Force
$cache | ConvertTo-Json | Set-Content .job_cache.json

Write-Host ""
Write-Host "Accepted. Run .\job-run.ps1 to generate resume + cover letter." -ForegroundColor Green
