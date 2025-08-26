import board
import busio
import adafruit_bme680
import time
import os
import json
import sys
import signal
import socket
from collections import deque
from datetime import datetime, timezone

# Configuration via environment variables
DEVICE_ID = os.getenv("DEVICE_ID", socket.gethostname())
READ_INTERVAL = float(os.getenv("READ_INTERVAL", "2.0"))

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor object using the BME680 library
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# You can set the sea level pressure for more accurate altitude readings
bme680.sea_level_pressure = 1013.25

# --- Air Quality Baseline Parameters ---
GAS_READINGS_WINDOW_SIZE = 60 # Number of readings to keep for moving average
gas_readings = deque(maxlen=GAS_READINGS_WINDOW_SIZE)
initial_baseline_established = False
BASELINE_WARMUP_PERIOD = 120 # Seconds to wait before establishing initial baseline
start_time = time.monotonic()

# Graceful shutdown handling
_STOP = False
def _handle_stop(signum, frame):
    global _STOP
    _STOP = True
    log_info("Received shutdown signal, gracefully stopping...")

signal.signal(signal.SIGTERM, _handle_stop)
signal.signal(signal.SIGINT, _handle_stop)

def get_timestamp():
    """Get current timestamp in ISO format"""
    return datetime.now(timezone.utc).isoformat()

def log_info(message, **extra_data):
    """Log info message as JSON"""
    log_entry = {
        "timestamp": get_timestamp(),
        "device_id": DEVICE_ID,
        "level": "INFO",
        "message": message,
        **extra_data
    }
    print(json.dumps(log_entry, separators=(",", ":")), flush=True)

def log_error(message, error=None, **extra_data):
    """Log error message as JSON to stderr"""
    log_entry = {
        "timestamp": get_timestamp(),
        "device_id": DEVICE_ID,
        "level": "ERROR",
        "message": message,
        **({"error": str(error)} if error else {}),
        **extra_data
    }
    print(json.dumps(log_entry, separators=(",", ":")), file=sys.stderr, flush=True)

def calculate_air_quality_score(current_gas, baseline_gas):
    """Calculate air quality score based on gas resistance"""
    if baseline_gas == 0:
        return 0.0
    
    ratio = current_gas / baseline_gas
    score = 50 + (ratio - 1) * 50
    return round(max(0, min(100, score)), 2)

def get_sensor_reading():
    """Get current sensor reading and return as dict"""
    return {
        "temperature_c": round(float(bme680.temperature), 2),
        "pressure_hpa": round(float(bme680.pressure), 2), 
        "humidity_rh": round(float(bme680.humidity), 2),
        "gas_ohms": round(float(bme680.gas), 2),
        "altitude_m": round(float(bme680.altitude), 2)
    }

# Log startup
log_info("BMP680 sensor reader starting", 
         read_interval=READ_INTERVAL,
         gas_window_size=GAS_READINGS_WINDOW_SIZE,
         warmup_period=BASELINE_WARMUP_PERIOD)

reading_count = 0

while not _STOP:
    try:
        reading_count += 1
        
        # Get sensor reading
        reading = get_sensor_reading()
        gas = reading["gas_ohms"]
        
        # Update gas readings for dynamic baseline
        gas_readings.append(gas)
        
        current_air_quality_score = None
        baseline_gas_resistance = None
        
        # Establish initial baseline after warmup period
        if not initial_baseline_established:
            if time.monotonic() - start_time > BASELINE_WARMUP_PERIOD and len(gas_readings) == GAS_READINGS_WINDOW_SIZE:
                baseline_gas_resistance = round(sum(gas_readings) / len(gas_readings), 2)
                initial_baseline_established = True
                log_info("Gas resistance baseline established", 
                         baseline_gas_ohms=baseline_gas_resistance,
                         readings_collected=len(gas_readings))
            else:
                log_info("Collecting baseline readings", 
                         collected=len(gas_readings),
                         needed=GAS_READINGS_WINDOW_SIZE,
                         warmup_remaining=max(0, BASELINE_WARMUP_PERIOD - (time.monotonic() - start_time)))
        
        if initial_baseline_established:
            baseline_gas_resistance = round(sum(gas_readings) / len(gas_readings), 2)
            current_air_quality_score = calculate_air_quality_score(gas, baseline_gas_resistance)
        
        # Create comprehensive sensor data payload
        sensor_data = {
            "timestamp": get_timestamp(),
            "device_id": DEVICE_ID,
            "reading_count": reading_count,
            "uptime_seconds": round(time.monotonic() - start_time, 1),
            **reading
        }
        
        if baseline_gas_resistance is not None:
            sensor_data["gas_baseline_ohms"] = baseline_gas_resistance
        if current_air_quality_score is not None:
            sensor_data["air_quality_score"] = current_air_quality_score
            
        # Add some additional computed metrics
        sensor_data.update({
            "dew_point_c": round(reading["temperature_c"] - ((100 - reading["humidity_rh"]) / 5), 2),
            "heat_index_c": round(reading["temperature_c"] + 0.5 * reading["humidity_rh"] / 10, 2),
            "gas_readings_buffer_size": len(gas_readings),
            "baseline_established": initial_baseline_established
        })
        
        # Output the main sensor data as JSON
        print(json.dumps(sensor_data, separators=(",", ":")), flush=True)
        
        # Every 10 readings, output a summary
        if reading_count % 10 == 0:
            summary = {
                "timestamp": get_timestamp(),
                "device_id": DEVICE_ID,
                "type": "SUMMARY",
                "reading_count": reading_count,
                "avg_temp_last_10": round(reading["temperature_c"], 2),  # Simplified for demo
                "avg_humidity_last_10": round(reading["humidity_rh"], 2),
                "avg_pressure_last_10": round(reading["pressure_hpa"], 2),
                "current_gas_trend": "stable" if len(gas_readings) > 1 and abs(gas_readings[-1] - gas_readings[-2]) < 100 else "changing"
            }
            print(json.dumps(summary, separators=(",", ":")), flush=True)
        
        # Every 30 readings, output detailed statistics
        if reading_count % 30 == 0 and len(gas_readings) > 5:
            stats = {
                "timestamp": get_timestamp(),
                "device_id": DEVICE_ID,
                "type": "STATISTICS",
                "gas_stats": {
                    "min_ohms": round(min(gas_readings), 2),
                    "max_ohms": round(max(gas_readings), 2),
                    "avg_ohms": round(sum(gas_readings) / len(gas_readings), 2),
                    "readings_count": len(gas_readings)
                },
                "sensor_status": "healthy",
                "memory_usage_readings": len(gas_readings)
            }
            print(json.dumps(stats, separators=(",", ":")), flush=True)
            
    except Exception as e:
        log_error("Failed to read sensor data", error=e, reading_count=reading_count)
        
    # Wait before next reading
    time.sleep(READ_INTERVAL)

# Final shutdown log
log_info("BMP680 sensor reader stopped", total_readings=reading_count)
