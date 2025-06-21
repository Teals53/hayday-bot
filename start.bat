@echo off
title Hayday Bot
echo ========================================
echo           Hayday Bot
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please run install.bat first
    pause
    exit /b 1
)

echo Checking ADB...
adb\adb.exe version >nul 2>&1
if errorlevel 1 (
    echo WARNING: ADB might not be working properly
    echo Make sure your device drivers are installed
    echo.
)

echo Starting Hayday Bot...
echo.
echo ========================================
echo      Application Starting...
echo ========================================
echo.
echo - Use the Connection tab to connect
echo - Configure your farm in Farm Config tab
echo - Start botting in Bot Control tab
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo           Error Occurred
    echo ========================================
    echo.
    echo The application encountered an error.
    echo Check the error message above.
    echo.
    echo Common solutions:
    echo 1. Run install.bat to install dependencies
    echo 2. Make sure Python 3.8+ is installed
    echo 3. Check that all required packages are installed
    echo.
    pause
) 