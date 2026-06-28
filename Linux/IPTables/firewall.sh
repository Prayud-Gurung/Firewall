#!/bin/bash

# Configure firewall to only allow SSH and HTTP connection
# Default policy, drops all packets when no other rules matches
iptables -P INPUT DROP
iptables -P FORWARD DROP
# Allow outgoing packets
iptables -P OUTPUT ACCEPT

# Allow loopback requests
iptables -A INPUT -i lo -j ACCEPT
# Allow packets from established connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Accept request from SSH, HTTP, HTTPS
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Log the pacekt before dropping
iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "DROP: "
iptables -A INPUT -j DROP