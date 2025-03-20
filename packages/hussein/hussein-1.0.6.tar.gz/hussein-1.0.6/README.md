# HUSSEIN - Universal Cybersecurity CLI Tool

```
██╗  ██╗██╗   ██╗███████╗███████╗███████╗██╗███╗   ██╗
██║  ██║██║   ██║██╔════╝██╔════╝██╔════╝██║████╗  ██║
███████║██║   ██║███████╗███████╗█████╗  ██║██╔██╗ ██║
██╔══██║██║   ██║╚════██║╚════██║██╔══╝  ██║██║╚██╗██║
██║  ██║╚██████╔╝███████║███████║███████╗██║██║ ╚████║
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝
```

**HUSSEIN** is a lightweight yet powerful command-line cybersecurity tool designed for both **red team (offensive) and blue team (defensive) professionals**. This tool provides essential functionalities such as **network scanning, IP tracking, encryption, WHOIS lookup, subdomain enumeration, and system hardening**.

## Installation On Kali Linux

For an isolated, system-wide installation, use [pipx](https://pypa.github.io/pipx/):

```bash
# Install pipx if not installed
sudo apt update
sudo apt install -y pipx
python3 -m pipx ensurepath

# Install Hussein tool globally
pipx install hussein

# Confirm installation
hussein --help

```
## Installation On windows

```bash
# Install pipx if not installed
python -m pip install --user pipx
python -m pipx ensurepath

# Install Hussein tool globally
pipx install hussein

# Confirm installation
hussein --help

```
## Features

- Network scanning for open ports and services
- IP information retrieval (public, local, geolocation)
- File encryption and decryption using AES
- WHOIS domain and IP lookup
- Subdomain enumeration for websites

## Usage

```bash
# Show help
hussein -h

# Scan a network
hussein scan 192.168.1.1 -p 1-1000

# Show IP information
hussein ip

# Get geolocation info for an IP
hussein geo 8.8.8.8

# Encrypt a file
hussein encrypt file.txt

# Decrypt a file
hussein decrypt file.txt.enc

# Get WHOIS information
hussein whois example.com

# Find subdomains
hussein subdomains example.com -o subdomains.txt
```

## Project Credits & Branding

- **Tool Name**: HUSSEIN
- **Creator**: Hussein Taha
- **Platform**: Python
- **Category**: Cybersecurity, Ethical Hacking, Pentesting
- **Inspired by**: Nmap, Metasploit, Recon-ng, Shodan, OSINT Framework
- **Target Audience**: Ethical Hackers, Pentesters, System Admins, Blue & Red Team Operators

## License

MIT License

## Roadmap

- Automation & reporting capabilities
- Integration with Shodan/ZoomEye APIs
- Custom exploit module
- Web vulnerability scanner