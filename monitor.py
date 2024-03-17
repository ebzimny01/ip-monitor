# Script: monitor.py
# Description: A Python script to monitor the availability of an IP address and send a Slack notification when the status changes
# Notes: The Slack webhook URL and channel must be set in the SLACK_WEBHOOK_URL and SLACK_CHANNEL variables
# Notes: The IP address to monitor must be set in the IP_ADDRESS variable

import subprocess
import time
import datetime
import requests
import json

# Slack webhook URL and channel
SLACK_WEBHOOK_URL = "SLACK_WEBHOOK_URL"
SLACK_CHANNEL = "SLACK_CHANNEL"

# IP address to monitor
IP_ADDRESS = "192.168.1.72"

def ping_host(ip_address):
    command = ["ping", "-c", "1", ip_address]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def send_slack_notification(message, channel=SLACK_CHANNEL, success=True):
    emoji = ":white_check_mark:" if success else ":octagonal_sign:"
    payload = {
        "text": f"{emoji} {message}",
        "channel": channel
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)

def monitor_ip(ip_address):
    first_success = True
    first_failure = True
    first_success_time = None
    last_success_time = None
    first_failure_time = None
    last_failure_time = None
    time_between_failure_and_success = None
    time_between_success_and_failure = None

    while True:
        if ping_host(ip_address):
            if first_success:
                first_success = False
                first_success_time = datetime.datetime.now()
                last_success_time = datetime.datetime.now()
                if last_failure_time:
                    time_between_failure_and_success = last_success_time - first_failure_time
                    send_slack_notification(f"Successfully pinged {ip_address} after {time_between_failure_and_success} of failure", success=True)
                    first_failure = True
                    last_failure_time = None
                else:
                    send_slack_notification(f"Successfully pinged {ip_address} at {last_success_time}", success=True)
            else:
                last_success_time = datetime.datetime.now()
            print(f"Last successful ping time: {last_success_time}")
        else:
            if first_failure:
                first_failure = False
                first_failure_time = datetime.datetime.now()
                last_failure_time = datetime.datetime.now()
                if last_success_time:
                    time_between_success_and_failure = last_failure_time - first_success_time
                    send_slack_notification(f"Failed to ping {ip_address} after {time_between_success_and_failure} of success", success=False)
                    first_success = True
                    last_success_time = None
                else:
                    send_slack_notification(f"Failed to ping {ip_address} at {last_failure_time}", success=False)
            else:
                last_failure_time = datetime.datetime.now()
            print(f"Last failure time: {last_failure_time}")

        time.sleep(30)  # Ping interval (in seconds)

if __name__ == "__main__":
    ip_address = IP_ADDRESS  # Change this to your desired IP address
    monitor_ip(ip_address)
