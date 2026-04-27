param(
  [Parameter(Mandatory=$true)][string]$Uuid,
  [switch]$AllResume
)

$ErrorActionPreference = "Stop"

if (-not $env:VIRTUAL_ENV) {
  throw "Python environment not active. Run .\\env_setter.ps1 first, then rerun this command."
}

$pythonCmd = Join-Path $env:VIRTUAL_ENV "Scripts\python.exe"
if (-not (Test-Path $pythonCmd)) {
  throw "Active virtual environment does not contain Scripts\\python.exe. Re-run .\\env_setter.ps1."
}

if ($AllResume) {
  & $pythonCmd scripts/05_render_resume.py --uuid $Uuid --full
} else {
  & $pythonCmd scripts/05_render_resume.py --uuid $Uuid
}

& $pythonCmd scripts/08_render_cover_letter.py --uuid $Uuid
