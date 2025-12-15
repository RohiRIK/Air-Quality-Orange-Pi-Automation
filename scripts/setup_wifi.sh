#!/bin/bash

# setup_wifi.sh
# Interactive Wi-Fi setup for Orange Pi using NetworkManager (nmcli)

# Ensure running as root
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root (sudo ./setup_wifi.sh)"
  exit 1
fi

# Check if nmcli is installed
if ! command -v nmcli &> /dev/null; then
    echo "Error: nmcli (NetworkManager) is not installed."
    echo "Try installing it: sudo apt-get install network-manager"
    exit 1
fi

echo "=================================="
echo "   Orange Pi Wi-Fi Setup Tool"
echo "=================================="

# 1. Enable Wi-Fi if not already
echo "Enabling Wi-Fi..."
nmcli radio wifi on
sleep 2

# 2. Rescan
echo "Scanning for networks..."
nmcli device wifi rescan
sleep 3

# 3. List Networks
echo "Available Networks:"
echo "----------------------------------"
# format: SSID, SIGNAL, SECURITY
nmcli -f SSID,SIGNAL,SECURITY device wifi list
echo "----------------------------------"

# 4. Prompt for SSID
echo ""
read -p "Enter the SSID (Name) of the network you want to connect to: " SSID_NAME

if [ -z "$SSID_NAME" ]; then
    echo "Error: SSID cannot be empty."
    exit 1
fi

# 5. Prompt for Password
echo ""
read -s -p "Enter Wi-Fi Password: " WIFI_PASS
echo ""

# 6. Connect
echo "Connecting to '$SSID_NAME'..."
if nmcli device wifi connect "$SSID_NAME" password "$WIFI_PASS"; then
    echo "----------------------------------"
    echo "SUCCESS: Connected to $SSID_NAME"
    echo "----------------------------------"
    
    # Show IP info
    echo "Current IP Configuration:"
    ip addr show wlan0 | grep "inet " | awk '{print $2}'
else
    echo "----------------------------------"
    echo "FAILED: Could not connect. Check password and try again."
    echo "----------------------------------"
fi
