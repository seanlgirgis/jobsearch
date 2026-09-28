param(
    [switch]$RequireOnly
)
$root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $root
. "$root\env_setter.ps1"
$argsList = @("$root\scripts\search_bots_sor.py", "--root", $root)
if ($RequireOnly) { $argsList += "--require" }
python @argsList
exit $LASTEXITCODE
