@echo off
title Smart Courier - A* Algorithm
color 0A
echo.
echo ================================
echo Smart Courier - A* Algorithm
echo ================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [INFO] Checking Python version...
python --version

echo [INFO] Setting up backend...
cd backend

if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [INFO] Installing dependencies...
pip install -q -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ================================
echo [SUCCESS] Setup Complete!
echo ================================
echo.
echo [INFO] Backend: http://localhost:5000
echo [INFO] Frontend: Open ../frontend/index.html in browser
echo.
echo [INFO] Press Ctrl+C to stop the server
echo.

python app.py
pause
