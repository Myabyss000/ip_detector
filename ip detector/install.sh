#!/bin/bash

# Install script for Linux
echo "Setting up IP Location Detector (Python version)..."

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Installing..."
    
    # Detect Linux distribution and install Python3
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum install -y python3 python3-pip
    elif command -v dnf &> /dev/null; then
        # Fedora
        sudo dnf install -y python3 python3-pip
    else
        echo "Could not detect package manager. Please install Python3 manually."
        exit 1
    fi
fi

# Install required packages
echo "Installing required Python packages..."
pip3 install -r requirements.txt

# Make the script executable
chmod +x ip_locator.py

# Create a system-wide link (optional)
read -p "Do you want to install ip-locator system-wide? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo cp ip_locator.py /usr/local/bin/ip-locator
    sudo chmod +x /usr/local/bin/ip-locator
    echo "ip-locator installed to /usr/local/bin/"
    echo "You can now use 'ip-locator' from anywhere!"
else
    echo "Local installation complete. Use './ip_locator.py' to run."
fi

echo "Installation complete!"
echo ""
echo "Usage examples:"
echo "  ./ip_locator.py                    # Detect your public IP"
echo "  ./ip_locator.py -ip 8.8.8.8       # Locate specific IP"
echo "  ./ip_locator.py -ip 1.1.1.1 -f json  # JSON output"
