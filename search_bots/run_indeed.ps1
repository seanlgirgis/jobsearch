param(
    [string]$File,
    [switch]$DryRun,
    [switch]$Live,
    [int]$Limit = 1,
    [string]$Query,
    [int]$Fromage,
    [switch]$Fresh,
    [switch]$Scheduled
)
$root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $root
. "$root\env_setter.ps1"
$argsList = @("$root\scripts\search_bots_indeed.py", "--root", $root)
if ($Scheduled) {
    $argsList += @("--live", "--scheduled", "--limit", "$Limit")
} elseif ($Live) {
    $argsList += @("--live", "--limit", "$Limit")
    if ($Query) { $argsList += @("--query", $Query) }
    if ($PSBoundParameters.ContainsKey("Fromage")) { $argsList += @("--fromage", "$Fromage") }
    if ($Fresh) { $argsList += "--fresh" }
} elseif ($File) {
    $argsList += @("--file", $File)
} else {
    $argsList += "--inbox"
}
if ($DryRun) { $argsList += "--dry-run" }
python @argsList
exit $LASTEXITCODE
