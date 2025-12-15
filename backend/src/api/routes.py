from flask import Blueprint, jsonify, request, redirect
from typing import Dict
from src.state import state
from src.core.database import db
import src.services.google as google_service

api_bp = Blueprint("api", __name__)


# --- Sensor Data Ingestion & Retrieval ---

@api_bp.route("/ingest", methods=["POST"])
def ingest_data():
    """Receive data from remote sensor nodes."""
    try:
        data = request.json
        if not data or "device_id" not in data:
            return jsonify({"error": "Missing device_id"}), 400

        # Update metadata
        db.upsert_sensor(data["device_id"])
        
        # Save reading
        db.add_reading(data)
        
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/sensors", methods=["GET"])
def list_sensors():
    """List all active sensors."""
    active_sensors = db.get_active_sensors(threshold_minutes=15)
    return jsonify(active_sensors)


@api_bp.route("/sensors/<device_id>", methods=["PUT"])
def update_sensor(device_id):
    """Update sensor friendly name."""
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Missing name"}), 400
        
    db.upsert_sensor(device_id, name=data["name"])
    return jsonify({"status": "updated"})


@api_bp.route("/data")
def api_data():
    """Get sensor data. 
    Query Params:
    - device_id: specific ID, or 'average', or missing (returns local/all)
    """
    device_id = request.args.get("device_id")

    # 1. Specific Device Request
    if device_id and device_id != "average":
        readings = db.get_latest_readings([device_id])
        if device_id in readings:
            data = readings[device_id]
            # Add explanation if it's the local hub (or we could propagate n8n explanation globally)
            if state.reader and state.reader.device_id == device_id:
                data["explanation"] = state.explanation
            return jsonify(data)
        return jsonify({"error": "Device not found or inactive"}), 404

    # 2. Average Request
    if device_id == "average":
        active_sensors = db.get_active_sensors()
        if not active_sensors:
             return jsonify({"error": "No active sensors"}), 503
             
        ids = [s['device_id'] for s in active_sensors]
        readings = db.get_latest_readings(ids)
        
        if not readings:
            return jsonify({"error": "No readings available"}), 503

        # Calculate Averages
        avg_data = {
            "device_id": "average",
            "timestamp": list(readings.values())[0]['timestamp'], # Use one timestamp
            "temperature_c": 0, "humidity_rh": 0, "pressure_hpa": 0, 
            "gas_ohms": 0, "air_quality_score": 0,
            "explanation": state.explanation # Global explanation
        }
        
        count = len(readings)
        for r in readings.values():
            avg_data["temperature_c"] += r["temperature_c"]
            avg_data["humidity_rh"] += r["humidity_rh"]
            avg_data["pressure_hpa"] += r["pressure_hpa"]
            avg_data["gas_ohms"] += r["gas_ohms"]
            avg_data["air_quality_score"] += r["air_quality_score"]
            
        for k in ["temperature_c", "humidity_rh", "pressure_hpa", "gas_ohms", "air_quality_score"]:
            avg_data[k] = round(avg_data[k] / count, 2)
            
        # Determine status based on avg score
        score = avg_data["air_quality_score"]
        if score >= 90: avg_data["air_quality_status"] = "Air is Crisp"
        elif score >= 75: avg_data["air_quality_status"] = "Good"
        elif score >= 60: avg_data["air_quality_status"] = "Moderate"
        elif score >= 40: avg_data["air_quality_status"] = "Stale Air"
        else: avg_data["air_quality_status"] = "Polluted"

        return jsonify(avg_data)

    # 3. Default: Return Local Hub Data (Backward Compatibility)
    if not state.reader:
        return jsonify({"error": "Sensor not initialized"}), 503

    data = state.reader.latest_data.copy()
    data["explanation"] = state.explanation
    return jsonify(data)


@api_bp.route("/history")
def api_history():
    if not state.reader:
        return jsonify({"error": "Sensor not initialized"}), 503

    # Return a list of all historical readings
    # TODO: In future, fetch from DB based on device_id param
    return jsonify(list(state.reader.history_buffer))


# --- Google Services ---

@api_bp.route("/calendar")
def api_calendar():
    events = google_service.fetch_events()
    return jsonify(events)


@api_bp.route("/auth/google")
def google_auth():
    # Construct the host URL dynamically or from settings
    host_url = request.url_root.rstrip("/")
    auth_url, error = google_service.get_auth_url(host_url)
    if error:
        return jsonify({"error": error}), 500
    return redirect(auth_url)


@api_bp.route("/auth/callback")
def google_auth_callback():
    code = request.args.get("code")
    if not code:
        return "Error: No code provided", 400

    host_url = request.url_root.rstrip("/")
    success, message = google_service.handle_auth_callback(code, host_url)

    if success:
        return redirect("/")  # Redirect back to dashboard
    else:
        return f"Authentication Failed: {message}", 500