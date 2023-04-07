from scapy.all import *


# TODO
#   Becasue of how i send pkt's i need to add a
#   TCPDUMP sniffer that finds the pkt on the dst host and reports it to the oracle.
#   Send some Raw data to find in the logs using regex?
def send_msg(dstIP, srcMAC, dstMAC, payload,  vlan=None):
    # if vlan is not None:
    #     packet = Ether(src=srcMAC, dst=dstMAC) / \
    #         Dot1Q(vlan=vlan)/IP(dst=dstIP)/ICMP()/Raw(load=payload)
    # else:
    #     packet = Ether(src=srcMAC, dst=dstMAC)/IP(dst=dstIP)/ICMP()

    if vlan is not None:
        packet = Ether(src=srcMAC, dst=dstMAC)/Dot1Q(vlan=vlan) / \
            IP(dst=dstIP)/ICMP()/Raw(load=payload)
    else:
        packet = IP(dst=dstIP)
    print("Packet structure:")
    packet.show()
    sendp(packet)


# Example usage
# ping("10.0.3.10")  # Without VLAN tag

# send_msg(dstIP="10.0.2.2", srcMAC="08:00:00:00:01:11",
#         dstMAC="08:00:00:00:02:22", payload="tjaa")

send_msg(dstIP="10.0.0.10", srcMAC="00:00:00:00:00:02",
         dstMAC="00:00:00:00:00:01", payload="tjaa", vlan=10)  # With VLAN tag

# send_msg("10.0.2.2", srcMAC="08:00:00:00:01:11",
#         dstMAC="08:00:00:00:02:22", payload="tjaa", vlan=20)
