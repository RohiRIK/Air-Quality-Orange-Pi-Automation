from typing import Optional
from src.services.sensor import BME680Reader


class AppState:
    def __init__(self):
        self.explanation: str = "No explanation received from n8n yet."
        self.reader: Optional[BME680Reader] = None
        self.running: bool = True


state = AppState()
