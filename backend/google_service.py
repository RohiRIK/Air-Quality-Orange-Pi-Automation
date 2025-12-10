import os
import logging
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from config import settings

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json' # User must provide this

def get_credentials():
    creds = None
    # Load existing token
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            logger.error(f"Error loading token: {e}")

    # Refresh if expired
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Save the refreshed credentials
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            creds = None

    return creds

def get_auth_url(host_url):
    """Generates the Google Login URL."""
    if not os.path.exists(CREDENTIALS_FILE):
        return None, "credentials.json not found"

    try:
        # Determine redirect URI dynamically based on request host
        # If running in Docker/Reverse Proxy, this might need adjustment in settings
        redirect_uri = f"{host_url}/api/auth/callback"
        
        flow = Flow.from_client_secrets_file(
            CREDENTIALS_FILE,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        
        auth_url, _ = flow.authorization_url(prompt='consent')
        return auth_url, None
    except Exception as e:
        logger.error(f"Error generating auth URL: {e}")
        return None, str(e)

def handle_auth_callback(code, host_url):
    """Exchanges code for token."""
    try:
        redirect_uri = f"{host_url}/api/auth/callback"
        
        flow = Flow.from_client_secrets_file(
            CREDENTIALS_FILE,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        flow.fetch_token(code=code)
        creds = flow.credentials
        
        # Save credentials
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            
        return True, "Successfully authenticated"
    except Exception as e:
        logger.error(f"Auth callback failed: {e}")
        return False, str(e)

def fetch_events():
    """Fetches upcoming events from the primary calendar."""
    creds = get_credentials()
    if not creds:
        return []

    try:
        service = build('calendar', 'v3', credentials=creds)
        
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=now,
            maxResults=20, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        formatted_events = []
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            
            # Parse start time for UI friendly format
            # RFC3339 format: 2025-12-10T10:00:00+02:00
            time_str = "All Day"
            is_all_day = False
            
            if 'T' in start:
                dt = datetime.datetime.fromisoformat(start)
                time_str = dt.strftime("%H:%M")
                date_str = dt.date().isoformat()
            else:
                is_all_day = True
                date_str = start # It's already YYYY-MM-DD
            
            formatted_events.append({
                "id": event['id'],
                "title": event.get('summary', 'No Title'),
                "date": date_str,
                "time": time_str,
                "type": "meeting" # We could infer type from colorId if needed
            })
            
        return formatted_events
        
    except Exception as e:
        logger.error(f"Google API Error: {e}")
        return []
