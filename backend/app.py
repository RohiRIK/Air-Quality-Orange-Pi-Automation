from flask import Flask, jsonify
import threading
import requests
import time
import logging
import signal
import sys
import os
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, redirect

from bmp_reader import BME680Reader
from config import settings
from logger import setup_logging
import google_service

# Initialize Logging
setup_logging()
logger = logging.getLogger(__name__)

# Backend API Application
app = Flask(__name__)

# Application State
class AppState:
    def __init__(self):
        self.explanation: str = "No explanation received from n8n yet."
        self.reader: Optional[BME680Reader] = None
        self.running: bool = True

state = AppState()

def n8n_sender_thread():
    """Background thread to send data to n8n."""
    logger.info("Starting n8n sender thread")
    while state.running:
        webhook_url = settings.n8n_webhook_url
        
        if state.reader and state.reader.latest_data and webhook_url:
            try:
                response = requests.post(webhook_url, json=state.reader.latest_data, timeout=5)
                if response.status_code == 200:
                    state.explanation = response.json().get("explanation", "No explanation field in n8n response.")
                else:
                    state.explanation = f"Error from n8n: {response.status_code}"
                    logger.warning(f"n8n error: {response.status_code}", extra={"status": response.status_code})
            except requests.exceptions.RequestException as e:
                state.explanation = f"Could not connect to n8n: {e}"
                logger.error(f"n8n connection failed: {e}")
        
        # Sleep for a bit, but check running status frequently
        for _ in range(50):  # 5 seconds total (50 * 0.1)
            if not state.running:
                break
            time.sleep(0.1)
    logger.info("n8n sender thread stopped")

def signal_handler(sig, frame):
    """Graceful shutdown handler."""
    logger.info("Shutdown signal received")
    state.running = False
    if state.reader:
        state.reader.stop()
    sys.exit(0)

@app.route('/api/data')
def api_data():
    if not state.reader:
         return jsonify({"error": "Sensor not initialized"}), 503
         
    data = state.reader.latest_data.copy()
    data['explanation'] = state.explanation
    return jsonify(data)

@app.route('/api/history')
def api_history():
    if not state.reader:
        return jsonify({"error": "Sensor not initialized"}), 503
    
    # Return a list of all historical readings
    return jsonify(list(state.reader.history_buffer))

@app.route('/api/calendar')
def api_calendar():
    events = google_service.fetch_events()
    return jsonify(events)

@app.route('/api/auth/google')
def google_auth():
    # Construct the host URL dynamically or from settings
    host_url = request.url_root.rstrip('/')
    auth_url, error = google_service.get_auth_url(host_url)
    if error:
        return jsonify({"error": error}), 500
    return redirect(auth_url)

@app.route('/api/auth/callback')
def google_auth_callback():
    code = request.args.get('code')
    if not code:
        return "Error: No code provided", 400
        
    host_url = request.url_root.rstrip('/')
    success, message = google_service.handle_auth_callback(code, host_url)
    
    if success:
        return redirect('/') # Redirect back to dashboard
    else:
        return f"Authentication Failed: {message}", 500

def start_app():
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initialize Sensor
    state.reader = BME680Reader()
    
    # Start Sensor Thread
    sensor_thread = threading.Thread(target=state.reader.run, name="SensorThread")
    sensor_thread.daemon = True # Still daemon so it dies if main thread dies hard, but we use stop_event too
    sensor_thread.start()

    # Start N8N Thread
    n8n_thread = threading.Thread(target=n8n_sender_thread, name="N8NThread")
    n8n_thread.daemon = True
    n8n_thread.start()
    
    logger.info("Application started (API Only)", extra={
        "n8n_enabled": bool(settings.n8n_webhook_url)
    })

    # Run Flask
    app.run(host='0.0.0.0', port=5000, use_reloader=False) 
    # use_reloader=False is important when using threads + signals in dev

if __name__ == '__main__':
    start_app()