# WinStorageGuard - Fast Safe Cleaner
$ErrorActionPreference = 'SilentlyContinue'

$initial = (Get-Volume -DriveLetter C).SizeRemaining

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " WinStorageGuard: FAST CLEANER RUNNING" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

Clear-RecycleBin -DriveLetter C -Force -ErrorAction SilentlyContinue

$targets = @(
    "$env:TEMP",
    "C:\Windows\Temp",
    "C:\Users\$env:USERNAME\AppData\Local\npm-cache",
    "C:\Users\$env:USERNAME\AppData\Local\pip\cache",
    "C:\Users\$env:USERNAME\AppData\Local\pypoetry\cache",
    "C:\Users\$env:USERNAME\AppData\Local\ms-playwright",
    "C:\Users\$env:USERNAME\AppData\Local\.dartServer",
    "C:\Users\$env:USERNAME\AppData\Local\Pub\Cache",
    "C:\Users\$env:USERNAME\AppData\Roaming\Code\CachedExtensionVSIXs",
    "C:\Users\$env:USERNAME\AppData\Roaming\Cursor\CachedExtensionVSIXs",
    "C:\Users\$env:USERNAME\.gradle\caches",
    "C:\Users\$env:USERNAME\.gradle\daemon"
)

foreach ($t in $targets) {
    if (Test-Path -LiteralPath $t) {
        Remove-Item -LiteralPath $t -Recurse -Force -ErrorAction SilentlyContinue
    }
}

$final = (Get-Volume -DriveLetter C).SizeRemaining
$freedGB = [math]::Round(($final - $initial) / 1GB, 2)
$currentFreeGB = [math]::Round($final / 1GB, 2)

Write-Host "`n[+] Cleanup Complete!" -ForegroundColor Green
Write-Host "    Freed Space: $freedGB GB" -ForegroundColor Green
Write-Host "    Current Free Space on C: $currentFreeGB GB" -ForegroundColor Green
