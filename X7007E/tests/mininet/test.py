from scapy.all import *

# Get the UDP checksum computed by Scapy
#packet = IP(dst="10.0.2.20")/TCP()
packet = IP(dst="10.0.2.15")/TCP()
ans, unans = sr(IP(raw(packet)),timeout=2) # Build packet (automatically done when sending)

print(ans.show())
unans.show()