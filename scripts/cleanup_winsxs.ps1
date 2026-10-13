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

# Check for pending system reboot
$rebootKeys = @(
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending",
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired"
)
$pendingReboot = $false
foreach ($key in $rebootKeys) {
    if (Test-Path $key) {
        $pendingReboot = $true
        break
    }
}

if ($pendingReboot) {
    Write-Host "[!] WARNING: A Windows reboot is pending from a recent update." -ForegroundColor Yellow
    Write-Host "    DISM cleanup cannot proceed until the system is restarted." -ForegroundColor Red
    Write-Host "    Please restart your computer and run this cleanup again.`n" -ForegroundColor Yellow
    Write-Host "Press any key to exit..."
    try { $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") } catch { Pause }
    exit 1
}

Write-Host "[+] Running DISM Component Store Cleanup (/resetbase)..." -ForegroundColor Yellow
Write-Host "[!] Note: Superseded components will be permanently purged." -ForegroundColor Gray
Write-Host "[!] Existing updates will not be uninstallable after this process." -ForegroundColor Gray
Write-Host "[!] This operation typically takes 3-10 minutes. Please wait...`n" -ForegroundColor Gray

$cBefore = (Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'").FreeSpace

dism.exe /online /cleanup-image /startcomponentcleanup /resetbase
$dismExitCode = $LASTEXITCODE

$cAfter = (Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'").FreeSpace
$diffGb = [math]::Round(($cAfter - $cBefore) / 1GB, 2)
$freedGb = if ($diffGb -gt 0) { $diffGb } else { 0.0 }
$newFreeGb = [math]::Round($cAfter / 1GB, 2)

Write-Host ""
Write-Host "========================================================" -ForegroundColor $(if ($dismExitCode -eq 0) { "Green" } else { "Red" })
if ($dismExitCode -eq 0) {
    Write-Host "[+] WinSxS Cleanup Completed Successfully!" -ForegroundColor Green
    Write-Host "    Current Free Space on C: $newFreeGb GB (Freed ~$freedGb GB)" -ForegroundColor Green
} else {
    Write-Host "[-] DISM completed with exit code: $dismExitCode" -ForegroundColor Red
    Write-Host "    Some component store files could not be removed." -ForegroundColor Yellow
}
Write-Host "========================================================" -ForegroundColor $(if ($dismExitCode -eq 0) { "Green" } else { "Red" })
Write-Host ""

Write-Host "Press any key to exit..."
try {
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} catch {
    cmd.exe /c pause >nul
}
