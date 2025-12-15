# IoT System Testing Protocol: Multi-Sensor Air Quality Monitor

**Version:** 1.0
**Status:** Draft
**Target Audience:** QA Engineers, AI Agents, Developers
**Scope:** Validation of the `feature/multi-sensor-support` branch across Firmware, Backend, Database, and Frontend.

---

## 1. Introduction
This document defines the comprehensive testing protocol for the Air Quality Monitoring System. It ensures that the system reliably ingests, stores, and visualizes data from multiple distributed sensors (ESP32-C3) via a central Hub (Orange Pi 3 LTS).

### 1.1 Objectives
- Validate reliable data ingestion from remote nodes.
- Ensure data integrity and persistence in the SQLite database.
- Verify secure API access using API Keys.
- Confirm accurate real-time visualization and averaging on the Dashboard.
- Test resilience against network failures and invalid data.

---

## 2. Test Environment

### 2.1 Hardware Requirements
- **Hub:** Orange Pi 3 LTS (Target) or Docker-compatible Host (Dev).
- **Nodes:** ESP32-C3 SuperMini (x1 minimum) + BME680 Sensor.
- **Network:** Local Wi-Fi (2.4GHz) with visibility between Nodes and Hub.

### 2.2 Software Prerequisites
- **Docker & Compose:** For running the Hub stack (`nginx`, `backend`, `frontend`).
- **Python 3.11+:** For running simulation and test scripts.
- **MicroPython:** Flashed on ESP32-C3 nodes.

---

## 3. Automated Verification (CI/CD)

**Goal:** Ensure logic correctness before deployment.

### 3.1 Unit & Integration Tests
Run the `pytest` suite to verify API endpoints, database constraints, and business logic (averaging, renaming).

*   **Command:** `make test` (or `pytest backend/tests/`)
*   **Success Criteria:** All tests passed (Exit Code 0).
*   **Key Test Cases:**
    *   `test_ingest_flow`: Verifies 201 Created and DB persistence.
    *   `test_sensor_renaming`: Verifies `PUT` updates `sensors` table.
    *   `test_average_calculation`: Verifies math for `device_id=average`.
    *   `test_security_rejection`: Verifies 401 Unauthorized without API Key.

---

## 4. System Simulation (Virtual Integration)

**Goal:** Test the full data pipeline without physical hardware.

### 4.1 Nominal Data Flow
Use `scripts/simulate_sensors.py` to mimic 3 active sensors ("Living Room", "Bedroom", "Kitchen").

1.  **Configure:** Check `API_KEY` in script matches `.env`.
2.  **Run:** `python3 scripts/simulate_sensors.py`
3.  **Verify Backend:**
    *   Logs should show `POST /api/ingest 201`.
    *   DB should contain entries in `readings` table.
4.  **Verify Frontend:**
    *   Open Dashboard (`http://localhost`).
    *   Dropdown should list the 3 simulated sensors.
    *   Select "Living Room" -> Gauge shows ~22°C.
    *   Select "Average" -> Gauge shows aggregate value.

### 4.2 Stress Testing (Load)
Modify the simulation script to spawn 20 threads sending data every 1 second.
*   **Observation:** Monitor `docker stats`. Check if `nginx` or `gunicorn` drops requests.
*   **Success Criteria:** No 500 errors; Dashboard remains responsive.

### 4.3 Network Partition Simulation
1.  Run simulation.
2.  Stop simulation (Ctrl+C).
3.  Wait 15 minutes.
4.  **Verification:** Dashboard Dropdown should mark sensors as `(Offline)`.

---

## 5. Security Validation

**Goal:** Ensure the system is protected against unauthorized access.

### 5.1 API Key Enforcement
1.  **Valid Request:**
    ```bash
    curl -X POST http://localhost/api/ingest \
      -H "Content-Type: application/json" \
      -H "X-API-Key: dev-secret-key" \
      -d '{"device_id": "test_secure", "temperature_c": 25}'
    ```
    *   **Result:** `201 Created`

2.  **Invalid Request (Wrong Key):**
    ```bash
    curl -X POST http://localhost/api/ingest \
      -H "Content-Type: application/json" \
      -H "X-API-Key: wrong-password" \
      -d '{"device_id": "test_hack", "temperature_c": 25}'
    ```
    *   **Result:** `401 Unauthorized`

3.  **Missing Header:**
    ```bash
    curl -X POST http://localhost/api/ingest \
      -d '{"device_id": "test_hack", "temperature_c": 25}'
    ```
    *   **Result:** `401 Unauthorized`

---

## 6. Hardware Verification (Field Test)

**Goal:** Validate physical layer and connectivity.

### 6.1 I2C Sensor Check (Hub)
Run the diagnostic tool on the Orange Pi container to verify the local BME680.
*   **Command:** `docker-compose run --rm --privileged bmp-sensor python scripts/test_sensor_hardware.py`
*   **Success:** Output "Sensor Initialized" with valid readings.

### 6.2 ESP32 Node Commissioning
1.  **Flash:** Upload `boot.py`, `config.py` (with Wi-Fi/API creds), and `main.py`.
2.  **Power On:** Connect USB-C power.
3.  **Observe:** Check Dashboard after ~60 seconds.
4.  **Success:** New Sensor ID appears in the dropdown. Rename it via Settings -> Sensors.

---

## 7. Exit Criteria

The feature is considered **Production Ready** when:
- [ ] Automated tests pass (100%).
- [ ] Simulation validates data flow and averaging logic.
- [ ] Security tests confirm unauthorized access is blocked.
- [ ] Frontend correctly displays "Offline" status for stale sensors.
- [ ] At least one physical node has successfully reported data.