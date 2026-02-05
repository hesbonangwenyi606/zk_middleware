from zk import ZK
from logger import log_error

def fetch_logs(device_ip, last_sync=None):
    zk = ZK(device_ip, port=4370)
    try:
        conn = zk.connect()
        logs = conn.get_attendance()
        conn.disconnect()
        
        filtered_logs = []
        for l in logs:
            ts = l.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            if last_sync is None or ts > last_sync:
                filtered_logs.append({
                    "user_id": l.user_id,
                    "timestamp": ts,
                    "event": l.status,
                    "device_serial": device_ip
                })
        return filtered_logs
    except Exception as e:
        log_error(f"Failed to fetch logs from {device_ip}: {e}")
        return []
