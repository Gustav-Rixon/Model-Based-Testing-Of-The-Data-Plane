# saved as greeting-server.py
import Pyro5.api
import json
from scapy.all import *
import pynng
import socket


def Find_pattern(pattern, timeout):
    # Set up the tcpdump command with appropriate flags
    tcpdump_cmd = ["tcpdump", "-l", "-n", "-i", "eth0"]

    # Start tcpdump and capture its output as a stream
    tcpdump_process = subprocess.Popen(tcpdump_cmd, stdout=subprocess.PIPE)

    # Set up the regex pattern to search for
    pattern = re.compile(pattern)

    # Set up the start time
    start_time = time.time()

    # Initialize the pattern found flag to False
    pattern_found = False

    # Iterate over the lines of tcpdump's output
    while True:
        # Wait for the stream to become ready for reading within the timeout interval
        ready, _, _ = select.select(
            [tcpdump_process.stdout], [], [], timeout)

        # If the stream is not ready within the timeout interval, terminate the program
        if not ready:
            print(f"Pattern not found within {timeout} seconds.")
            tcpdump_process.terminate()
            break

        # Read the line from the stream
        line = tcpdump_process.stdout.readline()

        # If the line is empty, terminate the program
        if not line:
            break

        # Decode the bytes into a string and remove whitespace
        decoded_line = line.decode().strip()

        # Search for the pattern in the line
        match = pattern.search(decoded_line)

        # If the pattern is found, print the line, set the pattern found flag to True, and terminate the program
        if match:
            print(decoded_line)
            pattern_found = True
            tcpdump_process.terminate()
            break

        # If the timeout interval has elapsed, terminate the program
        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout:
            print(f"Pattern not found within {timeout} seconds.")
            tcpdump_process.terminate()
            break

    # Return the appropriate value based on whether the pattern was found or not
    if pattern_found:
        return "True".encode()
    else:
        return "False".encode()


def CreateMsg(dstIP, srcMAC, dstMAC, payload,  vlan=None):
    if vlan is not None:
        pkt = Ether(src=srcMAC, dst=dstMAC)/Dot1Q(vlan=vlan) / \
            IP(dst=dstIP)/ICMP()/Raw(load=payload)
    else:
        pkt = Ether(src=srcMAC, dst=dstMAC) / \
            IP(dst=dstIP)/ICMP()/Raw(load=payload)
    return pkt


@Pyro5.api.expose
class GreetingMaker(object):
    def get_fortune(self):
        return "s"

    def sendPkt(self, data):
        data = json.loads(data)
        pkt = CreateMsg(dstIP=data["dstIP"], srcMAC=data["srcMAC"],
                        dstMAC=data["dstMAC"], payload="tjaa", vlan=10)
        sendp(pkt)

    def pub(self, pattern, pup):
        address = 'tcp://0.0.0.0:65432'  # listen on all available interfaces
        with pynng.Pub0(listen=address) as socket:
            print(f"Publisher listening on {address}...")
            msg = Find_pattern(pattern, pup)
            socket.send(msg)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
s.close()

daemon = Pyro5.server.Daemon(host=ip_address)         # make a Pyro daemon
ns = Pyro5.api.locate_ns("0.0.0.0")             # find the name server
# register the greeting maker as a Pyro object
uri = daemon.register(GreetingMaker)
# register the object with a name in the name server
ns.register("example.greeting", uri)

print("Ready.")
# start the event loop of the server to wait for calls
daemon.requestLoop()
