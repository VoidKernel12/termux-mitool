#!/bin/bash
# SMART XIAOMI TERMUX TOOLKIT - Installer
# For educational & own device repair only

echo "[*] Updating Termux..."
pkg update -y && pkg upgrade -y

echo "[*] Installing dependencies..."
pkg install python android-tools git -y

echo "[*] Checking tool.py..."
if [ -f "tool.py" ]; then
    chmod +x tool.py
    echo ""
    echo "=================================="
    echo "  INSTALLATION SUCCESSFUL! "
    echo "=================================="
    echo "Run with: python tool.py"
else
    echo "[-] Error: tool.py not found!"
    echo "Make sure install.sh and tool.py are in same folder."
    exit 1
fi