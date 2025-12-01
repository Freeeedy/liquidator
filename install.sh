#!/bin/bash
echo "[+] Updating system..."
sudo apt update -y
sudo apt upgrade -y

echo "[+] Installing dependencies..."
sudo apt install -y python3 python3-pip ffmpeg exiftool calibre git

echo "[+] Installing mat2..."
sudo apt install -y mat2

echo "[+] All dependencies installed successfully!"
echo "[+] You can now run the tool using: python3 liquidator.py"