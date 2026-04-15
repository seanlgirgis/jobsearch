# job-run.ps1 — Step 4: Generate resume + cover letter for accepted job
# Usage: .\job-run.ps1 [-Model grok-3] [-Version v1]

param(
    [string]$Model   = "grok-3",
    [string]$Version = "v1"
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
if (-not $cache.accepted) {
    Write-Host "ERROR: Job has not been accepted. Run .\job-accept.ps1 first." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== STEP 4: Generating Documents ===" -ForegroundColor Cyan
Write-Host "UUID   : $uuid"
Write-Host "Model  : $Model"
Write-Host "Version: $Version"
Write-Host ""

function Run-Step {
    param([string]$Label, [string[]]$Cmd)
    Write-Host "--- $Label ---" -ForegroundColor Yellow
    & python $Cmd
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAILED at: $Label" -ForegroundColor Red
        exit 1
    }
}

Run-Step "03 Tailor job data"     @("scripts\03_tailor_job_data.py",              "--uuid", $uuid, "--version", $Version, "--model", "grok-3-mini")
Run-Step "04 Generate resume"     @("scripts\04_generate_resume_intermediate.py",  "--uuid", $uuid, "--version", $Version, "--model", $Model)
Run-Step "05 Render resume"       @("scripts\05_render_resume.py",                 "--uuid", $uuid, "--version", $Version, "--all")
Run-Step "06 Company research"    @("scripts\06_company_research.py",              "--uuid", $uuid, "--version", $Version, "--model", "grok-3-mini")
Run-Step "07 Generate cover"      @("scripts\07_generate_cover_intermediate.py",   "--uuid", $uuid, "--version", $Version, "--model", $Model)
Run-Step "08 Render cover"        @("scripts\08_render_cover_letter.py",           "--uuid", $uuid, "--version", $Version)

# Find generated folder and open it
$jobFolder = Get-ChildItem data\jobs -Directory | Where-Object { $_.Name -match $uuid } | Select-Object -First 1
$generatedPath = Join-Path $jobFolder.FullName "generated"

Write-Host ""
Write-Host "=== DONE ===" -ForegroundColor Green
Write-Host "Files ready at: $generatedPath" -ForegroundColor Yellow

# Open Explorer at the output folder
Start-Process explorer.exe $generatedPath

# Update cache
$cache | Add-Member -NotePropertyName documents_ready -NotePropertyValue $true -Force
$cache | ConvertTo-Json | Set-Content .job_cache.json

Write-Host ""
Write-Host "Submit resume_v$Version.docx and cover_letter.docx, then run .\job-apply.ps1" -ForegroundColor Green
