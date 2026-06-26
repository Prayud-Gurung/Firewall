import subprocess
import socket
import dns.resolver
# import re
urls = ["youtube.com", "google.com"]
# for url in urls:
#     res = subprocess.run(["ping", "-c", "1", url], stdout=subprocess.PIPE)
#     match = re.search(r"\((\d+\.\d+\.\d+\.\d+)\)", res.stdout.decode())
#     print(match.group(1))
# for url in urls:
#     try:
#         _, _, ips= socket.gethostbyname_ex(url)
#         for ip in ips:
#             print(f"{url}: ip {ip}")
#     except socket.gaierror:
#         pass

# def get_all_subdomain_ips(domain):
#     subdomains = ['', 'www.', 'm.', 'api.', 'cdn.', 'static.']
#     all_ips = set()
    
#     for prefix in subdomains:
#         full_domain = f"{prefix}{domain}"
#         try:
#             _, _, ips = socket.gethostbyname_ex(full_domain)
#             all_ips.update(ips)
#         except:
#             pass
    
#     return all_ips

# for url in urls:
#     ips = get_all_subdomain_ips(url)
#     print(type(ips))


import dns.resolver
import socket

# Test system DNS
try:
    _, _, ips = socket.gethostbyname_ex('youtube.com')
    print(f"System DNS: {ips}")
except Exception as e:
    print(f"System DNS failed: {e}")

# Test Google DNS
try:
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8']
    answers = resolver.resolve('youtube.com', 'A')
    ips = [str(r) for r in answers]
    print(f"Google DNS: {ips}")
except Exception as e:
    print(f"Google DNS failed: {e}")
