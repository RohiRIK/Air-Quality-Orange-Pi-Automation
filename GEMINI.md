# GEMINI.md

## Project Overview

This project is a full-stack air quality monitoring system designed to run on an Orange Pi 3 LTS. It uses a BME680/BMP680 sensor to collect data on temperature, humidity, pressure, and air quality. The system is containerized using Docker and consists of a Python backend, a Next.js frontend, and an n8n workflow for data analysis.

### Key Technologies

*   **Backend:** Python, Flask
*   **Frontend:** Next.js, React, TypeScript
*   **Containerization:** Docker, Docker Compose
*   **Data Analysis:** n8n (optional)
*   **Hardware:** Orange Pi 3 LTS, BME680/BMP680 sensor

### Architecture

The system is composed of three main services defined in the `docker-compose.yml` file:

1.  **`bmp-sensor` (Backend):** A Python Flask application that reads data from the BME680 sensor connected to the Orange Pi's I2C pins. It provides a REST API to expose the sensor data.
2.  **`frontend` (Frontend):** A Next.js application that provides a real-time dashboard to visualize the sensor data. It fetches data from the backend's API.
3.  **`watchtower`:** A service that automatically updates the running Docker containers when new images are available.

## Building and Running

### Prerequisites

*   Docker and Docker Compose installed on the host machine.
*   An Orange Pi 3 LTS with a BME680/BMP680 sensor connected to the I2C pins.

### Build the containers

```bash
sudo docker-compose build
```

### Run the application

```bash
sudo docker-compose up -d
```

The frontend will be available at `http://<your-orange-pi-ip>:3000`.

### View logs

```bash
# View backend logs
sudo docker logs -f bmp-sensor-container

# View frontend logs
sudo docker logs -f frontend-container
```

## Development Conventions

### Backend

*   The main application logic is in `backend/app.py`.
*   The sensor reading logic is in `backend/bmp_reader.py`.
*   Python dependencies are managed with `pip` and are listed in `backend/requirements.txt`.
*   The backend provides the following API endpoints:
    *   `/api/data`: Returns the latest sensor data.
    *   `/api/history`: Returns a buffer of historical sensor readings.
    *   `/api/calendar`: Fetches calendar events from Google Calendar.

### Frontend

*   The frontend is a Next.js application.
*   The main page is `frontend/app/page.tsx`, which renders the `Dashboard` component.
*   The `Dashboard` component (`frontend/components/Dashboard.tsx`) is the main UI component, and it fetches data from the backend using `useSWR`.
*   Components are located in `frontend/components`.
*   Types are defined in `frontend/types`.
*   API interaction logic is in `frontend/lib/api.ts`.
*   The frontend uses a theme context (`frontend/lib/ThemeContext.tsx`) for styling.
