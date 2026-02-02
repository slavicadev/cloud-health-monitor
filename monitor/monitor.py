import os
import json
import requests
import time
from config import SERVICES

# --- PATH CONFIGURATION ---
# This ensures we find the 'data' folder at the root of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "status_history.json")

def get_status_from_api(service):
    """Fetches status from a specific API and traverses the JSON path."""
    try:
        response = requests.get(service["url"], timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Navigate through the keys defined in config.py
            for key in service["key_path"]:
                data = data[key]
            return data
        return f"Offline (HTTP {response.status_code})"
    except Exception as e:
        return f"Error: {str(e)}"

def load_full_history():
    """Loads the entire history list from the JSON file."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                content = json.load(f)
                return content if isinstance(content, list) else []
        except (json.JSONDecodeError, ValueError):
            return []
    return []

def save_history(new_entry):
    """Appends a new check entry to the historical list and saves it."""
    # 1. Load existing history
    history_list = load_full_history()
    
    # 2. Add timestamp to the new entry
    new_entry['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    
    # 3. Append the new check
    history_list.append(new_entry)
    
    # 4. Keep only the last 100 entries to prevent the file from growing too large
    history_list = history_list[-100:]
    
    # 5. Ensure the data directory exists and save
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(history_list, f, indent=4)

def run_monitor():
    print("🚀 Cloud-Pulse Monitor Engine: ACTIVE")
    print(f"📁 Storing data in: {DATA_FILE}")
    
    while True:
        # Load history to find the 'previous' state for comparison
        history_list = load_full_history()
        last_entry = history_list[-1] if history_list else {}

        current_check = {}
        print(f"\n--- Health Check Started: {time.strftime('%H:%M:%S')} ---")
        
        for service in SERVICES:
            name = service["name"]
            current_status = get_status_from_api(service)
            
            # Compare current status with the very last recorded status
            last_status = last_entry.get(name)

            if last_status and current_status != last_status:
                print(f"🚨 ALERT: {name} changed from '{last_status}' to '{current_status}'")
            else:
                print(f"✅ {name}: {current_status}")
            
            current_check[name] = current_status

        # Save the result of this full sweep
        save_history(current_check)
        
        print(f"Check complete. Next check in 10 minutes...")
        time.sleep(600)

if __name__ == "__main__":
    run_monitor()