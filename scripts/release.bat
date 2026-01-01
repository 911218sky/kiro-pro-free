@echo off
REM Release Script - Automatically bump version and push tag
setlocal enabledelayedexpansion

echo ========================================
echo Release Script
echo ========================================
echo.

REM Get latest tag
for /f "tokens=*" %%i in ('git describe --tags --abbrev^=0 2^>nul') do set LATEST_TAG=%%i

if "%LATEST_TAG%"=="" (
    set LATEST_TAG=v0.0.0
    echo [INFO] No existing tags found, starting from v0.0.0
) else (
    echo [INFO] Current version: %LATEST_TAG%
)

REM Parse version numbers (remove 'v' prefix)
set VERSION=%LATEST_TAG:~1%
for /f "tokens=1,2,3 delims=." %%a in ("%VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
    set PATCH=%%c
)

REM Calculate next versions
set /a NEXT_PATCH=%PATCH%+1
set /a NEXT_MINOR=%MINOR%+1
set /a NEXT_MAJOR=%MAJOR%+1

set PATCH_VERSION=v%MAJOR%.%MINOR%.%NEXT_PATCH%
set MINOR_VERSION=v%MAJOR%.%NEXT_MINOR%.0
set MAJOR_VERSION=v%NEXT_MAJOR%.0.0

echo.
echo Select version bump type:
echo   [1] Patch : %LATEST_TAG% -^> %PATCH_VERSION% (bug fixes)
echo   [2] Minor : %LATEST_TAG% -^> %MINOR_VERSION% (new features)
echo   [3] Major : %LATEST_TAG% -^> %MAJOR_VERSION% (breaking changes)
echo   [4] Custom version
echo   [5] Cancel
echo.

set /p CHOICE="Enter choice (1-5): "

if "%CHOICE%"=="1" (
    set NEW_VERSION=%PATCH_VERSION%
) else if "%CHOICE%"=="2" (
    set NEW_VERSION=%MINOR_VERSION%
) else if "%CHOICE%"=="3" (
    set NEW_VERSION=%MAJOR_VERSION%
) else if "%CHOICE%"=="4" (
    set /p NEW_VERSION="Enter custom version (e.g., v1.2.3): "
) else (
    echo [INFO] Release cancelled
    pause
    exit /b 0
)

echo.
echo [INFO] New version: %NEW_VERSION%
echo.

REM Confirm (default: y)
set /p CONFIRM="Confirm release %NEW_VERSION%? [Y/n]: "
if /i "%CONFIRM%"=="n" (
    echo [INFO] Release cancelled
    pause
    exit /b 0
)

echo.
echo [INFO] Creating tag %NEW_VERSION%...
git tag %NEW_VERSION%
if errorlevel 1 (
    echo [ERROR] Failed to create tag
    pause
    exit /b 1
)

echo [INFO] Pushing tag to origin...
git push origin %NEW_VERSION%
if errorlevel 1 (
    echo [ERROR] Failed to push tag
    git tag -d %NEW_VERSION%
    pause
    exit /b 1
)

echo.
echo ========================================
echo [OK] Release %NEW_VERSION% created!
echo ========================================
echo.
echo GitHub Actions will now build and publish the release.
echo Check: https://github.com/911218sky/kiro-pro-free/actions
echo.
pause
