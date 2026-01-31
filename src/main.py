from scapy.all import *

packet = IP(dst="google.com")/ICMP()
response = sr1(packet, timeout=2)
if response:
    print(f"Ответ от {response[IP].src}")