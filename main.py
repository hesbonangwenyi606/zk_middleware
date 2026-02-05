import time
import json
from zk_device import fetch_logs
from zoho_api import push_log_to_zoho
from logger import log_info

# Load config
with open('config.json') as f:
    config = json.load(f)

def update_last_sync(device_index, timestamp):
    config['devices'][device_index]['last_sync'] = timestamp
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)

def run_middleware():
    poll_interval = config.get("poll_interval_minutes", 5) * 60
    log_info("Middleware started...")
    
    while True:
        for i, device in enumerate(config['devices']):
            logs = fetch_logs(device['ip'], device['last_sync'])
            if logs:
                for log in logs:
                    push_log_to_zoho(log, device['serial'], config)
                # Update last sync to latest timestamp
                last_ts = max(l['timestamp'] for l in logs)
                update_last_sync(i, last_ts)
                log_info(f"Updated last_sync for device {device['ip']} to {last_ts}")
            else:
                log_info(f"No new logs for device {device['ip']}")
        time.sleep(poll_interval)

if __name__ == "__main__":
    run_middleware()
