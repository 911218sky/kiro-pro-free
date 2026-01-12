@echo off
REM Kiro Bypass Tool - Windows Start Script

echo ========================================
echo Kiro IDE Bypass Tool
echo ========================================
echo.

REM Set environment path
set ENV_PATH=%~dp0kiro_env

REM Check if environment exists
if not exist "%ENV_PATH%" (
    echo [ERROR] Conda environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate conda environment
call conda activate "%ENV_PATH%"
if errorlevel 1 (
    echo [ERROR] Failed to activate conda environment
    pause
    exit /b 1
)

echo [OK] Environment activated
python --version
echo.

REM Run main script
python kiro_main.py

REM Deactivate environment on exit
call conda deactivate

pause
