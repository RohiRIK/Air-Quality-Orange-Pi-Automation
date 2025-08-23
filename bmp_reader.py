import board
import busio
import adafruit_bme680 # Changed import
import time
import requests
import os
import json

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor object using the BME680 library
# The BME688 is compatible with this library
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# You can set the sea level pressure for more accurate altitude readings
# This value can be found from a local weather station.
bme680.sea_level_pressure = 1013.25

# Define the endpoint URL to send data to (replace with your target)
URL = "https://httpbin.org/post"  # Example; change to your server URL

while True:
    # Read sensor data
    temperature = bme680.temperature
    gas = bme680.gas # New reading
    humidity = bme680.humidity # New reading
    pressure = bme680.pressure
    altitude = bme680.altitude

    # Create JSON data payload
    sensor_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        "temperature_c": round(temperature, 2),
        "pressure_hpa": round(pressure, 2),
        "humidity_rh": round(humidity, 2), # New data point
        "gas_ohms": round(gas, 2), # New data point
        "altitude_m": round(altitude, 2)
    }

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