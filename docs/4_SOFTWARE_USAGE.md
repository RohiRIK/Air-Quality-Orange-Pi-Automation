# Software Installation and Usage

---

## Local Setup (Without Docker)

**1. Install dependencies:**
```sh
sudo apt update
sudo apt install python3-pip i2c-tools
pip3 install -r requirements.txt
```
*Note: `requirements.txt` includes `adafruit-circuitpython-bme680`, `adafruit-blinka`, `Flask`, and `requests`.*

**2. Enable I2C:**
- Edit `/boot/armbianEnv.txt` to add `overlays=i2c0` and reboot.

**3. Configure n8n Webhook (Optional):**
Set the environment variable for your n8n webhook URL. The script prioritizes the `_TEST` variable.
```sh
# For testing
export N8N_WEBHOOK_URL_TEST="<your-n8n-test-webhook-url>"

# For production
export N8N_WEBHOOK_URL_PROD="<your-n8n-prod-webhook-url>"
```

**4. Run the application:**
```sh
python3 app.py
```
Then, open your browser and go to `http://<your-orange-pi-ip>:5000`.

---

## Docker Compose Setup

**1. Install Docker and Docker Compose:**
Follow the official Docker documentation to install Docker Engine and the Docker Compose plugin for your system.

**2. Configure Environment Variables:**
Create a `.env` file in the project root directory. Add your n8n webhook URL(s). The application will use the `_TEST` URL if it is defined, otherwise it will use the `_PROD` URL.

**Example for testing:**
```
N8N_WEBHOOK_URL_TEST=<your-n8n-test-webhook-url>
```

**Example for production:**
```
N8N_WEBHOOK_URL_PROD=<your-n8n-prod-webhook-url>
```
This step is optional. If you don't provide any URL, the application will run without sending data to n8n.

**3. Build and Run the Application:**
Navigate to the project's root directory (where `docker-compose.yml` is located) and run:
```sh
sudo docker-compose up --build -d
```
- `--build`: This flag tells Docker Compose to build the image before starting the service.
- `-d`: This runs the container in detached mode.

**4. Accessing the Frontend:**
Open a web browser and navigate to the IP address of your Orange Pi, followed by port `5000`.
```
http://<your-orange-pi-ip>:5000
```
For example: `http://192.168.1.100:5000`

**5. Viewing Logs:**
To view the logs from the running container (which now come from the Flask application), use:
```sh
sudo docker-compose logs -f
```

**6. Stopping the Application:**
To stop the service, run:
```sh
sudo docker-compose down
```

---

### Development and Update Workflow

You can update the code running on your Orange Pi from anywhere by pushing a new Docker image.

**1. Prerequisites:**
   - A [Docker Hub](https://hub.docker.com/) account and a public repository.

**2. Make Code Changes:**
   - Modify `app.py`, `bmp_reader.py`, or files in the `templates` or `static` directories.

**3. Build and Push the new image:**
   ```sh
   docker login
   sudo docker-compose build
   sudo docker-compose push
   ```

**4. Automatic Update on Orange Pi:**
   - The Watchtower service (if enabled in `docker-compose.yml`) will automatically pull the new image and restart the service.

---

## Data Flow

- The `bmp_reader.py` script, now structured as a class, runs in a background thread of the `app.py` Flask application.
- It reads sensor data every 2 seconds.
- **(Optional) n8n Integration**: If an `N8N_WEBHOOK_URL_TEST` or `N8N_WEBHOOK_URL_PROD` is configured, the application sends the sensor data to the appropriate URL.
- n8n processes the data and returns a JSON response containing an "explanation".
- The `app.py` application serves the frontend at the root URL (`/`) and provides the latest sensor data and the n8n explanation at the `/api/data` endpoint.
- The frontend (`index.html` and `script.js`) fetches data from `/api/data` and updates the display and chart in real-time.
- For a detailed explanation of the air quality baseline and sensor calibration, refer to [docs/7_CALIBRATION_AND_AIR_QUALITY.md](docs/7_CALIBRATION_AND_AIR_QUALITY.md).

  **Sample API Response from `/api/data`:**
  ```json
  {
    "timestamp": "2025-08-26T10:20:30.123456+00:00",
    "temperature_c": 25.5,
    "pressure_hpa": 1013.2,
    "humidity_rh": 45.5,
    "gas_ohms": 50000,
    "altitude_m": 10.25,
    "gas_baseline_ohms": 48000,
    "air_quality_score": 65.23,
    "explanation": "Air quality is good. No action needed."
  }
  ```

---

## Application Structure Overview

The application is now composed of a backend and a frontend:

- **`app.py` (Backend)**: The main entry point. It starts the sensor reading thread and runs the Flask web server to handle HTTP requests and the n8n integration.
- **`bmp_reader.py` (Sensor Logic)**: A class that encapsulates all the logic for interacting with the BME688 sensor.
- **`templates/index.html` (Frontend)**: The HTML structure of the web dashboard.
- **`static/script.js` and `static/style.css` (Frontend)**: The JavaScript and CSS for the web dashboard.

For more details on the frontend, see [docs/9_FRONTEND_SETUP.md](docs/9_FRONTEND_SETUP.md).
