# job-score.ps1 — Step 2: Score the job against your master profile
# Usage: .\job-score.ps1 [-Model grok-3] [-Temperature 0.5]

param(
    [string]$Model       = "grok-3-mini",
    [string]$Temperature = "0.5"
)

Set-Location $PSScriptRoot
. .\env_setter.ps1

if (-not (Test-Path .job_cache.json)) {
    Write-Host "ERROR: No cache found. Run .\job-check.ps1 first." -ForegroundColor Red
    exit 1
}

$cache = Get-Content .job_cache.json | ConvertFrom-Json
$intakeFile = $cache.intake_file

Write-Host ""
Write-Host "=== STEP 2: Scoring ===" -ForegroundColor Cyan
Write-Host "File : $intakeFile"
Write-Host "Model: $Model"
Write-Host ""

# Snapshot existing job folders before running
$before = Get-ChildItem data\jobs -Directory | Select-Object -ExpandProperty Name

# Run with live output streaming directly to console — no capture
# --no-move keeps the intake file in place (does not delete it after scoring)
python scripts\01_score_job.py $intakeFile --model $Model --temperature $Temperature --no-move
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Scoring failed." -ForegroundColor Red
    exit 1
}

# Find the new folder that just appeared
$after     = Get-ChildItem data\jobs -Directory | Select-Object -ExpandProperty Name
$newFolder = $after | Where-Object { $before -notcontains $_ } | Select-Object -First 1

if (-not $newFolder) {
    Write-Host "ERROR: Could not find new job folder after scoring." -ForegroundColor Red
    exit 1
}

# Read UUID from metadata.yaml — no text parsing needed
$metaFile  = "data\jobs\$newFolder\metadata.yaml"
$meta      = Get-Content $metaFile | Where-Object { $_ -match "^uuid:" } | Select-Object -First 1
$uuid      = ($meta -replace "^uuid:\s*['""]?", "").Trim().TrimEnd("'`"")
$uuidShort = $uuid.Substring(0, 8)
$jobFolder = Get-Item "data\jobs\$newFolder"

# Update cache
$cache | Add-Member -NotePropertyName uuid       -NotePropertyValue $uuid      -Force
$cache | Add-Member -NotePropertyName uuid_short -NotePropertyValue $uuidShort -Force
$cache | Add-Member -NotePropertyName job_folder -NotePropertyValue $jobFolder.Name -Force
$cache | ConvertTo-Json | Set-Content .job_cache.json

Write-Host ""
Write-Host "UUID : $uuid" -ForegroundColor Yellow
Write-Host "Score report: data\jobs\$($jobFolder.Name)\score\" -ForegroundColor Yellow
Write-Host ""
Write-Host "Review the score, then run .\job-accept.ps1 (or .\job-accept.ps1 -Reject)" -ForegroundColor Green
