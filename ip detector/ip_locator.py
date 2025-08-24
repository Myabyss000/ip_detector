#!/usr/bin/env python3
"""
IP Location Detector
A comprehensive tool for detecting geographical location of IP addresses.
Supports multiple providers and output formats.
"""

import argparse
import json
import requests
import sys
import ipaddress
import time
from typing import Dict, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

@dataclass
class LocationData:
    """Data class for storing location information"""
    ip: str
    country: str = ""
    country_code: str = ""
    city: str = ""
    region: str = ""
    region_code: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    isp: str = ""
    organization: str = ""
    asn: str = ""
    timezone: str = ""
    accuracy: str = "City-level (±50km typical)"

class GeoLocator(ABC):
    """Abstract base class for geolocation providers"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 10
    
    @abstractmethod
    def get_location(self, ip: str) -> Optional[LocationData]:
        """Get location data for an IP address"""
        pass

class IPAPILocator(GeoLocator):
    """IP-API.com geolocation provider (free tier)"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "http://ip-api.com/json"
        self.rate_limit = 45  # requests per minute
    
    def get_location(self, ip: str) -> Optional[LocationData]:
        """Get location from ip-api.com"""
        try:
            url = f"{self.base_url}/{ip}"
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'fail':
                print(f"{Colors.RED}Error: {data.get('message', 'API request failed')}{Colors.END}")
                return None
            
            return LocationData(
                ip=data.get('query', ip),
                country=data.get('country', ''),
                country_code=data.get('countryCode', ''),
                city=data.get('city', ''),
                region=data.get('regionName', ''),
                region_code=data.get('region', ''),
                latitude=float(data.get('lat', 0)),
                longitude=float(data.get('lon', 0)),
                isp=data.get('isp', ''),
                organization=data.get('org', ''),
                asn=data.get('as', ''),
                timezone=data.get('timezone', ''),
                accuracy="City-level (±50km typical)"
            )
        
        except requests.RequestException as e:
            print(f"{Colors.RED}Network error: {e}{Colors.END}")
            return None
        except json.JSONDecodeError:
            print(f"{Colors.RED}Error: Invalid JSON response{Colors.END}")
            return None
        except Exception as e:
            print(f"{Colors.RED}Unexpected error: {e}{Colors.END}")
            return None

class IPInfoLocator(GeoLocator):
    """IPInfo.io geolocation provider"""
    
    def __init__(self, token: str = ""):
        super().__init__()
        self.base_url = "https://ipinfo.io"
        self.token = token
    
    def get_location(self, ip: str) -> Optional[LocationData]:
        """Get location from ipinfo.io"""
        try:
            url = f"{self.base_url}/{ip}/json"
            params = {"token": self.token} if self.token else {}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Handle error responses
            if 'error' in data:
                print(f"{Colors.RED}Error: {data['error']['message']}{Colors.END}")
                return None
            
            # Parse coordinates
            lat, lon = 0.0, 0.0
            if 'loc' in data and data['loc']:
                try:
                    coords = data['loc'].split(',')
                    if len(coords) == 2:
                        lat, lon = float(coords[0]), float(coords[1])
                except ValueError:
                    pass
            
            return LocationData(
                ip=data.get('ip', ip),
                country=data.get('country', ''),
                city=data.get('city', ''),
                region=data.get('region', ''),
                latitude=lat,
                longitude=lon,
                organization=data.get('org', ''),
                timezone=data.get('timezone', ''),
                accuracy="City-level (±50km typical)"
            )
        
        except requests.RequestException as e:
            print(f"{Colors.RED}Network error: {e}{Colors.END}")
            return None
        except json.JSONDecodeError:
            print(f"{Colors.RED}Error: Invalid JSON response{Colors.END}")
            return None
        except Exception as e:
            print(f"{Colors.RED}Unexpected error: {e}{Colors.END}")
            return None

class IPStackLocator(GeoLocator):
    """IPStack.com geolocation provider"""
    
    def __init__(self, token: str):
        super().__init__()
        self.base_url = "http://api.ipstack.com"
        self.token = token
    
    def get_location(self, ip: str) -> Optional[LocationData]:
        """Get location from ipstack.com"""
        try:
            url = f"{self.base_url}/{ip}"
            params = {"access_key": self.token}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'error' in data:
                print(f"{Colors.RED}Error: {data['error']['info']}{Colors.END}")
                return None
            
            return LocationData(
                ip=data.get('ip', ip),
                country=data.get('country_name', ''),
                country_code=data.get('country_code', ''),
                city=data.get('city', ''),
                region=data.get('region_name', ''),
                region_code=data.get('region_code', ''),
                latitude=float(data.get('latitude', 0)),
                longitude=float(data.get('longitude', 0)),
                timezone=data.get('time_zone', {}).get('id', ''),
                accuracy="City-level (±50km typical)"
            )
        
        except requests.RequestException as e:
            print(f"{Colors.RED}Network error: {e}{Colors.END}")
            return None
        except json.JSONDecodeError:
            print(f"{Colors.RED}Error: Invalid JSON response{Colors.END}")
            return None
        except Exception as e:
            print(f"{Colors.RED}Unexpected error: {e}{Colors.END}")
            return None

