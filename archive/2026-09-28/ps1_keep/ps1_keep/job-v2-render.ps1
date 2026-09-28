# job-v2-render.ps1
# Manual-v2 step 2: validate artifacts, render resume/cover, run quality gate.
#
# Usage:
#   .\job-v2-render.ps1
#   .\job-v2-render.ps1 -Version v1
#   .\job-v2-render.ps1 -SkipCover
#   .\job-v2-render.ps1 -NoStrict

param(
    [string]$Version = "v1",
    [switch]$SkipCover,
    [switch]$NoStrict,
    [switch]$NoNormalize
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

Write-Host ""
Write-Host "=== MANUAL V2 RENDER ===" -ForegroundColor Cyan
Write-Host "UUID   : $uuid"
Write-Host "Version: $Version"
Write-Host ""

$validateArgs = @("scripts_v2\01_validate_manual_artifacts.py", "--uuid", $uuid, "--version", $Version)
if ($SkipCover) { $validateArgs += "--skip-cover" }
python @validateArgs
if ($LASTEXITCODE -ne 0) {
    Write-Host "Artifact validation failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

$resumeArgs = @("scripts\05_render_resume.py", "--uuid", $uuid, "--version", $Version, "--all")
if (-not $NoNormalize) { $resumeArgs += "--normalize" }
python @resumeArgs
if ($LASTEXITCODE -ne 0) {
    Write-Host "Resume render failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

if (-not $SkipCover) {
    python scripts\08_render_cover_letter.py --uuid $uuid --version $Version
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Cover render failed." -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

$qualityArgs = @("scripts\quality_check.py", "--uuid", $uuid, "--version", $Version)
if (-not $NoStrict) { $qualityArgs += "--strict" }
python @qualityArgs
if ($LASTEXITCODE -ne 0) {
    Write-Host "Quality check failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

$cache | Add-Member -NotePropertyName documents_ready -NotePropertyValue $true -Force
$cache | Add-Member -NotePropertyName render_version -NotePropertyValue $Version -Force
$cache | ConvertTo-Json | Set-Content -LiteralPath ".job_cache_v2.json"

Write-Host ""
Write-Host "Render complete. Documents are ready." -ForegroundColor Green
Write-Host "Next: .\job-v2-apply.ps1" -ForegroundColor Yellow
