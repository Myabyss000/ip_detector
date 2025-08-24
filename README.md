# IP Location Detector

A powerful command-line tool written in Python for detecting geographical location of IP addresses on Linux systems.

## Features

- **Multiple API Providers**: Supports ip-api.com (free), ipinfo.io, and ipstack.com
- **Auto-detection**: Automatically detects your public IP if none provided
- **Multiple Output Formats**: Simple, JSON, and table formats
- **Cross-platform**: Works on Linux, macOS, and Windows
- **Colorized Output**: Beautiful colored terminal output (can be disabled)
- **Comprehensive Data**: Country, city, coordinates, ISP, organization, timezone
- **Input Validation**: Validates IP addresses and checks for private IPs
- **Google Maps Integration**: Provides direct links to location
- **Error Handling**: Robust error handling with helpful messages

## Installation

### Method 1: Quick Setup (Recommended)
```bash
# Clone or download the files
cd ip-location-detector

# Run the install script (Linux) - handles externally-managed-environment automatically
chmod +x install.sh
./install.sh
```

### Method 2: Manual Installation
```bash
# Install Python3 if not already installed
sudo apt update && sudo apt install python3 python3-pip  # Ubuntu/Debian
sudo yum install python3 python3-pip                     # CentOS/RHEL
sudo dnf install python3 python3-pip                     # Fedora

# Install required packages
pip3 install -r requirements.txt

# If you get "externally-managed-environment" error, use one of these methods:
# Method A: Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows
pip install -r requirements.txt

# Method B: Use pipx (if available)
pipx install --editable .

# Method C: Use --break-system-packages flag (use with caution)
pip3 install -r requirements.txt --break-system-packages

# Make script executable
chmod +x ip_locator.py

# Optional: Install system-wide
sudo cp ip_locator.py /usr/local/bin/ip-locator
sudo chmod +x /usr/local/bin/ip-locator
```

### Method 3: Using pip (if you package it)
```bash
pip3 install ip-location-detector
```

## Usage

### Basic Usage
```bash
# Detect your own public IP location
python3 ip_locator.py
# or if installed system-wide:
ip-locator

# Locate a specific IP address
python3 ip_locator.py -ip 8.8.8.8

# Use different output format
python3 ip_locator.py -ip 1.1.1.1 -f json
python3 ip_locator.py -ip 1.1.1.1 -f table
```

### Advanced Usage
```bash
# Use different API provider
python3 ip_locator.py -ip 8.8.8.8 -p ipinfo -t YOUR_TOKEN
python3 ip_locator.py -ip 8.8.8.8 -p ipstack -t YOUR_TOKEN

# Disable colored output
python3 ip_locator.py -ip 8.8.8.8 --no-color

# Show help
python3 ip_locator.py --help

# Show version
python3 ip_locator.py --version
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--ip-address` | `-ip` | IP address to locate (leave empty for auto-detection) | None |
| `--provider` | `-p` | API provider: `ipapi`, `ipinfo`, or `ipstack` | `ipapi` |
| `--format` | `-f` | Output format: `simple`, `json`, or `table` | `simple` |
| `--token` | `-t` | API token for ipinfo or ipstack providers | None |
| `--no-color` | | Disable colored output | False |
| `--version` | `-v` | Show version information | |
| `--help` | `-h` | Show help message | |

## Output Examples

### Simple Format
```
IP: 8.8.8.8
Location: Mountain View, California, United States (US)
Coordinates: 37.405991, -122.078514
ISP: Google LLC
Organization: Google Public DNS
ASN: AS15169 Google LLC
Timezone: America/Los_Angeles
Accuracy: City-level (±50km typical)

Google Maps: https://maps.google.com/?q=37.405991,-122.078514
```

### JSON Format
```json
{
  "ip": "8.8.8.8",
  "country": "United States",
  "country_code": "US",
  "city": "Mountain View",
  "region": "California",
  "region_code": "CA",
  "latitude": 37.405991,
  "longitude": -122.078514,
  "isp": "Google LLC",
  "organization": "Google Public DNS",
  "asn": "AS15169 Google LLC",
  "timezone": "America/Los_Angeles",
  "accuracy": "City-level (±50km typical)"
}
```

### Table Format
```
┌─────────────────┬─────────────────────────────────────────┐
│ Field           │ Value                                   │
├─────────────────┼─────────────────────────────────────────┤
│ IP Address      │ 8.8.8.8                                 │
│ Country         │ United States (US)                      │
│ Region          │ California (CA)                         │
│ City            │ Mountain View                           │
│ Coordinates     │ 37.405991, -122.078514                  │
│ ISP             │ Google LLC                              │
│ Organization    │ Google Public DNS                       │
│ ASN             │ AS15169 Google LLC                      │
│ Timezone        │ America/Los_Angeles                     │
│ Accuracy        │ City-level (±50km typical)              │
└─────────────────┴─────────────────────────────────────────┘
```

## API Providers

### ip-api.com (Default)
- **Free**: 1,000 requests per month
- **No registration**: Works out of the box
- **Rate limit**: 45 requests per minute
- **Features**: Basic location data, ASN information

