import board
import busio
import adafruit_bme680
import time
import logging
import json
import os
from collections import deque
from datetime import datetime, timezone
from typing import Dict, Optional, Any

from src.core.config import settings
from src.core.database import db

logger = logging.getLogger(__name__)

BASELINE_FILE = "baseline.json"


class BME680Reader:
    def __init__(
        self, device_id: Optional[str] = None, read_interval: Optional[float] = None
    ):
        self.device_id = device_id or settings.DEVICE_ID
        self.read_interval = read_interval or settings.READ_INTERVAL

        # Initialize I2C bus
        try:
            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(self.i2c)
            self.bme680.sea_level_pressure = 1013.25
        except Exception as e:
            logger.error(
                f"Failed to initialize BME680: {e}", extra={"device_id": self.device_id}
            )
            self.bme680 = None

        # Air Quality Baseline Persistence
        self.gas_baseline = 50000.0  # Default fallback (Ohms)
        self._load_baseline()

        self.start_time: float = time.monotonic()
        self.reading_count: int = 0
        self.latest_data: Dict[str, Any] = {}
        self.history_buffer = deque(
            maxlen=1800
        )  # Store ~1 hour of data at 2-second intervals
        self.stop_event: bool = False

    def _load_baseline(self):
        try:
            if os.path.exists(BASELINE_FILE):
                with open(BASELINE_FILE, "r") as f:
                    data = json.load(f)
                    self.gas_baseline = data.get("gas_baseline_ohms", 50000.0)
                    logger.info(f"Loaded baseline from file: {self.gas_baseline} Ohms")
        except Exception as e:
            logger.error(f"Error loading baseline: {e}")

    def _save_baseline(self):
        try:
            with open(BASELINE_FILE, "w") as f:
                json.dump(
                    {
                        "gas_baseline_ohms": self.gas_baseline,
                        "last_updated": datetime.now().isoformat(),
                    },
                    f,
                )
        except Exception as e:
            logger.error(f"Error saving baseline: {e}")

    def get_timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def calculate_humidity_score(self, current_humidity: float) -> float:
        """
        Humidity Score:
        - 40% - 60%: Ideal (100%)
        - Outside this range: Penalize distance
        """
        if 40 <= current_humidity <= 60:
            return 100.0

        distance = 0
        if current_humidity < 40:
            distance = 40 - current_humidity
        else:
            distance = current_humidity - 60

        # Penalty factor: Dropping to 0 at extreme ends (0% or 100%)
        # If humidity is 0, distance is 40. 100 - (40 * 2.5) = 0
        # If humidity is 100, distance is 40. 100 - (40 * 2.5) = 0
        score = 100 - (distance * 2.5)
        return max(0.0, score)

    def calculate_gas_score(self, current_gas: float) -> float:
        """
        Gas Score:
        - Ratio of current reading to historical max (cleanest air).
        """
        if self.gas_baseline == 0:
            return 0.0

        # Calculate ratio. If current > baseline, it's 100% (and baseline will update)
        ratio = current_gas / self.gas_baseline
        score = ratio * 100.0
        return min(100.0, score)

    def get_air_quality_status(self, score: float) -> str:
        if score >= 90:
            return "Air is Crisp"
        if score >= 75:
            return "Good"
        if score >= 60:
            return "Moderate"
        if score >= 40:
            return "Stale Air"
        return "Polluted / Cooking"

    def get_sensor_reading(self) -> Dict[str, float]:
        if not self.bme680:
            # If sensor is missing (e.g., local dev without hardware),
            # we raise error. The run loop handles it.
            raise RuntimeError("Sensor not initialized")

        return {
            "temperature_c": round(float(self.bme680.temperature), 2),
            "pressure_hpa": round(float(self.bme680.pressure), 2),
            "humidity_rh": round(float(self.bme680.humidity), 2),
            "gas_ohms": round(float(self.bme680.gas), 2),
            "altitude_m": round(float(self.bme680.altitude), 2),
        }

    def run(self) -> None:
        logger.info("BMP680 sensor reader starting with Advanced Logic")

        while not self.stop_event:
            try:
                self.reading_count += 1
                reading = self.get_sensor_reading()

                # 1. Update Baseline (Persistence)
                current_gas = reading["gas_ohms"]
                if current_gas > self.gas_baseline:
                    self.gas_baseline = current_gas
                    self._save_baseline()
                    logger.info(
                        f"New cleaner air baseline found: {self.gas_baseline} Ohms"
                    )

                # 2. Calculate Scores
                gas_score = self.calculate_gas_score(current_gas)
                hum_score = self.calculate_humidity_score(reading["humidity_rh"])

                # Weighted Composite Score (75% Gas, 25% Humidity)
                final_score = (gas_score * 0.75) + (hum_score * 0.25)
                final_score = round(final_score, 1)

                status_text = self.get_air_quality_status(final_score)

                sensor_data = {
                    "timestamp": self.get_timestamp(),
                    "device_id": self.device_id,
                    "reading_count": self.reading_count,
                    "uptime_seconds": round(time.monotonic() - self.start_time, 1),
                    **reading,
                    "gas_baseline_ohms": round(self.gas_baseline, 2),
                    "air_quality_score": final_score,
                    "air_quality_status": status_text,
                    "components": {
                        "gas_score": round(gas_score, 1),
                        "humidity_score": round(hum_score, 1),
                    },
                }

                self.latest_data = sensor_data
                self.history_buffer.append(sensor_data)
                
                # Persist to Database
                db.upsert_sensor(self.device_id)
                db.add_reading(sensor_data)

            except Exception as e:
                # Log error but keep loop alive (exponential backoff could be added here)
                logger.error(
                    "Failed to read sensor data",
                    extra={"error": str(e), "reading_count": self.reading_count},
                )

            time.sleep(self.read_interval)

    def stop(self) -> None:
        self.stop_event = True