def validate_ip(ip: str) -> bool:
    """Validate IP address format"""
    try:
        ipaddress.ip_address(ip)
        # Check if it's a public IP
        ip_obj = ipaddress.ip_address(ip)
        return not (ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local)
    except ValueError:
        return False

def is_valid_ip(ip: str) -> bool:
    """Check if IP address format is valid (public or private)"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def analyze_private_ip(ip: str) -> Optional[LocationData]:
    """Analyze private IP and provide network information"""
    try:
        ip_obj = ipaddress.ip_address(ip)
        
        if ip_obj.is_loopback:
            network_type = "Loopback"
            description = "localhost/loopback address"
        elif ip_obj.is_link_local:
            network_type = "Link-Local"
            description = "automatically assigned local address"
        elif ip_obj.is_private:
            if ip_obj in ipaddress.ip_network("10.0.0.0/8"):
                network_type = "Private Class A"
                description = "large private network (10.0.0.0/8)"
            elif ip_obj in ipaddress.ip_network("172.16.0.0/12"):
                network_type = "Private Class B"
                description = "medium private network (172.16.0.0/12)"
            elif ip_obj in ipaddress.ip_network("192.168.0.0/16"):
                network_type = "Private Class C"
                description = "small private network (192.168.0.0/16)"
            else:
                network_type = "Private"
                description = "private network address"
        else:
            return None
        
        return LocationData(
            ip=ip,
            country="Local Network",
            city=network_type,
            region=description,
            accuracy="Network-level identification only",
            organization="Private/Local Network",
            timezone="System timezone"
        )
    except ValueError:
        return None

def get_public_ip() -> Optional[str]:
    """Get the public IP address of the current machine"""
    services = [
        "https://api.ipify.org?format=text",
        "https://ipinfo.io/ip",
        "https://icanhazip.com",
        "https://ident.me"
    ]
    
    for service in services:
        try:
            response = requests.get(service, timeout=5)
            response.raise_for_status()
            ip = response.text.strip()
            if validate_ip(ip):
                return ip
        except:
            continue
    
    return None

def print_simple_format(data: LocationData) -> None:
    """Print location data in simple format"""
    print(f"{Colors.BOLD}IP Location Information{Colors.END}")
    print("=" * 50)
    print(f"{Colors.CYAN}IP Address:{Colors.END} {data.ip}")
    
    if data.country:
        location_parts = [data.city, data.region, data.country]
        location_parts = [part for part in location_parts if part]
        location_str = ", ".join(location_parts)
        if data.country_code:
            location_str += f" ({data.country_code})"
        print(f"{Colors.CYAN}Location:{Colors.END} {location_str}")
    
    if data.latitude and data.longitude:
        print(f"{Colors.CYAN}Coordinates:{Colors.END} {data.latitude:.6f}, {data.longitude:.6f}")
    
    if data.isp:
        print(f"{Colors.CYAN}ISP:{Colors.END} {data.isp}")
    
    if data.organization:
        print(f"{Colors.CYAN}Organization:{Colors.END} {data.organization}")
    
    if data.asn:
        print(f"{Colors.CYAN}ASN:{Colors.END} {data.asn}")
    
    if data.timezone:
        print(f"{Colors.CYAN}Timezone:{Colors.END} {data.timezone}")
    
    print(f"{Colors.YELLOW}Accuracy:{Colors.END} {data.accuracy}")

def print_json_format(data: LocationData) -> None:
    """Print location data in JSON format"""
    json_data = {
        "ip": data.ip,
        "country": data.country,
        "country_code": data.country_code,
        "city": data.city,
        "region": data.region,
        "region_code": data.region_code,
        "latitude": data.latitude,
        "longitude": data.longitude,
        "isp": data.isp,
        "organization": data.organization,
        "asn": data.asn,
        "timezone": data.timezone,
        "accuracy": data.accuracy
    }
    print(json.dumps(json_data, indent=2))

def print_table_format(data: LocationData) -> None:
    """Print location data in table format"""
    table_data = [
        ("IP Address", data.ip),
        ("Country", f"{data.country} ({data.country_code})" if data.country_code else data.country),
        ("Region", f"{data.region} ({data.region_code})" if data.region_code else data.region),
        ("City", data.city),
        ("Coordinates", f"{data.latitude:.6f}, {data.longitude:.6f}" if data.latitude and data.longitude else "N/A"),
        ("ISP", data.isp),
        ("Organization", data.organization),
        ("ASN", data.asn),
        ("Timezone", data.timezone),
        ("Accuracy", data.accuracy)
    ]
    
    # Filter out empty values
    table_data = [(field, value) for field, value in table_data if value and value != "N/A"]
    
    if not table_data:
        print("No data available")
        return
    
    # Calculate column widths
    max_field_width = max(len(field) for field, _ in table_data)
    max_value_width = max(len(str(value)) for _, value in table_data)
    
    # Print table
    print("┌" + "─" * (max_field_width + 2) + "┬" + "─" * (max_value_width + 2) + "┐")
    print(f"│ {'Field':<{max_field_width}} │ {'Value':<{max_value_width}} │")
    print("├" + "─" * (max_field_width + 2) + "┼" + "─" * (max_value_width + 2) + "┤")
    
    for field, value in table_data:
        print(f"│ {field:<{max_field_width}} │ {str(value):<{max_value_width}} │")
    
    print("└" + "─" * (max_field_width + 2) + "┴" + "─" * (max_value_width + 2) + "┘")

def print_location_data(data: LocationData, format_type: str) -> None:
    """Print location data in the specified format"""
    if format_type == "json":
        print_json_format(data)
    elif format_type == "table":
        print_table_format(data)
    else:
        print_simple_format(data)
    
    # Add Google Maps link if coordinates are available
    if data.latitude and data.longitude:
        maps_url = f"https://maps.google.com/?q={data.latitude:.6f},{data.longitude:.6f}"
        print(f"\n{Colors.GREEN}Google Maps:{Colors.END} {maps_url}")

def show_accuracy_info():
    """Show accuracy information"""
    print(f"\n{Colors.YELLOW}IP Geolocation Accuracy Information:{Colors.END}")
    print("• Country level: 95-99% accurate")
    print("• City level: 55-80% accurate")
    print("• Precise location: Not reliable due to privacy protections")
    print(f"• VPNs/Proxies: Show server location, not user location")

def main():
    parser = argparse.ArgumentParser(
        description="IP Location Detector - Get geographical information for IP addresses",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Detect your public IP location
  %(prog)s -ip 8.8.8.8                  # Locate specific IP
  %(prog)s -ip 1.1.1.1 -f json          # JSON output format
  %(prog)s -ip 8.8.8.8 -f table         # Table output format
  %(prog)s -ip 8.8.8.8 -p ipinfo -t TOKEN  # Use ipinfo.io with token
        """
    )
    
    parser.add_argument(
        "-ip", "--ip-address",
        help="IP address to locate (leave empty to detect your public IP)"
    )
    
    parser.add_argument(
        "-p", "--provider",
        choices=["ipapi", "ipinfo", "ipstack"],
        default="ipapi",
        help="Geolocation API provider (default: ipapi)"
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=["simple", "json", "table"],
        default="simple",
        help="Output format (default: simple)"
    )
    
    parser.add_argument(
        "-t", "--token",
        help="API token for ipinfo or ipstack providers"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="IP Location Detector v1.0 - Python Edition"
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    
    args = parser.parse_args()
    
    # Disable colors if requested
    if args.no_color:
        Colors.RED = Colors.GREEN = Colors.YELLOW = Colors.BLUE = ""
        Colors.MAGENTA = Colors.CYAN = Colors.WHITE = Colors.BOLD = Colors.END = ""
    
    # Get target IP
    target_ip = args.ip_address
    if not target_ip:
        print(f"{Colors.BLUE}No IP provided, detecting your public IP...{Colors.END}")
        target_ip = get_public_ip()
        if not target_ip:
            print(f"{Colors.RED}Error: Could not detect public IP address{Colors.END}")
            sys.exit(1)
        print(f"{Colors.GREEN}Your public IP: {target_ip}{Colors.END}\n")
    
    # Validate IP address format
    if not is_valid_ip(target_ip):
        print(f"{Colors.RED}Error: Invalid IP address format: {target_ip}{Colors.END}")
        sys.exit(1)
    
    # Check if it's a private IP and handle accordingly
    if not validate_ip(target_ip):
        print(f"{Colors.YELLOW}Private/Local IP detected: {target_ip}{Colors.END}")
        print(f"{Colors.BLUE}Analyzing local network information...{Colors.END}\n")
        
        location_data = analyze_private_ip(target_ip)
        if location_data:
            print_location_data(location_data, args.format)
            print(f"\n{Colors.YELLOW}Note: Private IPs cannot be geolocated using external APIs{Colors.END}")
            print(f"{Colors.CYAN}This analysis is based on RFC 1918 private network ranges{Colors.END}")
        else:
            print(f"{Colors.RED}Error: Could not analyze IP address{Colors.END}")
        
        sys.exit(0)
    
    # Create locator based on provider
    locator = None
    if args.provider == "ipapi":
        locator = IPAPILocator()
    elif args.provider == "ipinfo":
        locator = IPInfoLocator(args.token or "")
    elif args.provider == "ipstack":
        if not args.token:
            print(f"{Colors.RED}Error: IPStack requires an API token (use -t TOKEN){Colors.END}")
            sys.exit(1)
        locator = IPStackLocator(args.token)
    
    # Get location data
    print(f"{Colors.BLUE}Locating IP {target_ip} using {args.provider}...{Colors.END}")
    location_data = locator.get_location(target_ip)
    
    if not location_data:
        print(f"{Colors.RED}Failed to get location data{Colors.END}")
        sys.exit(1)
    
    # Print results
    print()
    print_location_data(location_data, args.format)
    
    # Show accuracy information
    if args.format == "simple":
        show_accuracy_info()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}Unexpected error: {e}{Colors.END}")
        sys.exit(1)
