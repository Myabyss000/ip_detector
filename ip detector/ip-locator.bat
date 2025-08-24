@echo off
REM Windows batch file to run the IP Location Detector
REM Usage: ip-locator.bat [arguments]

REM Change to script directory
cd /d "%~dp0"

REM Run the Python script with all passed arguments
python ip_locator.py %*
