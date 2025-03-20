#!/usr/bin/env python3
import argparse
import socket
import requests
import json
import os
import sys
import time
import platform
from getpass import getpass
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import whois
import ipaddress
import re
from datetime import datetime
import threading
import signal
from typing import Tuple

# ASCII art banner with color support
BANNER = """
\033[1;36m██╗  ██╗██╗   ██╗███████╗███████╗███████╗██╗███╗   ██╗
██║  ██║██║   ██║██╔════╝██╔════╝██╔════╝██║████╗  ██║
███████║██║   ██║███████╗███████╗█████╗  ██║██╔██╗ ██║
██╔══██║██║   ██║╚════██║╚════██║██╔══╝  ██║██║╚██╗██║
██║  ██║╚██████╔╝███████║███████║███████╗██║██║ ╚████║
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝\033[0m
                                                      
\033[1;32mUniversal Cybersecurity CLI Tool | Created by Hussein Taha
Version 1.0.8 | Type 'hussein -h' for help\033[0m
"""


class HusseinTool:
    def __init__(self):
        self.parser = self._create_parser()
        self.running = True
        self.progress_thread = None
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        """Handle interrupt signals gracefully"""
        print("\n\033[1;33m[!] Operation interrupted by user\033[0m")
        self.running = False
        sys.exit(0)
        
    def _create_parser(self):
        parser = argparse.ArgumentParser(
            description="HUSSEIN - Universal Cybersecurity CLI Tool",
            usage="hussein <command> [options]"
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Commands")
        
        # Scan command with improved options
        scan_parser = subparsers.add_parser("scan", help="Scan network for open ports")
        scan_parser.add_argument("target", help="Target IP address or hostname")
        scan_parser.add_argument("-p", "--ports", help="Port range to scan (e.g., 22-100)", default="1-1000")
        scan_parser.add_argument("-t", "--timeout", help="Timeout for each port (seconds)", type=float, default=0.5)
        scan_parser.add_argument("-v", "--verbose", help="Show detailed output", action="store_true")
        scan_parser.add_argument("-o", "--output", help="Output file for results")
        
        # IP info command
        ip_parser = subparsers.add_parser("ip", help="Show IP information")
        ip_parser.add_argument("-d", "--detailed", help="Show detailed network information", action="store_true")
        
        # Geo IP command
        geo_parser = subparsers.add_parser("geo", help="Get geolocation info for an IP")
        geo_parser.add_argument("ip", help="IP address to lookup")
        geo_parser.add_argument("-o", "--output", help="Output file for results")
        
        # Encrypt command
        encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file using AES")
        encrypt_parser.add_argument("file", help="File to encrypt")
        encrypt_parser.add_argument("-o", "--output", help="Output file path (default: input.enc)")
        
        # Decrypt command
        decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt an encrypted file")
        decrypt_parser.add_argument("file", help="File to decrypt")
        decrypt_parser.add_argument("-o", "--output", help="Output file path (default: input without .enc)")
        
        # WHOIS command
        whois_parser = subparsers.add_parser("whois", help="Get WHOIS information")
        whois_parser.add_argument("domain", help="Domain or IP to lookup")
        whois_parser.add_argument("-o", "--output", help="Output file for results")
        
        # Subdomains command
        subdomains_parser = subparsers.add_parser("subdomains", help="Find subdomains of a domain")
        subdomains_parser.add_argument("domain", help="Domain to scan for subdomains")
        subdomains_parser.add_argument("-w", "--wordlist", help="Path to subdomain wordlist")
        subdomains_parser.add_argument("-o", "--output", help="Output file for results")
        subdomains_parser.add_argument("-t", "--timeout", help="DNS lookup timeout", type=float, default=1.0)
        
        # Add a new hash command
        hash_parser = subparsers.add_parser("hash", help="Generate hash of a file or string")
        hash_parser.add_argument("input", help="File path or string to hash")
        hash_parser.add_argument("-a", "--algorithm", help="Hash algorithm (md5, sha1, sha256, sha512)", default="sha256")
        hash_parser.add_argument("-f", "--file", help="Input is a file path", action="store_true")
      
        # Add update command
        update_parser = subparsers.add_parser("update", help="Check for updates and update the tool")
        update_parser.add_argument("--force", help="Force update without confirmation", action="store_true")

        return parser
    
    def clear_screen(self):
        """Clear the terminal screen based on OS"""
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')
            
    def run(self):
        # Clear the screen first
        self.clear_screen()
        print(BANNER)
        
        args = self.parser.parse_args()
        
        if not args.command:
            self.parser.print_help()
            return
        
        try:
            # Only initialize progress animation for subdomains, not for scan
            if args.command == "subdomains":
                self.start_progress_animation(f"Preparing {args.command} operation")
            
            if args.command == "scan":
                self.scan_network(args.target, args.ports, args.timeout, args.verbose, args.output)
            elif args.command == "update":
                self.check_for_updates(args.force if hasattr(args, 'force') else False)
            elif args.command == "ip":
                self.show_ip_info(args.detailed)
            elif args.command == "geo":
                self.geolocate_ip(args.ip, args.output)
            elif args.command == "encrypt":
                self.encrypt_file(args.file, args.output)
            elif args.command == "decrypt":
                self.decrypt_file(args.file, args.output)
            elif args.command == "whois":
                self.whois_lookup(args.domain, args.output)
            elif args.command == "subdomains":
                self.stop_progress_animation()
                self.find_subdomains(args.domain, args.wordlist, args.timeout, args.output)
            elif args.command == "hash":
                self.generate_hash(args.input, args.algorithm, args.file)
                
        except KeyboardInterrupt:
            print("\n\033[1;33m[!] Operation interrupted by user\033[0m")
        except Exception as e:
            print(f"\n\033[1;31m[!] Error: {e}\033[0m")
            if hasattr(args, 'verbose') and args.verbose:
                import traceback
                print("\nDetailed error information:")
                traceback.print_exc()
        finally:
            self.stop_progress_animation()


    def start_progress_animation(self, message="Processing"):
        """Start a threaded progress animation"""
        self.running = True
        self.progress_thread = threading.Thread(target=self._progress_animation, args=(message,))
        self.progress_thread.daemon = True
        self.progress_thread.start()
        
    def stop_progress_animation(self):
        """Stop the progress animation thread"""
        if self.progress_thread and self.progress_thread.is_alive():
            self.running = False
            self.progress_thread.join(1)
            sys.stdout.write('\r' + ' ' * 80 + '\r')
            sys.stdout.flush()
    
    def _progress_animation(self, message):
        """Display a spinner animation with a message"""
        chars = "|/-\\"
        i = 0
        while self.running:
            sys.stdout.write(f'\r\033[1;34m[{chars[i % len(chars)]}] {message}...\033[0m')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

    def _save_to_file(self, content, output_file, content_type="results"):
        """Save content to a file with proper error handling"""
        try:
            with open(output_file, 'w') as f:
                f.write(content)
            print(f"\n\033[1;32m[+] {content_type.capitalize()} saved to: {output_file}\033[0m")
            return True
        except Exception as e:
            print(f"\n\033[1;31m[!] Error saving to file: {e}\033[0m")
            return False
    
    def scan_network(self, target: str, port_range: str, timeout: float = 0.5, verbose: bool = False, output_file: str = None) -> None:
        """
        Scan a target for open ports with improved feedback and error handling.
        """
        print(f"\n\033[1;34m[*] Scanning target: {target}\033[0m")
        print(f"\033[1;34m[*] Port range: {port_range}\033[0m")

        try:
            # Parse the port range using a helper method
            start_port, end_port = self._parse_port_range(port_range)

            if start_port > end_port:
                start_port, end_port = end_port, start_port
                print("\033[1;33m[!] Port range reversed to lowest-highest\033[0m")

            open_ports = []
            closed_ports = 0
            filtered_ports = 0
            start_time = time.time()

            # Resolve hostname to IP
            try:
                ip = socket.gethostbyname(target)
                if ip != target:
                    print(f"\033[1;34m[*] Resolved {target} to {ip}\033[0m")
            except socket.gaierror:
                raise ValueError(f"Hostname {target} could not be resolved")

            total_ports = end_port - start_port + 1
            print(f"\n\033[1;34m[*] Starting scan on {ip} ({total_ports} ports)...\033[0m")
            print("\033[1;37m" + "═" * 60 + "\033[0m")
            print(f"\033[1;37m{'PORT':<10}{'STATE':<12}{'SERVICE':<20}{'DETAILS':<18}\033[0m")
            print("\033[1;37m" + "═" * 60 + "\033[0m")

            # Start progress animation for the scan
            self.start_progress_animation(f"Scanning ports on {ip}")

            try:
                for port in range(start_port, end_port + 1):
                    if not self.running:
                        break

                    # Update progress animation every 10 ports
                    if (port - start_port) % 10 == 0:
                        progress_percent = (port - start_port) / total_ports * 100
                        self.stop_progress_animation()
                        self.start_progress_animation(f"Scanning: {port}/{end_port} ({progress_percent:.1f}%)")

                    # Use a context manager to ensure socket closure
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(timeout)
                        try:
                            result = sock.connect_ex((ip, port))
                        except socket.error:
                            result = None

                    service = self._get_service_name(port)
                    banner = self._get_banner(ip, port) if verbose and result == 0 else ""

                    if result == 0:
                        open_ports.append(port)
                        # Stop animation to print the result, then restart it
                        self.stop_progress_animation()
                        print(f"\033[1;32m{port:<10}{'open':<12}{service:<20}{banner:<18}\033[0m")
                        self.start_progress_animation(f"Scanning: {port}/{end_port} ({(port - start_port) / total_ports * 100:.1f}%)")
                    elif verbose:
                        # Stop animation to print the result, then restart it
                        self.stop_progress_animation()
                        if result in (111, 10061):  # Connection refused (Linux/Windows)
                            print(f"\033[1;31m{port:<10}{'closed':<12}{service:<20}{'':<18}\033[0m")
                            closed_ports += 1
                        else:
                            print(f"\033[1;33m{port:<10}{'filtered':<12}{service:<20}{'':<18}\033[0m")
                            filtered_ports += 1
                        self.start_progress_animation(f"Scanning: {port}/{end_port} ({(port - start_port) / total_ports * 100:.1f}%)")
                    else:
                        if result in (111, 10061):
                            closed_ports += 1
                        else:
                            filtered_ports += 1

            except KeyboardInterrupt:
                self.stop_progress_animation()
                scan_time = time.time() - start_time
                print("\n\033[1;31m[!] Scan interrupted by user\033[0m")
                print(f"\033[1;32m[+] Partial scan completed in {scan_time:.2f} seconds\033[0m")
                print(f"\033[1;32m[+] {len(open_ports)} ports open, {closed_ports} closed, {filtered_ports} filtered\033[0m")
                return

            # Stop the progress animation before displaying the final results
            self.stop_progress_animation()

            scan_time = time.time() - start_time
            print("\033[1;37m" + "═" * 60 + "\033[0m")
            print(f"\n\033[1;32m[+] Scan completed in {scan_time:.2f} seconds\033[0m")
            print(f"\033[1;32m[+] {len(open_ports)} ports open, {closed_ports} closed, {filtered_ports} filtered\033[0m")

            # Save results if an output file is specified and open ports were found
            if output_file and open_ports:
                result_content = (
                    f"# HUSSEIN Port Scan Results\n"
                    f"# Target: {target} ({ip})\n"
                    f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"# Port range: {port_range}\n"
                    f"# Open ports: {len(open_ports)}\n\n"
                    "PORT\tSTATE\tSERVICE\n"
                    "----\t-----\t-------\n"
                )
                for port in open_ports:
                    service = self._get_service_name(port)
                    result_content += f"{port}\topen\t{service}\n"
                self._save_to_file(result_content, output_file, "scan results")

        except ValueError as ve:
            self.stop_progress_animation()
            print(f"\n\033[1;31m[!] Configuration error: {ve}\033[0m")
        except socket.error as se:
            self.stop_progress_animation()
            print(f"\n\033[1;31m[!] Connection error: {se}\033[0m")
        except Exception as e:
            self.stop_progress_animation()
            print(f"\n\033[1;31m[!] Unexpected error: {e}\033[0m")

    def _parse_port_range(self, port_range: str) -> Tuple[int, int]:
        """
        Parse the port range string and return a tuple (start_port, end_port).
        Accepts a single port (e.g., "80") or a range (e.g., "1-1000").
        """
        if "-" in port_range:
            parts = port_range.split("-")
            if len(parts) != 2:
                raise ValueError("Invalid port range format")
            try:
                start_port, end_port = map(int, parts)
            except ValueError:
                raise ValueError("Invalid port numbers in range")
        else:
            try:
                start_port = end_port = int(port_range)
            except ValueError:
                raise ValueError("Invalid port number")

        if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
            raise ValueError("Port numbers must be between 1 and 65535")
        return start_port, end_port
    
    def _get_banner(self, ip, port):
        """Try to get service banner from an open port"""
        common_requests = {
            80: b"GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % ip.encode(),
            25: b"HELO hussein.tool\r\n",
            22: b"SSH-2.0-HUSSEIN_1.0\r\n",
            21: b"HELP\r\n",
            23: b"\r\n",
            110: b"CAPA\r\n",
            143: b"A1 CAPABILITY\r\n"
        }
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, port))
            
            # For known protocols, send appropriate request
            if port in common_requests:
                sock.send(common_requests[port])
            
            # Read response
            response = sock.recv(1024)
            sock.close()
            
            # Clean and truncate the banner
            banner = response.split(b'\n')[0].strip()
            banner = banner.decode('utf-8', errors='replace')
            return banner[:18]  # Limit length for display
        except:
            return ""
    
    def _get_service_name(self, port):
        """Get service name for common ports with more comprehensive list"""
        common_ports = {
            20: "FTP-data",
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            67: "DHCP",
            68: "DHCP",
            69: "TFTP",
            80: "HTTP",
            88: "Kerberos",
            110: "POP3",
            119: "NNTP",
            123: "NTP",
            137: "NetBIOS",
            138: "NetBIOS",
            139: "NetBIOS",
            143: "IMAP",
            161: "SNMP",
            162: "SNMP",
            389: "LDAP",
            443: "HTTPS",
            445: "SMB",
            500: "IKE",
            514: "Syslog",
            587: "SMTP",
            631: "IPP",
            636: "LDAPS",
            989: "FTPS",
            990: "FTPS",
            993: "IMAPS",
            995: "POP3S",
            1080: "SOCKS",
            1433: "MSSQL",
            1521: "Oracle",
            1723: "PPTP",
            2049: "NFS",
            2082: "cPanel",
            2083: "cPanel",
            2086: "WHM",
            2087: "WHM",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5900: "VNC",
            5901: "VNC",
            6379: "Redis",
            8080: "HTTP-Alt",
            8443: "HTTPS-Alt",
            9000: "Portainer",
            9090: "Cockpit",
            9200: "Elasticsearch",
            9418: "Git",
            27017: "MongoDB"
        }
        return common_ports.get(port, "unknown")
            
    def show_ip_info(self, detailed=False):
        """Show public and local IP information with enhanced details"""
        print("\n\033[1;34m[*] IP Information:\033[0m")
        print("\033[1;37m" + "═" * 60 + "\033[0m")
        
        # Get all local IP addresses
        local_ips = []
        try:
            # Get primary local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            primary_ip = s.getsockname()[0]
            s.close()
            local_ips.append(primary_ip)
            
            # Get all interfaces if detailed is enabled
            if detailed:
                hostname = socket.gethostname()
                print(f"\033[1;37mHostname: \033[0m{hostname}")
                print(f"\033[1;37mFQDN: \033[0m{socket.getfqdn()}")
                
                # Get all IP addresses for all interfaces
                all_ips = socket.getaddrinfo(hostname, None)
                for ip in all_ips:
                    if ip[0] == socket.AF_INET:  # IPv4
                        addr = ip[4][0]
                        if addr not in local_ips and addr != "127.0.0.1":
                            local_ips.append(addr)
        
        except socket.error:
            local_ips.append("Could not determine local IP")
        
        # Display local IPs
        print(f"\033[1;37mPrimary Local IP: \033[0m{local_ips[0]}")
        if detailed and len(local_ips) > 1:
            print("\033[1;37mAll Local IPs:\033[0m")
            for ip in local_ips:
                print(f"  - {ip}")
        
        # Get public IP with timeout and retry
        public_ip = "Could not determine (connection error)"
        for attempt in range(2):  # Try twice
            try:
                response = requests.get("https://api.ipify.org?format=json", timeout=3)
                if response.status_code == 200:
                    public_ip = response.json()["ip"]
                    break
            except requests.RequestException:
                if attempt == 0:  # Only for first attempt
                    print("\033[1;33m[!] First API attempt failed, trying alternative...\033[0m")
                    time.sleep(1)
                try:
                    # Alternative API
                    response = requests.get("https://ifconfig.me/ip", timeout=3)
                    if response.status_code == 200:
                        public_ip = response.text.strip()
                        break
                except:
                    pass
        
        print(f"\033[1;37mPublic IP: \033[0m{public_ip}")
        
        # Show additional network info if detailed
        if detailed:
            print("\n\033[1;34m[*] Additional Network Information:\033[0m")
            print("\033[1;37m" + "═" * 60 + "\033[0m")
            
            # Get MAC address (platform-specific)
            try:
                if platform.system() == "Windows":
                    import uuid
                    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                                   for elements in range(0, 48, 8)][::-1])
                else:
                    # Linux/Mac
                    import uuid
                    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                                   for elements in range(0, 48, 8)][::-1])
                print(f"\033[1;37mMAC Address: \033[0m{mac}")
            except:
                print("\033[1;37mMAC Address: \033[0mUnable to determine")
            
            # Get default gateway
            gateway = "Unable to determine"
            try:
                if platform.system() == "Windows":
                    import subprocess
                    output = subprocess.check_output("ipconfig", shell=True).decode()
                    for line in output.split('\n'):
                        if "Default Gateway" in line and not ":" in line.split(":")[-1].strip():
                            continue
                        if "Default Gateway" in line:
                            gateway = line.split(":")[-1].strip()
                            break
                else:
                    # For Linux/Mac - simplified approach
                    import subprocess
                    output = subprocess.check_output("ip route | grep default", shell=True).decode()
                    gateway = output.split()[2]
            except:
                pass
                
            print(f"\033[1;37mDefault Gateway: \033[0m{gateway}")
            
            # DNS servers
            dns_servers = ["Unable to determine"]
            try:
                import dns.resolver
                dns_servers = dns.resolver.Resolver().nameservers
            except:
                try:
                    # Fallback method for Windows
                    if platform.system() == "Windows":
                        import subprocess
                        output = subprocess.check_output("ipconfig /all", shell=True).decode()
                        dns_servers = []
                        for line in output.split('\n'):
                            if "DNS Servers" in line and not ":" in line.split(":")[-1].strip():
                                continue
                            if "DNS Servers" in line:
                                dns = line.split(":")[-1].strip()
                                if dns and dns not in dns_servers:
                                    dns_servers.append(dns)
                except:
                    pass
            
            print("\033[1;37mDNS Servers: \033[0m")
            for dns in dns_servers:
                print(f"  - {dns}")
                
        print("\033[1;37m" + "═" * 60 + "\033[0m")
    
    def geolocate_ip(self, ip, output_file=None):
        """Get geolocation information for an IP address with improved reliability"""
        print(f"\n\033[1;34m[*] Getting geolocation info for: {ip}\033[0m")
        
        # Validate IP format
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            try:
                # Try to resolve hostname to IP
                resolved_ip = socket.gethostbyname(ip)
                print(f"\033[1;33m[!] Input appears to be a hostname. Resolved to {resolved_ip}\033[0m")
                ip = resolved_ip
            except socket.gaierror:
                print(f"\033[1;31m[!] Invalid IP address or hostname: {ip}\033[0m")
                return
        
        # Try primary API with fallback
        data = None
        apis = [
            {"url": f"https://ipinfo.io/{ip}/json", "parser": lambda r: r.json()},
            {"url": f"https://ipapi.co/{ip}/json", "parser": lambda r: r.json()}
        ]
        
        for api in apis:
            try:
                self.start_progress_animation(f"Contacting geolocation service")
                response = requests.get(api["url"], timeout=5)
                self.stop_progress_animation()
                
                if response.status_code == 200:
                    data = api["parser"](response)
                    break
            except Exception as e:
                self.stop_progress_animation()
                print(f"\033[1;33m[!] API attempt failed: {e}\033[0m")
        
        if not data:
            print(f"\033[1;31m[!] Could not retrieve geolocation data from any API\033[0m")
            return
            
        # Print the results
        print("\n\033[1;32m[+] IP Geolocation Information:\033[0m")
        print("\033[1;37m" + "═" * 60 + "\033[0m")
        
        # Format different APIs into consistent output
        fields = {
            "IP": data.get("ip", "N/A"),
            "Hostname": data.get("hostname", data.get("domain", "N/A")),
            "City": data.get("city", "N/A"),
            "Region": data.get("region", data.get("regionName", "N/A")),
            "Country": data.get("country", "N/A"),
            "Location": data.get("loc", f"{data.get('latitude', '')},{data.get('longitude', '')}"),
            "Organization": data.get("org", data.get("asn", "N/A")),
            "Postal": data.get("postal", data.get("zip", "N/A")),
            "Timezone": data.get("timezone", "N/A")
        }
        
        # Print formatted data
        for key, value in fields.items():
            if value and value != "N/A" and value != ",":
                print(f"\033[1;37m{key}: \033[0m{value}")
        
        print("\033[1;37m" + "═" * 60 + "\033[0m")
        
        # Save to file if requested
        if output_file:
            result_content = f"# HUSSEIN Geolocation Results\n"
            result_content += f"# IP: {ip}\n"
            result_content += f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            for key, value in fields.items():
                if value and value != "N/A" and value != ",":
                    result_content += f"{key}: {value}\n"
                    
            self._save_to_file(result_content, output_file, "geolocation results")
    
    def encrypt_file(self, file_path, output_file=None):
        """Encrypt a file using AES encryption with improved handling"""
        if not os.path.exists(file_path):
            print(f"\033[1;31m[!] File not found: {file_path}\033[0m")
            return
            
        if not os.path.isfile(file_path):
            print(f"\033[1;31m[!] Not a file: {file_path}\033[0m")
            return
            
        file_size = os.path.getsize(file_path)
        print(f"\n\033[1;34m[*] Encrypting file: {file_path} ({self._format_size(file_size)})\033[0m")
        
        # Set output file if not specified
        if not output_file:
            output_file = file_path + ".enc"
        
        # Check if output file already exists
        if os.path.exists(output_file):
            overwrite = input(f"\033[1;33m[?] Output file already exists. Overwrite? (y/n): \033[0m").lower() == 'y'
            if not overwrite:
                print("\033[1;33m[!] Encryption cancelled\033[0m")
                return
            
        # Ask for password with confirmation and strength check
        while True:
            password = getpass("\033[1;34m[*] Enter encryption password: \033[0m")
            
            # Check password strength
            if len(password) < 8:
                print("\033[1;33m[!] Password is too short (minimum 8 characters)\033[0m")
                continue
                
            password_strength = self._check_password_strength(password)
            if password_strength == "weak":
                print("\033[1;33m[!] Weak password. Consider using a stronger one.\033[0m")
                continue_anyway = input("\033[1;33m[?] Continue anyway? (y/n): \033[0m").lower() == 'y'
                if not continue_anyway:
                    continue
            
            confirm_password = getpass("\033[1;34m[*] Confirm password: \033[0m")
            
            if password != confirm_password:
                print("\033[1;31m[!] Passwords do not match\033[0m")
                continue
            
            break
            
        try:
            # Start progress animation
            self.start_progress_animation("Encrypting file")
            
            # Read the file
            with open(file_path, 'rb') as f:
                data = f.read()
                
            # Generate a random salt
            salt = get_random_bytes(16)
            
            # Create a key from the password
            from Crypto.Protocol.KDF import PBKDF2
            key = PBKDF2(password.encode(), salt, dkLen=32)
            
            # Create cipher
            cipher = AES.new(key, AES.MODE_CBC)
            
            # Encrypt the data
            ciphertext = cipher.encrypt(pad(data, AES.block_size))
            
            # Combine salt, IV, and ciphertext
            encrypted_data = salt + cipher.iv + ciphertext
            
            # Write to output file
            with open(output_file, 'wb') as f:
                f.write(encrypted_data)
                
            self.stop_progress_animation()
            
            encrypted_size = os.path.getsize(output_file)
            print(f"\n\033[1;32m[+] File encrypted successfully: {output_file} ({self._format_size(encrypted_size)})\033[0m")
            print(f"\033[1;32m[+] Encryption ratio: {encrypted_size/file_size:.2f}x\033[0m")
            
        except Exception as e:
            self.stop_progress_animation()
            print(f"\033[1;31m[!] Encryption error: {e}\033[0m")
    
    def _check_password_strength(self, password):
        """Check password strength"""
        # Simple password strength checker
        if len(password) < 8:
            return "weak"
        
        score = 0
        # Check for mixed case
        if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
            score += 1
        # Check for digits
        if re.search(r'\d', password):
            score += 1
        # Check for special characters
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
            
        if score < 2:
            return "weak"
        elif score == 2:
            return "medium"
        else:
            return "strong"

    def _format_size(self, size_bytes):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} PB"
    
    def decrypt_file(self, file_path, output_file=None):
        """Decrypt an encrypted file with improved handling"""
        if not os.path.exists(file_path):
            print(f"\033[1;31m[!] File not found: {file_path}\033[0m")
            return
            
        file_size = os.path.getsize(file_path)
        
        if file_size < 48:  # Minimum size for header (salt + IV) + content
            print(f"\033[1;31m[!] File is too small to be a valid encrypted file\033[0m")
            return
            
        if not file_path.endswith(".enc"):
            print("\033[1;33m[!] File does not appear to be encrypted (missing .enc extension)\033[0m")
            continue_anyway = input("\033[1;33m[?] Continue anyway? (y/n): \033[0m").lower() == 'y'
            if not continue_anyway:
                return
                
        print(f"\n\033[1;34m[*] Decrypting file: {file_path} ({self._format_size(file_size)})\033[0m")
        
        # Set output file if not specified
        if not output_file:
            output_file = file_path[:-4] if file_path.endswith(".enc") else file_path + ".dec"
        
        # Check if output file already exists
        if os.path.exists(output_file):
            overwrite = input(f"\033[1;33m[?] Output file already exists. Overwrite? (y/n): \033[0m").lower() == 'y'
            if not overwrite:
                print("\033[1;33m[!] Decryption cancelled\033[0m")
                return
        
        # Ask for password
        password = getpass("\033[1;34m[*] Enter decryption password: \033[0m")
        
        try:
            # Start progress animation
            self.start_progress_animation("Decrypting file")
            
            # Read the encrypted file
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
                
            # Extract salt, IV, and ciphertext
            salt = encrypted_data[:16]
            iv = encrypted_data[16:32]
            ciphertext = encrypted_data[32:]
            
            # Recreate the key from the password and salt
            from Crypto.Protocol.KDF import PBKDF2
            key = PBKDF2(password.encode(), salt, dkLen=32)
            
            # Create cipher
            cipher = AES.new(key, AES.MODE_CBC, iv)
            
            # Decrypt the data
            try:
                decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
                
                # Write to output file
                with open(output_file, 'wb') as f:
                    f.write(decrypted_data)
                
                self.stop_progress_animation()
                decrypted_size = os.path.getsize(output_file)
                print(f"\n\033[1;32m[+] File decrypted successfully: {output_file} ({self._format_size(decrypted_size)})\033[0m")
                
            except ValueError:
                self.stop_progress_animation()
                print("\033[1;31m[!] Decryption failed: Invalid password or corrupted file\033[0m")
                
        except Exception as e:
            self.stop_progress_animation()
            print(f"\033[1;31m[!] Decryption error: {e}\033[0m")
    
    def whois_lookup(self, domain, output_file=None):
        """Perform WHOIS lookup on a domain or IP with improved output handling"""
        print(f"\n\033[1;34m[*] Performing WHOIS lookup for: {domain}\033[0m")
        
        try:
            # Start progress animation
            self.start_progress_animation("Contacting WHOIS servers")
            
            # Check if input is an IP or domain
            try:
                ipaddress.ip_address(domain)
                is_ip = True
            except ValueError:
                is_ip = False
                
            # Perform the lookup
            result = whois.whois(domain)
            self.stop_progress_animation()
            
            print("\n\033[1;32m[+] WHOIS Information:\033[0m")
            print("\033[1;37m" + "═" * 60 + "\033[0m")
            
            # Extract and organize result
            whois_info = {}
            
            # Format the output in a consistent way
            if result:
                # Domain name
                if 'domain_name' in result and result['domain_name']:
                    domain_name = result['domain_name']
                    if isinstance(domain_name, list):
                        whois_info["Domain Name"] = domain_name[0]
                    else:
                        whois_info["Domain Name"] = domain_name
                        
                # Registrar
                if 'registrar' in result and result['registrar']:
                    whois_info["Registrar"] = result['registrar']
                    
                # WHOIS Server
                if 'whois_server' in result and result['whois_server']:
                    whois_info["WHOIS Server"] = result['whois_server']
                    
                # Creation Date
                if 'creation_date' in result and result['creation_date']:
                    creation_date = result['creation_date']
                    if isinstance(creation_date, list) and creation_date:
                        whois_info["Creation Date"] = creation_date[0].strftime('%Y-%m-%d %H:%M:%S') if hasattr(creation_date[0], 'strftime') else creation_date[0]
                    elif creation_date:
                        whois_info["Creation Date"] = creation_date.strftime('%Y-%m-%d %H:%M:%S') if hasattr(creation_date, 'strftime') else creation_date
                        
                # Expiration Date
                if 'expiration_date' in result and result['expiration_date']:
                    expiration_date = result['expiration_date']
                    if isinstance(expiration_date, list) and expiration_date:
                        whois_info["Expiration Date"] = expiration_date[0].strftime('%Y-%m-%d %H:%M:%S') if hasattr(expiration_date[0], 'strftime') else expiration_date[0]
                    elif expiration_date:
                        whois_info["Expiration Date"] = expiration_date.strftime('%Y-%m-%d %H:%M:%S') if hasattr(expiration_date, 'strftime') else expiration_date
                
                # Updated Date
                if 'updated_date' in result and result['updated_date']:
                    updated_date = result['updated_date']
                    if isinstance(updated_date, list) and updated_date:
                        whois_info["Updated Date"] = updated_date[0].strftime('%Y-%m-%d %H:%M:%S') if hasattr(updated_date[0], 'strftime') else updated_date[0]
                    elif updated_date:
                        whois_info["Updated Date"] = updated_date.strftime('%Y-%m-%d %H:%M:%S') if hasattr(updated_date, 'strftime') else updated_date
                
                # Name Servers
                if 'name_servers' in result and result['name_servers']:
                    name_servers = result['name_servers']
                    if isinstance(name_servers, list):
                        if len(name_servers) > 5:
                            whois_info["Name Servers"] = ", ".join(name_servers[:5]) + f" (+ {len(name_servers) - 5} more)"
                        else:
                            whois_info["Name Servers"] = ", ".join(name_servers)
                    else:
                        whois_info["Name Servers"] = name_servers
                
                # Status
                if 'status' in result and result['status']:
                    status = result['status']
                    if isinstance(status, list):
                        if len(status) > 3:
                            whois_info["Status"] = ", ".join(status[:3]) + f" (+ {len(status) - 3} more)"
                        else:
                            whois_info["Status"] = ", ".join(status)
                    else:
                        whois_info["Status"] = status

                # Registrant, Admin, Tech Contact info
                contacts = {
                    "Registrant": "registrant_",
                    "Admin": "admin_",
                    "Tech": "tech_"
                }
                
                for contact_type, prefix in contacts.items():
                    contact_info = {}
                    
                    fields = [
                        ("Name", f"{prefix}name"),
                        ("Organization", f"{prefix}organization"),
                        ("Email", f"{prefix}email"),
                        ("Phone", f"{prefix}phone"),
                        ("Country", f"{prefix}country")
                    ]
                    
                    for label, field in fields:
                        if field in result and result[field]:
                            contact_info[label] = result[field]
                    
                    if contact_info:
                        whois_info[f"{contact_type} Contact"] = contact_info
                
                # Display information
                for key, value in whois_info.items():
                    if isinstance(value, dict):
                        print(f"\033[1;37m{key}:\033[0m")
                        for subkey, subvalue in value.items():
                            print(f"  \033[1;37m{subkey}:\033[0m {subvalue}")
                    else:
                        print(f"\033[1;37m{key}:\033[0m {value}")
            else:
                print("\033[1;31m[!] No WHOIS information found\033[0m")
                
            print("\033[1;37m" + "═" * 60 + "\033[0m")
            
            # Save to file if requested
            if output_file:
                result_content = f"# HUSSEIN WHOIS Results\n"
                result_content += f"# Query: {domain}\n"
                result_content += f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                
                for key, value in whois_info.items():
                    if isinstance(value, dict):
                        result_content += f"{key}:\n"
                        for subkey, subvalue in value.items():
                            result_content += f"  {subkey}: {subvalue}\n"
                    else:
                        result_content += f"{key}: {value}\n"
                        
                self._save_to_file(result_content, output_file, "WHOIS results")
            
        except Exception as e:
            self.stop_progress_animation()
            print(f"\033[1;31m[!] WHOIS lookup failed: {e}\033[0m")
    
    def find_subdomains(self, domain, wordlist_path=None, timeout=1.0, output_file=None):
        """Find subdomains of a given domain with enhanced methods"""
        print(f"\n\033[1;34m[*] Searching for subdomains of: {domain}\033[0m")
        
        # Validate domain format
        if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$', domain):
            print("\033[1;31m[!] Invalid domain format\033[0m")
            return
        
        # Populate wordlist for subdomain bruteforcing
        wordlist = set()
        wordlist.add("www")  # Always check www
        
        # Common subdomains to try if no wordlist provided
        common_subdomains = [
            "mail", "webmail", "remote", "portal", "dev", "test", "staging", "api",
            "admin", "blog", "ftp", "shop", "store", "app", "support", "secure",
            "vpn", "cdn", "m", "mobile", "cloud", "forum", "wiki", "help", "new",
            "images", "img", "videos", "media", "docs", "files", "beta"
        ]
        
        # If wordlist file provided, load it
        if wordlist_path:
            if os.path.exists(wordlist_path):
                try:
                    with open(wordlist_path, 'r') as f:
                        for line in f:
                            subdomain = line.strip().lower()
                            if subdomain:
                                wordlist.add(subdomain)
                    print(f"\033[1;34m[*] Loaded {len(wordlist)} subdomains from wordlist\033[0m")
                except Exception as e:
                    print(f"\033[1;31m[!] Error loading wordlist: {e}\033[0m")
                    # Fall back to common subdomains
                    wordlist.update(common_subdomains)
            else:
                print(f"\033[1;31m[!] Wordlist file not found: {wordlist_path}\033[0m")
                print("\033[1;33m[*] Falling back to common subdomains list\033[0m")
                wordlist.update(common_subdomains)
        else:
            print(f"\033[1;34m[*] No wordlist provided, using {len(common_subdomains)} common subdomains\033[0m")
            wordlist.update(common_subdomains)
            
        # Found subdomains collection
        found_subdomains = []
        
        # Start progress animation
        self.start_progress_animation(f"Scanning subdomains (0/{len(wordlist)})")
        
        # Counter for progress reporting
        count = 0
        total = len(wordlist)
        
        print("\n\033[1;37m" + "═" * 60 + "\033[0m")
        
        try:
            # Try each subdomain
            for subdomain in wordlist:
                if not self.running:
                    break
                    
                count += 1
                if count % 10 == 0:  # Update progress every 10 attempts
                    self.stop_progress_animation()
                    self.start_progress_animation(f"Scanning subdomains ({count}/{total})")
                
                hostname = f"{subdomain}.{domain}"
                try:
                    # Try to resolve the hostname
                    ip = socket.gethostbyname(hostname)
                    found_subdomains.append((hostname, ip))
                    self.stop_progress_animation()
                    print(f"\033[1;32m[+] Found: {hostname} ({ip})\033[0m")
                    self.start_progress_animation(f"Scanning subdomains ({count}/{total})")
                except socket.gaierror:
                    pass  # Domain does not resolve, continue to next
                    
                time.sleep(0.1)  # Small delay to be nice to DNS servers
            
            self.stop_progress_animation()
            
            # Summary
            print("\n\033[1;37m" + "═" * 60 + "\033[0m")
            print(f"\033[1;32m[+] Subdomain scan completed: {len(found_subdomains)} found\033[0m")
            
            if found_subdomains:
                # Sort subdomains alphabetically
                found_subdomains.sort(key=lambda x: x[0])
                
                # List all found subdomains
                print("\n\033[1;34m[*] Found subdomains:\033[0m")
                print("\033[1;37m" + "═" * 60 + "\033[0m")
                print(f"{'SUBDOMAIN':<40} {'IP ADDRESS':<15}")
                print("\033[1;37m" + "═" * 60 + "\033[0m")
                
                for hostname, ip in found_subdomains:
                    print(f"{hostname:<40} {ip:<15}")
                
                # Save to file if requested
                if output_file:
                    result_content = f"# HUSSEIN Subdomain Scan Results\n"
                    result_content += f"# Target domain: {domain}\n"
                    result_content += f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    result_content += f"# Found subdomains: {len(found_subdomains)}\n\n"
                    result_content += "SUBDOMAIN,IP ADDRESS\n"
                    
                    for hostname, ip in found_subdomains:
                        result_content += f"{hostname},{ip}\n"
                        
                    self._save_to_file(result_content, output_file, "subdomain scan results")
            
        except KeyboardInterrupt:
            self.stop_progress_animation()
            print("\n\033[1;33m[!] Subdomain scan interrupted\033[0m")
        except Exception as e:
            self.stop_progress_animation()
            print(f"\n\033[1;31m[!] Error during subdomain scan: {e}\033[0m")

    def generate_hash(self, input_data, algorithm="sha256", is_file=False):
        """Generate hash of a file or string using various algorithms"""
        import hashlib
        
        algorithms = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512
        }
        
        if algorithm.lower() not in algorithms:
            print(f"\033[1;31m[!] Unsupported algorithm: {algorithm}\033[0m")
            print(f"\033[1;33m[*] Supported algorithms: {', '.join(algorithms.keys())}\033[0m")
            return
            
        hash_func = algorithms[algorithm.lower()]
        
        try:
            if is_file:
                if not os.path.exists(input_data):
                    print(f"\033[1;31m[!] File not found: {input_data}\033[0m")
                    return
                    
                file_size = os.path.getsize(input_data)
                print(f"\n\033[1;34m[*] Generating {algorithm.upper()} hash of file: {input_data} ({self._format_size(file_size)})\033[0m")
                
                # Start progress animation for larger files
                if file_size > 1024 * 1024:  # 1MB
                    self.start_progress_animation(f"Generating {algorithm.upper()} hash")
                  
                # Read file in chunks to handle large files
                hasher = hash_func()
                with open(input_data, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b''):
                        hasher.update(chunk)
             
                hash_value = hasher.hexdigest()
                
                if file_size > 1024 * 1024:
                    self.stop_progress_animation()
            else:
                print(f"\n\033[1;34m[*] Generating {algorithm.upper()} hash of string\033[0m")
                hasher = hash_func()
                hasher.update(input_data.encode())
                hash_value = hasher.hexdigest()
            
            print("\n\033[1;32m[+] Hash generated:\033[0m")
            print("\033[1;37m" + "═" * 60 + "\033[0m")
            print(f"\033[1;37mAlgorithm: \033[0m{algorithm.upper()}")
            print(f"\033[1;37mHash: \033[0m{hash_value}")
            print("\033[1;37m" + "═" * 60 + "\033[0m")
            
        except Exception as e:
            if hasattr(self, 'progress_thread') and self.progress_thread and self.progress_thread.is_alive():
                self.stop_progress_animation()
            print(f"\033[1;31m[!] Error generating hash: {e}\033[0m")

    def check_for_updates(self, force=False):
        """Check for updates and update the tool if installed via pipx"""
        print("\n\033[1;34m[*] Checking for updates...\033[0m")
        current_version = self.get_current_version()

        try:
            self.start_progress_animation("Contacting update server")
            # Get the latest version from PyPI
            latest_version, changes = self.fetch_latest_version_info()
            self.stop_progress_animation()

            if latest_version > current_version:
                print(f"\n\033[1;32m[+] Update available: v{latest_version}\033[0m")
                print("\n\033[1;34m[*] Changes in this version:\033[0m")
                for change in changes:
                    print(f" \033[1;37m{change}\033[0m")

                if force or input("\n\033[1;33m[?] Do you want to update now? (y/n): \033[0m").lower() == 'y':
                    self.start_progress_animation("Updating package")
                    success, message = self.update_package()
                    self.stop_progress_animation()

                    if success:
                        print("\n\033[1;32m[+] Update completed successfully!\033[0m")
                        print("\033[1;32m[+] Please restart HUSSEIN to use the new version.\033[0m")
                    else:
                        print(f"\n\033[1;31m[!] Update failed: {message}\033[0m")
                        print("\033[1;33m[!] Try updating manually with: pipx upgrade hussein\033[0m")
                else:
                    print("\n\033[1;33m[!] Update canceled by user\033[0m")
            else:
                print(f"\n\033[1;32m[+] HUSSEIN is already up to date (v{current_version})\033[0m")
        except Exception as e:
            self.stop_progress_animation()
            print(f"\n\033[1;31m[!] Update check failed: {e}\033[0m")
            print("\033[1;33m[!] You can manually update with: pipx upgrade hussein\033[0m")

    def get_current_version(self):
        """Get the current version of the package from __init__.py or metadata"""
        
        # Attempt to read version from __init__.py
        try:
            init_path = os.path.join(os.path.dirname(__file__), "__init__.py")
            init_path = os.path.abspath(init_path)
            if os.path.exists(init_path):
                with open(init_path, "r", encoding="utf-8") as f:
                    init_content = f.read()
                version_match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", init_content)
                if version_match:
                    return version_match.group(1)
        except Exception as e:
            print(f"Error reading version from __init__.py: {e}")

        # Fallback to installed package version using metadata
        try:
            from importlib.metadata import version  
            return version("hussein")  # Get installed package version
        except Exception as e:
            print(f"Error fetching installed package version: {e}")
            return "unknown"  # Return "unknown" if all methods fail



    def fetch_latest_version_info(self):
        """Fetch the latest version and changes from PyPI"""
        import json
        import urllib.request

        try:
            # Get package info from PyPI
            with urllib.request.urlopen("https://pypi.org/pypi/hussein/json") as response:
                data = json.loads(response.read().decode())

            latest_version = data["info"]["version"]

            # Extract changes from release history or description
            # This is a simplified approach - actual implementation may vary based on how you store release notes
            changes = []
            description = data["info"]["description"]

            # Extract changes from the latest release in the description
            # This assumes a certain format in your README/description
            if f"## {latest_version}" in description:
                changes_section = description.split(f"## {latest_version}")[1].split("##")[0]
                changes = [line.strip() for line in changes_section.strip().split("\n") 
                          if line.strip().startswith("-")][:5]  # Get first 5 changes

            # Fallback if no changes found
            if not changes:
                changes = ["- New features and bug fixes"]

            return latest_version, changes
        except Exception as e:
            # If we can't fetch info, raise to the caller
            raise Exception(f"Could not fetch version info: {str(e)}")

    def update_package(self):
        """Update the package using pipx"""
        import subprocess
        import sys

        try:
            # Run pipx upgrade command
            result = subprocess.run(
                ["pipx", "upgrade", "hussein"],
                capture_output=True,
                text=True,
                check=False  # Don't raise exception on non-zero exit
            )

            if result.returncode == 0:
                return True, "Success"
            else:
                return False, result.stderr or "Unknown error"
        except FileNotFoundError:
            return False, "pipx command not found. Is pipx installed?"
        except Exception as e:
            return False, str(e)


def main():
    tool = HusseinTool()
    tool.run()

if __name__ == "__main__":
    main()