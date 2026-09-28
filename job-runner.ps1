param(
    [Parameter(Mandatory=$true, Position=0)][string]$Intake,
    [ValidateSet('gate','triage','generate','apply')][string]$Mode = 'triage',
    [switch]$DryRun,
    [switch]$OverrideDuplicate,
    [switch]$OverrideSuitability,
    [string]$Reason,
    [switch]$Cover,
    [string]$AnalysisProfile = 'economy',
    [string]$GenerationProfile = 'quality',
    [switch]$AssumeApplied,
    [string]$Method,
    [string]$Date,
    [string]$Notes,
    [switch]$Json
)
. "$PSScriptRoot\env_setter.ps1"
$arguments = @("$PSScriptRoot\scripts\canonical_runner.py", $Intake, '--root', $PSScriptRoot, '--mode', $Mode)
$arguments += @('--analysis-profile', $AnalysisProfile, '--generation-profile', $GenerationProfile)
if ($DryRun) { $arguments += '--dry-run' }
if ($OverrideDuplicate) { $arguments += '--override-duplicate' }
if ($OverrideSuitability) { $arguments += '--override-suitability' }
if ($Reason) { $arguments += @('--reason', $Reason) }
if ($Cover) { $arguments += '--cover' }
if ($AssumeApplied) { $arguments += '--assume-applied' }
if ($Method) { $arguments += @('--method', $Method) }
if ($Date) { $arguments += @('--date', $Date) }
if ($Notes) { $arguments += @('--notes', $Notes) }
if ($Json) { $arguments += '--json' }
python @arguments
exit $LASTEXITCODE
