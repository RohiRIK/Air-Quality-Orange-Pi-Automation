
# Project To-Do List

- [x] **1. Create Project Files**
    - [x] Create `requirements.txt` with necessary Python libraries.
    - [x] Create the initial `bmp_reader.py` script based on the documentation.
    - [x] Create the `Dockerfile` to containerize the application.

- [ ] **2. Install Armbian and Connect Sensor:**
    - [ ] Install Armbian OS on Orange Pi.
    - [ ] Connect BME688 sensor to Orange Pi.
    - [ ] Verify sensor connection (`sudo i2cdetect -y 0`).

- [x] **3. Upgrade to BME688 Sensor**
    - [x] Update `requirements.txt` with the `adafruit-circuitpython-bme680` library.
    - [x] Update `bmp_reader.py` to read humidity and gas data.
    - [x] Update all documentation to reflect new sensor capabilities.

- [x] **4. Add Update Automation**
    - [x] Create `scripts/update_os.sh` for OS package maintenance.
    - [x] Create `docker-compose.yml` with Watchtower for automatic container updates.
    - [x] Document the Docker Hub push/pull workflow for updates.

- [X] **5. Push to GitHub**
    - [X] Initialize a new GitHub repository.
    - [X] Add all current project files.
    - [X] Create and push the initial commit.

- [ ] **6. Test and Deploy**
    - [ ] Phase 1: Local Testing (Optional)
        - [ ] Install dependencies and run the Python script directly on the Orange Pi.
        - [ ] Verify sensor readings.
    - [ ] Phase 2: Docker Testing
        - [ ] Build and run services with `docker-compose up --build -d`.
        - [ ] Verify the container is running and sending data.
    - [ ] Phase 3: Deploy to Docker Hub
        - [ ] Log in to Docker Hub (`docker login`).
        - [ ] Push the image with `docker-compose push`.

- [ ] **7. Create Comprehensive Setup Script**
    - [ ] Update OS packages.
    - [ ] Install `git`, `python3-pip`, `i2c-tools`.
    - [ ] Install `docker.io` and `docker-compose-v2`.
    - [ ] Clone the project repository.
    - [ ] Enable I2C (with user prompt for reboot).
    - [ ] Install Python dependencies.
    - [ ] Build and run Docker Compose services.
    - [ ] (Optional) Set up cron jobs for `update_os.sh`.

- [ ] **8. Refine and Enhance**
    - [ ] Refactor the Python script for robustness.
    - [ ] Implement an air quality baseline feature.