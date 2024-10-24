@echo off
REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Installing from Microsoft Store...
    powershell -Command "Start-Process ms-windows-store://pdp/?productid=9NRWMJP3717K"
    echo Please install Python from the Microsoft Store and try again.
    pause
    exit /b
)

REM Start the Flask app
echo Starting the Flask app...
run.py
pause
