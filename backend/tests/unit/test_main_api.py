import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
import requests_mock
from datetime import datetime

client = TestClient(app)

def test_get_sensor_data():
    with requests_mock.Mocker() as m:
        mock_response = {
            "timestamp": datetime.now().isoformat(),
            "temperature_c": 26.0,
            "pressure_hpa": 1015.0,
            "humidity_rh": 50.0,
            "gas_ohms": 10000.0,
            "altitude_m": 100.0
        }
        m.get("http://bmp-sensor:5000/api/data", json=mock_response)

        response = client.get("/api/data")
        assert response.status_code == 200
        data = response.json()
        assert "timestamp" in data
        assert data["temperature"] == 26.0
        assert data["pressure"] == 1015.0
        assert data["humidity"] == 50.0
