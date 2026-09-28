# Create a timestamped Indeed inbox file and open it for paste.
$root = Split-Path -Parent $PSScriptRoot
$inbox = Join-Path $root "search_bots\sites\indeed\inbox"
$template = Join-Path $root "search_bots\sites\indeed\CAPTURE_TEMPLATE.md"
New-Item -ItemType Directory -Force -Path $inbox | Out-Null
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$dest = Join-Path $inbox "capture_$stamp.md"
Copy-Item -LiteralPath $template -Destination $dest -Force
Write-Host "Created: $dest"
Write-Host "Paste the Indeed URL + full JD, save, close, then:"
Write-Host "  .\search_bots\run_indeed.ps1"
if (Get-Command npp -ErrorAction SilentlyContinue) {
    npp $dest
} elseif (Test-Path "$env:ProgramFiles\Notepad++\notepad++.exe") {
    & "$env:ProgramFiles\Notepad++\notepad++.exe" $dest
} else {
    notepad $dest
}
