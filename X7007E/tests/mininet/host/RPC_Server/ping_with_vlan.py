from scapy.all import *


def send_msg(dstIP, srcMAC, dstMAC, payload,  vlan=None):

    if vlan is not None:
        packet = Ether(src=srcMAC, dst=dstMAC)/Dot1Q(vlan=vlan) / \
            IP(dst=dstIP)/ICMP()/Raw(load=payload)
    else:
        packet = Ether(src=srcMAC, dst=dstMAC) / \
            IP(dst=dstIP)/ICMP()/Raw(load=payload)
    print("Packet structure:")
    packet.show()
    sendp(packet)


send_msg(dstIP="10.0.3.10", srcMAC="00:00:00:00:00:03",
         dstMAC="00:00:00:00:00:04", payload="tjaa", vlan=10)  # With VLAN tag
