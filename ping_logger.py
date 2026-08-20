import subprocess  
#subprocess is a built-in Python module that allows Python to start and communicate with other programs/commands running on your operating system.

import csv
#A CSV file is basically a table stored as plain text.

import os
#The os module provides a way to interact with the operating system, allowing you to perform tasks like file and directory management, environment variable access, and more.

from datetime import datetime
#That timestamp tells us when that particular network measurement was taken.

"""
ping → the Linux networking command
-c → count, meaning how many ping packets to send
1 → send one ping
{target_ip} → the destination IP address
"""
target_ip = "1.1.1.1"
result = subprocess.run(
    ["ping", "-c", "1", target_ip],
    capture_output = True,
    #"Don't simply let the command print everything directly. Capture its output so that my Python program can access it."
    text = True
    #It tells Python to give us the command's output as normal text/string data rather than raw bytes.
)

"""
print(result.stdout)
#print the standard output of the ping command, which contains the result of the ping operation.
"""

line = result.stdout.splitlines()[1]
#splitline() → splits the output into a list of lines, and [1] selects the second line (index 1) which contains the ping result.
#print(line)

parts = line.split()
#split() → splits the selected line into a list of words/parts based on whitespace.

#print(parts[6]) #That's the 7th item, but Python counts from 0, so its index is 6.
latency_ms = float(parts[6].split("=")[1] )
# break down the 7th item (which is "time=138.123 ms") into two parts using "=" as the separator, and take the second part (index 1), which is the actual latency value (e.g., "138.123 ms").
#we're using "=" to separate time from 138.

#we are converting the latency value from a string to a float so that we can perform numerical operations on it later if needed.
print(latency_ms) # Give me the latency value in milliseconds as a float.

#print(type(latency_ms)) 
# # Give me the type of the latency variable, which should be <class 'float'>.

#Now, let's log the latency value along with a timestamp to a file for future reference.
timestamp = datetime.now()
print(timestamp)

#Also gave the target IP address to the log file for reference.
print(target_ip)

#Now, let's find the status of the ping command to determine if it was successful or not. The returncode attribute of the result object will give us this information.
status = "success" if result.returncode == 0 else "failure"
print(status)

# Sequence of the log entry: latency_ms, timestamp, target IP address, and status.

#Now, let's write the log entry to a CSV file. We'll use the csv module to handle this.
"""
"a" means append.
writer.writerow(...) writes one complete row:
latency | timestamp | IP | status
"""
file_exists = os.path.exists("network_latency.csv")
#Check if the CSV file already exists. If it doesn't, we'll create it and write the header row first.

with open("network_latency.csv", "a" , newline="") as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(["latency_ms", "timestamp", "target_ip", "status"])
    writer.writerow([latency_ms, timestamp, target_ip, status])

# Progrss report: The program successfully pings the target IP address, extracts the latency value, logs it along with a timestamp and status to a CSV file, and handles the creation of the file if it doesn't already exist.
"""
There's one important thing still missing.

Currently, every time you manually run:

python3 ping_logger.py

you get one measurement.

Our actual project requirement is to make the program automatically collect measurements, for example:

Ping
 ↓
wait 10 seconds
 ↓
Ping
 ↓
wait 10 seconds
 ↓
Ping
 ↓
...

So the next stage is automation.

Before we add the loop, though, I recommend we make one small improvement to the logger: handle a failed ping safely.

Right now our code assumes that result.stdout.splitlines()[1] exists. If the network fails, that assumption could break the program.

So our next lesson should be:

Successful ping → extract latency
Failed ping → record failed without crashing

Then we'll add the 10-second loop.

That gives us a much more reliable logger before we let it run for an hour.
"""