#!/bin/bash

# DAG Editor Pro - Quick Start Script

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          🚀 DAG Editor Pro - Quick Start                      ║"
echo "║                                                                ║"
echo "║  Standalone NiceGUI + FastAPI Application                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create storage directory
mkdir -p storage
echo "✓ Storage directory ready"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                   🌐 Starting Application                     ║"
echo "║                                                                ║"
echo "║  🔗 Web UI:        http://localhost:8000                      ║"
echo "║  🔌 API:           http://localhost:8000/api                  ║"
echo "║                                                                ║"
echo "║  Press Ctrl+C to stop the server                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Run the app
python app_advanced.py
