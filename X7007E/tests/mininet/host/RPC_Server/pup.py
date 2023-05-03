import subprocess
import re
import select
import pynng
import threading

import socket


def get_computer_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def find_pattern(pattern):
    # listen on all available interfaces
    address = 'tcp://%s:65432' % get_computer_ip()
    with pynng.Pub0(listen=address) as socket:
        while True:
            # Set up the tcpdump command with appropriate flags
            tcpdump_cmd = ["tcpdump", "-l", "-n", "-i", "eth0"]

            # Start tcpdump and capture its output as a stream
            tcpdump_process = subprocess.Popen(
                tcpdump_cmd, stdout=subprocess.PIPE)

            # Set up the regex pattern to search for
            pattern = re.compile(pattern)

            # Initialize the pattern found flag to False
            pattern_found = False

            # Iterate over the lines of tcpdump's output
            while True:
                # Wait for the stream to become ready for reading
                ready, _, _ = select.select(
                    [tcpdump_process.stdout], [], [], None)

                # If the stream is not ready, terminate the program
                if not ready:
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

            # Return the appropriate value based on whether the pattern was found or not
            if pattern_found:
                msg = "True".encode()
                socket.send(msg)
            else:
                msg = "False".encode()
                socket.send(msg)


find_pattern("tjaa")
