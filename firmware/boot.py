import network
import time
from config import WIFI_SSID, WIFI_PASS

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_PASS)
        
        # Wait for connection
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)
            
    if wlan.isconnected():
        print('Network config:', wlan.ifconfig())
    else:
        print('Wifi connection failed')

# Connect on boot
connect_wifi()
