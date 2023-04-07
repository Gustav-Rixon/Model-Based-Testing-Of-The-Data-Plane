import subprocess
import re
import select
import pynng
import threading


def find_pattern(pattern, timeout):
    address = 'tcp://0.0.0.0:65432'  # listen on all available interfaces
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

            # Define a function to check the timeout and terminate tcpdump if necessary
            def check_timeout():
                nonlocal pattern_found
                nonlocal tcpdump_process
                nonlocal socket

                # Wait for the specified timeout
                timeout_event.wait(timeout)

                # If the pattern hasn't been found, terminate tcpdump and publish the False message
                if not pattern_found:
                    tcpdump_process.terminate()
                    msg = "False".encode()
                    socket.send(msg)

            # Start a thread to check for the timeout
            timeout_event = threading.Event()
            timeout_thread = threading.Thread(target=check_timeout)
            timeout_thread.start()

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

            # Signal the timeout thread to stop waiting
            timeout_event.set()

            # Return the appropriate value based on whether the pattern was found or not
            if pattern_found:
                msg = "True".encode()
                socket.send(msg)
            else:
                msg = "False".encode()
                socket.send(msg)


# If no msg found in 10 sek restart
find_pattern("tjaa", 10)
