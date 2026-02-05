import requests
import json
from logger import log_info, log_error

def push_log_to_zoho(log, device_lookup_id, config):
    url = f"https://creator.zoho.com/api/v2/{config['zoho']['owner_name']}/{config['zoho']['app_name']}/form/Raw_Attendance_Logs/record"
    headers = {"Authorization": f"Zoho-oauthtoken {config['zoho']['api_token']}"}
    payload = {
        "data": {
            "ZKTeco_User_ID": log["user_id"],
            "Timestamp": log["timestamp"],
            "Event_Type": log["event"],
            "Device_ID": device_lookup_id,
            "Raw_JSON": json.dumps(log)
        }
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 201:
            log_info(f"Pushed log {log['user_id']} at {log['timestamp']} successfully")
        else:
            log_error(f"Failed to push log {log['user_id']}: {response.text}")
        return response.status_code, response.text
    except Exception as e:
        log_error(f"Exception while pushing log {log['user_id']}: {e}")
        return None, str(e)
