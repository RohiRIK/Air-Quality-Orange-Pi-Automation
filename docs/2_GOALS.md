# Project Goals

## Primary Goal
To create a fully automated air quality monitoring system for a home environment. The system should be scalable, easy to deploy, and require minimal manual intervention.

## Key Objectives
- **Automated Deployment:** Utilize Docker to create a "less touch" deployment process, allowing new sensor devices to be added to the network seamlessly.
- **Scalability:** Design the system to support multiple sensor devices concurrently, collecting data from various points within the home.
- **Home Automation Integration:** Integrate with platforms like Home Assistant to use sensor data to trigger automated actions, such as activating air purifiers or adjusting ventilation based on air quality thresholds.
- **Real-time Monitoring:** Provide a simple web interface for real-time monitoring of sensor data, including temperature, humidity, pressure, and a dynamic air quality score.
- **Intelligent Air Quality Assessment:** Implement a dynamic baseline and scoring mechanism for gas resistance to provide more meaningful and actionable insights into real-time air quality.
- **Actionable Insights via n8n:** Integrate with n8n to process sensor data and provide actionable explanations and recommendations on the frontend.
- **Web-based Visualization:** Offer a local, web-based dashboard to visualize sensor readings and trends directly from the device.