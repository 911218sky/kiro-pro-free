@echo off
REM Kiro Bypass Tool - Windows Setup Script (Conda)

echo ========================================
echo Kiro IDE Bypass Tool - Setup (Conda)
echo ========================================
echo.

REM Check conda installation
where conda >nul 2>&1
if errorlevel 1 (
    echo [INFO] Conda not found, attempting to install via winget...
    echo.
    
    REM Check winget
    where winget >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] winget is not available
        echo Please install winget from Microsoft Store or manually install Miniconda
        echo https://docs.conda.io/en/latest/miniconda.html
        pause
        exit /b 1
    )
    
    echo Installing Miniconda via winget...
    winget install -e --id Anaconda.Miniconda3 --accept-package-agreements --accept-source-agreements
    if errorlevel 1 (
        echo [ERROR] Failed to install Miniconda
        pause
        exit /b 1
    )
    
    echo.
    echo [OK] Miniconda installed successfully
    echo.
    echo ========================================
    echo IMPORTANT: Please restart your terminal
    echo and run setup.bat again!
    echo ========================================
    pause
    exit /b 0
)

echo [OK] Conda found
call conda --version
echo.

REM Set environment name and path
set ENV_NAME=kiro_env
set ENV_PATH=%~dp0%ENV_NAME%

REM Check if environment already exists
if exist "%ENV_PATH%" (
    echo [INFO] Environment already exists at %ENV_PATH%
    echo Skipping environment creation...
) else (
    echo Creating conda environment with Python 3.11...
    call conda create -y -p "%ENV_PATH%" python=3.11
    if errorlevel 1 (
        echo [ERROR] Failed to create conda environment
        pause
        exit /b 1
    )
    echo [OK] Conda environment created
)

echo.
echo Activating environment...
call conda activate "%ENV_PATH%"
if errorlevel 1 (
    echo [ERROR] Failed to activate conda environment
    pause
    exit /b 1
)

echo [OK] Environment activated
python --version
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [OK] Dependencies installed
echo.

REM Verify Kiro installation
echo Verifying Kiro installation...
python kiro_config.py
if errorlevel 1 (
    echo [WARNING] Kiro verification had issues
    echo Please check the output above
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the tool:
echo   start.bat
echo   or: python kiro_main.py
echo.
echo For help, see docs\QUICKSTART.md
echo.
pause
