# IP Location Detector - Python Edition

## Quick Start Guide

### Windows Users
1. Make sure Python is installed: `python --version`
2. Install requirements: `pip install requests`
3. Run the tool: `python ip_locator.py -ip 8.8.8.8`
4. Or use the batch file: `ip-locator.bat -ip 8.8.8.8`

### Linux/macOS Users  
1. Make script executable: `chmod +x ip_locator.py`
2. Install requirements: `pip3 install requests` 
3. Run the tool: `./ip_locator.py -ip 8.8.8.8`
4. Or install system-wide: `sudo cp ip_locator.py /usr/local/bin/ip-locator`

## Examples

```bash
# Auto-detect your IP location
python ip_locator.py

# Locate Google DNS
python ip_locator.py -ip 8.8.8.8

# JSON format
python ip_locator.py -ip 1.1.1.1 -f json

# Table format
python ip_locator.py -ip 8.8.8.8 -f table

# Disable colors
python ip_locator.py -ip 8.8.8.8 --no-color

# Use ipinfo.io (with free token)
python ip_locator.py -ip 8.8.8.8 -p ipinfo -t YOUR_TOKEN
```

## Features

✅ **Multiple API providers** (ip-api, ipinfo, ipstack)  
✅ **Auto IP detection**  
✅ **Multiple output formats** (simple, JSON, table)  
✅ **Colorized output**  
✅ **Input validation**  
✅ **Error handling**  
✅ **Cross-platform** (Windows/Linux/macOS)  
✅ **Google Maps integration**  

## API Tokens

### Get ipinfo.io token (50K requests/month free):
1. Visit: https://ipinfo.io/signup
2. Sign up for free
3. Get token from dashboard
4. Use: `python ip_locator.py -ip 8.8.8.8 -p ipinfo -t YOUR_TOKEN`

### Get ipstack.com token (10K requests/month free):
1. Visit: https://ipstack.com/signup/free  
2. Sign up for free
3. Get access key
4. Use: `python ip_locator.py -ip 8.8.8.8 -p ipstack -t YOUR_KEY`
