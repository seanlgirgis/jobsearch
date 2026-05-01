# env_setter.ps1 - portable repo bootstrap with one allowed absolute path: C:\pyenv

# Repo root = folder containing this script
$env:PROJECT_ROOT = Convert-Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

# Canonical shared venv location across machines
# Priority:
# 1) JOBSEARCH_VENV (explicit override)
# 2) C:\pyenv\JobSearch
# 3) C:\py_venv\JobSearch (legacy fallback)
$venvCandidates = @()
if ($env:JOBSEARCH_VENV) { $venvCandidates += $env:JOBSEARCH_VENV }
$venvCandidates += "C:\pyenv\JobSearch"
$venvCandidates += "C:\py_venv\JobSearch"

$venvPath = $null
foreach ($candidate in $venvCandidates) {
    if ($candidate -and (Test-Path -LiteralPath "$candidate\Scripts\Activate.ps1")) {
        $venvPath = $candidate
        break
    }
}

if (-not $venvPath) {
    Write-Host "ERROR: No venv found. Expected one of:" -ForegroundColor Red
    $venvCandidates | ForEach-Object { Write-Host "- $_" -ForegroundColor Red }
    Write-Host "Create it once, e.g.:" -ForegroundColor Yellow
    Write-Host "python -m venv C:\pyenv\JobSearch" -ForegroundColor Yellow
    exit 1
}

# Activate venv
& "$venvPath\Scripts\Activate.ps1"

# Keep imports repo-relative
$env:PYTHONPATH = "$env:PROJECT_ROOT\src;$env:PYTHONPATH"

# Data / storage paths (repo-relative)
$env:JOBS_DB_DIR    = "$env:PROJECT_ROOT\data\jobs"
$env:RESUMES_DIR    = "$env:PROJECT_ROOT\data\resumes"
$env:VECTOR_DB_PATH = "$env:PROJECT_ROOT\data\vectorstore"

# Model/provider defaults
$env:DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
$env:DEFAULT_LLM_PROVIDER = "xai"
$env:STUDYBOOK_EMBEDDING_LOCAL_ONLY = "1"
$env:HF_HUB_OFFLINE = "1"
$env:TRANSFORMERS_OFFLINE = "1"

# UTF-8 console safety
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "JobSearch environment activated [OK]" -ForegroundColor Green
Write-Host "Project Root: $env:PROJECT_ROOT" -ForegroundColor DarkGray
Write-Host "Venv Path: $venvPath" -ForegroundColor DarkGray
python --version
Write-Host "Use 'deactivate' to exit venv"
