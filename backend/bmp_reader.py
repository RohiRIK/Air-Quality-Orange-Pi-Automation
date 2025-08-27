import os
import time
import json
import sys
import socket
import random
from collections import deque
from datetime import datetime, timezone

# Check if running in development mode
IS_DEV_MODE = os.environ.get('DEV_MODE', 'false').lower() == 'true'

if IS_DEV_MODE:
    # --- Development Mode: Mock BME680 Reader ---
    class BME680Reader:
        def __init__(self, device_id=None, read_interval=2.0):
            self.device_id = device_id or "dev-device"
            self.read_interval = read_interval
            self.latest_data = {}
            self.stop_event = False
            self.reading_count = 0
            self.start_time = time.monotonic()
            self.log_info("Running in DEVELOPMENT MODE. Using mock sensor data.")

        def get_timestamp(self):
            return datetime.now(timezone.utc).isoformat()

        def log_info(self, message, **extra_data):
            log_entry = {
                "timestamp": self.get_timestamp(),
                "device_id": self.device_id,
                "level": "INFO",
                "message": message,
                **extra_data
            }
            print(json.dumps(log_entry, separators=(",", ":")), flush=True)

        def log_error(self, message, error=None, **extra_data):
            log_entry = {
                "timestamp": self.get_timestamp(),
                "device_id": self.device_id,
                "level": "ERROR",
                "message": message,
                **({"error": str(error)} if error else {}),
                **extra_data
            }
            print(json.dumps(log_entry, separators=(",", ":")), file=sys.stderr, flush=True)

        def get_sensor_reading(self):
            # Simulate realistic sensor data
            return {
                "temperature_c": round(random.uniform(20, 25), 2),
                "pressure_hpa": round(random.uniform(1000, 1020), 2),
                "humidity_rh": round(random.uniform(40, 60), 2),
                "gas_ohms": round(random.uniform(25000, 35000), 2),
                "altitude_m": round(random.uniform(100, 150), 2)
            }

        def run(self):
            self.log_info("Mock BMP680 sensor reader starting", read_interval=self.read_interval)
            while not self.stop_event:
                try:
                    self.reading_count += 1
                    reading = self.get_sensor_reading()
                    
                    sensor_data = {
                        "timestamp": self.get_timestamp(),
                        "device_id": self.device_id,
                        "reading_count": self.reading_count,
                        "uptime_seconds": round(time.monotonic() - self.start_time, 1),
                        **reading,
                        "air_quality_score": round(random.uniform(10, 40), 2),
                        "gas_baseline_ohms": round(random.uniform(28000, 32000), 2),
                        "dew_point_c": round(reading["temperature_c"] - ((100 - reading["humidity_rh"]) / 5), 2),
                        "heat_index_c": round(reading["temperature_c"] + 0.5 * reading["humidity_rh"] / 10, 2),
                        "gas_readings_buffer_size": 60,
                        "baseline_established": True
                    }
                    self.latest_data = sensor_data
                except Exception as e:
                    self.log_error("Error in mock sensor loop", error=e)
                
                time.sleep(self.read_interval)
            self.log_info("Mock BMP680 sensor reader stopped", total_readings=self.reading_count)

        def stop(self):
            self.stop_event = True

else:
    # --- Production Mode: Real BME680 Reader ---
    import board
    import busio
    import adafruit_bme680

    class BME680Reader:
        def __init__(self, device_id=None, read_interval=2.0):
            self.device_id = device_id or socket.gethostname()
            self.read_interval = read_interval
            
            # Initialize I2C bus
            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(self.i2c)
            self.bme680.sea_level_pressure = 1013.25

            # Air Quality Baseline Parameters
            self.gas_readings = deque(maxlen=60)
            self.initial_baseline_established = False
            self.baseline_warmup_period = 120
            self.start_time = time.monotonic()
            
            self.reading_count = 0
            self.latest_data = {}
            self.stop_event = False

        def get_timestamp(self):
            return datetime.now(timezone.utc).isoformat()

        def log_info(self, message, **extra_data):
            log_entry = {
                "timestamp": self.get_timestamp(),
                "device_id": self.device_id,
                "level": "INFO",
                "message": message,
                **extra_data
            }
            print(json.dumps(log_entry, separators=(",", ":")), flush=True)

        def log_error(self, message, error=None, **extra_data):
            log_entry = {
                "timestamp": self.get_timestamp(),
                "device_id": self.device_id,
                "level": "ERROR",
                "message": message,
                **({"error": str(error)} if error else {}),
                **extra_data
            }
            print(json.dumps(log_entry, separators=(",", ":")), file=sys.stderr, flush=True)

        def calculate_air_quality_score(self, current_gas, baseline_gas):
            if baseline_gas == 0:
                return 0.0
            ratio = current_gas / baseline_gas
            score = 50 + (ratio - 1) * 50
            return round(max(0, min(100, score)), 2)

        def get_sensor_reading(self):
            return {
                "temperature_c": round(float(self.bme680.temperature), 2),
                "pressure_hpa": round(float(self.bme680.pressure), 2),
                "humidity_rh": round(float(self.bme680.humidity), 2),
                "gas_ohms": round(float(self.bme680.gas), 2),
                "altitude_m": round(float(self.bme680.altitude), 2)
            }

        def run(self):
            self.log_info("BMP680 sensor reader starting",
                          read_interval=self.read_interval,
                          gas_window_size=self.gas_readings.maxlen,
                          warmup_period=self.baseline_warmup_period)

            while not self.stop_event:
                try:
                    self.reading_count += 1
                    reading = self.get_sensor_reading()
                    gas = reading["gas_ohms"]
                    self.gas_readings.append(gas)

                    current_air_quality_score = None
                    baseline_gas_resistance = None

                    if not self.initial_baseline_established:
                        if time.monotonic() - self.start_time > self.baseline_warmup_period and len(self.gas_readings) == self.gas_readings.maxlen:
                            baseline_gas_resistance = round(sum(self.gas_readings) / len(self.gas_readings), 2)
                            self.initial_baseline_established = True
                            self.log_info("Gas resistance baseline established",
                                          baseline_gas_ohms=baseline_gas_resistance,
                                          readings_collected=len(self.gas_readings))
                    
                    if self.initial_baseline_established:
                        baseline_gas_resistance = round(sum(self.gas_readings) / len(self.gas_readings), 2)
                        current_air_quality_score = self.calculate_air_quality_score(gas, baseline_gas_resistance)

                    sensor_data = {
                        "timestamp": self.get_timestamp(),
                        "device_id": self.device_id,
                        "reading_count": self.reading_count,
                        "uptime_seconds": round(time.monotonic() - self.start_time, 1),
                        **reading
                    }

                    if baseline_gas_resistance is not None:
                        sensor_data["gas_baseline_ohms"] = baseline_gas_resistance
                    if current_air_quality_score is not None:
                        sensor_data["air_quality_score"] = current_air_quality_score

                    sensor_data.update({
                        "dew_point_c": round(reading["temperature_c"] - ((100 - reading["humidity_rh"]) / 5), 2),
                        "heat_index_c": round(reading["temperature_c"] + 0.5 * reading["humidity_rh"] / 10, 2),
                        "gas_readings_buffer_size": len(self.gas_readings),
                        "baseline_established": self.initial_baseline_established
                    })
                    
                    self.latest_data = sensor_data

                except Exception as e:
                    self.log_error("Failed to read sensor data", error=e, reading_count=self.reading_count)

                time.sleep(self.read_interval)

            self.log_info("BMP680 sensor reader stopped", total_readings=self.reading_count)

        def stop(self):
            self.stop_event = True