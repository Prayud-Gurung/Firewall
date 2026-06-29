### NFTables

####
###### nft add table inet filter
> This create filter table, just like in iptables
###### nft add chain inet input {type filter hook **input** priority 0 \; policy drop \;}
> Create input chain, just like in iptables.\ This chain is attached to input hook in kernel, in iptables it is pre configured\ Filter type is used to accept, drop, reject, log
###### nft add rule inet filter input tcp dport 22 accept
> Add rule to input chain to allow incomming ssh

#### NFTables operations
1. add, insert
2. list, get, monitor
3. replace, rename, reset
4. delete, flush, destroy

#### Firewall objects
1. Tables
2. Chains
3. Rules
4. Sets
5. Maps
6. Counters
7. Quotas
8. Limits
9. Flow tables
10. Elements

#### Types in chain
1. filter => accept, drop, reject, log
2. nat => snat, dnat, masquerade
3. route => equivalent to mangle

#### Family
1. ip => ipv4
2. ip6 => ipv6
3. inet => ipv4 + ipv6
4. bridege => Ethernet bridge
5. arp => arp
6. netdev => Interface ingress

### Sets
nft add set inet customtable customlist { type ipv4_addr ;}
> Create a set or list of ipv4 address
nft add elements inet customtable customlist { 10.0.0.1, 10.0.0.2 }
> Add elements to the set
nft add rule inet customtable customchain ip saddr @customlist drop
> Add rule to the chain where source destination in customlist is dropped

### Maps
nft add map inet customtable custommap { type ipv4_addr : verdict }
nft add element inet customtable custommap { 10.0.0.1 : accept, 10.0.0.2: accept, 10.0.0.3: drop }
nft add rule inet customtable customchain ip saddr vmap @custommap

nft add map inet customtable portmap { type inet_service: verdict }
nft add elemeent inet customtable portmap { 22: accept, 80: drop, 443: accept }
nft add rule inet customtable customchain tcp dport vmap @portmap

nft add map inet customtable concat { type ipv4_addr . inet_service : verdict }
nft add element inet customtable concat {192.168.1.20 . 22 : drop, 10.0.0.3 . 22: accept}
nft add rule inet customtable customchain ip saddr . tcp dport vmap @concat

#### Types in Sets and maps
1. ipv4_addr
2. ipv6_addr
3. inet_service
4. ifname
5. ether_addr
6. inet_proto
7. verdict
8. boolean
9. time
10. rate
