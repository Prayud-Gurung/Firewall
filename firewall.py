from scapy.all import sniff, IP, TCP, send
import ipaddress

block_ports = [22, 80, 443]
# block_IPs = ["10.10.10.10", "15.10.10.0"]

def process_packets(packet):
    if not packet.haslayer(IP) or not packet.haslayer(TCP):
        return
    
    dport = packet[TCP].dport
    sport = packet[TCP].sport

    if dport in block_ports or sport in block_ports:
        #packet incomming (sport = 3030, dport = 443, src=10.10.10.10, dest=. my machine)
        #now to send packet if dest=443 the send(sport=443, dport=3030, src=mymachine, dest=10.10.10.10)
        print(f"incomming packet in port {dport} blocked!")
        ip = IP(src=packet[IP].dst, dst= packet[IP].src)
        tcp = TCP(sport=dport, dport=sport, flags="R", seq=packet[TCP].ack if hasattr(packet[TCP], "ack") else 0)
        reset_packet= ip/tcp
        send(reset_packet, verbose=False)
        print(f"Sent reset packet")
    pass

#region
# def process_packets(packet):

#     if not packet.haslayer(IP) or not packet.haslayer(TCP):
#         return
#     ip = packet[IP]
#     tcp = packet[TCP]

#     dport = tcp.dport
#     sport = tcp.sport

#     # block any traffic involving these ports (both directions)
#     if dport in block_ports or sport in block_ports:

#         print(f"[BLOCK] {ip.src}:{sport} -> {ip.dst}:{dport}")

#         rst = IP(
#             src=ip.dst,
#             dst=ip.src
#         ) / TCP(
#             sport=dport,
#             dport=sport,
#             flags="R",
#             seq=tcp.ack if tcp.ack is not None else 0
#         )
#         send(rst, verbose=False)
#         print("Sent reset packet")
#endregion
sniff(filter="tcp", prn= process_packets, store= 0)