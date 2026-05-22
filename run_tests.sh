#!/bin/bash
set -e

CLEANUP() {
    echo "Cleaning up: stopping and removing container..."
    docker stop test-api 2>/dev/null || true
    docker rm test-api 2>/dev/null || true
}
trap CLEANUP EXIT

echo "Setting up virtual environment..."
if [ -d ".venv" ]; then
    echo "Virtual environment already exists. Activating..."
    source .venv/bin/activate
else
    echo "Creating new virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
fi

echo "Starting API container..."
docker run -d --name test-api -p 8080:8080 infralightio/test-integration-api

echo "Waiting for API to be ready..."
until curl -s --fail http://localhost:8080/swagger/index.html > /dev/null; do
    sleep 1
done

echo "Running tests..."
pytest --html=reports/report.html --self-contained-html

echo "Report generated at reports/report.html"