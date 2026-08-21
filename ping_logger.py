# Day-1/2: Network Latency Logger

import subprocess
import csv
import os
from datetime import datetime
import time

target_ip = "1.1.1.1"

while True:
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

    # Wait 10 seconds before the next ping
    time.sleep(10)