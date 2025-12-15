from flask import Blueprint, jsonify, request, redirect
from src.state import state
import src.services.google as google_service

api_bp = Blueprint('api', __name__)

@api_bp.route('/data')
def api_data():
    if not state.reader:
         return jsonify({"error": "Sensor not initialized"}), 503
         
    data = state.reader.latest_data.copy()
    data['explanation'] = state.explanation
    return jsonify(data)

@api_bp.route('/history')
def api_history():
    if not state.reader:
        return jsonify({"error": "Sensor not initialized"}), 503
    
    # Return a list of all historical readings
    return jsonify(list(state.reader.history_buffer))

@api_bp.route('/calendar')
def api_calendar():
    events = google_service.fetch_events()
    return jsonify(events)

@api_bp.route('/auth/google')
def google_auth():
    # Construct the host URL dynamically or from settings
    host_url = request.url_root.rstrip('/')
    auth_url, error = google_service.get_auth_url(host_url)
    if error:
        return jsonify({"error": error}), 500
    return redirect(auth_url)

@api_bp.route('/auth/callback')
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
