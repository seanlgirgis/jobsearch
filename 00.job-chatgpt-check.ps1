# 00.job-chatgpt-check.ps1
# ChatGPT pipeline step 1: duplicate check using clipboard job description.
#
# Usage:
#   .\00.job-chatgpt-check.ps1

Set-Location $PSScriptRoot
. .\env_setter.ps1

$clipboardText = Get-Clipboard -Raw
if ([string]::IsNullOrWhiteSpace($clipboardText)) {
    Write-Host "ERROR: Clipboard is empty. Copy a job description first." -ForegroundColor Red
    exit 1
}

$intakeDir = "intake"
if (-not (Test-Path -LiteralPath $intakeDir)) {
    New-Item -ItemType Directory -Path $intakeDir | Out-Null
}

$intakeFile = Join-Path $intakeDir "clipboard_intake.md"
$clipboardText | Set-Content -LiteralPath $intakeFile -Encoding utf8

$sourceHint = ""
$firstLine = ($clipboardText -split "`r?`n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -First 1)
$probe = (($firstLine + "`n" + $clipboardText).ToLowerInvariant())
if ($probe -match "dice") {
    $sourceHint = "Dice"
} elseif ($probe -match "indeed") {
    $sourceHint = "Indeed"
} elseif ($probe -match "linkedin") {
    $sourceHint = "LinkedIn"
} elseif ($probe -match "greenhouse|myworkdayjobs|workday") {
    $sourceHint = "Company Site"
}

Write-Host ""
Write-Host "=== CHATGPT PIPELINE: STEP 1 / DUPLICATE CHECK (CLIPBOARD) ===" -ForegroundColor Cyan
python scripts\00_check_applied_before.py $intakeFile --max-age-days 45
if ($LASTEXITCODE -ne 0) {
    Write-Host "Duplicate detected or check failed. Stopping." -ForegroundColor Red
    exit $LASTEXITCODE
}

$cache = @{
    pipeline = "chatgpt"
    intake_file = $intakeFile
    intake_source = "clipboard"
    source_hint = $sourceHint
    duplicate_checked = $true
    duplicate_checked_at = (Get-Date).ToString("s")
    accepted = $false
    documents_ready = $false
    applied = $false
}
$cache | ConvertTo-Json | Set-Content -LiteralPath ".job_cache_chatgpt.json"

Write-Host ""
Write-Host "Duplicate check passed." -ForegroundColor Green
Write-Host "Saved clipboard intake to: $intakeFile" -ForegroundColor Yellow
Write-Host "Next: .\02.job-chatgpt-accept.ps1" -ForegroundColor Yellow
