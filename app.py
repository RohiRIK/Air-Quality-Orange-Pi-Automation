from flask import Flask, jsonify, render_template
import threading
import os
import requests
import time
from bmp_reader import BME680Reader

app = Flask(__name__)

# Global variable to store the latest explanation from n8n
explanation = "No explanation received from n8n yet."

# Create an instance of the sensor reader
reader = BME680Reader(read_interval=2.0)

def get_n8n_webhook_url():
    """
    Gets the n8n webhook URL based on environment variables.
    Priority: TEST > PROD
    """
    test_url = os.getenv("N8N_WEBHOOK_URL_TEST")
    if test_url:
        return test_url
    
    prod_url = os.getenv("N8N_WEBHOOK_URL_PROD")
    if prod_url:
        return prod_url
        
    return None

def sensor_and_n8n_thread():
    global explanation
    n8n_webhook_url = get_n8n_webhook_url()

    # Start the sensor reading loop in the reader instance
    sensor_thread = threading.Thread(target=reader.run)
    sensor_thread.daemon = True
    sensor_thread.start()

    while not reader.stop_event:
        if reader.latest_data and n8n_webhook_url:
            try:
                response = requests.post(n8n_webhook_url, json=reader.latest_data)
                if response.status_code == 200:
                    explanation = response.json().get("explanation", "No explanation field in n8n response.")
                else:
                    explanation = f"Error from n8n: {response.status_code}"
            except requests.exceptions.RequestException as e:
                explanation = f"Could not connect to n8n: {e}"
        
        time.sleep(5) # Send data to n8n every 5 seconds

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def api_data():
    data = reader.latest_data.copy()
    data['explanation'] = explanation
    return jsonify(data)

if __name__ == '__main__':
    # Start the background thread for sensor reading and n8n communication
    background_thread = threading.Thread(target=sensor_and_n8n_thread)
    background_thread.daemon = True
    background_thread.start()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
