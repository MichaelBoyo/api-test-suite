# API Test Automation Suite

Run with: `./run_tests.sh`

HTML report will be in `reports/report.html`.

To run on Linux/Mac:
```bash
chmod +x run_tests.sh
./run_tests.sh
```

To run on Windows Command Prompt:
```cmd
run_tests.bat
```

To run on PowerShell (Windows):
```powershell
powershell -ExecutionPolicy Bypass -File run_tests.ps1
```

# Notes for all scripts
- Docker must be installed and running.

- Python 3 and pip must be available in PATH.

- On Windows, you may need to enable script execution for PowerShell (Set-ExecutionPolicy RemoteSigned -Scope CurrentUser).