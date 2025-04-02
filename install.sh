#!/bin/bash

USERNAME=$(whoami)

# Stop digilinux if already running
systemctl --user stop digilinux 2>/dev/null || true

echo "Creating digilinux directory"
mkdir -p /home/$USERNAME/digilinux
cp -r * /home/$USERNAME/digilinux/

echo "Setting up systemd service"
mkdir -p /home/$USERNAME/.config/systemd/user/
sed "s/{{USERNAME}}/$USERNAME/" digilinux.service | sudo tee /home/$USERNAME/.config/systemd/user/digilinux.service >/dev/null

# Reload systemd services
systemctl --user daemon-reload

echo "Enabling digilinux service"
systemctl --user enable digilinux

echo "Starting digilinux service"
systemctl --user start digilinux

# Check digilinux service
systemctl --user status digilinux

echo "Digital Wellbeing for Linux is installed and running."
