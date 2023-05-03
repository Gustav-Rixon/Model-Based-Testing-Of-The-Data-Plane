from scapy.all import *
import pynng


def Send(dstIP, srcMAC, dstMAC, payload,  vlan=None):

    if vlan is not None:
        packet = Ether(src=srcMAC, dst=dstMAC)/Dot1Q(vlan=vlan) / \
            IP(dst=dstIP)/ICMP()/Raw(load=payload)
    else:
        packet = Ether(src=srcMAC, dst=dstMAC) / \
            IP(dst=dstIP)/ICMP()/Raw(load=payload)
    print("Packet structure:")
    packet.show()
    sendp(packet)


def Sub(target, max_timeouts):
    address = f'tcp://{target}:65432'
    timeouts = 0
    try:
        with pynng.Sub0(dial=address, recv_timeout=1) as socket:
            socket.subscribe(b'')

            while timeouts <= max_timeouts:
                try:
                    Send(dstIP="10.0.1.10", srcMAC="00:00:00:00:00:01",
                         dstMAC="00:00:00:00:00:02", payload="tjaa", vlan=10)
                    Send(dstIP="10.0.1.10", srcMAC="00:00:00:00:00:01",
                         dstMAC="00:00:00:00:00:02", payload="tjaa", vlan=10)
                    Send(dstIP="10.0.1.10", srcMAC="00:00:00:00:00:01",
                         dstMAC="00:00:00:00:00:02", payload="tjaa", vlan=10)
                    Send(dstIP="10.0.1.10", srcMAC="00:00:00:00:00:01",
                         dstMAC="00:00:00:00:00:02", payload="tjaa", vlan=10)
                    if socket.recv().decode() == 'True':
                        return True
                except pynng.Timeout:
                    timeouts += 1
    except pynng.exceptions.NNGException as e:  # This is a problem
        print(f"Connection error: {e}")
        return (f"Connection error: {e}")

    return False


res = Sub('10.0.1.10', 5)
print(res)
