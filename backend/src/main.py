from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.models.sensor_data import SensorData
from src.models.ai_recommendation import AIRecommendation
# from src.services.ai_service import AIService # Commented out
import requests
import os # Import os module

app = FastAPI()

# Added CORS middleware
origins = [
    "http://localhost:3000", # Frontend default port
    "http://localhost:3111", # User's current frontend port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ai_service = AIService() # Commented out

# Read SENSOR_API_URL from environment variable
SENSOR_API_URL = os.getenv("SENSOR_API_URL", "http://bmp-sensor:5000/api/data")

@app.get("/")
async def read_root():
    return {"message": "Hello from Backend!"}

@app.get("/api/data", response_model=SensorData)
async def get_sensor_data():
    try:
        response = requests.get(SENSOR_API_URL) # Use SENSOR_API_URL
        response.raise_for_status() # Raise an exception for HTTP errors
        sensor_data = response.json()
        # The bmp_reader.py returns temperature_c, pressure_hpa, humidity_rh, gas_ohms, altitude_m
        # Our SensorData model expects timestamp, temperature, pressure, humidity
        # We need to map these fields
        return SensorData(
            timestamp=sensor_data["timestamp"],
            device_id=sensor_data["device_id"],
            reading_count=sensor_data["reading_count"],
            uptime_seconds=sensor_data["uptime_seconds"],
            temperature=sensor_data["temperature_c"],
            pressure=sensor_data["pressure_hpa"],
            humidity=sensor_data["humidity_rh"],
            gas_ohms=sensor_data["gas_ohms"],
            altitude_m=sensor_data["altitude_m"],
            gas_baseline_ohms=sensor_data.get("gas_baseline_ohms"),
            air_quality_score=sensor_data.get("air_quality_score"),
            dew_point_c=sensor_data.get("dew_point_c"),
            heat_index_c=sensor_data.get("heat_index_c"),
            gas_readings_buffer_size=sensor_data.get("gas_readings_buffer_size"),
            baseline_established=sensor_data.get("baseline_established")
        )
    except requests.exceptions.RequestException as e:
        # Handle connection errors or other request issues
        raise HTTPException(status_code=500, detail=f"Could not connect to BMP sensor: {e}")
    except KeyError as e:
        # Handle missing keys in the response
        raise HTTPException(status_code=500, detail=f"Missing data in BMP sensor response: {e}")

# @app.post("/recommendation", response_model=AIRecommendation) # Commented out
# async def get_recommendation(sensor_data: SensorData): # Commented out
#     recommendation = ai_service.generate_recommendation(sensor_data) # Commented out
#     return recommendation # Commented out
