@echo off
echo.
echo ==========================================
echo      NexaJobs - Starting Application
echo ==========================================
echo.

cd /d "%~dp0job_recommendation_project"

REM Check if .env exists, if not create from example
if not exist ".env" (
    echo [!] No .env file found. Creating one...
    copy .env.example .env >nul
    echo.
    echo ==========================================
    echo   IMPORTANT: Set up your Gmail to enable
    echo   email notifications!
    echo.
    echo   1. Open: job_recommendation_project\.env
    echo   2. Add your Gmail and App Password
    echo   3. Restart this file
    echo ==========================================
    echo.
)

echo [1/3] Running database migrations...
py -3.12 manage.py migrate --run-syncdb
echo.

echo [2/3] Seeding Pakistani company jobs...
py -3.12 manage.py seed_jobs
echo.

echo [3/3] Starting server...
echo.
echo ==========================================
echo   App is running at: http://127.0.0.1:8000
echo   Press Ctrl+C to stop the server
echo ==========================================
echo.

py -3.12 manage.py runserver
