@echo off
title WinStorageGuard Launcher
color 0B
echo ========================================================
echo         WinStorageGuard - System Storage Optimizer      
echo ========================================================
echo.
echo [1] Full Disk Analysis (فحص وتحليل القرص)
echo [2] Safe Cache Cleanup (تنظيف الكاش فوراً)
echo [3] Reset Windows Update Cache (إصلاح وتصفير كاش التحديثات)
echo [4] Deep WinSxS Cleanup - Admin (تنظيف ملفات النظام القديمة عبر DISM)
echo [5] Setup Weekly Automation (تفعيل الجدولة والتنظيف التلقائي أسبوعياً)
echo [6] Check Automation Status (فحص حالة الأتمتة المجدولة)
echo [7] Remove Automation Schedule (إلغاء الجدولة التلقائية)
echo [8] Exit
echo.
set /p choice="Enter option [1-8]: "

if "%choice%"=="1" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\analyze_disk.ps1"
    pause
    exit /b
)
if "%choice%"=="2" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\quick_clean.ps1"
    pause
    exit /b
)
if "%choice%"=="3" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\reset_windows_update.ps1"
    pause
    exit /b
)
if "%choice%"=="4" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\cleanup_winsxs.ps1"
    exit /b
)
if "%choice%"=="5" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\setup_automation.ps1"
    pause
    exit /b
)
if "%choice%"=="6" (
    python "%~dp0storage_guard.py" --schedule-status
    pause
    exit /b
)
if "%choice%"=="7" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\remove_automation.ps1"
    pause
    exit /b
)
