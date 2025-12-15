import pytest
from src.core.database import db

def test_ingest_flow(client):
    """Test full flow: Ingest -> List -> Get Data"""
    
    # 1. Ingest Data
    payload = {
        "device_id": "test_sensor_1",
        "temperature_c": 25.0,
        "humidity_rh": 50.0,
        "pressure_hpa": 1013.0,
        "gas_ohms": 15000.0,
        "air_quality_score": 95.0
    }
    
    response = client.post("/api/ingest", json=payload)
    assert response.status_code == 201
    
    # 2. Verify it appears in sensor list
    response = client.get("/api/sensors")
    assert response.status_code == 200
    data = response.json
    # Check if test_sensor_1 is in the list
    ids = [s["device_id"] for s in data]
    assert "test_sensor_1" in ids
    
    # 3. Get Specific Data
    response = client.get("/api/data?device_id=test_sensor_1")
    assert response.status_code == 200
    assert response.json["temperature_c"] == 25.0

def test_sensor_renaming(client):
    """Test renaming a sensor."""
    # Register sensor via ingest
    client.post("/api/ingest", json={"device_id": "raw_id", "temperature_c": 20})
    
    # Rename it
    response = client.put("/api/sensors/raw_id", json={"name": "Living Room"})
    assert response.status_code == 200
    
    # Verify new name
    response = client.get("/api/sensors")
    assert response.json[0]["name"] == "Living Room"

def test_average_calculation(client):
    """Test averaging logic with two sensors."""
    
    # Sensor 1: 20C, 40%
    client.post("/api/ingest", json={
        "device_id": "s1", "temperature_c": 20.0, "humidity_rh": 40.0,
        "pressure_hpa": 1000, "gas_ohms": 10000, "air_quality_score": 80
    })
    
    # Sensor 2: 30C, 60%
    client.post("/api/ingest", json={
        "device_id": "s2", "temperature_c": 30.0, "humidity_rh": 60.0,
        "pressure_hpa": 1000, "gas_ohms": 10000, "air_quality_score": 80
    })
    
    # Request Average
    response = client.get("/api/data?device_id=average")
    assert response.status_code == 200
    data = response.json
    
    # Expect: 25C, 50%
    assert data["device_id"] == "average"
    assert data["temperature_c"] == 25.0
    assert data["humidity_rh"] == 50.0

def test_inactive_sensor_filtering(client):
    """Ensure we don't crash if no active sensors exist."""
    # No data ingested yet
    response = client.get("/api/data?device_id=average")
    # Should return 503 Service Unavailable or similar error
    assert response.status_code == 503
    assert "error" in response.json
