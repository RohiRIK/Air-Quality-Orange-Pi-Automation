# Software Installation and Usage

---

## Local Setup (Without Docker)

**Install dependencies:**
```sh
sudo apt update
sudo apt install python3-pip i2c-tools
pip3 install adafruit-circuitpython-bmp3xx requests
```

**Enable I2C:**
- Edit `/boot/armbianEnv.txt` to add `overlays=i2c0` and reboot.

**Run the script:**
```sh
python3 bmp_reader.py
```

---

## Docker Setup

**Install Docker:**
```sh
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

**Build and run:**
```sh
docker build -t bmp-sensor .
docker run --rm -it --privileged --device /dev/i2c-0:/dev/i2c-0 --network host bmp-sensor
```

> **Note:** The `--privileged` flag and `--device /dev/i2c-0:/dev/i2c-0` are required for I2C access. The `--network host` ensures network connectivity.

---

## Data Flow

- The sensor reads data every 2 seconds.
- Data is formatted as JSON:
  ```json
  {
    "timestamp": "YYYY-MM-DD HH:MM:SS",
    "temperature_c": 25.5,
    "pressure_hpa": 1013.2,
    "altitude_m": 10.25
  }
  ```
- Sent via HTTP POST to the configured URL in `bmp_reader.py`.

---

## Sample `bmp_reader.py` Script

```python
import board
import busio
import adafruit_bmp3xx
import time
import requests
import os
import json

# Initialize I2C bus (adjust I2C device path if needed)
i2c_dev = os.getenv("I2C_DEVICE", "/dev/i2c-0")
i2c = busio.I2C(board.SCL, board.SDA, i2c_device=i2c_dev)

# Create sensor object
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.sea_level_pressure = 1013.25

# Define the endpoint URL to send data to (replace with your target)
URL = "https://httpbin.org/post"  # Example; change to your server URL

while True:
    # Read sensor data
    temperature = bmp.temperature
    pressure = bmp.pressure
    altitude = bmp.altitude

    # Create JSON data
    sensor_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        "temperature_c": round(temperature, 2),
        "pressure_hpa": round(pressure, 2),
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

    # Wait 2 seconds before the next reading
    time.sleep(2)
```
