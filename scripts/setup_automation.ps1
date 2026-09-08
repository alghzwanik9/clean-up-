# WinStorageGuard - Automated Task Setup
$ErrorActionPreference = 'SilentlyContinue'

$taskName = "WinStorageGuard_AutoClean"
$scriptPath = "D:\DEV\ACTIVE\win-storage-guard\scripts\quick_clean.ps1"
$action = "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`""

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " SETTING UP AUTOMATED MAINTENANCE SCHEDULE" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Create weekly scheduled task (Every Sunday at 3:00 AM)
$cmd = "schtasks /create /tn `"$taskName`" /tr `"$action`" /sc WEEKLY /d SUN /st 03:00 /f /ru `"$env:USERNAME`""
Invoke-Expression $cmd

$query = schtasks /query /tn "$taskName" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[+] Success! Scheduled Task registered successfully." -ForegroundColor Green
    Write-Host "    Task Name : $taskName" -ForegroundColor Yellow
    Write-Host "    Schedule  : Weekly on Sundays at 03:00 AM" -ForegroundColor Yellow
    Write-Host "    Mode      : Silent (WindowStyle Hidden, zero interruption)" -ForegroundColor Yellow
} else {
    Write-Host "`n[!] Notice: If running without admin, creating task for current user..." -ForegroundColor Yellow
    schtasks /create /tn "$taskName" /tr "$action" /sc WEEKLY /d SUN /st 03:00 /f
}
