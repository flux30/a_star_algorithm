#!/bin/bash

echo ""
echo "================================"
echo "Smart Courier - A* Algorithm"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed${NC}"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo -e "${GREEN}[INFO]${NC} Python version:"
python3 --version

echo -e "${GREEN}[INFO]${NC} Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${GREEN}[INFO]${NC} Creating virtual environment..."
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Failed to create virtual environment${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${GREEN}[INFO]${NC} Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Failed to activate virtual environment${NC}"
    exit 1
fi

# Install dependencies
echo -e "${GREEN}[INFO]${NC} Installing dependencies..."
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Failed to install dependencies${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}[SUCCESS] Setup Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${YELLOW}[INFO] Backend: http://localhost:5000${NC}"
echo -e "${YELLOW}[INFO] Frontend: Open ../frontend/index.html in browser${NC}"
echo ""
echo -e "${YELLOW}[INFO] Press Ctrl+C to stop the server${NC}"
echo ""

python app.py

