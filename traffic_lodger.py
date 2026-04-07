import requests
import csv
import time
from datetime import datetime
import os

API_KEY = "TcWjxW2MOtYyeE7J7h48ha9AyUzbiW1L"  
CSV_FILE = "data/traffic_history.csv"


LOCATIONS = {
    "Clock_Tower": (30.3242, 78.0401),
    "ISBT_Dehradun": (30.2845, 78.0000),
    "Rajpur_Road": (30.3395, 78.0587),
    "Balliwala_Chowk": (30.3215, 77.9995),
    "Sahastradhara_Road": (30.3420, 78.0750),
    "Dilaram_Chowk": (30.3340, 78.0530),     
  "Prince_Chowk": (30.3160, 78.0375),      
  "Survey_Chowk": (30.3275, 78.0515),      
  "Kanwali_Road_Jn": (30.3200, 78.0250)    
}

if not os.path.exists('data'):
    os.makedirs('data')

def fetch_traffic_data(name, lat, lon):
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={API_KEY}&point={lat},{lon}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()['flowSegmentData']
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "location": name,
                "current_speed": data['currentSpeed'],
                "free_flow_speed": data['freeFlowSpeed'],
                "congestion_level": round(1 - (data['currentSpeed'] / data['freeFlowSpeed']), 3)
            }
    except Exception as e:
        print(f"Error fetching {name}: {e}")
    return None

def log_data():
    file_exists = os.path.isfile(CSV_FILE)
    
    with open(CSV_FILE, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "location", "current_speed", "free_flow_speed", "congestion_level"])
        
        if not file_exists or os.stat(CSV_FILE).st_size == 0:
            writer.writeheader()
            
        print(f"--- Logging Traffic at {datetime.now().strftime('%H:%M:%S')} ---")
        for name, coords in LOCATIONS.items():
            result = fetch_traffic_data(name, coords[0], coords[1])
            if result:
                writer.writerow(result)
                print(f"Logged: {name} | Speed: {result['current_speed']} km/h")
        
        f.flush()  

if __name__ == "__main__":
    while True:
        log_data()
        print("Sleeping for 15 minutes...")
        time.sleep(900) 