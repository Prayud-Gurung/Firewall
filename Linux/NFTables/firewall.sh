#!/bin/bash

# configure firewall to only allow SSH and HTTP connection
nft add table inet customtable
#create a table called customtable, unlike iptables
nft add chain inet customtable customchain {type filter hook input priority 0 \; policy drop\;}
nft add chain inet customtable customchain iif lo accept
nft add rule inet customtable customchain ct state established,related accept
#add rule to accept loopback from inbound interface, oif => outbound interface
nft add rule inet customtable customchain tcp dport {22, 80, 443} accept
#can create set, much simpler than iptables