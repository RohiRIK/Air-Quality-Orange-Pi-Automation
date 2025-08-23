# BMP688 Sensor Project on Orange Pi 3 LTS

## Project Overview
This project demonstrates how to connect a BMP688 barometric pressure sensor to an Orange Pi 3 LTS single-board computer, read environmental data (temperature, pressure, and altitude), format it as JSON, and send it to a remote endpoint. The setup is containerized using Docker for portability and ease of deployment. The project is designed for beginners in electronics and IoT, providing a step-by-step guide to hardware connection, software configuration, and data transmission.

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
├── .DS_Store
├── README.md
├── .git/
├── assets/
│   ├── Armbian_community_25.8.0-trunk.481_Orangepi3-lts_bookworm_current_6.12.35_minimal.img
│   ├── IMG_4730.HEIC
│   ├── IMG_4731.HEIC
│   ├── IMG_4733.HEIC
│   └── IMG_4734.HEIC
└── docs/
    ├── 1_OVERVIEW.md
    ├── 2_GOALS.md
    ├── 3_HARDWARE_SETUP.md
    ├── 4_SOFTWARE_USAGE.md
    ├── 5_TROUBLESHOOTING.md
    └── 6_FUTURE_ENHANCEMENTS.md
```