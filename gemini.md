# GEMINI.md: Project Context & Operational Guidelines

## 1. Project Overview
**Name:** Air-Quality-Orange-Pi-Automation
**Goal:** Automated air quality monitoring system running on Orange Pi 3 LTS using BME680/BMP680 sensors.
**Core Functionality:**
- Reads sensor data (Temperature, Humidity, Pressure, Gas Resistance).
- Calculates Air Quality Score based on a dynamic baseline.
- Exposes data via a Flask API (`/api/data`).
- Sends data to an n8n webhook for external processing/explanation.
- Serves a Next.js web dashboard via Nginx.

## 2. Architecture & Stack
- **Hardware:** Orange Pi 3 LTS, BME680/BMP680 Sensor (I2C interface).
- **Infrastructure:**
    - **Docker Compose:** Orchestrates services.
    - **Nginx:** Reverse proxy for API and Frontend (Port 80).
    - **Network:** Bridge network (`app-network`).
- **Backend:** 
    - **Language:** Python 3.11.
    - **Framework:** Flask (served by Gunicorn).
    - **Structure:** Modular package (`src/`).
    - **Sensor Logic:** `src/services/sensor.py` (Background thread).
- **Frontend:**
    - **Framework:** Next.js (React).
    - **Serving:** Node.js (Standalone mode).
- **Data Integration:** POSTs JSON data to n8n webhooks.

## 3. Key Files & Components

### Backend (`backend/`)
- **`wsgi.py`**: Entry point for Gunicorn.
- **`src/app.py`**: App factory, thread management (Sensor & N8N).
- **`src/api/routes.py`**: API Endpoints (`/api/data`, `/api/history`, etc.).
- **`src/services/sensor.py`**: `BME680Reader` class, hardware interface.
- **`src/state.py`**: Global state management (`AppState`).
- **`src/core/`**: Configuration (`config.py`) and structured logging (`logger.py`).

### Frontend (`frontend/`)
- **`Dockerfile`**: Multi-stage build for Next.js standalone output.
- **`next.config.ts`**: Configured for `output: 'standalone'`.

### Infrastructure
- **`docker-compose.yml`**: Defines `nginx`, `bmp-sensor`, `frontend`, and `watchtower`.
- **`nginx/nginx.conf`**: Routing rules for `/api` (Backend) and `/` (Frontend).
- **`Makefile`**: Shortcuts for build, deploy, and test commands.

## 4. Development & Operational Workflows

### Running with Docker (Recommended)
1.  **Build & Start:** `make up` (or `docker-compose up -d --build`)
2.  **Logs:** `make logs`
3.  **Stop:** `make down`

### Testing
- **Backend Tests:** `make test` (Runs `pytest` inside the container).
- **API Check:** `curl http://localhost/api/data`

### Configuration (Environment Variables)
Defined in `docker-compose.yml` or `.env`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `READ_INTERVAL` | Seconds between sensor reads | `2.0` |
| `N8N_WEBHOOK_URL` | Webhook URL for n8n | `None` |
| `BLINKA_FORCEBOARD` | Hardware type | `ORANGE_PI_3_LTS` |
| `DEVICE_ID` | Unit Identifier | `hostname` |

## 5. Coding Conventions & Style
- **Python:** PEP 8, Modular structure (`src/`), Typed.
- **Logging:** JSON structured logging (`src.core.logger`).
- **Threading:** Sensor and N8N logic run in daemon threads.
- **State:** Managed via `src.state.AppState` singleton.

## 6. Important Notes for Agent
- **Hardware Simulation:** Sensor code (`src/services/sensor.py`) requires I2C. Mocking is needed for local non-hardware tests.
- **Nginx:** All external access is via Port 80. Do not access port 5000 or 3000 directly in production.
- **Changes:** Always rebuild containers after code changes (`make build` or `make up`).