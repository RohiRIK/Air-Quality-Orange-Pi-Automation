# GEMINI.md: Project Context & Operational Guidelines

## 1. Project Overview
**Name:** Air-Quality-Orange-Pi-Automation
**Goal:** Automated air quality monitoring system running on Orange Pi 3 LTS using BME680/BMP680 sensors.
**Core Functionality:**
- Reads sensor data (Temperature, Humidity, Pressure, Gas Resistance).
- Calculates Air Quality Score based on a dynamic baseline.
- Exposes data via a Flask API (`/api/data`).
- Sends data to an n8n webhook for external processing/explanation.
- Serves a simple web dashboard.

## 2. Architecture & Stack
- **Hardware:** Orange Pi 3 LTS, BME680/BMP680 Sensor (I2C interface).
- **Backend:** Python (Flask).
- **Sensor Logic:** `adafruit-circuitpython-bme680` library running in a background thread (`bmp_reader.py`).
- **Data Integration:** POSTs JSON data to n8n webhooks; receives "explanation" string in response.
- **Frontend:**
    - **Current:** Flask templates (`templates/index.html`) + Static assets (`static/`).
    - **Potential/Legacy:** `frontend/` directory (Next.js traces), but currently `app.py` serves the Flask templates.
- **Deployment:** Docker & Docker Compose.

## 3. Key Files & Components

### `app.py` (Main Entry Point)
- **Role:** Flask web server & Orchestrator.
- **Key Features:**
    - Starts `BME680Reader` in a background thread.
    - Runs a loop (`sensor_and_n8n_thread`) that sends data to n8n and updates the global `explanation` variable.
    - Routes:
        - `/`: Serves the dashboard.
        - `/api/data`: Returns current sensor readings + n8n explanation as JSON.
- **Configuration:** Uses `N8N_WEBHOOK_URL_TEST` or `N8N_WEBHOOK_URL_PROD`.

### `bmp_reader.py` (Sensor Logic)
- **Role:** Hardware interface and data processing.
- **Key Class:** `BME680Reader`.
- **Logic:**
    - Maintains a rolling buffer (`deque`) of gas resistance readings.
    - Establishes a baseline after a warmup period (default 120s).
    - Calculates "Air Quality Score" (0-100) based on deviation from baseline.
    - Handles I2C communication via `busio` and `board`.

### Infrastructure
- **`Dockerfile`**: Python environment setup.
- **`docker-compose.yml`**: Service definition, hardware device mapping (`/dev/i2c-0`), and environment variable injection.

## 4. Development & Operational Workflows

### Running Locally (Without Docker)
*Requires hardware access (I2C)*
1.  **Install Deps:** `pip install -r requirements.txt`
2.  **Env Setup:**
    ```bash
    export BLINKA_FORCEBOARD=ORANGE_PI_3_LTS
    export READ_INTERVAL=2.0
    export N8N_WEBHOOK_URL_TEST="your_url_here"
    ```
3.  **Run:** `python app.py`

### Running with Docker
1.  **Build:** `docker-compose build`
2.  **Run:** `docker-compose up -d`
3.  **Logs:** `docker logs -f bmp-sensor-container`

### Testing/Verification
- **API Check:** `curl http://localhost:5000/api/data`
- **I2C Check:** `sudo i2cdetect -y 0` (on host)

## 5. Configuration (Environment Variables)

| Variable | Description | Default |
| :--- | :--- | :--- |
| `READ_INTERVAL` | Seconds between sensor reads | `2.0` |
| `N8N_WEBHOOK_URL_TEST` | Webhook URL for n8n (Test) | `None` |
| `N8N_WEBHOOK_URL_PROD` | Webhook URL for n8n (Prod) | `None` |
| `BLINKA_FORCEBOARD` | Forces hardware type for libraries | `ORANGE_PI_3_LTS` |
| `DEVICE_ID` | Identifier for the unit | `hostname` |

## 6. Coding Conventions & Style
- **Python:** Standard PEP 8.
- **Logging:** JSON structured logging (implemented in `bmp_reader.py`) for machine readability.
- **Threading:** Sensor logic runs in a daemon thread to prevent blocking the Flask main loop. Ensure thread safety when accessing shared data (`reader.latest_data`).
- **Error Handling:** Graceful degradation. If n8n fails, the app continues to serve sensor data with an error message in the 'explanation' field.

## 7. Important Notes for Agent
- **Hardware Simulation:** You cannot run the actual sensor code (`bmp_reader.py`) successfully in this environment because the I2C hardware is missing. Changes to logic should be verified by analysis or by asking the user to test.
- **Frontend Source:** If asked to modify the UI, edit `templates/index.html` and `static/`, *not* the `frontend/` folder unless explicitly instructed to switch to Next.js.
