# pentit - Universal Cybersecurity CLI Tool

```
██████╗ ███████╗███╗   ██╗████████╗██╗████████╗
██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██║╚══██╔══╝
██████╔╝█████╗  ██╔██╗ ██║   ██║   ██║   ██║   
██╔═══╝ ██╔══╝  ██║╚██╗██║   ██║   ██║   ██║   
██║     ███████╗██║ ╚████║   ██║   ██║   ██║   
╚═╝     ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝   ╚═╝
```

**pentit** is a lightweight yet powerful command-line cybersecurity tool designed for both **red team (offensive) and blue team (defensive) professionals**. This tool provides essential functionalities such as **network scanning, IP tracking, encryption, WHOIS lookup, subdomain enumeration, and system hardening**.

## Installation On Kali Linux

For an isolated, system-wide installation, use [pipx](https://pypa.github.io/pipx/):

```bash
# Install pipx if not installed
sudo apt update
sudo apt install -y pipx
python3 -m pipx ensurepath

# Install pentit tool globally
pipx install pentit

# Confirm installation
pentit --help

```
## Installation On windows

```bash
# Install pipx if not installed
python -m pip install --user pipx
python -m pipx ensurepath

# Install pentit tool globally
pipx install pentit

# Confirm installation
pentit --help

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
pentit -h

# Scan a network
pentit scan 192.168.1.1 -p 1-1000

# Show IP information
pentit ip

# Get geolocation info for an IP
pentit geo 8.8.8.8

# Encrypt a file
pentit encrypt file.txt

# Decrypt a file
pentit decrypt file.txt.enc

# Get WHOIS information
pentit whois example.com

# Find subdomains
pentit subdomains example.com -o subdomains.txt
```

## Project Credits & Branding

- **Tool Name**: pentit
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