#!/bin/bash

echo "[+] Updating system..."
sudo apt update -y
sudo apt upgrade -y

echo "[+] Installing system dependencies..."
sudo apt install -y python3 python3-pip ffmpeg exiftool calibre git

echo "[+] Installing mat2..."
sudo apt install -y mat2

echo "[+] Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install opencv-python

echo "[+] Cleaning up (optional)..."
sudo apt autoremove -y

echo "[+] All dependencies installed successfully!"
echo "[+] You can now run the tool using: python3 liquidator.py"