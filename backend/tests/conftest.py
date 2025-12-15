import pytest
import sys
from unittest import mock

# Mock hardware dependencies BEFORE importing app logic
sys.modules["board"] = mock.MagicMock()
sys.modules["busio"] = mock.MagicMock()
sys.modules["adafruit_bme680"] = mock.MagicMock()
sys.modules["adafruit_blinka"] = mock.MagicMock()

from src.app import create_app
from src.core.database import db

@pytest.fixture
def app():
    import tempfile
    import os
    
    # Create a temp file for the DB
    fd, temp_db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd) # Close the file descriptor, we just need the path

    # Patch the DB path
    with mock.patch("src.core.database.DB_PATH", temp_db_path):
        # Re-initialize the global db instance with the new path
        db.__init__(temp_db_path)
        
        app = create_app()
        app.config.update({
            "TESTING": True,
        })
        yield app
        
    # Cleanup
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)

@pytest.fixture
def client(app):
    return app.test_client()