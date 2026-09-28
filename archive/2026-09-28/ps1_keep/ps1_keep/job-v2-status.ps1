# job-v2-status.ps1
# Manual-v2 helper: update application status in system of record.
#
# Usage:
#   .\job-v2-status.ps1 -NewStatus "Interview Scheduled"
#   .\job-v2-status.ps1 -NewStatus "Rejected" -Notes "No sponsorship fit"

param(
    [Parameter(Mandatory=$true)]
    [string]$NewStatus,
    [string]$Notes = "",
    [string]$FollowupDate = ""
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

$argsList = @(
    "scripts\09_update_application_status.py",
    "--uuid", $uuid,
    "status",
    "--new-status", $NewStatus
)
if ($Notes) { $argsList += @("--notes", $Notes) }
if ($FollowupDate) { $argsList += @("--followup-date", $FollowupDate) }

python @argsList
if ($LASTEXITCODE -ne 0) {
    Write-Host "Status update failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "Status updated for job $uuid." -ForegroundColor Green

