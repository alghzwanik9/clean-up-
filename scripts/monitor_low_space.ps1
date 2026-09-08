# WinStorageGuard - Smart Storage Monitor
$ErrorActionPreference = 'SilentlyContinue'

$cDrive = Get-Volume -DriveLetter C
$freeGB = [math]::Round($cDrive.SizeRemaining / 1GB, 2)
$pctFree = [math]::Round(($cDrive.SizeRemaining / $cDrive.Size) * 100, 2)

# If free space is less than 10 GB or less than 10%, trigger silent clean
if ($freeGB -lt 10.0 -or $pctFree -lt 10.0) {
    Write-Host "[!] C: Drive is running low on space ($freeGB GB / $pctFree% Free). Triggering automated cleanup..." -ForegroundColor Yellow
    & "D:\DEV\ACTIVE\win-storage-guard\scripts\quick_clean.ps1"
} else {
    Write-Host "[OK] C: Drive storage healthy ($freeGB GB / $pctFree% Free)." -ForegroundColor Green
}
