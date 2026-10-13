@echo off
chcp 65001 >nul
title WinStorageGuard - Windows Storage ^& System Performance Optimizer
color 0B

:MENU
cls
echo ===================================================================
echo     WinStorageGuard - Windows Storage ^& Performance Optimizer    
echo ===================================================================
echo.
echo  [1]  Full Disk Analysis            (فحص وتحليل القرص C:)
echo  [2]  Safe Cache Cleanup            (تنظيف الكاش والملفات المؤقتة فوراً)
echo  [3]  Full System Optimization      (تحسين أداء الجهاز، SSD TRIM، وكاش الشبكة والرام)
echo  [4]  Startup Apps Impact           (رصد البرامج التي تبطئ إقلاع الويندوز)
echo  [5]  System Health Check ^& SFC     (فحص وإصلاح ملفات النظام عبر SFC/DISM)
echo  [6]  Deep WinSxS Cleanup - Admin   (تنظيف ملفات مكونات النظام القديمة)
echo  [7]  Reset Windows Update Cache    (إصلاح وتصفير كاش التحديثات المعلقة)
echo  [8]  Setup Weekly Automation       (تفعيل الجدولة التلقائية أسبوعياً)
echo  [9]  Check Automation Status       (فحص حالة الأتمتة المجدولة)
echo  [10] Remove Automation Schedule     (إلغاء الجدولة التلقائية)
echo  [11] Exit                          (خروج)
echo.
echo ===================================================================
set /p choice="Enter your choice [1-11]: "

if "%choice%"=="1" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\analyze_disk.ps1"
    pause
    goto MENU
)
if "%choice%"=="2" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\quick_clean.ps1"
    pause
    goto MENU
)
if "%choice%"=="3" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\optimize_system.ps1"
    pause
    goto MENU
)
if "%choice%"=="4" (
    python "%~dp0storage_guard.py" --startup
    pause
    goto MENU
)
if "%choice%"=="5" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\system_health.ps1"
    pause
    goto MENU
)
if "%choice%"=="6" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\cleanup_winsxs.ps1"
    goto MENU
)
if "%choice%"=="7" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\reset_windows_update.ps1"
    pause
    goto MENU
)
if "%choice%"=="8" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\setup_automation.ps1"
    pause
    goto MENU
)
if "%choice%"=="9" (
    python "%~dp0storage_guard.py" --schedule-status
    pause
    goto MENU
)
if "%choice%"=="10" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\remove_automation.ps1"
    pause
    goto MENU
)
if "%choice%"=="11" (
    exit /b
)

echo Invalid choice, please try again.
pause
goto MENU
