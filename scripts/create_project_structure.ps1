# create_project_structure.ps1
# Creates the proposed folder layout for the jobsearch RAG / second-brain project
# Idempotent → safe to run multiple times

$root = Get-Location
Write-Host "Creating project structure under: $root" -ForegroundColor Cyan

# Helper function
function New-FolderSafe {
    param ([string]$Path)
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "Created: $Path" -ForegroundColor Green
    } else {
        Write-Host "Already exists: $Path" -ForegroundColor DarkGray
    }
}

# ── Top-level folders ────────────────────────────────────────────────
$folders = @(
    "src",
    "data",
    "data\jobs",
    "data\resumes",
    "data\vectorstore",
    "notebooks",
    ".grok",
    "docs",           # using docs/ instead of startingDocs/ going forward
    "tests"
)

foreach ($f in $folders) {
    New-FolderSafe (Join-Path $root $f)
}

# ── Empty data subfolders need .gitkeep so Git tracks them ───────────
$gitkeeps = @(
    "data\jobs\.gitkeep",
    "data\resumes\.gitkeep",
    "data\vectorstore\.gitkeep"
)

foreach ($gk in $gitkeeps) {
    $full = Join-Path $root $gk
    if (-not (Test-Path $full)) {
        New-Item -ItemType File -Path $full -Force | Out-Null
        Write-Host "Added placeholder: $gk" -ForegroundColor Green
    }
}

# ── .grok/rules.md  (only if missing) ────────────────────────────────
$grokRulesPath = Join-Path $root ".grok\rules.md"
if (-not (Test-Path $grokRulesPath)) {
    @"
# .grok/rules.md – Our working agreement with Grok

- All code & chat stays public in this repo
- Prefer modular, iterative commits (small PRs or direct pushes)
- Use xAI models / Grok API when possible
- Responses should be code-first when implementing features
- Keep building toward full RAG + second-brain capabilities
- No secrets, API keys, personal data or large binaries in repo
- Ask clarifying questions if scope is unclear
- Commit messages: keep descriptive, use conventional style when possible

Last updated: $(Get-Date -Format "yyyy-MM-dd")
"@ | Out-File -FilePath $grokRulesPath -Encoding utf8
    Write-Host "Created: .grok/rules.md" -ForegroundColor Green
} else {
    Write-Host "Already exists: .grok/rules.md (not overwritten)" -ForegroundColor DarkGray
}

# ── Optional: empty starter files in src/ and notebooks/ ─────────────
$starters = @(
    "src\__init__.py",
    "src\main.py",              # or app.py later
    "notebooks\00_exploration.ipynb"   # placeholder name
)

foreach ($s in $starters) {
    $full = Join-Path $root $s
    if (-not (Test-Path $full)) {
        New-Item -ItemType File -Path $full -Force | Out-Null
        Write-Host "Created empty starter: $s" -ForegroundColor Green
    }
}

# ── Reminders for files we don't auto-create/overwrite ───────────────
Write-Host "`nSummary:" -ForegroundColor Cyan
Write-Host "Structure created (or already present)."
Write-Host "Files NOT touched (manual update recommended if needed):"
Write-Host "  - requirements.txt"
Write-Host "  - .gitignore"
Write-Host "  - env_setter.ps1"
Write-Host "  - README.md"
Write-Host "  - startingDocs/ contents (consider moving to docs/)"

Write-Host "`nNext suggested steps:"
Write-Host "1. git add . && git commit -m 'feat: initialize project folder structure'"
Write-Host "2. Update README.md with the latest quick-start instructions"
Write-Host "3. Start defining data models in src/ (Job posting, Resume, etc.)"
Write-Host "   or create first notebook for playing with embeddings"

Write-Host "`nDone ✓" -ForegroundColor Green