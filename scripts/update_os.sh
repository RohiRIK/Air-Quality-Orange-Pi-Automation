#!/bin/bash
# This script automates OS package updates.
# It should be run with sudo or as root.

echo "========================================="
echo "Starting OS update on $(date)"
echo "========================================="

# Fetch the latest package lists
apt-get update

# Upgrade all installed packages without interactive prompts
apt-get upgrade -y

# Remove packages that are no longer required
apt-get autoremove -y

# Clean up the local repository of retrieved package files
apt-get clean

echo "========================================="
echo "OS update finished on $(date)"
echo "========================================="