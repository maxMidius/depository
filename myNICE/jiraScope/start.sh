#!/bin/bash
# Startup script for JIRA Scope DAG Editor

echo "Starting JIRA Scope DAG Editor..."
echo "================================"
echo ""

# Activate virtual environment if it exists
if [ -f "/home/dasur/VENV/venvNICE/bin/activate" ]; then
    echo "Activating virtual environment..."
    source /home/dasur/VENV/venvNICE/bin/activate
fi

# Navigate to the app directory
cd "$(dirname "$0")"

echo "Starting NiceGUI application..."
echo "Application will be available at: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application
python app.py
