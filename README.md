# ip-monitor
Simple python script that can be run as a systemd service to monitor an ip address and send notification of changes in state to a Slack channel via webhook

## Change Variables used for Slack Webhook
You need to replace the values of 2 variables with your own unique values: `SLACK_WEBHOOK_URL` and `SLACK_CHANNEL`. More details about how to create and use Slack Webhooks can be found [here](https://api.slack.com/messaging/webhooks). Example variables:
```
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
SLACK_CHANNEL = "#genmon"
```

## Run Script from Linux console
python3 monitor.py

## Run as a systemd service on Linux
1. Create a new service file by running:
   ```
   sudo nano /etc/systemd/system/monitor_ip.service
   ```

3. Add the following content to the file:
```
[Unit]
Description=Monitor IP service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/monitor.py
Restart=always

[Install]
WantedBy=multi-user.target
```
3. Replace `/usr/bin/python3` with the path to your Python interpreter if it's located elsewhere, and replace `/path/to/monitor.py` with the full path to your Python script.
4. Save and exit the editor.
5. Enable the service to run at boot time by running:
   ```
   sudo systemctl enable monitor_ip.service
   ```
6. Start the service:
   ```
   sudo systemctl start monitor_ip.service
   ```
### Other commands

To stop the service:
   ```
   sudo systemctl stop monitor_ip.service
   ```
To disable the service from running at boot time:
   ```
   sudo systemctl disable monitor_ip.service
   ```
To check the status of the service:
```
systemctl status monitor_ip.service
```
To restart the service:
```
systemctl restart monitor_ip.service
```
To view the service logs:
```
journalctl -u monitor_ip.service
```
To follow the service logs in realtime:
```
journalctl -u monitor_ip.service -f
```
