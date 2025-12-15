import requests
import logging
from typing import Dict, Any, Optional
from src.core.config import settings

logger = logging.getLogger(__name__)

def send_to_n8n(data: Dict[str, Any]) -> str:
    """
    Sends sensor data to n8n webhook and returns the explanation.
    Returns None if n8n is not configured or fails.
    """
    webhook_url = settings.n8n_webhook_url
    if not webhook_url:
        return "n8n not configured"

    try:
        # Add metadata source if not present
        payload = data.copy()
        if "source" not in payload:
            payload["source"] = "hub_forwarder"

        response = requests.post(webhook_url, json=payload, timeout=5)
        
        if response.status_code == 200:
            return response.json().get("explanation", "Analysis complete (No text)")
        else:
            logger.warning(f"n8n error: {response.status_code}")
            return f"Error from n8n: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        logger.error(f"n8n connection failed: {e}")
        return f"Could not connect to n8n: {str(e)}"
