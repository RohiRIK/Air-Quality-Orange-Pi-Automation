import pytest
from fastapi.testclient import TestClient
from backend.src.main import app # Assuming app is in backend/src/main.py

client = TestClient(app)

def test_post_recommendation():
    sample_sensor_data = {
        "timestamp": "2025-09-11T10:00:00Z",
        "temperature": 25.5,
        "pressure": 1012.5,
        "humidity": 45.2
    }
    response = client.post("/recommendation", json=sample_sensor_data)
    assert response.status_code == 200
    assert "recommendation_text" in response.json()
