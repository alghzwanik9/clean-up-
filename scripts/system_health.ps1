# WinStorageGuard - Windows System File & Component Store Health Check
# Elevates to Administrator if needed
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Elevating privileges to Administrator for system file check..." -ForegroundColor Yellow
    Start-Process powershell.exe -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   WinStorageGuard - Windows System Health & Repair      " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[1/2] Checking Windows Component Store Health (DISM)..." -ForegroundColor Yellow
dism.exe /online /cleanup-image /checkhealth

Write-Host ""
Write-Host "[2/2] Running System File Checker (SFC scan)..." -ForegroundColor Yellow
Write-Host "[!] Scanning protected system files for corruption..." -ForegroundColor Gray
sfc /scannow

Write-Host ""
Write-Host "========================================================" -ForegroundColor Green
Write-Host "   [+] System Health Check & Repair Completed!           " -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
