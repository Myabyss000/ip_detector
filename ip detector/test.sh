#!/bin/bash

# Test script for IP Location Detector (Python version)
echo "=== IP Location Detector Test Suite (Python) ==="
echo ""

# Check if Python3 and required packages are available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 not found. Please install Python3."
    exit 1
fi

# Install requirements if not already installed
if ! python3 -c "import requests" 2>/dev/null; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
    echo ""
fi

# Make sure script is executable
chmod +x ip_locator.py

echo "Running tests..."
echo ""

# Test 1: Version check
echo "Test 1: Version information"
echo "----------------------------"
python3 ip_locator.py --version
echo ""

# Test 2: Help message
echo "Test 2: Help message"
echo "--------------------"
python3 ip_locator.py --help
echo ""

# Test 3: Auto-detect public IP
echo "Test 3: Auto-detect your public IP"
echo "----------------------------------"
python3 ip_locator.py
echo ""

# Test 4: Locate Google DNS
echo "Test 4: Locate Google DNS (8.8.8.8)"
echo "-----------------------------------"
python3 ip_locator.py -ip 8.8.8.8
echo ""

# Test 5: JSON format
echo "Test 5: JSON output format"
echo "--------------------------"
python3 ip_locator.py -ip 1.1.1.1 -f json
echo ""

# Test 6: Table format
echo "Test 6: Table output format"
echo "---------------------------"
python3 ip_locator.py -ip 208.67.222.222 -f table
echo ""

# Test 7: Invalid IP (should fail gracefully)
echo "Test 7: Invalid IP test (should show error)"
echo "-------------------------------------------"
python3 ip_locator.py -ip 192.168.1.1
echo ""

# Test 8: Private IP (should fail gracefully)
echo "Test 8: Private IP test (should show error)"
echo "-------------------------------------------"
python3 ip_locator.py -ip 10.0.0.1
echo ""

# Test 9: No color output
echo "Test 9: No color output"
echo "-----------------------"
python3 ip_locator.py -ip 8.8.8.8 --no-color
echo ""

echo "=== All tests completed ==="
echo ""
echo "If all tests passed successfully, the tool is ready to use!"
