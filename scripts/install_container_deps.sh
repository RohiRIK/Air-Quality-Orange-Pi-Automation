#!/bin/bash
# This script installs the necessary prerequisites for running the Air Quality Orange Pi Automation project in a containerized environment.
# It also sets up the update_os.sh script as a daily cron job.
# It should be run on the Orange Pi with sudo privileges.

# Define log file path and name
LOG_DIR="/var/log"
LOG_FILE="${LOG_DIR}/air_quality_container_install_$(date +%Y%m%d_%H%M%S).log"

# Ensure log directory exists
sudo mkdir -p "$LOG_DIR"
sudo touch "$LOG_FILE"
sudo chmod 644 "$LOG_FILE"

# Function to log messages to console and file
log_message() {
    echo "$@" | sudo tee -a "$LOG_FILE"
}

log_message "========================================="
log_message "Starting container environment setup on $(date)"
log_message "Log file: $LOG_FILE"
log_message "========================================="

# Update package lists
log_message "Updating package lists..."
sudo apt-get update -y | sudo tee -a "$LOG_FILE"

# Install Docker Engine
log_message "Installing Docker Engine (docker.io)..."
sudo apt-get install -y docker.io | sudo tee -a "$LOG_FILE"
sudo systemctl start docker | sudo tee -a "$LOG_FILE"
sudo systemctl enable docker | sudo tee -a "$LOG_FILE"

# Install Docker Compose v2
log_message "Installing Docker Compose v2..."
sudo apt-get install -y docker-compose-v2 | sudo tee -a "$LOG_FILE"

# Add current user to the docker group to run Docker commands without sudo
CURRENT_USER=$(whoami)
if ! getent group docker | grep -q "\b$CURRENT_USER\b"; then
    log_message "Adding user '$CURRENT_USER' to the 'docker' group..."
    sudo usermod -aG docker "$CURRENT_USER" | sudo tee -a "$LOG_FILE"
    log_message "Please log out and log back in for the group change to take effect."
else
    log_message "User '$CURRENT_USER' is already in the 'docker' group."
fi

# --- Set up update_os.sh as a daily cron job ---
log_message "Setting up update_os.sh as a daily cron job..."
CRON_JOB_PATH="/usr/local/bin/update_os.sh" # Standard path for custom scripts

# Copy update_os.sh to a standard location and make it executable
sudo cp /Users/rohirikman/Library/CloudStorage/OneDrive-OnCloud/Terminal/Projects/Air-Quality-Orange-Pi-Automation/scripts/update_os.sh "$CRON_JOB_PATH" | sudo tee -a "$LOG_FILE"
sudo chmod +x "$CRON_JOB_PATH" | sudo tee -a "$LOG_FILE"

# Add cron job for root user (runs daily at 4 AM)
(sudo crontab -l 2>/dev/null; echo "0 4 * * * $CRON_JOB_PATH") | sudo crontab -
log_message "Cron job added: '0 4 * * * $CRON_JOB_PATH' (runs daily at 4 AM)."

log_message "========================================="
log_message "Container environment setup finished on $(date)"
log_message "========================================="

log_message "IMPORTANT: If you were added to the 'docker' group, you need to log out and log back in for changes to take effect."
log_message "You can then proceed to clone your project and run docker-compose up."
