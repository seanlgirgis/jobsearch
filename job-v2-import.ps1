# job-v2-import.ps1
# Import ChatGPT artifacts into the current v2 job folder.
#
# Usage examples:
#   .\job-v2-import.ps1 -FromClipboard
#   .\job-v2-import.ps1 -InputFile "D:\temp\chatgpt_output.txt"
#   .\job-v2-import.ps1 -InputFile "D:\temp\chatgpt_output.txt" -Force

param(
    [string]$InputFile = "",
    [switch]$FromClipboard,
    [switch]$Force
)

Set-Location $PSScriptRoot
. .\env_setter.ps1

if (-not $InputFile -and -not $FromClipboard) {
    Write-Host "ERROR: Provide -InputFile or -FromClipboard." -ForegroundColor Red
    exit 1
}

$argsList = @("scripts_v2\02_import_chatgpt_artifacts.py")
if ($InputFile) { $argsList += @("--input", $InputFile) }
if ($FromClipboard) { $argsList += "--from-clipboard" }
if ($Force) { $argsList += "--force" }

python @argsList
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "Artifacts imported. Next: .\job-v2-render.ps1" -ForegroundColor Green

