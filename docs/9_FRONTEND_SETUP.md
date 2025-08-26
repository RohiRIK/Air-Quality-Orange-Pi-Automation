# 9. Frontend Setup and Usage

This document explains the structure and usage of the Flask-based web frontend for monitoring sensor data in real-time.

## Overview

The project includes a simple web interface to visualize the data from the BME688 sensor. This frontend is served by a Flask application (`app.py`) and uses JavaScript to fetch and display data from a local API endpoint.

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS, JavaScript
- **Charting**: Chart.js for dynamic data visualization

## File Structure

The frontend components are organized into `templates` and `static` directories:

```
/Air-Quality-Orange-Pi-Automation
├── app.py                  # Main Flask application
├── bmp_reader.py           # Sensor reading logic (as a class)
├── templates/
│   └── index.html          # The main HTML page for the frontend
├── static/
│   ├── style.css           # CSS for styling the frontend
│   └── script.js           # JavaScript for fetching data and updating the UI
├── Dockerfile
├── docker-compose.yml
└── ...
```

## How it Works

1.  **Backend (`app.py`)**:
    -   Initializes the BME688 sensor in a background thread to read data continuously.
    -   If an `N8N_WEBHOOK_URL` is provided, it sends the sensor data to this webhook.
    -   It receives a JSON response from n8n containing an "explanation".
    -   Starts a Flask web server.
    -   Provides two main routes:
        -   `/`: Serves the `index.html` page.
        -   `/api/data`: Returns the latest sensor reading and the n8n explanation as a JSON object.

2.  **Frontend (`index.html` and `script.js`)**:
    -   The `index.html` file provides the structure for the dashboard, including placeholders for data values, a canvas for the chart, and a section for the n8n explanation.
    -   The `script.js` file runs in the browser and periodically (every 2 seconds) sends a request to the `/api/data` endpoint.
    -   When new data is received, the script updates the values on the page (temperature, humidity, etc.), adds the new data points to the real-time chart, and displays the explanation from n8n.

## Accessing the Frontend

1.  **Run the Application**: Start the application using Docker Compose:
    ```sh
    sudo docker-compose up
    ```

2.  **Open in Browser**: Open a web browser and navigate to the IP address of your Orange Pi, followed by port `5000`.
    ```
    http://<your-orange-pi-ip>:5000
    ```
    For example: `http://192.168.1.100:5000`

You should see the dashboard with real-time data from your sensor.
