import random

class Packet:
    def __init__(self, src_ip, dest_ip, protocol, port, payload=""):
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        self.protocol = protocol
        self.port = port
        self.payload = payload
    
    def __repr__(self):
        return f"Packet(src={self.src_ip}, dest={self.dest_ip}, protocol={self.protocol}, port={self.port})"
    
    @staticmethod
    def generate_random():
        protocols = ["TCP", "UDP", "ICMP"]
        src = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        dest = f"192.168.1.{random.randint(1,100)}"
        protocol = random.choice(protocols)
        port = random.randint(1,65535)

        return Packet(src, dest, protocol, port)
if __name__ == "__main__":
    pkt = Packet.generate_random()
    print(f"Generated Packet: {pkt}")