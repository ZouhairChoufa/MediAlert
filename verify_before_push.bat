@echo off
echo ========================================
echo MediAlert - Pre-Push Verification
echo ========================================
echo.

echo Checking for sensitive files...
echo.

REM Check for Firebase credentials
if exist "*firebase-adminsdk*.json" (
    echo [WARNING] Firebase credentials found!
    echo Please ensure they are in .gitignore
    echo.
) else (
    echo [OK] No Firebase credentials in root
)

REM Check for .env file
if exist ".env" (
    echo [OK] .env file exists (should be in .gitignore)
) else (
    echo [INFO] No .env file found
)

REM Check for .env.example
if exist ".env.example" (
    echo [OK] .env.example exists
) else (
    echo [WARNING] .env.example not found
)

REM Check for LICENSE
if exist "LICENSE" (
    echo [OK] LICENSE file exists
) else (
    echo [WARNING] LICENSE file not found
)

REM Check for README.md
if exist "README.md" (
    echo [OK] README.md exists
) else (
    echo [ERROR] README.md not found!
)

REM Check for .gitignore
if exist ".gitignore" (
    echo [OK] .gitignore exists
) else (
    echo [ERROR] .gitignore not found!
)

echo.
echo ========================================
echo Verification complete!
echo.
echo If all checks passed, you can proceed with:
echo   git_setup.bat
echo ========================================
pause
