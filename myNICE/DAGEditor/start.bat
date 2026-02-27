@echo off
REM DAG Editor Pro - Quick Start Script for Windows

setlocal enabledelayedexpansion

cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║          🚀 DAG Editor Pro - Quick Start (Windows)            ║
echo ║                                                                ║
echo ║  Standalone NiceGUI + FastAPI Application                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Python found: %PYTHON_VERSION%
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing dependencies...
python -m pip install -q --upgrade pip
pip install -q -r requirements.txt
echo ✓ Dependencies installed

REM Create storage directory
if not exist "storage" mkdir storage
echo ✓ Storage directory ready

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                   🌐 Starting Application                     ║
echo ║                                                                ║
echo ║  🔗 Web UI:        http://localhost:8000                      ║
echo ║  🔌 API:           http://localhost:8000/api                  ║
echo ║                                                                ║
echo ║  Press Ctrl+C to stop the server                              ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Run the app
python app_advanced.py

pause
