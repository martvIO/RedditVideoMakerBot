#!/bin/bash
# Setup script for Reddit Video Maker Bot - Linux/macOS
# This script runs the Python setup process

echo "==============================================="
echo "Reddit Video Maker Bot - Setup"
echo "==============================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.10 or 3.11"
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS: brew install python@3.10"
        echo "Or download from: https://www.python.org/downloads/"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Ubuntu/Debian: sudo apt-get install python3.10"
        echo "Fedora: sudo dnf install python3.10"
        echo "Or download from: https://www.python.org/downloads/"
    fi
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

echo "Running Python setup script..."
echo ""

python3 setup.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Setup failed. Please check the errors above."
    exit 1
fi

echo ""
echo "==============================================="
echo "Setup completed successfully!"
echo "==============================================="
