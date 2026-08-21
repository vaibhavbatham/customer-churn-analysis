@echo off
echo ===================================================
echo Push Customer Churn Analysis to Your GitHub
echo ===================================================
echo.
set /p REPO_URL="Enter your GitHub Repository URL (e.g. https://github.com/your-username/customer-churn-analysis.git): "
if "%REPO_URL%"=="" (
    echo Error: No repository URL provided!
    pause
    exit /b
)
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main
git push -u origin main
echo.
echo ===================================================
echo Successfully pushed to GitHub!
echo Your dashboard will be automatically deployed on GitHub Pages.
echo ===================================================
pause
