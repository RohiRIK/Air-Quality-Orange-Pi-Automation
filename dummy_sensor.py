from flask import Flask, jsonify
from datetime import datetime, timezone
import time
import random

app = Flask(__name__)

@app.route('/api/data')
def get_dummy_sensor_data():
    timestamp = datetime.now(timezone.utc).isoformat()
    temperature_c = round(random.uniform(20.0, 30.0), 2)
    pressure_hpa = round(random.uniform(900.0, 1100.0), 2)
    humidity_rh = round(random.uniform(30.0, 70.0), 2)
    gas_ohms = round(random.uniform(1000.0, 10000.0), 2)
    altitude_m = round(random.uniform(0.0, 500.0), 2)
    air_quality_score = round(random.uniform(0.0, 100.0), 2)

    return jsonify({
        "timestamp": timestamp,
        "device_id": "dummy-sensor",
        "reading_count": 1, # Dummy value
        "uptime_seconds": 1, # Dummy value
        "temperature_c": temperature_c,
        "pressure_hpa": pressure_hpa,
        "humidity_rh": humidity_rh,
        "gas_ohms": gas_ohms,
        "altitude_m": altitude_m,
        "gas_baseline_ohms": 5000.0, # Dummy value
        "air_quality_score": air_quality_score,
        "dew_point_c": round(temperature_c - ((100 - humidity_rh) / 5), 2),
        "heat_index_c": round(temperature_c + 0.5 * humidity_rh / 10, 2),
        "gas_readings_buffer_size": 60, # Dummy value
        "baseline_established": True # Dummy value
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
