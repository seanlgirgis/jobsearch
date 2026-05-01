param(
    [string]$FromDir = "D:\Users\shareuser\Downloads"
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$dest = Join-Path $repoRoot "docs\chatgpt_projects\MyFuture"
New-Item -ItemType Directory -Force -Path $dest | Out-Null

$files = @(
    'source_of_truth.json',
    'AboutMe.txt',
    'SomeIdeas.txt',
    'pipeline-guide.md',
    'PIPELINE_RUNBOOK.md',
    'CHATGPT_HANDOFF_JOBSEARCH.md',
    'jobsearch-project-analysis.md'
)

foreach ($f in $files) {
    $src = Join-Path $FromDir $f
    if (Test-Path -LiteralPath $src) {
        Copy-Item -LiteralPath $src -Destination (Join-Path $dest $f) -Force
        Write-Host "Synced: $f" -ForegroundColor Green
    } else {
        Write-Host "Missing in source folder: $f" -ForegroundColor Yellow
    }
}

$registry = Join-Path $dest "MYFUTURE_SOURCE_REGISTRY.md"
if (Test-Path -LiteralPath $registry) {
    Add-Content -LiteralPath $registry -Value "- $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): Synced from $FromDir"
}

Write-Host "Done. Target: $dest" -ForegroundColor Cyan
