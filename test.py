from scapy.all import sniff, IP, TCP, send, conf
# capture = sniff(count = 10)
# capture.summary()
# print(capture)
# print("-" * 90)

# captureoffline = sniff(offline=capture, filter="ip")
# captureoffline.summary()

BLOCKED_PORTS = [80, 443] 

def send_reset(packet):
    rst_packet = IP(src=packet[IP].dst, dst=packet[IP].src) / \
                 TCP(sport=packet[TCP].dport, dport=packet[TCP].sport, \
                 flags='RA', seq=packet[TCP].ack)
    send(rst_packet, verbose=0)
    print(f"Reset sent: {packet[IP].src} -> {packet[IP].dst}:{packet[TCP].dport}")

def packet_filter(packet):
    if packet.haslayer(TCP) and packet.haslayer(IP):
        if packet[TCP].dport in BLOCKED_PORTS:
            send_reset(packet)
    return True

print(f"Listening on ...")
sniff(prn=packet_filter, filter="tcp", store=0)   