# job-apply.ps1 — Step 5: Record that you submitted the application
# Usage: .\job-apply.ps1 [-Method "LinkedIn"] [-Notes "any notes"]

param(
    [string]$Method = "LinkedIn",
    [string]$Notes  = "Applied via pipeline"
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
if (-not $cache.documents_ready) {
    Write-Host "ERROR: Documents not ready. Run .\job-run.ps1 first." -ForegroundColor Red
    exit 1
}

$today = (Get-Date).ToString("yyyy-MM-dd")

Write-Host ""
Write-Host "=== STEP 5: Recording Application ===" -ForegroundColor Cyan
Write-Host "UUID  : $uuid"
Write-Host "Method: $Method"
Write-Host "Date  : $today"
Write-Host ""

python scripts\09_update_application_status.py --uuid $uuid apply `
    --date $today `
    --method $Method `
    --notes $Notes

if ($LASTEXITCODE -ne 0) { exit 1 }

# Clear the cache — this job is done
Remove-Item .job_cache.json -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Application recorded. Good luck!" -ForegroundColor Green
Write-Host "Cache cleared — ready for the next job." -ForegroundColor Gray
