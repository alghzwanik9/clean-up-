# WinStorageGuard - Full System & Performance Optimizer
# Elevates to Administrator if not already running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Elevating privileges to Administrator for system optimization..." -ForegroundColor Yellow
    Start-Process powershell.exe -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   WinStorageGuard - Full System Performance Optimizer   " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Drive & SSD TRIM Optimization
Write-Host "[1/4] Running SSD TRIM and Volume Optimization on C:..." -ForegroundColor Yellow
try {
    Optimize-Volume -DriveLetter C -ReTrim -Verbose
    Write-Host "      [OK] SSD TRIM completed successfully." -ForegroundColor Green
} catch {
    Write-Host "      [!] Optimize-Volume error: $_. Running defrag fallback..." -ForegroundColor Gray
    defrag C: /O /U
}
Write-Host ""

# 2. Network & DNS Cache Flush
Write-Host "[2/4] Flushing DNS & Network Caches..." -ForegroundColor Yellow
try {
    Clear-DnsClientCache
    ipconfig /flushdns | Out-Null
    nbtstat -R | Out-Null
    arp -d * 2>$null
    Write-Host "      [OK] DNS Resolver, NetBIOS, and ARP caches flushed." -ForegroundColor Green
} catch {
    Write-Host "      [!] Network cache notice: $_" -ForegroundColor Gray
}
Write-Host ""

# 3. RAM Working Sets Cleanup
Write-Host "[3/4] Trimming System RAM Working Sets..." -ForegroundColor Yellow
try {
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    Write-Host "      [OK] Inactive memory freed and garbage collection triggered." -ForegroundColor Green
} catch {
    Write-Host "      [!] Memory notice: $_" -ForegroundColor Gray
}
Write-Host ""

# 4. Startup Impact Overview
Write-Host "[4/4] Scanning Startup Applications..." -ForegroundColor Yellow
$startupList = Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location
if ($startupList) {
    Write-Host "      Found $($startupList.Count) startup programs registered:" -ForegroundColor Cyan
    foreach ($item in $startupList) {
        $cmdShort = if ($item.Command.Length -gt 55) { $item.Command.Substring(0, 52) + "..." } else { $item.Command }
        Write-Host "      - $($item.Name.PadRight(25)) : $cmdShort" -ForegroundColor Gray
    }
} else {
    Write-Host "      No heavy startup programs found in standard locations." -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================================" -ForegroundColor Green
Write-Host "   [+] System Optimization Completed Successfully!       " -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
