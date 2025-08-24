# Project Goals

## Primary Goal
To create a fully automated air quality monitoring system for a home environment. The system should be scalable, easy to deploy, and require minimal manual intervention.

## Key Objectives
- **Automated Deployment:** Utilize Docker to create a "less touch" deployment process, allowing new sensor devices to be added to the network seamlessly.
- **Scalability:** Design the system to support multiple sensor devices concurrently, collecting data from various points within the home.
- **Home Automation Integration:** Integrate with platforms like Home Assistant to use sensor data to trigger automated actions, such as activating air purifiers or adjusting ventilation based on air quality thresholds.
- **Reliable Data Transmission:** Ensure comprehensive environmental data, including dynamic air quality assessments (temperature, pressure, humidity, gas resistance, and an air quality score), is reliably formatted as JSON and sent to a central endpoint for logging, analysis, and visualization.
- **Intelligent Air Quality Assessment:** Implement a dynamic baseline and scoring mechanism for gas resistance to provide more meaningful and actionable insights into real-time air quality.
- **Centralized Control:** Lay the groundwork for a system that can be monitored and managed from a central dashboard or application.