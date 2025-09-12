# Backend Service

This service provides the API for the Air Quality Monitor application. It fetches sensor data from the `bmp-sensor` container and generates AI-powered recommendations.

## How to Run (Docker)

This service is part of the `docker-compose` setup. To run it, navigate to the project root and execute:

```bash
docker-compose up --build backend
```

## API Endpoints

*   `GET /`: Returns a welcome message.
*   `GET /api/data`: Fetches and returns sensor data from the `bmp-sensor` container.
*   `POST /recommendation`: Generates and returns an AI-powered recommendation based on provided sensor data.
