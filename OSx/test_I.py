import subprocess
from pathlib import Path
import shutil
import atexit
import ipaddress
import os
import re
import socket
import dns.resolver

blocked_ports = []
blocked_ip = []
blocked_urls = [
    "youtube.com", 
    "www.youtube.com", 
    "m.youtube.com", 
    "youtu.be",
    "googlevideo.com", 
    "ytimg.com", 
    "i.ytimg.com",
    "googleapis.com",  # Used for YouTube API
    "ggpht.com",       # Google content hosting
    "google.com",      # Some YouTube assets come from google.com
]

if os.geteuid() != 0:
    raise PermissionError("Run as root.")

pfconf = Path("/etc/pf.conf")
shutil.copy(pfconf, "/etc/backup_pf.conf")

def get_ips(domain):
    ip_v4s = set()
    ip_v6s = set()
    try:
        for dns_server in ['8.8.8.8', '1.1.1.1', '9.9.9.9']:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [dns_server]
            try:
                answers = resolver.resolve(domain, 'A')
                answers_v6 = resolver.resolve(domain, 'AAAA')
                for rdata in answers:
                    ip_v4s.add(str(rdata))
                for rdata in answers_v6:
                    ip_v6s.add(str(rdata))
            except:
                pass
    except:
            pass
    return ip_v4s, ip_v6s

def write_rules():
    rules = []
    for port in blocked_ports:
        rules.append(f"block drop proto tcp from any to any port {port}")
        rules.append(f"block drop proto udp from any to any port {port}")
    for ip in blocked_ip:
        ipaddress.ip_address(ip)
        rules.append(f"block drop from {ip} to any")
        rules.append(f"block drop from any to {ip}")

    all_ip_v4s = set()
    all_ip_v6s = set()
    for url in blocked_urls:
        print(f"Resolving {url}...")
        ips_v4s, ips_v6s = get_ips(url)
        all_ip_v4s.update(ips_v4s)
        all_ip_v6s.update(ips_v6s)
    
    for ip in all_ip_v4s:
        rules.append(f"block drop from {ip} to any")
        rules.append(f"block drop from any to {ip}")
    for ip in all_ip_v6s:
        rules.append(f"block drop inet6 from {ip} to any")
        rules.append(f"block drop inet6 from any to {ip}")
    rule_string = "\n".join(rules) + "\n"
    return rule_string

def create_anchor():
    anchor_dir = Path("/etc/pf.anchors")
    anchor_dir.mkdir(exist_ok=True, parents=True)
    path = anchor_dir / "custom_rules"
    with open(path, "w") as file:
        file.write(write_rules())

def update_pfconf():
    pfconf_entry = (
        '\n'
        'anchor "custom_rules"\n'
        'load anchor "custom_rules" from "/etc/pf.anchors/custom_rules"\n'
    )
    with open(pfconf, "r") as file:
        content = file.read()
        if 'load anchor "custom_rules"' not in content:
            with open(pfconf, "a") as f:
                f.write(pfconf_entry)

def reset_pfconf():
    shutil.copy("/etc/backup_pf.conf", pfconf)
    subprocess.run(["pfctl", "-f", "/etc/pf.conf"], check=False)
    anchor = Path("/etc/pf.anchors/custom_rules")
    if anchor.exists():
        anchor.unlink()

atexit.register(reset_pfconf)

try:
    create_anchor()
    update_pfconf()
    # input("Inspect /etc/pf.conf now, then press Enter...")
    subprocess.run(["pfctl", "-nf", "/etc/pf.conf"], check=True)
    subprocess.run(["pfctl", "-f", "/etc/pf.conf"], check=True)
    subprocess.run(["pfctl", "-e"], check=False)
    print("Firewall rules applied. Press Ctrl+C to revert.")
    input()
except KeyboardInterrupt:
    print("\nReverting...")
    reset_pfconf()
except Exception as e:
    print(f"Error: {e}")
    reset_pfconf()