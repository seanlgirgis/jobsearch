param(
  [string]$LogRoot = "C:\ProgramData\DriveMaintenance\logs"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $LogRoot)) {
  New-Item -ItemType Directory -Path $LogRoot -Force | Out-Null
}

$stamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$logFile = Join-Path $LogRoot "drive_maintenance_$stamp.log"

Start-Transcript -Path $logFile -Append | Out-Null

try {
  Write-Host "=== Drive maintenance started at $(Get-Date -Format s) ==="

  Write-Host "\n--- Volume health snapshot ---"
  Get-Volume -DriveLetter C,D | Select-Object DriveLetter, FileSystemLabel, HealthStatus, SizeRemaining, Size | Format-Table -AutoSize

  Write-Host "\n--- Physical disk health snapshot ---"
  Get-PhysicalDisk | Select-Object FriendlyName, MediaType, HealthStatus, OperationalStatus, Size | Format-Table -AutoSize

  Write-Host "\n--- C: SSD optimize (retrim/optimize) ---"
  defrag C: /L /O

  Write-Host "\n--- D: HDD optimize (defrag) ---"
  defrag D: /O

  Write-Host "\n--- Online filesystem scan ---"
  chkdsk C: /scan
  chkdsk D: /scan

  Write-Host "\n=== Drive maintenance completed at $(Get-Date -Format s) ==="
}
catch {
  Write-Error "Drive maintenance failed: $($_.Exception.Message)"
  throw
}
finally {
  Stop-Transcript | Out-Null
}
