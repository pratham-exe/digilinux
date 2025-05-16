#!/bin/bash

USERNAME=$(whoami)

# Stop digilinux if already running
systemctl --user stop digilinux 2>/dev/null || true

echo "Creating digilinux directory"
sudo mkdir -p /home/$USERNAME/digilinux
sudo cp -r * /home/$USERNAME/digilinux/

echo "Setting up systemd service"
mkdir -p /home/$USERNAME/.config/systemd/user
sudo cp ./digilinux.service ./digilinux-restart.timer ./digilinux-restart.service /home/$USERNAME/.config/systemd/user/

# Reload systemd services
systemctl --user daemon-reload

echo "Enabling digilinux service"
systemctl --user enable digilinux.service
systemctl --user enable digilinux-restart.timer

echo "Starting digilinux service"
systemctl --user start digilinux.service
systemctl --user start digilinux-restart.timer

# Check digilinux service
systemctl --user status digilinux

echo "Digital Wellbeing for Hyprland is installed and running."
