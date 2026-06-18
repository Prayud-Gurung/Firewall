from rule import Rule
class Firewall:
    def __init__(self, rules_file):
        self.rules = []
        self.load_rules(rules_file)
        pass

    def load_rules(self, filepath):
        print("Loading rules from ruses.conf")
        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                action = parts[0]
                src_ip = parts[1]
                port = parts[2] if len(parts) > 2 else "*"
                protocol = parts[3] if len(parts) > 3 else "*"

                rule = Rule(action, src_ip, port, protocol)
                self.rules.append(rule)
                print(f"Loaded rule: {rule}")
    
    def inspect_packet(self, packet):
        for rule in self.rules:
            if rule.match(packet):
                return rule.action, rule
        return "block", "Default Policy"


