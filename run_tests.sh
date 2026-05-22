#!/bin/bash
set -e
echo "Setting up virtual environment..."

check_venv() {
  if [ -d ".venv" ]; then
    echo "Virtual environment already exists. Continuing with existing one..."
    source .venv/bin/activate
  else
    echo "Creating new virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate

    echo "Installing dependencies..."
    pip install -q -r requirements.txt
  fi
}

check_venv

echo "Starting API container..."
docker run -d --name test-api -p 8080:8080 infralightio/test-integration-api

echo "Waiting for API to be ready..."
until curl -s http://localhost:8080/swagger/index.html > /dev/null; do
  sleep 1
done

echo "Running tests..."
pytest --html=reports/report.html --self-contained-html

echo "Stopping container..."
docker stop test-api && docker rm test-api

echo "Report generated at reports/report.html"
