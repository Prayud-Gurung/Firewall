import ipaddress
class Rule:
    def __init__(self, action, src_ip_cidr, port=None, protocol=None):
        self.action = action.lower()
        self.src_network = ipaddress.ip_network(src_ip_cidr, strict=False)
        self.port = int(port) if port and port != "*" else None
        self.protocol = protocol.upper() if protocol and protocol != "*" else None
        pass

    def match(self, packet):
        packet_ip = ipaddress.ip_address(packet.src_ip)
        if packet_ip not in self.src_network:
            return False
        if self.protocol and self.protocol != packet.protocol:
            return False
        if self.port and self.port != packet.port:
            return False
        return True
    
    def __repr__(self):
        return f"Rule({self.action.upper()}: IP={self.src_network}, Port={self.port}, Protocol={self.protocol})"
        pass