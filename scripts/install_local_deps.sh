#!/bin/bash
# This script installs the necessary dependencies for running the Air Quality Orange Pi Automation project locally (without Docker).
# It should be run on the Orange Pi with sudo privileges.

# Define log file path and name
LOG_DIR="/var/log"
LOG_FILE="${LOG_DIR}/air_quality_install_$(date +%Y%m%d_%H%M%S).log"

# Ensure log directory exists
sudo mkdir -p "$LOG_DIR"
sudo touch "$LOG_FILE"
sudo chmod 644 "$LOG_FILE"

# Function to log messages to console and file
log_message() {
    echo "$@" | sudo tee -a "$LOG_FILE"
}

log_message "========================================="
log_message "Starting local dependency installation on $(date)"
log_message "Log file: $LOG_FILE"
log_message "========================================="

# Update package lists
log_message "Updating package lists..."
sudo apt-get update -y | sudo tee -a "$LOG_FILE"

# Install system packages
log_message "Installing python3-pip and i2c-tools..."
sudo apt-get install -y python3-pip i2c-tools | sudo tee -a "$LOG_FILE"

# Install Python libraries using pip3
log_message "Installing Python libraries from requirements.txt..."
sudo pip3 install -r ../requirements.txt | sudo tee -a "$LOG_FILE"

# --- I2C Enablement Check and Modification ---
I2C_CONFIG_FILE="/boot/armbianEnv.txt"
I2C_OVERLAY="overlays=i2c0"

log_message "Checking I2C configuration in $I2C_CONFIG_FILE..."

if grep -q "^overlays=.*i2c0" "$I2C_CONFIG_FILE"; then
    log_message "I2C overlay 'i2c0' already present in $I2C_CONFIG_FILE."
elif grep -q "^overlays=" "$I2C_CONFIG_FILE"; then
    # overlays line exists, append i2c0
    sudo sed -i "s/^overlays=\(.*\)/overlays=\1 i2c0/" "$I2C_CONFIG_FILE"
    log_message "Added 'i2c0' to existing overlays in $I2C_CONFIG_FILE."
else
    # overlays line does not exist, add it
    echo "$I2C_OVERLAY" | sudo tee -a "$I2C_CONFIG_FILE" > /dev/null
    log_message "Added new line '$I2C_OVERLAY' to $I2C_CONFIG_FILE."
fi

log_message "========================================="
log_message "Local dependency installation finished on $(date)"
log_message "========================================="

log_message "IMPORTANT: A reboot is required for I2C changes to take effect."
log_message "Please reboot your Orange Pi now: sudo reboot"
