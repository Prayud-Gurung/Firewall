### IPTables

### Built-in tables
1. Filter (default) -> Chains( **INPUT, OUTPUT, FORWARD** ) 
2. NAT -> Chains ( **PREROUTING, OUTPUT, POSTROUTING** )
3. MANGLE -> Change TTL, QOS, etc ( **Advanced Packet Handling** )
4. RAW -> Low Level connection ( **Advance Networking** )
5. SECURITY -> Security policies

### Breakdown
###### iptables -F
>Flush iptables
###### iptables -X
>Remove custom chains
###### iptables -Z
>Reset statistics
###### iptables -P INPUT DROP
>Default drop if no rules match
###### iptables -A INPUT -i lo -j ACCEPT
>Append rule to INPUT from -inbound interface loopback -jump packet to ACCEPT
###### iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
>Append rule to INPUT, also use extra module conntrack that connection, if connection is ESTABLISHED or RELATED and not NEW then -jummp packet to ACCEPT
###### iptables -A INPUT -p tcp --dport 22 -j ACCEPT
>Append rule to INPUT, packets from -protocol with TCP on --destination port 22 -jump packet to ACCEPT
###### iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
>Append rules to FORWARD, when packet is not intended for the machine, let the machine act as a router and forward th epacke from -inbound interface eth0 to outbound interface eth1, -jump packet to ACCEPT
###### iptables -A INPUT -j LOG --log-prefix "DROP: "
>Append rule to INPUT, when packet is being dropped, log with prefix DROP.\Note: This should be placed at the end
###### iptables -t NAT -A PREROUTING -p tcp --dport 80 \ -j DNAT --to-destination 192.168.1.10:80
>Uses tabel NAT and append the rule to PREROUTING, any packets to port TCP/80 gets sent to device with ip 192.168.1.10
###### iptables -t NAT -A PREROUTING -p tcp --dport 80 \ -j REDIRECT --to-ports 8090
>Uses tabel NAT and append the rule to PREROUTING, any packets to port TCP/80 gets sent to proxy port 8080
###### iptables -t MANGLE -A PREROUTING -j MARK --set-mark 1
>Marks the pakets for advacne routing, speed limiting, load balancing, routing table selection, etc
###### iptables -A INPUT -p tcp --dport 22 -m limit --limit 3/min -j ACCEPT
>Append rule to INPUT, rate limiting SSH to 3 per minute


#### Custom Chain in iptable
1. Filtering in INPUT chain
>iptables -N customchain\
>iptables -A INPUT -p tcp --dport 22 -j customchain\
>iptables -A customchain -j ACCEPT

2. Filtering in customchain
>iptables -N customchain\
>iptables -A customchain -p tcp --dport 22 -j ACCEPT\
>iptables -A INPUT -j customchain

## Flags
| Flag | Description |
|---|---|
| -A | Append |
| -i | Incomming interface |
| -o | Outgoing interface |
| -j | Jump |
| -m | Use extra module |
| -ctstate | Connection state |
| -p | Protocol |
| --dport | Destination port |
| -F | Flush iptables |
| -X | Remove custom chains |
| -Z | Reset statistics |
| --log-prefix | Add prefix for log |
| -t | Use table |
| --to-ports | Redirect |