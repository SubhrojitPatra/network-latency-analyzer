# Data Network Latency Logger

import subprocess 
# to run ping command and capture its output
import csv
# to write the measurement data to a CSV file -- csv means comma-separated values, a common format for storing tabular data
import os
# to check if the CSV file already exists
from datetime import datetime
# to get the current timestamp for each measurement
import time
# to control the duration of the logging and the interval between pings

target_ip = "1.1.1.1" 
# This is the IP address of the target server we want to ping. In this case, it's set to Cloudflare's public DNS server 

# Set the duration of the data collection
start_time = time.time()
duration_hours = 1
duration = duration_hours * 60 * 60  # Convert hours to seconds

while True:
    # Check if the duration has been reached
    elapsed_time = time.time() - start_time
    if elapsed_time >= duration:
        break

    # Run one ping
    result = subprocess.run(
        ["ping", "-c", "1", target_ip],
        capture_output=True,
        text=True
    )

    # Extract latency if ping is successful
    latency_ms = None

    if result.returncode == 0:
        line = result.stdout.splitlines()[1]
        parts = line.split()
        latency_ms = float(parts[6].split("=")[1])
        print(latency_ms)
        print("Ping successful!")
    else:
        print("Ping failed. Please check the target IP address or your network connection.")

    # Record measurement information
    timestamp = datetime.now()
    status = "success" if result.returncode == 0 else "failure"

    # Save the measurement to CSV
    file_exists = os.path.exists("network_latency.csv")

    with open("network_latency.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["latency_ms", "timestamp", "target_ip", "status"])

        writer.writerow([latency_ms, timestamp, target_ip, status])

    # Wait 5 seconds before the next ping
    time.sleep(5)