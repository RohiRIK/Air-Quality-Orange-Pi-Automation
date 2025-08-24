# Software Installation and Usage

---

## Local Setup (Without Docker)

**Install dependencies:**
```sh
sudo apt update
sudo apt install python3-pip i2c-tools
pip3 install adafruit-circuitpython-bme680 requests
```

**Enable I2C:**
- Edit `/boot/armbianEnv.txt` to add `overlays=i2c0` and reboot.

**Run the script:**
```sh
python3 bmp_reader.py
```

---

## Docker Compose Setup

**1. Install Docker and Docker Compose:**
Follow the official Docker documentation to install Docker Engine and the Docker Compose plugin for your system. A typical command for Debian-based systems like Armbian is:
```sh
# Install Docker
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
sudo apt install docker-compose-v2
```

**2. Build and Run the Application:**
Navigate to the project's root directory (where `docker-compose.yml` is located) and run:
```sh
docker-compose up --build -d
```
- `--build`: This flag tells Docker Compose to build the `bmp-sensor` image before starting the services.
- `-d`: This runs the containers in detached mode (in the background).

**3. Automatic Updates with Watchtower:**
The `docker-compose.yml` file includes the Watchtower service. It will automatically check for updates to the `rohirikman/air-quality-sensor` image every day at 4 AM (as per the schedule `"0 0 4 * * *"`). If it finds a new version, it will gracefully restart the `bmp-sensor` container with the updated image. No manual intervention is needed.

**4. Viewing Logs:**
To view the logs from the running sensor container, use:
```sh
docker-compose logs -f bmp-sensor
```

**5. Stopping the Application:**
To stop the services, run:
```sh
docker-compose down
```

---

### Development and Update Workflow

The primary advantage of this setup is that you can update the code running on your Orange Pi from anywhere, without needing to access the device directly. The process relies on Docker Hub (or another container registry) as the bridge.

The end-to-end workflow is as follows:

**1. Prerequisites:**
   - Create a free account on [Docker Hub](https://hub.docker.com/).
   - On Docker Hub, create a public repository named `air-quality-sensor` (or a name of your choice, but be sure to update the `image` name in `docker-compose.yml` to match).

**2. Make Code Changes:**
   - Modify the `bmp_reader.py` script or any other project file on your local development machine.

**3. Build, Push, and Deploy:**
   - Open a terminal in the project root directory.
   - **Log in to Docker Hub:**
     ```sh
     docker login
     ```
     (Enter your Docker Hub username and password when prompted).
   - **Build the new image:** This command reads the `image` tag from your `docker-compose.yml` file.
     ```sh
     docker-compose build
     ```
   - **Push the new image to Docker Hub:**
     ```sh
     docker-compose push
     ```

**4. Automatic Update on Orange Pi:**
   - That's it! You are done.
   - The Watchtower container running on your Orange Pi will detect that a new version of the `rohirikman/air-quality-sensor` image has been pushed to Docker Hub during its next scheduled check.
   - It will automatically pull the new image and restart the `bmp-sensor` service with your updated code.

---

## Data Flow

- The sensor reads data every 5 seconds.
- Data is formatted as JSON. In addition to environmental parameters, it now includes a dynamic air quality baseline and a calculated air quality score.
- For a detailed explanation of the air quality baseline and sensor calibration, refer to [docs/7_CALIBRATION_AND_AIR_QUALITY.md](docs/7_CALIBRATION_AND_AIR_QUALITY.md).

  ```json
  {
    "timestamp": "YYYY-MM-DD HH:MM:SS",
    "temperature_c": 25.5,
    "pressure_hpa": 1013.2,
    "humidity_rh": 45.5,
    "gas_ohms": 50000,
    "altitude_m": 10.25,
    "gas_baseline_ohms": 48000,   // Dynamic baseline for gas resistance
    "air_quality_score": 65.23    // Score from 0-100, where 50 is baseline
  }
  ```
- Sent via HTTP POST to the configured URL in `bmp_reader.py`.

---

## Sample `bmp_reader.py` Script

```python
import board
import busio
import adafruit_bme680
import time
import requests
import os
import json

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor object using the BME680 library
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# Set sea level pressure for more accurate altitude readings
bme680.sea_level_pressure = 1013.25

# Define the endpoint URL to send data to
URL = "https://httpbin.org/post"  # Example; change to your server URL

while True:
    # Read sensor data
    temperature = bme680.temperature
    gas = bme680.gas
    humidity = bme680.humidity
    pressure = bme680.pressure
    altitude = bme680.altitude

    # Create JSON data payload
    sensor_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        "temperature_c": round(temperature, 2),
        "pressure_hpa": round(pressure, 2),
        "humidity_rh": round(humidity, 2),
        "gas_ohms": round(gas, 2),
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

    # Wait 5 seconds before the next reading
    time.sleep(5)
```