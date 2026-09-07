# start_grok_jobsearch.ps1
# STABLE — do not modify without explicit request from Sean.
#
# Runtime copy (use this):  C:\scripts\start_grok_jobsearch.ps1
# Repo archive (git only):  D:\Workarea\jobsearch\start_grok_jobsearch.ps1
# Keep both files identical when a change is ever required.
#
# Location-agnostic launcher: jobsearch -> Grok Build TUI
#
# Usage (from anywhere):
#   pwsh -ExecutionPolicy Bypass -File "C:\scripts\start_grok_jobsearch.ps1"
#
# Opens a new PowerShell window by default. To run in the current shell:
#   ...\start_grok_jobsearch.ps1 -NoNewWindow

param(
    [string]$JobsearchRoot = 'D:\Workarea\jobsearch',
    [switch]$NoNewWindow
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$WindowTitle = 'grok_jobsearch'

function Resolve-JobsearchPaths {
    param([string]$Root)

    if (-not (Test-Path -LiteralPath $Root)) {
        throw "jobsearch folder not found: $Root"
    }

    return [ordered]@{
        JobsearchRoot = (Resolve-Path -LiteralPath $Root).Path
    }
}

function Resolve-PwshExecutable {
    $pwshCmd = Get-Command pwsh -ErrorAction SilentlyContinue
    if ($pwshCmd) {
        return $pwshCmd.Source
    }

    $candidates = @(
        (Join-Path $env:ProgramFiles 'PowerShell\7\pwsh.exe')
        (Join-Path $env:ProgramFiles 'PowerShell\6\pwsh.exe')
    )

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }

    throw "pwsh not found on PATH or under Program Files\PowerShell. Install PowerShell 7+ first."
}

function Resolve-GrokExecutable {
    $grokCmd = Get-Command grok -ErrorAction SilentlyContinue
    if ($grokCmd) {
        return $grokCmd.Source
    }

    $fallback = Join-Path $env:USERPROFILE '.grok\bin\grok.exe'
    if (Test-Path -LiteralPath $fallback) {
        return $fallback
    }

    throw "grok not found on PATH and not at $fallback. Install Grok CLI first."
}

function Get-GrokBootstrapRules {
    @'
For this jobsearch (job-market pipeline) session:
- Read canonical Sean pack first: D:\Workarea\Grok_DIRECTOR\Grok_SEAN.md then Grok_SEAN_NOW.md. The 2026-06-15 learning export is archive, not current.
- Read BOOTSTRAP.md startup order before executing any task.
- Then read Grok_PROJECT_PROFILE.md when boundaries or routing are unclear.
- Read Grok_CURRENT_STATE.md only for status or planning.
- Read Grok_PROJECT_MEMORY.md only when stable conventions are needed.
- Use Grok_ prefix for agent files (Grok_PROJECT_PROFILE.md, Grok_PROJECT_MEMORY.md, Grok_CURRENT_STATE.md).
- Activate .\env_setter.ps1 before Python (venv C:\py_venv\JobSearch).
- Default work mode: bite-sized — one job or one pipeline step unless Sean requests otherwise.
- Sean has ADD/ADHD: keep every response ~1 page or less; one concept at a time; wait for his reply before continuing.
- When Sean asks for an opinion, give an honest assessment with tradeoffs — not blind agreement.
- Sean manages Git; batch sync via C:\scripts\gitqall.ps1 (jobsearch is registered).
- Work-learning belongs in ALOK; courses in learning; LeetCode in python_dsa; command nuggets in local_memory.
'@
}

function Get-GrokBootstrapPrompt {
    param([string]$RootPath)

    @"
New Grok Build session for jobsearch.

Read Grok_SEAN.md and Grok_SEAN_NOW.md from D:\Workarea\Grok_DIRECTOR, then BOOTSTRAP.md in this repo, and follow startup order before doing any work. Confirm the Grok agent files are loaded and you are operating repository-first in $RootPath. Default to bite-sized work (one job or one pipeline step).
"@
}

function Start-GrokJobsearchSession {
    $paths = Resolve-JobsearchPaths -Root $JobsearchRoot
    $grokExe = Resolve-GrokExecutable

    try {
        $Host.UI.RawUI.WindowTitle = $WindowTitle
    } catch {
        # Some hosts do not support title changes.
    }

    Write-Host "=== $WindowTitle ===" -ForegroundColor Cyan
    Write-Host "jobsearch: $($paths.JobsearchRoot)" -ForegroundColor DarkGray

    Set-Location -LiteralPath $paths.JobsearchRoot
    Write-Host "Working directory: $(Get-Location)" -ForegroundColor Green

    $rules = Get-GrokBootstrapRules
    $prompt = Get-GrokBootstrapPrompt -RootPath $paths.JobsearchRoot

    Write-Host "`nStarting Grok Build..." -ForegroundColor Yellow
    & $grokExe --cwd $paths.JobsearchRoot --rules $rules $prompt
}

if (-not $NoNewWindow) {
    $pwshExe = Resolve-PwshExecutable
    $paths = Resolve-JobsearchPaths -Root $JobsearchRoot
    $scriptPath = $PSCommandPath

    $argList = @(
        '-NoExit'
        '-ExecutionPolicy', 'Bypass'
        '-File', $scriptPath
        '-JobsearchRoot', $paths.JobsearchRoot
        '-NoNewWindow'
    )

    Start-Process -FilePath $pwshExe -ArgumentList $argList -WorkingDirectory $paths.JobsearchRoot | Out-Null
    return
}

Start-GrokJobsearchSession
