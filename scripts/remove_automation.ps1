# WinStorageGuard - Remove Automated Schedule
$ErrorActionPreference = 'SilentlyContinue'

$taskName = "WinStorageGuard_AutoClean"
schtasks /delete /tn "$taskName" /f

Write-Host "[+] Automated Task '$taskName' removed." -ForegroundColor Green
