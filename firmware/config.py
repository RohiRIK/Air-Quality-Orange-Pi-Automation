# Configuration for ESP32-C3 Air Quality Node

# Wi-Fi Settings
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASS = "YOUR_WIFI_PASSWORD"

# Hub Settings (Orange Pi)
HUB_IP = "192.168.1.XXX" # IP of your Orange Pi
HUB_PORT = 80
HUB_URL = f"http://{HUB_IP}:{HUB_PORT}/api/ingest"

# Device Settings
DEVICE_ID = "esp32_c3_01" # Unique ID for this node
READ_INTERVAL = 60 # Seconds between readings
