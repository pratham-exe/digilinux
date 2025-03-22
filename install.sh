#!/bin/bash

USERNAME=$(whoami)

# Stop digilinux if already running
sudo systemctl stop digilinux 2>/dev/null || true

echo "Creating /opt/digilinux directory"
sudo mkdir -p /opt/digilinux
sudo cp -r * /opt/digilinux/

echo "Setting up systemd service"
sed "s/{{USERNAME}}/$USERNAME/" digilinux.service | sudo tee /etc/systemd/system/digilinux.service >/dev/null

# Reload systemd services
sudo systemctl daemon-reload

echo "Enabling digilinux service"
sudo systemctl enable digilinux

echo "Starting digilinux service"
sudo systemctl start digilinux

# Check digilinux service
sudo systemctl status digilinux

echo "Digital Wellbeing for Linux is installed and running."
