import machine
import time
import urequests
import ujson
from machine import I2C, Pin
from config import HUB_URL, DEVICE_ID, READ_INTERVAL, API_KEY
import bme680 # Requires bme680.py driver on the device

# ESP32-C3 SuperMini I2C Pins (Default)
# SCL = GPIO 9
# SDA = GPIO 8
i2c = I2C(0, scl=Pin(9), sda=Pin(8))

try:
    sensor = bme680.BME680_I2C(i2c=i2c)
except Exception as e:
    print("Sensor not found:", e)
    sensor = None

def get_reading():
    if not sensor:
        return None
    
    try:
        temp = sensor.temperature
        hum = sensor.humidity
        pres = sensor.pressure
        gas = sensor.gas
        
        return {
            "device_id": DEVICE_ID,
            "temperature_c": round(temp, 2),
            "humidity_rh": round(hum, 2),
            "pressure_hpa": round(pres, 2),
            "gas_ohms": round(gas, 2),
            # Air Quality Score can be calculated here or on the backend.
            # Sending raw values for backend consistency is often better.
            "air_quality_score": 0 # Placeholder, backend calculates or we add logic here
        }
    except Exception as e:
        print("Reading error:", e)
        return None

def send_data(data):
    try:
        print("Sending data:", data)
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY
        }
        response = urequests.post(HUB_URL, data=ujson.dumps(data), headers=headers)
        print("Response:", response.status_code)
        response.close()
    except Exception as e:
        print("Upload error:", e)

def main():
    print(f"Starting Sensor Node: {DEVICE_ID}")
    
    while True:
        data = get_reading()
        if data:
            send_data(data)
        
        time.sleep(READ_INTERVAL)

if __name__ == "__main__":
    main()