### ipinfo.io
- **Free tier**: 50,000 requests per month with registration
- **Requires token**: Sign up at ipinfo.io for free account
- **Better accuracy**: More accurate data
- **Additional features**: More detailed information

### ipstack.com
- **Free tier**: 10,000 requests per month with registration
- **Requires token**: Sign up at ipstack.com
- **Commercial grade**: Professional accuracy
- **Additional features**: ISP data, threat detection

To get an ipinfo.io token:
1. Visit https://ipinfo.io/signup
2. Sign up for free account
3. Get your access token from the dashboard
4. Use with `-token YOUR_TOKEN`

## System Requirements

- **Operating System**: Linux, macOS, Windows (with Python 3.6+)
- **Python**: Version 3.6 or higher
- **Dependencies**: `requests` library (automatically installed)
- **Network**: Internet connection for API calls
- **Memory**: < 50MB RAM usage
- **Storage**: < 1MB disk space

## Accuracy Information

IP geolocation accuracy varies significantly:

| Level | Accuracy | Use Cases |
|-------|----------|-----------|
| **Country** | 95-99% | Compliance, basic geo-blocking |
| **Region/State** | 80-90% | Regional content delivery |
| **City** | 55-80% | Local advertisements, weather |
| **Precise Location** | Not reliable | Privacy protected by ISPs |

### Factors Affecting Accuracy
- **VPNs/Proxies**: Show VPN server location, not user location
- **Mobile Networks**: Often less accurate due to network routing
- **ISP Infrastructure**: Large ISPs may route traffic through distant servers
- **Privacy Measures**: ISPs increasingly protect user location privacy

## Privacy and Legal Considerations

- **GDPR Compliance**: Ensure compliance with data protection laws
- **User Consent**: Obtain consent before collecting location data
- **Data Retention**: Don't store personal location data unnecessarily
- **Purpose Limitation**: Use location data only for stated purposes

## Troubleshooting

### Common Issues

1. **"externally-managed-environment" error**
   ```bash
   # This error occurs in Python 3.11+ and newer Linux distributions
   # Solution 1: Use virtual environment (RECOMMENDED)
   python3 -m venv ip-locator-env
   source ip-locator-env/bin/activate
   pip install -r requirements.txt
   python ip_locator.py -ip 8.8.8.8
   
   # Solution 2: Use pipx (if available)
   sudo apt install pipx  # Install pipx first
   pipx install requests
   python3 ip_locator.py -ip 8.8.8.8
   
   # Solution 3: System-wide install (use with caution)
   pip3 install -r requirements.txt --break-system-packages
   ```

2. **"Invalid IP address" error**
   ```bash
   # Check if IP format is correct
   ./ip-locator -ip 192.168.1.1  # Private IP won't work with public APIs
   ./ip-locator -ip 8.8.8.8      # Use public IP
   ```

2. **"Failed to make request" error**
   ```bash
   # Check internet connection
   ping google.com
   
   # Check if API is accessible
   curl http://ip-api.com/json/8.8.8.8
   ```

3. **Rate limit exceeded**
   ```bash
   # Wait a minute and try again, or use ipinfo provider
   ./ip-locator -ip 8.8.8.8 -provider ipinfo -token YOUR_TOKEN
   ```

### Installation Issues

1. **Python not found**
   ```bash
   # Install Python on Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   
   # Install Python on CentOS/RHEL
   sudo yum install python3 python3-pip
   
   # Install Python on Fedora
   sudo dnf install python3 python3-pip
   ```

2. **Permission denied**
   ```bash
   # Make script executable
   chmod +x ip_locator.py
   chmod +x install.sh
   chmod +x test.sh
   ```

## Development

### Project Structure
```
ip-location-detector/
├── ip_locator.py          # Main Python application ⭐
├── requirements.txt       # Python dependencies ⭐  
├── README.md             # Full documentation ⭐
├── LICENSE               # MIT License
├── QUICKSTART.md         # Quick start guide
├── .gitignore            # Git ignore file
├── .env.example          # Environment variables example
├── ip-locator.bat        # Windows batch file
├── install.sh            # Linux installation script
└── test.sh               # Test script
```

**Essential files**: `ip_locator.py`, `requirements.txt`, `README.md`  
**Optional files**: Everything else enhances user experience

### Development and Testing
```bash
# Run directly
python ip_locator.py -ip 8.8.8.8

# Install dependencies
pip install -r requirements.txt

# Run tests
chmod +x test.sh
./test.sh

# Install system-wide (Linux)
chmod +x install.sh
./install.sh
```

### Testing
```bash
# Test with various IPs
./ip-locator -ip 8.8.8.8
./ip-locator -ip 1.1.1.1
./ip-locator -ip 208.67.222.222

# Test different formats
./ip-locator -ip 8.8.8.8 -format json
./ip-locator -ip 8.8.8.8 -format table

# Test auto-detection
./ip-locator
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **ip-api.com** for providing free IP geolocation API
- **ipinfo.io** for accurate geolocation services
- **Python Community** for the excellent standard library and ecosystem
- **Open Source Community** for the collaborative development model
