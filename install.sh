#!/bin/bash

echo "[+] Updating system..."
sudo apt update -y
sudo apt upgrade -y

echo "[+] Installing system dependencies..."
sudo apt install -y \
    python3 \
    python3-pip \
    ffmpeg \
    exiftool \
    calibre \
    git \
    mat2 \
    libreoffice \
    ghostscript

echo "[+] Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install opencv-python mediapipe

echo "[+] All dependencies installed successfully!"
echo "[+] You can now run the tool using: python3 liquidator.py"