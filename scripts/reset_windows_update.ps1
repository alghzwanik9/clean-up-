# WinStorageGuard - Windows Update Reset Script
$ErrorActionPreference = 'SilentlyContinue'

Write-Host "Stopping Windows Update services..." -ForegroundColor Yellow
Stop-Service -Name wuauserv, bits, dosvc, cryptsvc -Force -ErrorAction SilentlyContinue

Write-Host "Clearing stuck downloads in SoftwareDistribution..." -ForegroundColor Yellow
$dl = "C:\Windows\SoftwareDistribution\Download"
if (Test-Path -LiteralPath $dl) {
    Get-ChildItem -LiteralPath $dl -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "Restarting Windows Update services..." -ForegroundColor Yellow
Start-Service -Name cryptsvc, bits, wuauserv, dosvc -ErrorAction SilentlyContinue

Write-Host "Windows Update cache reset successfully." -ForegroundColor Green
