# BME688 Environmental Sensor Project on Orange Pi 3 LTS

## Project Overview
This project demonstrates how to connect a BME688 4-in-1 environmental sensor to an Orange Pi 3 LTS single-board computer. It reads comprehensive environmental data—temperature, pressure, humidity, and gas resistance (for air quality)—formats it as JSON, and sends it to a remote endpoint. The setup is fully containerized using Docker Compose and includes an automated update workflow with Watchtower, making it a robust and maintainable IoT solution.

## Getting Started

For complete details, please refer to the `docs` directory.

- **1. Overview**: [docs/1_OVERVIEW.md](docs/1_OVERVIEW.md)
- **2. Goals**: [docs/2_GOALS.md](docs/2_GOALS.md)
- **3. Hardware Setup**: [docs/3_HARDWARE_SETUP.md](docs/3_HARDWARE_SETUP.md)
- **4. Software Usage**: [docs/4_SOFTWARE_USAGE.md](docs/4_SOFTWARE_USAGE.md)
- **5. Troubleshooting**: [docs/5_TROUBLESHOOTING.md](docs/5_TROUBLESHOOTING.md)
- **6. Future Enhancements**: [docs/6_FUTURE_ENHANCEMENTS.md](docs/6_FUTURE_ENHANCEMENTS.md)

## Repository Structure

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