# Air Quality Monitoring with Next.js and AI

This project aims to create a web-based air quality monitoring dashboard with AI-powered recommendations.

## Project Goals

- **Primary:** Create a web-based air quality monitoring dashboard with AI-powered recommendations.
- **Key Objectives:**
    - Display relevant air quality data in a user-friendly web interface.
    - Provide a single, actionable recommendation based on AI analysis of the sensor data.
    - Automatically refresh the data and recommendation every 10 minutes.
    - The web application should be built with Next.js.
    - The entire application should be containerized and installable with a single command.

## Tech Stack

- **Hardware:**
    - **Primary:** Orange Pi 3 LTS
    - **Sensor:** BMP688
- **Software:**
    - **Frontend:** Next.js web application
    - **Backend:** Next.js API routes
    - **AI:** LangChain with Gemini API
    - **Containerization:** Docker
    - **Dependencies:** `package.json` (Next.js, React, LangChain, etc.)

## Data Flow

1. Data is read from the BMP688 sensor connected to the Orange Pi.
2. The data is sent to the Next.js backend.
3. The Next.js backend sends the data to the frontend for display.
4. The backend also sends the data to the Gemini API via LangChain for analysis.
5. The Gemini API returns a recommendation, which is then displayed on the frontend.
6. The data and recommendation are refreshed every 10 minutes.

## Development

- **Development Server:** `npm run dev`
- **Production Build:** `npm run build`
- **Production Start:** `npm run start`

## Deployment

The application is designed to be deployed in a Docker container. A one-line installation script will be provided for easy setup.

**Installation:**
```bash
curl -sSL https://your-repo-url/install.sh | bash
```
*(Note: The URL will be updated once the script is created.)*
