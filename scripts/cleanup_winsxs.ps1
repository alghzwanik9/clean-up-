# Self-elevate to Administrator if needed
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Elevating privileges to Administrator..." -ForegroundColor Yellow
    Start-Process powershell.exe -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   WinStorageGuard - Deep WinSxS Component Store Cleanup" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[+] Running DISM Component Store Cleanup (/resetbase)..." -ForegroundColor Yellow
Write-Host "[!] This process removes superseded Windows components and can take several minutes." -ForegroundColor Gray
Write-Host ""

$cBefore = (Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'").FreeSpace

dism.exe /online /cleanup-image /startcomponentcleanup /resetbase

$cAfter = (Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'").FreeSpace
$freedGb = [math]::Round(($cAfter - $cBefore) / 1GB, 2)
$newFreeGb = [math]::Round($cAfter / 1GB, 2)

Write-Host ""
Write-Host "========================================================" -ForegroundColor Green
Write-Host "[+] WinSxS Cleanup Completed!" -ForegroundColor Green
Write-Host "    New Free Space on C: $newFreeGb GB (Freed ~$freedGb GB)" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
