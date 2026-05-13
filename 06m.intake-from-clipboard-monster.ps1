<#
.SYNOPSIS
Create intake\intake.md from highlighted clipboard text for Monster jobs.

.DESCRIPTION
Reads clipboard text and rewrites intake\intake.md with this layout:
line 1: Monster.com
line 2-4: blank
line 5+: clipboard content

.EXAMPLE
.\06m.intake-from-clipboard-monster.ps1
#>

Set-Location $PSScriptRoot

function Get-ClipboardTextSafe {
    try {
        $t = Get-Clipboard -TextFormatType Text -Raw -ErrorAction Stop
        if (-not [string]::IsNullOrWhiteSpace($t)) { return $t }
    } catch {}

    try {
        $arr = Get-Clipboard -TextFormatType Text -ErrorAction Stop
        if ($arr) {
            $joined = ($arr -join "`n")
            if (-not [string]::IsNullOrWhiteSpace($joined)) { return $joined }
        }
    } catch {}

    try {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop | Out-Null
        if ([System.Windows.Forms.Clipboard]::ContainsText()) {
            $winTxt = [System.Windows.Forms.Clipboard]::GetText()
            if (-not [string]::IsNullOrWhiteSpace($winTxt)) { return $winTxt }
        }
    } catch {}

    return ""
}

$clipboardText = Get-ClipboardTextSafe
if ([string]::IsNullOrWhiteSpace($clipboardText)) {
    Write-Host "ERROR: Clipboard has no text. After highlighting in browser, press Ctrl+C, then rerun this script." -ForegroundColor Red
    exit 1
}

$intakeDir = "intake"
if (-not (Test-Path -LiteralPath $intakeDir)) {
    New-Item -ItemType Directory -Path $intakeDir | Out-Null
}

$intakePath = Join-Path $intakeDir "intake.md"

# Build file so clipboard text begins at line 5.
$content = @(
    "Monster.com",
    "",
    "",
    "",
    $clipboardText.Trim()
)

Set-Content -LiteralPath $intakePath -Value $content -Encoding utf8

Write-Host ""
Write-Host "Created: $intakePath" -ForegroundColor Green
Write-Host "Source header set to: Monster.com" -ForegroundColor Green
Write-Host "Clipboard content starts at line 5." -ForegroundColor Green
