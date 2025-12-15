import threading
import time
import logging
import requests
from flask import Flask

from src.core.config import settings
from src.core.logger import setup_logging
from src.state import state
from src.services.sensor import BME680Reader
from src.services.n8n import send_to_n8n
from src.api.routes import api_bp

logger = logging.getLogger(__name__)


def n8n_sender_thread():
    """Background thread to send data to n8n."""
    logger.info("Starting n8n sender thread")
    while state.running:
        if state.reader and state.reader.latest_data:
            state.explanation = send_to_n8n(state.reader.latest_data)

        # Sleep loop with check
        for _ in range(600):
            if not state.running:
                break
            time.sleep(0.1)
    logger.info("n8n sender thread stopped")


def create_app():
    setup_logging()
    app = Flask(__name__)

    app.register_blueprint(api_bp, url_prefix="/api")

    # Initialize Sensor & Threads
    # Note: In Gunicorn, this runs in the worker process.
    # Ensure Gunicorn is run with --workers 1 to prevent multiple processes accessing I2C.
    if not state.reader:
        try:
            logger.info("Initializing BME680 Reader...")
            state.reader = BME680Reader()

            t_sensor = threading.Thread(
                target=state.reader.run, name="SensorThread", daemon=True
            )
            t_sensor.start()

            t_n8n = threading.Thread(
                target=n8n_sender_thread, name="N8NThread", daemon=True
            )
            t_n8n.start()
        except Exception as e:
            logger.error(f"Failed to start background threads: {e}")

    return app
