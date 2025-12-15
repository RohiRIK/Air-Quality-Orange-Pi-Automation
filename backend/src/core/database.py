import sqlite3
import logging
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from src.core.config import settings

logger = logging.getLogger(__name__)

DB_PATH = "sensors.db"

class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initialize the database schema."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Table: sensors
                # Tracks known devices, their friendly names, and last active time.
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sensors (
                        device_id TEXT PRIMARY KEY,
                        name TEXT,
                        last_seen TIMESTAMP,
                        is_active BOOLEAN DEFAULT 1
                    )
                """)

                # Table: readings
                # Stores historical sensor data.
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS readings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        device_id TEXT,
                        timestamp TIMESTAMP,
                        temperature_c REAL,
                        pressure_hpa REAL,
                        humidity_rh REAL,
                        gas_ohms REAL,
                        air_quality_score REAL,
                        FOREIGN KEY(device_id) REFERENCES sensors(device_id)
                    )
                """)
                
                conn.commit()
                logger.info("Database initialized successfully.")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")

    def upsert_sensor(self, device_id: str, name: Optional[str] = None):
        """Register a new sensor or update its last_seen timestamp."""
        now = datetime.now(timezone.utc).isoformat()
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Check if exists to preserve name if not provided
                cursor.execute("SELECT name FROM sensors WHERE device_id = ?", (device_id,))
                row = cursor.fetchone()
                
                current_name = row['name'] if row else (name or device_id)
                if name: # If specific name update requested
                    current_name = name

                cursor.execute("""
                    INSERT INTO sensors (device_id, name, last_seen, is_active)
                    VALUES (?, ?, ?, 1)
                    ON CONFLICT(device_id) DO UPDATE SET
                        last_seen = ?,
                        is_active = 1,
                        name = CASE WHEN ? IS NOT NULL THEN ? ELSE name END
                """, (device_id, current_name, now, now, name, name))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to upsert sensor {device_id}: {e}")

    def add_reading(self, data: Dict[str, Any]):
        """Insert a new sensor reading."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO readings (device_id, timestamp, temperature_c, pressure_hpa, humidity_rh, gas_ohms, air_quality_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    data['device_id'],
                    data.get('timestamp') or datetime.now(timezone.utc).isoformat(),
                    data.get('temperature_c'),
                    data.get('pressure_hpa'),
                    data.get('humidity_rh'),
                    data.get('gas_ohms'),
                    data.get('air_quality_score')
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to save reading for {data.get('device_id')}: {e}")

    def get_active_sensors(self, threshold_minutes: int = 10) -> List[Dict]:
        """Get list of sensors active within the threshold."""
        # Note: SQLite handling of timediffs can be tricky, doing filtering in Python for robust parsing
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM sensors WHERE is_active = 1")
                rows = cursor.fetchall()
                
                active = []
                now = datetime.now(timezone.utc)
                for row in rows:
                    last_seen_str = row['last_seen']
                    try:
                        # Handle potential mixed formats if any
                        last_seen = datetime.fromisoformat(last_seen_str)
                        if last_seen.tzinfo is None:
                            last_seen = last_seen.replace(tzinfo=timezone.utc)
                            
                        diff = (now - last_seen).total_seconds() / 60
                        if diff <= threshold_minutes:
                            active.append(dict(row))
                    except Exception as e:
                        logger.warning(f"Error parsing date for sensor {row['device_id']}: {e}")
                        
                return active
        except Exception as e:
            logger.error(f"Failed to get active sensors: {e}")
            return []

    def get_latest_readings(self, device_ids: List[str]) -> Dict[str, Dict]:
        """Get the most recent reading for specific devices."""
        if not device_ids:
            return {}
            
        placeholders = ','.join(['?'] * len(device_ids))
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Efficient query to get latest per group
                query = f"""
                    SELECT r.* 
                    FROM readings r
                    INNER JOIN (
                        SELECT device_id, MAX(timestamp) as max_ts
                        FROM readings
                        WHERE device_id IN ({placeholders})
                        GROUP BY device_id
                    ) latest ON r.device_id = latest.device_id AND r.timestamp = latest.max_ts
                """
                cursor.execute(query, device_ids)
                rows = cursor.fetchall()
                return {row['device_id']: dict(row) for row in rows}
        except Exception as e:
            logger.error(f"Failed to get latest readings: {e}")
            return {}

# Singleton instance
db = Database()
