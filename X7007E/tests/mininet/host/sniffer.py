import subprocess
import re
import select
import time


def find_pattern(pattern, timeout):
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
        ready, _, _ = select.select([tcpdump_process.stdout], [], [], timeout)

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
        return True
    else:
        return False


find_pattern("tjaa", 100)
