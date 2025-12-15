import board
import busio
import adafruit_bme680
import time
import os

def test_sensor():
    print(f"Testing Sensor on Board: {os.environ.get('BLINKA_FORCEBOARD', 'Unknown')}")
    
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        print("I2C Bus Initialized")
        
        # Scan for devices
        while not i2c.try_lock():
            pass
        
        devices = i2c.scan()
        i2c.unlock()
        
        print("I2C Devices found:", [hex(d) for d in devices])
        
        if not devices:
            print("ERROR: No I2C devices found. Check wiring!")
            return

        sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
        print("Sensor Initialized!")
        
        print(f"Temperature: {sensor.temperature} C")
        print(f"Gas: {sensor.gas} ohms")
        print(f"Humidity: {sensor.humidity} %")
        print(f"Pressure: {sensor.pressure} hPa")
        
    except Exception as e:
        print(f"CRITICAL FAILURE: {e}")

if __name__ == "__main__":
    test_sensor()
