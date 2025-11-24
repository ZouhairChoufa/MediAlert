@echo off
echo ========================================
echo MediAlert - Git Repository Setup
echo ========================================
echo.

REM Initialize git if not already initialized
if not exist .git (
    echo Initializing Git repository...
    git init
    echo.
)

REM Add remote repository
echo Adding remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/ZouhairChoufa/MediAlert.git
echo.

REM Add all files
echo Adding files to Git...
git add .
echo.

REM Create initial commit
echo Creating commit...
git commit -m "Initial commit: MediAlert Pro - AI-Powered Emergency Medical System"
echo.

REM Rename branch to main
echo Renaming branch to main...
git branch -M main
echo.

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main
echo.

echo ========================================
echo Setup complete!
echo Repository: https://github.com/ZouhairChoufa/MediAlert
echo ========================================
pause
