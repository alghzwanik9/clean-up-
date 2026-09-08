# WinStorageGuard - PowerShell Disk Analyzer
$ErrorActionPreference = 'SilentlyContinue'

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " WinStorageGuard: DRIVE C: & D: CAPACITY" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Get-Volume | Where-Object { $_.DriveLetter -in @('C', 'D') } | Select-Object DriveLetter, FileSystemLabel,
    @{N='SizeGB';E={[math]::Round($_.Size/1GB, 2)}},
    @{N='FreeGB';E={[math]::Round($_.SizeRemaining/1GB, 2)}},
    @{N='UsedGB';E={[math]::Round(($_.Size - $_.SizeRemaining)/1GB, 2)}},
    @{N='PercentFree';E={[math]::Round(($_.SizeRemaining / $_.Size) * 100, 2)}} | Format-Table -AutoSize

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " TOP USER DIRECTORIES (C:\Users\$env:USERNAME)" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

$userDirs = Get-ChildItem -LiteralPath "C:\Users\$env:USERNAME" -Force -Directory
$results = @()
foreach ($d in $userDirs) {
    $cmdOut = cmd.exe /c "robocopy `"$($d.FullName)`" `"$env:TEMP\null`" /L /E /BYTES /NFL /NDL /NJH /R:0 /W:0 /XJ /MT:32 2>nul"
    $bytes = 0
    foreach ($l in $cmdOut) {
        if ($l -match 'Bytes\s*:\s*(\d+)') {
            $bytes = [int64]$matches[1]
            break
        }
    }
    $sizeGB = [math]::Round($bytes / 1GB, 2)
    if ($sizeGB -gt 0.2) {
        $results += [PSCustomObject]@{
            Folder = $d.Name
            SizeGB = $sizeGB
            Path = $d.FullName
        }
    }
}
$results | Sort-Object SizeGB -Descending | Format-Table -AutoSize
