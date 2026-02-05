from zk import ZK
from datetime import datetime

# List your devices here
devices = [
    {"ip": "192.168.1.10", "port": 4370},
    {"ip": "192.168.1.11", "port": 4370}
]

for device in devices:
    ip = device["ip"]
    port = device["port"]
    print(f"\nTesting device {ip}:{port} ...")
    try:
        zk = ZK(ip, port=port, timeout=5)
        conn = zk.connect()
        logs = conn.get_attendance()
        conn.disconnect()
        
        if logs:
            print(f"SUCCESS: {len(logs)} logs fetched from {ip}")
            for l in logs[:5]:  # Show first 5 logs
                print(f"UserID: {l.user_id}, Time: {l.timestamp}, Status: {l.status}")
        else:
            print(f"No logs found on {ip}")
    except Exception as e:
        print(f"ERROR: Could not connect to {ip}: {e}")
