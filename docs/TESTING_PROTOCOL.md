# Comprehensive Testing Protocol

**Goal:** Verify the functionality, security, and stability of the Multi-Sensor Air Quality System.
**Target Audience:** AI Agents, QA Engineers, Developers.
**Branch:** `feature/multi-sensor-support`

---

## 1. Environment Preparation

Before testing, ensure the environment is clean and running the latest code.

### 1.1. Reset & Start Stack
**Command:**
```bash
make down
docker volume prune -f # Optional: Clear DB to start fresh
make up
```
**Verification:**
- Run `make logs`.
- Ensure `bmp-sensor` and `nginx` containers are healthy.
- Ensure `frontend` is ready (Next.js build complete).

---

## 2. Backend Automated Tests (CI/CD)

Run the unit and integration tests suite to verify API logic and database interactions.

**Command:**
```bash
make test
```
*(Or locally: `pytest backend/tests/`)*

**Expectations:**
- [ ] `test_ingest_flow`: Verifies data ingestion, DB persistence, and listing.
- [ ] `test_sensor_renaming`: Verifies `PUT /api/sensors/{id}` works.
- [ ] `test_average_calculation`: Verifies the aggregation logic.
- [ ] **Result:** All tests passed (Exit Code 0).

---

## 3. Infrastructure & Integration Simulation

Use the simulation script to mimic multiple physical ESP32 nodes interacting with the Hub.

### 3.1. Configure Simulation
Ensure `scripts/simulate_sensors.py` has the correct `API_KEY` matching `backend/src/core/config.py` (default: `dev-secret-key`).

### 3.2. Run Simulation
**Command:**
```bash
python3 scripts/simulate_sensors.py
```

**Verification Steps:**
1.  **Console Output:** Verify it prints "Sent [Living Room]..." with HTTP 201.
2.  **Database Check:**
    - Query the API: `curl http://localhost/api/sensors`
    - **Expectation:** List contains "esp32_living_room", "esp32_bedroom", etc.
3.  **Security Test (Negative Case):**
    - Temporarily change `API_KEY` in the script to "wrong-key".
    - Run script.
    - **Expectation:** Console prints "Error: 401 - Unauthorized".

---

## 4. Frontend Verification (UI/UX)

Open the Dashboard at `http://localhost`.

### 4.1. Sensor Context Selector
- [ ] **Dropdown:** Click the sensor icon/name in the header.
- [ ] **List:** Verify it lists "Whole House (Average)" and all simulated sensors.
- [ ] **Selection:** Select "Living Room".
- [ ] **Data:** Verify the Gauge and Metrics update to match the simulation output (approx. 22°C for Living Room).

### 4.2. Average View
- [ ] Select "Whole House (Average)".
- [ ] Verify the values are an approximate average of all simulated nodes.

### 4.3. Offline Indicator
- [ ] Stop the simulation script.
- [ ] Wait 15 minutes (or manually update DB `last_seen` to old timestamp).
- [ ] **Expectation:** Dropdown list shows "(Offline)" next to sensor names.

### 4.4. Settings & Renaming
- [ ] Click "Settings" (Gear Icon).
- [ ] Switch to "Sensors" tab.
- [ ] Click "Edit" (Pencil) on a sensor.
- [ ] Rename "Living Room" to "Main Lounge".
- [ ] Save.
- [ ] **Expectation:** Name updates immediately in the list and the Dashboard header dropdown.

---

## 5. Hardware Verification (On Orange Pi)

Perform these tests only on the physical device.

### 5.1. I2C Connectivity
**Command:**
```bash
docker-compose run --rm --privileged bmp-sensor python scripts/test_sensor_hardware.py
```
**Expectation:**
- Output: "I2C Bus Initialized"
- Output: "Sensor Initialized!" with valid Temp/Gas readings.
- **Failure:** "No I2C devices found" -> Check wiring or `BLINKA_FORCEBOARD`.

### 5.2. Wi-Fi Setup
**Command:**
```bash
sudo ./scripts/setup_wifi.sh
```
**Expectation:**
- Scans and lists networks.
- Successfully connects and displays IP address.

---

## 6. N8N Integration

### 6.1. Forwarding Check
- Ensure `N8N_WEBHOOK_URL_TEST` is set in `.env` or `docker-compose.yml`.
- Run simulation or ingest data.
- **Expectation:**
    - n8n receives a POST request.
    - Dashboard shows "System Analysis: [SensorID] ..." text (if n8n workflow returns explanation).

---

## Summary Checklist

| Component | Test Method | Status |
| :--- | :--- | :--- |
| **Backend Logic** | `make test` | ⬜ |
| **API Security** | Simulation with invalid key | ⬜ |
| **Data Ingestion** | `simulate_sensors.py` | ⬜ |
| **Frontend UI** | Manual Click-through | ⬜ |
| **Physical Sensor** | `test_sensor_hardware.py` | ⬜ |
| **ESP32 Firmware** | Flash & Observe Logs | ⬜ |
