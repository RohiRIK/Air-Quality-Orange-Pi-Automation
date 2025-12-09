# BME688 Environmental Sensor Project on Orange Pi 3 LTS

## Project Overview
This project demonstrates how to connect a BME688 environmental sensor to an Orange Pi 3 LTS single-board computer. It reads comprehensive environmental data, sends it to an n8n workflow for analysis, and serves the data and analysis through a local web interface. The setup is containerized using Docker for portability and ease of deployment.

## Technology Stack
- **Hardware**:
  - Orange Pi 3 LTS: A compact single-board computer with GPIO pins for sensor integration.
  - BME688 Sensor: A 4-in-1 Bosch sensor module supporting I2C communication for measuring temperature, pressure, humidity, and gas (VOCs).
- **Software**:
  - **Operating System**: Armbian or Ubuntu on the Orange Pi.
  - **Programming Language**: Python 3.
  - **Backend**: Flask for the web server.
  - **Frontend**: HTML, CSS, JavaScript, and Chart.js for visualization.
  - **Automation**: n8n for workflow automation and generating explanations.
  - **Libraries**:
    - `adafruit-circuitpython-bme680`: For interfacing with the BME688 via I2C.
    - `adafruit-blinka`: For hardware API compatibility.
    - `requests`: For making HTTP requests to the n8n webhook.
  - **Containerization**: Docker and Docker Compose.
- **Protocols**:
  - I2C: For sensor communication.
  - HTTP/JSON: For the internal API between the frontend and backend.
  - Webhooks: For sending data to n8n.
- **Tools**:
  - `i2c-tools`: For detecting and verifying I2C devices.
  - SSH: For remote access to the Orange Pi during setup.

## Data Flow
1.  The Python script reads data from the BME688 sensor.
2.  The data is sent to an n8n webhook for processing.
3.  n8n returns an "explanation" of the data.
4.  The Flask backend serves the sensor data and the n8n explanation via a local API.
5.  The HTML/JavaScript frontend displays the data and explanation in real-time.

## Project Structure
The project is organized as follows:

```
/Air-Quality-Orange-Pi-Automation
├── app.py
├── bmp_reader.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── script.js
│   └── style.css
├── docs/
│   ├── 1_OVERVIEW.md
│   ├── ...
└── README.md
```

---

### Understanding the Air Quality (Gas) Sensor

The BME688 sensor provides a powerful air quality feature by detecting Volatile Organic Compounds (VOCs) in the air. These are gases emitted from sources like paints, cleaning supplies, cooking, and even human breath.

**How to Interpret the `gas_ohms` Reading:**

The value you see in the `gas_ohms` field is the electrical resistance of the sensor's gas-sensitive layer. It's important to understand how to interpret this value:

-   The sensor is heated, and when VOCs react with its surface, the resistance **decreases**.
-   Therefore, a **lower `gas_ohms` value generally indicates a higher concentration of VOCs** and potentially lower air quality.
-   A **higher `gas_ohms` value indicates cleaner air**.

**Getting a Meaningful Air Quality Score:**

A single resistance reading is not enough to determine if the air is "good" or "bad". To get a meaningful metric, you need to establish a **baseline**.

1.  **Establish a Baseline:** Run the sensor for a period (e.g., 20-30 minutes) in an environment you consider to have clean, fresh air. The stable `gas_ohms` reading you get during this time is your `baseline_gas_reading`.
2.  **Calculate a Score:** You can then calculate a relative air quality score. A common approach is to express the current air quality as a percentage of the clean air baseline.

The script implements a dynamic baseline logic for more advanced air quality monitoring.