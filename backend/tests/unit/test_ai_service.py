import pytest
from backend.src.services.ai_service import AIService
from backend.src.models.sensor_data import SensorData
from datetime import datetime

def test_generate_recommendation():
    ai_service = AIService()
    sample_sensor_data = SensorData(
        timestamp=datetime.now(),
        temperature=25.0,
        pressure=1012.0,
        humidity=45.0
    )
    recommendation = ai_service.generate_recommendation(sample_sensor_data)
    assert recommendation.recommendation_text == "This is a dummy AI recommendation based on your sensor data."
