import requests
import time
import json
import os
from config import SERVICES, DATA_FILE

def load_history():
    """Loads all previous statuses from a JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(history):
    """Saves the updated status dictionary."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(history, f, indent=4)

def get_status_from_api(service):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(service["url"], headers=headers, timeout=10)
        
        # If the URL is wrong (404), this jumps straight to the 'except' block
        response.raise_for_status() 
        
        data = response.json()
        val = data
        
        # Safe traversal logic
        for key in service["key_path"]:
            if isinstance(val, list) and isinstance(key, int):
                val = val[key] if len(val) > key else "No Data"
            elif isinstance(val, dict):
                val = val.get(key, "Unknown")
            else:
                return str(val)
        
        return str(val)

    except requests.exceptions.HTTPError as e:
        return f"Offline (HTTP {e.response.status_code})"
    except Exception as e:
        return f"Error: {str(e)}"
        
        # Specific fix for AWS data structure
        if service["name"] == "AWS" and isinstance(val, list):
            return "Operational" if len(val) == 0 else f"{len(val)} issues"

        return str(val)
    except requests.exceptions.HTTPError as e:
        return f"Provider Error (HTTP {e.response.status_code})"
    except Exception as e:
        return f"Fetch Error: {str(e)}"

def run_monitor():
    while True: # This starts an infinite loop inside the script
        history = load_history()
        new_history = {}

        print(f"\n--- Starting Health Check: {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
        
        for service in SERVICES:
            name = service["name"]
            current_status = get_status_from_api(service)
            last_status = history.get(name)

            if last_status and current_status != last_status:
                print(f"🚨 ALERT: {name} changed from '{last_status}' to '{current_status}'")
                # If you added Slack logic, call it here
            else:
                print(f"✅ {name}: {current_status}")
            
            new_history[name] = current_status

        save_history(new_history)
        
        print("Check complete. Sleeping for 10 minutes...")
        time.sleep(600) # 600 seconds = 10 minutes

if __name__ == "__main__":
    run_monitor()