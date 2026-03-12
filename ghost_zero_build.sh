#!/bin/bash
# ghost_zero_build.sh - Kali Linux One-Click Setup

echo "🐉 Ghost-Zero Kali Framework - Installing..."

# Kali dependencies
sudo apt update
sudo apt install -y gcc python3 python3-pip chromium-driver

# Python deps
pip3 install selenium requests

# Clean WebP template (legitimate image)
wget -O clean.webp "https://example.com/sample.webp" || \
echo -e "RIFF$\0\0VP8L\0\0\0\x40\0\0\0" > clean.webp

# Build C payload generator
gcc payload.c -o payload_gen -static

# Create targets file
echo "# Target phone numbers" > targets.txt
echo "# +1234567890" >> targets.txt

chmod +x binder.py
echo "✅ Framework ready!"
echo "Usage: python3 binder.py +1234567890"
