# job-chatgpt-render.ps1
# ChatGPT pipeline step 3: render resume + cover in one step from manual JSON artifacts.
#
# Usage:
#   .\job-chatgpt-render.ps1
#   .\job-chatgpt-render.ps1 -Version v1
#   .\job-chatgpt-render.ps1 -NoStrict

param(
    [string]$Version = "v1",
    [switch]$NoStrict,
    [switch]$NoNormalize
)

Set-Location $PSScriptRoot
. .\env_setter.ps1

$chatCachePath = ".job_cache_chatgpt.json"
if (-not (Test-Path -LiteralPath $chatCachePath)) {
    Write-Host "ERROR: No chatgpt cache found. Run .\job-chatgpt-check.ps1 then .\job-chatgpt-accept.ps1 first." -ForegroundColor Red
    exit 1
}

$cache = Get-Content -LiteralPath $chatCachePath | ConvertFrom-Json
$uuid = $cache.uuid_short
if (-not $uuid) {
    Write-Host "ERROR: Cache missing uuid_short." -ForegroundColor Red
    exit 1
}

$jobDir = Get-ChildItem data\jobs -Directory | Where-Object { $_.Name -like "*_$uuid*" } | Select-Object -First 1
if (-not $jobDir) {
    Write-Host "ERROR: Could not resolve job folder for UUID: $uuid" -ForegroundColor Red
    exit 1
}

$generated = Join-Path $jobDir.FullName "generated"
$resumeJson = Join-Path $generated "resume_intermediate_$Version.json"
$coverJson = Join-Path $generated "cover_intermediate_$Version.json"

$DownloadsPath = "D:\users\shareuser\Downloads"

if (-not (Test-Path -LiteralPath $DownloadsPath)) {
    Write-Host "ERROR: Downloads path not found: $DownloadsPath" -ForegroundColor Red
    exit 1
}

# Import all ChatGPT JSON artifacts from Downloads before validation/render.
$jsonCandidates = Get-ChildItem -LiteralPath $DownloadsPath -File -Filter "*.json" |
    Sort-Object LastWriteTime

if (-not $jsonCandidates) {
    Write-Host "ERROR: No .json files found in $DownloadsPath" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Imported from Downloads:" -ForegroundColor Yellow
foreach ($jsonFile in $jsonCandidates) {
    $dest = Join-Path $generated $jsonFile.Name
    Move-Item -LiteralPath $jsonFile.FullName -Destination $dest -Force
    Write-Host "- $($jsonFile.Name) -> $dest"
}

if (-not (Test-Path -LiteralPath $resumeJson)) {
    Write-Host "ERROR: Missing $resumeJson" -ForegroundColor Red
    exit 1
}
if ((Get-Item -LiteralPath $resumeJson).Length -eq 0) {
    Write-Host "ERROR: Resume JSON is empty: $resumeJson" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path -LiteralPath $coverJson)) {
    Write-Host "ERROR: Missing $coverJson" -ForegroundColor Red
    exit 1
}
if ((Get-Item -LiteralPath $coverJson).Length -eq 0) {
    Write-Host "ERROR: Cover JSON is empty: $coverJson" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== CHATGPT PIPELINE: STEP 3 / RENDER ===" -ForegroundColor Cyan
Write-Host "UUID   : $uuid"
Write-Host "Version: $Version"
Write-Host ""

$resumeArgs = @("scripts\05_render_resume.py", "--uuid", $uuid, "--version", $Version, "--all")
if (-not $NoNormalize) { $resumeArgs += "--normalize" }
python @resumeArgs
if ($LASTEXITCODE -ne 0) {
    Write-Host "Resume render failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

python scripts\08_render_cover_letter.py --uuid $uuid --version $Version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Cover render failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

# Optional PDF conversion for sites that require PDF uploads.
$docxTargets = @()
$resumeDocx = Join-Path $generated "resume.docx"
$resumeVersionedDocx = Join-Path $generated ("resume_{0}.docx" -f $Version)
$coverDocx = Join-Path $generated "cover.docx"

if (Test-Path -LiteralPath $resumeDocx) { $docxTargets += $resumeDocx }
if (Test-Path -LiteralPath $resumeVersionedDocx) { $docxTargets += $resumeVersionedDocx }
if (Test-Path -LiteralPath $coverDocx) { $docxTargets += $coverDocx }

if ($docxTargets.Count -gt 0) {
    $pdfTargets = @()
    foreach ($docxPath in $docxTargets) {
        $pdfTargets += [System.IO.Path]::ChangeExtension($docxPath, ".pdf")
    }

    python -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('docx2pdf') else 1)"
    $hasDocx2Pdf = ($LASTEXITCODE -eq 0)

    if ($hasDocx2Pdf) {
        Write-Host ""
        Write-Host "Converting DOCX to PDF..." -ForegroundColor Yellow
        foreach ($docxPath in $docxTargets) {
            $pdfPath = [System.IO.Path]::ChangeExtension($docxPath, ".pdf")
            $pyCmd = "from docx2pdf import convert; convert(r'''{0}''', r'''{1}''')" -f $docxPath, $pdfPath
            python -c $pyCmd
            if ($LASTEXITCODE -ne 0) {
                Write-Host "WARNING: PDF conversion failed for $docxPath" -ForegroundColor Yellow
            } else {
                Write-Host "PDF -> $pdfPath"
            }
        }
    } else {
        Write-Host ""
        Write-Host "WARNING: docx2pdf not installed; skipping PDF conversion." -ForegroundColor Yellow
        Write-Host "Install with: pip install docx2pdf" -ForegroundColor Yellow
    }

    Write-Host ""
    Write-Host "PDF output status:" -ForegroundColor Yellow
    foreach ($pdfPath in $pdfTargets) {
        if (Test-Path -LiteralPath $pdfPath) {
            Write-Host "OK      $pdfPath"
        } else {
            Write-Host "MISSING $pdfPath" -ForegroundColor Yellow
        }
    }
}

$qualityArgs = @("scripts\quality_check.py", "--uuid", $uuid, "--version", $Version)
if (-not $NoStrict) { $qualityArgs += "--strict" }
python @qualityArgs
if ($LASTEXITCODE -ne 0) {
    Write-Host "Quality check failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

$cache | Add-Member -NotePropertyName documents_ready -NotePropertyValue $true -Force
$cache | Add-Member -NotePropertyName render_version -NotePropertyValue $Version -Force
$cache | ConvertTo-Json | Set-Content -LiteralPath $chatCachePath

if (Test-Path -LiteralPath ".job_cache_v2.json") {
    $v2 = Get-Content -LiteralPath ".job_cache_v2.json" | ConvertFrom-Json
    $v2 | Add-Member -NotePropertyName documents_ready -NotePropertyValue $true -Force
    $v2 | Add-Member -NotePropertyName render_version -NotePropertyValue $Version -Force
    $v2 | ConvertTo-Json | Set-Content -LiteralPath ".job_cache_v2.json"
}

Write-Host ""
Write-Host "Render complete. Documents ready in: $generated" -ForegroundColor Green
Write-Host "Next: .\job-chatgpt-apply.ps1 -Method `"Dice`"" -ForegroundColor Yellow
