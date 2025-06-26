@echo off
echo ========================================
echo       Hayday Bot Installation
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.13+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found!
echo.

echo Installing required packages from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo.
echo ========================================
echo     Installation Complete!
echo ========================================
echo.

echo Testing ADB connection...
adb\adb.exe version >nul 2>&1
if errorlevel 1 (
    echo WARNING: ADB test failed. Make sure your device drivers are installed.
) else (
    echo ADB is working!
)

echo.
echo ========================================
echo           Setup Instructions
echo ========================================
echo.
echo 1. Add template images to the templates folder:
echo    - Decoration images in templates\decorations\
echo 2. Run start.bat to launch the application
echo.
echo Installation complete! Press any key to exit...
pause >nul 