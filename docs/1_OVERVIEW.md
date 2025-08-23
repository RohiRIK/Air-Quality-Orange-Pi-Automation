# BME688 Environmental Sensor Project on Orange Pi 3 LTS

## Project Overview
This project demonstrates how to connect a BME688 environmental sensor to an Orange Pi 3 LTS single-board computer. It reads comprehensive environmental data (temperature, pressure, humidity, and gas resistance for air quality), formats it as JSON, and sends it to a remote endpoint. The setup is containerized using Docker for portability and ease of deployment, and includes an automated update workflow using Watchtower.

## Technology Stack
- **Hardware**:
  - Orange Pi 3 LTS: A compact single-board computer with GPIO pins for sensor integration.
  - BME688 Sensor: A 4-in-1 Bosch sensor module supporting I2C communication for measuring temperature, pressure, humidity, and gas (VOCs).
  - Ribbon Cable or Jumper Wires: For connecting the sensor to the Orange Pi's GPIO pins.
- **Software**:
  - **Operating System**: Armbian or Ubuntu on the Orange Pi.
  - **Programming Language**: Python 3 for the sensor reading script.
  - **Libraries**:
    - `adafruit-circuitpython-bme680`: For interfacing with the BME688 via I2C.
    - `requests`: For sending JSON data over HTTP.
  - **Containerization**: Docker and Docker Compose.
  - **Automation**: Watchtower for automatic container updates, and a shell script for OS updates.
- **Protocols**:
  - I2C: For sensor communication.
  - HTTP/JSON: For data transmission to external endpoints.
- **Tools**:
  - `i2c-tools`: For detecting and verifying I2C devices.
  - SSH: For remote access to the Orange Pi during setup.

## Project Structure
The project is organized as follows:

```
/Air-Quality-Orange-Pi-Automation
├── Dockerfile
├── docker-compose.yml
├── bmp_reader.py
├── requirements.txt
├── scripts/
│   └── update_os.sh
├── docs/
│   ├── 1_OVERVIEW.md
│   ├── 2_GOALS.md
│   ├── ...
├── README.md
└── TODO.md
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
2.  **Calculate a Score:** You can then calculate a relative air quality score. A common approach is to express the current air quality as a percentage of the clean air baseline. For example:
    ```
    # Note: This is a conceptual formula, not actual code in the script yet.
    gas_baseline = 50000 # Example baseline resistance in Ohms
    current_gas = 25000 # Example current reading

    # Or, a simple air quality score where 100 is clean
    air_quality_score = (current_gas / gas_baseline) * 100
    ```

For now, the script reports the raw `gas_ohms` value. A future enhancement could be to implement this baseline logic directly into the script for more advanced air quality monitoring.