# job-v2-apply.ps1
# Manual-v2 step 3: record an application in metadata.yaml (system of record).
#
# Usage:
#   .\job-v2-apply.ps1
#   .\job-v2-apply.ps1 -Method "Company Site" -Notes "Applied with tailored docs"
#   .\job-v2-apply.ps1 -ClearCache

param(
    [string]$Method = "LinkedIn",
    [string]$Notes = "Applied via manual-v2 pipeline",
    [string]$Date = (Get-Date).ToString("yyyy-MM-dd"),
    [switch]$ClearCache
)

Set-Location $PSScriptRoot
. .\env_setter.ps1

if (-not (Test-Path -LiteralPath ".job_cache_v2.json")) {
    Write-Host "ERROR: No v2 cache found. Run .\job-v2-shell.ps1 first." -ForegroundColor Red
    exit 1
}

$cache = Get-Content -LiteralPath ".job_cache_v2.json" | ConvertFrom-Json
$uuid = $cache.uuid_short

if (-not $uuid) {
    Write-Host "ERROR: Cache missing uuid_short." -ForegroundColor Red
    exit 1
}

if (-not $cache.documents_ready) {
    Write-Host "ERROR: documents_ready=false. Run .\job-v2-render.ps1 first." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== MANUAL V2 APPLY ===" -ForegroundColor Cyan
Write-Host "UUID  : $uuid"
Write-Host "Method: $Method"
Write-Host "Date  : $Date"
Write-Host ""

python scripts\09_update_application_status.py --uuid $uuid apply `
    --date $Date `
    --method $Method `
    --notes $Notes

if ($LASTEXITCODE -ne 0) {
    Write-Host "Apply update failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

$cache | Add-Member -NotePropertyName applied -NotePropertyValue $true -Force
$cache | Add-Member -NotePropertyName applied_date -NotePropertyValue $Date -Force

if ($ClearCache) {
    Remove-Item -LiteralPath ".job_cache_v2.json" -ErrorAction SilentlyContinue
    Write-Host "Application recorded. v2 cache cleared." -ForegroundColor Green
} else {
    $cache | ConvertTo-Json | Set-Content -LiteralPath ".job_cache_v2.json"
    Write-Host "Application recorded. v2 cache retained." -ForegroundColor Green
}

