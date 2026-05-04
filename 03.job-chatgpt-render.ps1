# job-chatgpt-render.ps1
# ChatGPT pipeline step 3: render resume + cover in one step from manual JSON artifacts.
#
# Usage:
#   .\job-chatgpt-render.ps1
#   .\job-chatgpt-render.ps1 -Version v1
#   .\job-chatgpt-render.ps1 -NoStrict
#   .\job-chatgpt-render.ps1 -ApplyMethod "Dice"

param(
    [string]$Version = "v1",
    [switch]$NoStrict,
    [switch]$NoNormalize,
    [string]$ApplyMethod = "Auto",
    [string]$ApplyNotes = "Applied via chatGpt pipeline",
    [string]$ApplyDate = (Get-Date).ToString("yyyy-MM-dd"),
    [switch]$SkipIndexRefresh,
    [switch]$ClearCache
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

$metadataPath = Join-Path $jobDir.FullName "metadata.yaml"
if (-not (Test-Path -LiteralPath $metadataPath)) {
    Write-Host "ERROR: Missing metadata file: $metadataPath" -ForegroundColor Red
    exit 1
}

$generated = Join-Path $jobDir.FullName "generated"
$resumeJson = Join-Path $generated "resume_intermediate_$Version.json"
$coverJson = Join-Path $generated "cover_intermediate_$Version.json"
$resumeJsonAlt = Join-Path $generated ("resume_intermediate_{0}.json" -f ($Version -replace "v", "v_"))
$coverJsonAlt = Join-Path $generated ("cover_intermediate_{0}.json" -f ($Version -replace "v", "v_"))

$DownloadsPath = "D:\users\shareuser\Downloads"

if (-not (Test-Path -LiteralPath $DownloadsPath)) {
    Write-Host "ERROR: Downloads path not found: $DownloadsPath" -ForegroundColor Red
    exit 1
}

# Import candidate JSON artifacts from Downloads in a non-destructive way first.
$jsonCandidates = Get-ChildItem -LiteralPath $DownloadsPath -File -Filter "*intermediate*.json" |
    Sort-Object LastWriteTime

if (-not $jsonCandidates) {
    Write-Host "WARNING: No *intermediate*.json files found in $DownloadsPath; using existing generated files only." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Imported from Downloads (copy, non-destructive):" -ForegroundColor Yellow
foreach ($jsonFile in $jsonCandidates) {
    $dest = Join-Path $generated $jsonFile.Name
    Copy-Item -LiteralPath $jsonFile.FullName -Destination $dest -Force
    Write-Host "- $($jsonFile.Name) -> $dest"
}

# Resolve accepted filename variants.
if ((Test-Path -LiteralPath $resumeJsonAlt) -and ((Get-Item -LiteralPath $resumeJsonAlt).Length -gt 0)) {
    Copy-Item -LiteralPath $resumeJsonAlt -Destination $resumeJson -Force
}
if ((Test-Path -LiteralPath $coverJsonAlt) -and ((Get-Item -LiteralPath $coverJsonAlt).Length -gt 0)) {
    Copy-Item -LiteralPath $coverJsonAlt -Destination $coverJson -Force
}

if (-not (Test-Path -LiteralPath $resumeJson)) {
    Write-Host "ERROR: Missing resume JSON. Expected one of:" -ForegroundColor Red
    Write-Host "  - $resumeJson" -ForegroundColor Red
    Write-Host "  - $resumeJsonAlt" -ForegroundColor Red
    exit 1
}
if ((Get-Item -LiteralPath $resumeJson).Length -eq 0) {
    Write-Host "ERROR: Resume JSON is empty: $resumeJson" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path -LiteralPath $coverJson)) {
    Write-Host "ERROR: Missing cover JSON. Expected one of:" -ForegroundColor Red
    Write-Host "  - $coverJson" -ForegroundColor Red
    Write-Host "  - $coverJsonAlt" -ForegroundColor Red
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

# Inline step 4: apply/update tracking.
$resolvedMethod = $ApplyMethod
if ($resolvedMethod -eq "Auto") {
    $envSource = [string]$env:JOB_SOURCE
    if (-not [string]::IsNullOrWhiteSpace($envSource)) {
        $resolvedMethod = $envSource.Trim()
    } else {
    $hint = ""
    if ($cache.PSObject.Properties.Name -contains "source_hint") {
        $hint = [string]$cache.source_hint
    }
    if (-not [string]::IsNullOrWhiteSpace($hint)) {
        $resolvedMethod = $hint.Trim()
    } else {
        $detectedSource = python -c "from pathlib import Path; import yaml, re; p=Path(r'$jobDir'); m=Path(r'$metadataPath'); d=yaml.safe_load(m.read_text(encoding='utf-8')) if m.exists() else {}; d=d or {}; src=str(d.get('source') or '').strip().lower(); orig=str(d.get('original_filename') or '').strip().lower(); texts=[]; 
for c in [p/'raw'/'job_description.md', p/'raw'/'raw_intake.md', p/'clipboard_intake.md']: 
    if c.exists(): texts.append(c.read_text(encoding='utf-8', errors='ignore')[:10000].lower());
blob='\n'.join(texts); 
def pick():
    if src:
        if 'dice' in src: return 'Dice'
        if 'indeed' in src: return 'Indeed'
        if 'linkedin' in src: return 'LinkedIn'
        if 'greenhouse' in src: return 'Company Site'
        if 'workday' in src: return 'Company Site'
        return d.get('source')
    if 'dice' in orig or 'dice.com' in orig: return 'Dice'
    if 'indeed' in orig or 'indeed.com' in orig: return 'Indeed'
    if 'linkedin' in orig: return 'LinkedIn'
    if 'dice.com' in blob or re.search(r'\\bdice\\b', blob): return 'Dice'
    if 'indeed.com' in blob or re.search(r'\\bindeed\\b', blob): return 'Indeed'
    if 'linkedin.com' in blob or re.search(r'\\blinkedin\\b', blob): return 'LinkedIn'
    if 'greenhouse.io' in blob or 'myworkdayjobs.com' in blob or 'workday' in blob: return 'Company Site'
    return 'Dice'
print(pick())"
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($detectedSource)) {
            Write-Host "WARNING: Could not auto-detect source; defaulting to Dice." -ForegroundColor Yellow
            $resolvedMethod = "Dice"
        } else {
            $resolvedMethod = $detectedSource.Trim()
        }
    }
    }
}

# Final normalization for casing/aliases.
$lm = $resolvedMethod.ToLowerInvariant()
if ($lm -match "dice") { $resolvedMethod = "Dice" }
elseif ($lm -match "indeed") { $resolvedMethod = "Indeed" }
elseif ($lm -match "linkedin") { $resolvedMethod = "LinkedIn" }

Write-Host ""
Write-Host "=== CHATGPT PIPELINE: STEP 4 / APPLY ===" -ForegroundColor Cyan
Write-Host "UUID  : $uuid"
Write-Host "Method: $resolvedMethod"
Write-Host "Date  : $ApplyDate"
Write-Host ""

python scripts\09_update_application_status.py --uuid $uuid apply `
    --date $ApplyDate `
    --method $resolvedMethod `
    --notes $ApplyNotes

if ($LASTEXITCODE -ne 0) {
    Write-Host "Apply update failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

$indexRefreshOk = $true
if (-not $SkipIndexRefresh) {
    Write-Host ""
    Write-Host "Refreshing duplicate-check index..." -ForegroundColor Yellow
    $env:PYTHONIOENCODING = "utf-8"
    python -m scripts.utils.build_job_index --rebuild
    if ($LASTEXITCODE -ne 0) {
        $indexRefreshOk = $false
        Write-Host "WARNING: Application saved, but index refresh failed. Run manually:" -ForegroundColor Yellow
        Write-Host "python -m scripts.utils.build_job_index --rebuild" -ForegroundColor Yellow
    } else {
        Write-Host "Index refreshed successfully." -ForegroundColor Green
    }
}

$cache | Add-Member -NotePropertyName applied -NotePropertyValue $true -Force
$cache | Add-Member -NotePropertyName applied_date -NotePropertyValue $ApplyDate -Force
$cache | Add-Member -NotePropertyName applied_method -NotePropertyValue $resolvedMethod -Force
$cache | Add-Member -NotePropertyName index_refreshed_after_apply -NotePropertyValue $indexRefreshOk -Force

if ($ClearCache) {
    Remove-Item -LiteralPath $chatCachePath -ErrorAction SilentlyContinue
} else {
    $cache | ConvertTo-Json | Set-Content -LiteralPath $chatCachePath
}

# Optional cleanup: remove copied source artifacts from Downloads only after full success.
foreach ($jsonFile in $jsonCandidates) {
    Remove-Item -LiteralPath $jsonFile.FullName -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Render+Apply complete. Documents ready in: $generated" -ForegroundColor Green
if ($ClearCache) {
    Write-Host "Application recorded. chatgpt cache cleared." -ForegroundColor Green
} else {
    Write-Host "Application recorded. chatgpt cache retained." -ForegroundColor Green
}
