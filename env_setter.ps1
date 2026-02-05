# env_setter.ps1 – Activate JobSearch venv + set helpful environment variables

# Adjust if your venv is elsewhere
$venvPath = "C:\py_venv\JobSearch"

# Activate venv
& "$venvPath\Scripts\Activate.ps1"

# Prepend our custom Python (in case activation didn't fully override)
#$env:PATH = "C:\pyver\py312;C:\pyver\py312\Scripts;" + $env:PATH

# Project-specific environment variables (expand later)
$env:PROJECT_ROOT = Convert-Path (Split-Path -Parent $MyInvocation.MyCommand.Path)   # or hardcode repo path
$env:PYTHONPATH   = "$env:PROJECT_ROOT\src;$env:PYTHONPATH"                        # if you use src/ layout later

# LLM / API related (fill in real values when ready – never commit keys!)
# $env:XAI_API_KEY         = "your-xai-key-here"
# $env:OPENAI_API_KEY      = "sk-..."           # fallback / comparison
# $env:ANTHROPIC_API_KEY   = "..."

# Data / storage paths (can point to local folders or later cloud)
$env:JOBS_DB_DIR    = "$env:PROJECT_ROOT\data\jobs"
$env:RESUMES_DIR    = "$env:PROJECT_ROOT\data\resumes"
$env:VECTOR_DB_PATH = "$env:PROJECT_ROOT\data\vectorstore"

# Optional: embeddings model / LLM model selection
$env:DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"   # light & fast local
$env:DEFAULT_LLM_PROVIDER     = "xai"                                     # or grok, openai, etc.

Write-Host "JobSearch environment activated ✓" -ForegroundColor Green
Write-Host "Python: $(python --version)"
Write-Host "Use deactivate to exit venv"