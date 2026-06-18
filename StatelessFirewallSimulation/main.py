import time
from firewall import Firewall
from packet import Packet

def start_sim(firewall, packets_count):
    print("\n---Starting Simulation---")
    allowed_packets = 0
    blocked_packets = 0

    for i in range(packets_count):
        pkt = Packet.generate_random()
        result, rule = firewall.inspect_packet(pkt)

        print(f"{result.upper()}, packet: source={pkt.src_ip}, port={pkt.port}, protocol={pkt.protocol}")
        if result == "allow":
            allowed_packets += 1
        else:
            blocked_packets += 1
    print("-" * 80)
    print(f"Complete!! Allowed packets: {allowed_packets}, Blocked Packets: {blocked_packets}")

if __name__=="__main__":
    firewall = Firewall("rules.conf")
    start_sim(firewall, 50)