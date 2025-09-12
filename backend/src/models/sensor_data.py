from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class SensorData(BaseModel):
    timestamp: datetime
    device_id: str
    reading_count: int
    uptime_seconds: float
    temperature: float
    pressure: float
    humidity: float
    gas_ohms: float
    altitude_m: float
    gas_baseline_ohms: Optional[float] = None
    air_quality_score: Optional[float] = None
    dew_point_c: Optional[float] = None
    heat_index_c: Optional[float] = None
    gas_readings_buffer_size: Optional[int] = None
    baseline_established: Optional[bool] = None