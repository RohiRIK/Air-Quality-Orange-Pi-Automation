import board
import busio
import adafruit_bme680
import time
import requests
import os
import json
from collections import deque

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor object using the BME680 library
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# You can set the sea level pressure for more accurate altitude readings
# This value can be found from a local weather station.
bme680.sea_level_pressure = 1013.25

# Define the endpoint URL to send data to (replace with your target)
URL = "https://httpbin.org/post"  # Example; change to your server URL

# --- Air Quality Baseline Parameters ---
GAS_READINGS_WINDOW_SIZE = 60 # Number of readings to keep for moving average (e.g., 5 minutes at 5-sec interval)
gas_readings = deque(maxlen=GAS_READINGS_WINDOW_SIZE)
initial_baseline_established = False
BASELINE_WARMUP_PERIOD = 300 # Seconds to wait before establishing initial baseline (e.g., 5 minutes)
start_time = time.monotonic()

def calculate_air_quality_score(current_gas, baseline_gas):
    # A higher gas resistance typically indicates cleaner air
    # A lower gas resistance typically indicates more pollutants
    # We want a score where higher is better air quality.
    # This is a simplified inverse relationship.
    # You might need to fine-tune this based on actual sensor behavior and environment.

    if baseline_gas == 0: # Avoid division by zero
        return 0.0

    # The ratio will be > 1 for better than baseline, < 1 for worse.
    # We can scale this to a 0-100 score, where 50 is baseline.
    ratio = current_gas / baseline_gas
    score = 50 + (ratio - 1) * 50 # Adjust sensitivity as needed

    return round(max(0, min(100, score)), 2) # Clamp between 0 and 100

while True:
    # Read sensor data
    temperature = bme680.temperature
    gas = bme680.gas
    humidity = bme680.humidity
    pressure = bme680.pressure
    altitude = bme680.altitude

    # Update gas readings for dynamic baseline
    gas_readings.append(gas)

    current_air_quality_score = None
    baseline_gas_resistance = None

    # Establish initial baseline after a warmup period
    if not initial_baseline_established:
        if time.monotonic() - start_time > BASELINE_WARMUP_PERIOD and len(gas_readings) == GAS_READINGS_WINDOW_SIZE:
            baseline_gas_resistance = sum(gas_readings) / len(gas_readings)
            initial_baseline_established = True
            print(f"Initial gas resistance baseline established: {baseline_gas_resistance:.2f} Ohms")
        else:
            print(f"Warming up sensor and collecting initial gas readings... ({len(gas_readings)}/{GAS_READINGS_WINDOW_SIZE})")
    
    if initial_baseline_established:
        baseline_gas_resistance = sum(gas_readings) / len(gas_readings)
        current_air_quality_score = calculate_air_quality_score(gas, baseline_gas_resistance)


    # Create JSON data payload
    sensor_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        "temperature_c": round(temperature, 2),
        "pressure_hpa": round(pressure, 2),
        "humidity_rh": round(humidity, 2),
        "gas_ohms": round(gas, 2),
        "altitude_m": round(altitude, 2)
    }

    if baseline_gas_resistance is not None:
        sensor_data["gas_baseline_ohms"] = round(baseline_gas_resistance, 2)
    if current_air_quality_score is not None:
        sensor_data["air_quality_score"] = current_air_quality_score

    # Convert to JSON string
    json_data = json.dumps(sensor_data)

    try:
        # Send JSON data to the endpoint
        response = requests.post(URL, data=json_data, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            print("Data sent successfully:", sensor_data)
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data: {e}")

    # Wait before the next reading
    time.sleep(5) # Increased sleep time as gas sensor readings can take longer
