# job-chatgpt-apply.ps1
# ChatGPT pipeline step 4: mark job as applied in metadata tracking.
#
# Usage:
#   .\job-chatgpt-apply.ps1 -Method "Dice"
#   .\job-chatgpt-apply.ps1 -Method "Company Site" -Notes "Applied with ChatGPT-tailored docs"
#   .\job-chatgpt-apply.ps1 -Method "Dice" -SkipIndexRefresh

param(
    [string]$Method = "LinkedIn",
    [string]$Notes = "Applied via chatGpt pipeline",
    [string]$Date = (Get-Date).ToString("yyyy-MM-dd"),
    [switch]$ClearCache,
    [switch]$SkipIndexRefresh
)

Set-Location $PSScriptRoot
. .\env_setter.ps1

$chatCachePath = ".job_cache_chatgpt.json"
if (-not (Test-Path -LiteralPath $chatCachePath)) {
    Write-Host "ERROR: No chatgpt cache found. Run chatgpt pipeline steps first." -ForegroundColor Red
    exit 1
}

$cache = Get-Content -LiteralPath $chatCachePath | ConvertFrom-Json
$uuid = $cache.uuid_short
if (-not $uuid) {
    Write-Host "ERROR: Cache missing uuid_short." -ForegroundColor Red
    exit 1
}
if (-not $cache.documents_ready) {
    Write-Host "ERROR: documents_ready=false. Run .\job-chatgpt-render.ps1 first." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== CHATGPT PIPELINE: STEP 4 / APPLY ===" -ForegroundColor Cyan
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

$indexRefreshOk = $true
if (-not $SkipIndexRefresh) {
    Write-Host ""
    Write-Host "Refreshing duplicate-check index..." -ForegroundColor Yellow
    python scripts\utils\build_job_index.py --rebuild
    if ($LASTEXITCODE -ne 0) {
        $indexRefreshOk = $false
        Write-Host "WARNING: Application saved, but index refresh failed. Run manually:" -ForegroundColor Yellow
        Write-Host "python scripts\utils\build_job_index.py --rebuild" -ForegroundColor Yellow
    } else {
        Write-Host "Index refreshed successfully." -ForegroundColor Green
    }
}

$cache | Add-Member -NotePropertyName applied -NotePropertyValue $true -Force
$cache | Add-Member -NotePropertyName applied_date -NotePropertyValue $Date -Force
$cache | Add-Member -NotePropertyName index_refreshed_after_apply -NotePropertyValue $indexRefreshOk -Force

if ($ClearCache) {
    Remove-Item -LiteralPath $chatCachePath -ErrorAction SilentlyContinue
    Write-Host "Application recorded. chatgpt cache cleared." -ForegroundColor Green
} else {
    $cache | ConvertTo-Json | Set-Content -LiteralPath $chatCachePath
    Write-Host "Application recorded. chatgpt cache retained." -ForegroundColor Green
}
