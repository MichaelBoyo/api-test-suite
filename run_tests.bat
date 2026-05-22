@echo off
setlocal enabledelayedexpansion

echo Setting up virtual environment...
if exist ".venv\" (
    echo Virtual environment already exists. Activating...
    call .venv\Scripts\activate.bat
) else (
    echo Creating new virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -q -r requirements.txt
)

echo Starting API container...
docker run -d --name test-api -p 8080:8080 infralightio/test-integration-api

echo Waiting for API to be ready...
:waitloop
curl -s --fail http://localhost:8080/swagger/index.html > nul 2>&1
if errorlevel 1 (
    timeout /t 1 /nobreak > nul
    goto waitloop
)

echo Running tests...
pytest --html=reports/report.html --self-contained-html
set TEST_EXIT_CODE=%errorlevel%

echo Stopping container...
docker stop test-api > nul 2>&1
docker rm test-api > nul 2>&1

if %TEST_EXIT_CODE% neq 0 (
    echo Tests FAILED with exit code %TEST_EXIT_CODE%
    exit /b %TEST_EXIT_CODE%
)

echo Report generated at reports/report.html