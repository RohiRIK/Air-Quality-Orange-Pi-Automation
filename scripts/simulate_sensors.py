import requests
import time
import random
import json

# Configuration
API_URL = "http://localhost:80/api/ingest"  # Nginx port 80
API_KEY = "dev-secret-key"
# If running locally without Nginx, use http://localhost:5000/api/ingest

# Mock Devices
DEVICES = [
    {"id": "esp32_living_room", "name": "Living Room", "base_temp": 22.0, "base_hum": 45.0},
    {"id": "esp32_bedroom", "name": "Bedroom", "base_temp": 19.5, "base_hum": 50.0},
    {"id": "esp32_kitchen", "name": "Kitchen", "base_temp": 24.0, "base_hum": 60.0},
]

def generate_reading(device):
    """Generate slightly random data around a baseline."""
    temp = round(device["base_temp"] + random.uniform(-0.5, 0.5), 2)
    hum = round(device["base_hum"] + random.uniform(-2, 2), 2)
    pres = round(1013.25 + random.uniform(-5, 5), 2)
    gas = round(random.uniform(10000, 50000), 2)
    
    # Simple Mock Score Calculation (0-100)
    # Higher gas ohms = cleaner air generally (in this library context usually inverted but let's mock 0-100)
    score = round(random.uniform(80, 100), 1) 

    return {
        "device_id": device["id"],
        "temperature_c": temp,
        "humidity_rh": hum,
        "pressure_hpa": pres,
        "gas_ohms": gas,
        "air_quality_score": score
    }

def register_names():
    """Optional: Update friendly names via API to match our mocks."""
    print("Registering friendly names...")
    for device in DEVICES:
        try:
            url = f"http://localhost:80/api/sensors/{device['id']}"
            requests.put(url, json={"name": device["name"]})
        except Exception as e:
            print(f"Failed to register name for {device['id']}: {e}")

def main():
    print(f"Starting Sensor Simulation -> {API_URL}")
    print("Press Ctrl+C to stop.")
    
    # 1. Register Names First
    register_names()

    # 2. Data Loop
    while True:
        for device in DEVICES:
            payload = generate_reading(device)
            try:
                headers = {"X-API-Key": API_KEY}
                response = requests.post(API_URL, json=payload, headers=headers, timeout=2)
                if response.status_code == 201:
                    print(f"Sent [{device['name']}]: Temp={payload['temperature_c']}C Score={payload['air_quality_score']}")
                else:
                    print(f"Error [{device['name']}]: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Connection Error: {e}")
        
        time.sleep(5) # Send data every 5 seconds

if __name__ == "__main__":
    main()
