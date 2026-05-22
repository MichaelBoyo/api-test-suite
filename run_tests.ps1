# run_tests.ps1
$ErrorActionPreference = "Stop"

# Cleanup block
$containerName = "test-api"

function Cleanup {
    Write-Host "Cleaning up: stopping and removing container..." -ForegroundColor Yellow
    docker stop $containerName 2>&1 | Out-Null
    docker rm $containerName 2>&1 | Out-Null
}

try {
    Write-Host "Setting up virtual environment..." -ForegroundColor Cyan
    if (Test-Path ".venv") {
        Write-Host "Virtual environment already exists. Activating..."
        &.venv\Scripts\Activate.ps1
    } else {
        Write-Host "Creating new virtual environment..."
        python -m venv .venv
        &.venv\Scripts\Activate.ps1
        Write-Host "Installing dependencies..."
        pip install -q -r requirements.txt
    }

    Write-Host "Starting API container..." -ForegroundColor Cyan
    docker run -d --name $containerName -p 8080:8080 infralightio/test-integration-api

    Write-Host "Waiting for API to be ready..." -ForegroundColor Cyan
    do {
        Start-Sleep -Seconds 1
        $response = try { Invoke-WebRequest -Uri "http://localhost:8080/swagger/index.html" -Method Head -UseBasicParsing -ErrorAction Stop } catch { $null }
    } while (-not $response -or $response.StatusCode -ne 200)

    Write-Host "Running tests..." -ForegroundColor Cyan
    pytest --html=reports/report.html --self-contained-html

    Write-Host "Report generated at reports/report.html" -ForegroundColor Green
}
finally {
    Cleanup
}