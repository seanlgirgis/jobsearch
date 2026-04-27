param(
    [Parameter(Mandatory=$true)][string]$Intake,
    [string]$Company = "Unknown",
    [string]$Role = "Unknown Role",
    [string]$Location = "Unknown",
    [switch]$NoCopy
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$dataRoot = Join-Path $repoRoot "data"
$jobsRoot = Join-Path $dataRoot "jobs"

if (-not (Test-Path $jobsRoot)) {
    New-Item -ItemType Directory -Path $jobsRoot -Force | Out-Null
}

$resolvedIntake = Resolve-Path -LiteralPath $Intake -ErrorAction Stop
$intakePath = $resolvedIntake.Path

$existing = Get-ChildItem -Path $jobsRoot -Directory -ErrorAction SilentlyContinue
$maxSeq = 0
foreach ($dir in $existing) {
    if ($dir.Name -match "^(\d{5})_") {
        $seq = [int]$Matches[1]
        if ($seq -gt $maxSeq) { $maxSeq = $seq }
    }
}

$nextSeq = $maxSeq + 1
$uuid = [guid]::NewGuid().ToString()
$uuid8 = $uuid.Substring(0, 8)
$jobId = ("{0:D5}_{1}" -f $nextSeq, $uuid8)

$jobDir = Join-Path $jobsRoot $jobId
$rawDir = Join-Path $jobDir "raw"
$generatedDir = Join-Path $jobDir "generated"
$scoreDir = Join-Path $jobDir "score"
$tailoredDir = Join-Path $jobDir "tailored"
$researchDir = Join-Path $jobDir "research"

New-Item -ItemType Directory -Path $jobDir -Force | Out-Null
New-Item -ItemType Directory -Path $rawDir -Force | Out-Null
New-Item -ItemType Directory -Path $generatedDir -Force | Out-Null
New-Item -ItemType Directory -Path $scoreDir -Force | Out-Null
New-Item -ItemType Directory -Path $tailoredDir -Force | Out-Null
New-Item -ItemType Directory -Path $researchDir -Force | Out-Null

$jobIntakePath = Join-Path $jobDir "intake.md"
$rawIntakePath = Join-Path $rawDir "raw_intake.md"

if (-not $NoCopy) {
    Copy-Item -LiteralPath $intakePath -Destination $jobIntakePath -Force
    Copy-Item -LiteralPath $intakePath -Destination $rawIntakePath -Force
} else {
    "# Intake Placeholder" | Set-Content -Path $jobIntakePath -Encoding UTF8
    "# Raw Intake Placeholder" | Set-Content -Path $rawIntakePath -Encoding UTF8
}

$timestamp = (Get-Date).ToString("s")
$metadataPath = Join-Path $jobDir "metadata.yaml"

$metadata = @"
uuid: $uuid
job_id: $jobId
company: "$Company"
role: "$Role"
location: "$Location"
status: NEW
application:
  applied: false
  applied_date: null
  applied_method: null
  history:
    - timestamp: "$timestamp"
      event: "CREATED"
      note: "Job folder scaffolded via process_job_direct.ps1"
"@

$metadata | Set-Content -Path $metadataPath -Encoding UTF8

Write-Host "Created job scaffold:" -ForegroundColor Green
Write-Host "  job_id: $jobId"
Write-Host "  uuid:   $uuid"
Write-Host "  folder: $(Resolve-Path $jobDir)"
