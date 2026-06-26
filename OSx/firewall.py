#!/usr/bin/env python3
import subprocess
import atexit

ANCHOR_FILE = "/etc/pf.anchors/myrules"
PF_CONF = "/etc/pf.conf"

blocked_ports = [22, 23, 3389]
blocked_networks = ["192.168.1.50", "10.0.0.0/24", "172.16.5.10"]

rules = []

def write_rules():
    rules.append("# Auto-generated PF rules\n")
    for port in blocked_ports:
        rules.append(f"block drop proto tcp from any to any port {port}")
        rules.append(f"block drop proto udp from any to any port {port}")
    for net in blocked_networks:
        rules.append(f"block drop from {net} to any")
        rules.append(f"block drop from any to {net}")
    rule_text = "\n".join(rules) + "\n"
    return rule_text
    pass

def create_anchor():
    print(f"[+] Writing rules to {ANCHOR_FILE}")
    with open(ANCHOR_FILE, "w") as f:
        f.write(write_rules())
    pass

def write_pfconf():
    anchor_snippet = """
    anchor "myrules"
    load anchor "myrules" from "/etc/pf.anchors/myrules"
    """
    with open(PF_CONF, "r") as f:
        pfconf = f.read()

    if "myrules" not in pfconf:
        print("[+] Adding anchor to pf.conf (requires sudo)")
        with open(PF_CONF, "a") as f:
            f.write(anchor_snippet)
    pass

print("[+] Reloading PF rules")
def cleanup():
    
    pass

atexit.register(cleanup)
try:
    subprocess.run(["sudo", "pfctl", "-f", PF_CONF], check=True)
    subprocess.run(["sudo", "pfctl", "-e"], check=True)
    print("[+] PF updated successfully")
except subprocess.CalledProcessError as e:
    print("[-] Failed to reload PF:", e)



print("[+] Done")