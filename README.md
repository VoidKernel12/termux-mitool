unlock

A fast, lightweight, and user-friendly Termux toolkit designed to manage Xiaomi devices directly from your Android terminal.

---
## 🛠️ Requirements & Important Commands

### Prerequisites & Setup
- **Supported OS:** Android (via Termux app)
- **OTG Cable:** Required for connecting phone in Fastboot mode.
- **Official Apps Download:**
  - Download [Termux](https://termux.dev)
  - Download [Termux:API](https://wiki.termux.com/wiki/Termux:API)


 ## main permission install 
```bash
pkg install termux-tools -y
```
```bash
pkg install which -y
```
## 📥 Installation & Execution
Open your **Termux** application and execute the following commands step by step:

### Step 1: Setup Storage & Update Packages
```bash
termux-setup-storage
```
## tool clone git
```bash
git clone https://github.com/VoidKernel12/termux-mitool.git
```
## create folder
```bash
cd termux-mitool
```
## permission allowed tool 
```bash
chmod +x install.sh
```
```bash
./install.sh
```

# OTG USB Permission & Termux:API Setup Guide

Termux runs inside a strict Android sandbox environment, meaning it cannot directly access hardware ports or scan USB devices without explicit system authorization. To bypass this restriction and establish an OTG hardware connection for fastboot commands, you must use the Termux:API bridge.

### Required Prerequisites & Installation

1. Install both Termux and the official Termux:API companion app from the same source (such as F-Droid or GitHub) so their application signatures match.
2. Open Termux and run the following command to update packages and install the necessary API package:
```bash
pkg update && pkg upgrade -y
```
```bash
pkg install termux-api -y
```
### USB Permission Trigger Commands

Connect your target device via an OTG cable, then execute the following commands in sequence to trigger the native Android USB permission popup:

1. List the connected USB devices to locate your target device's address path:
```bash
termux-usb -l
```
2. Request direct hardware access using the specific custom path you found from the first command:
```bash
termux-usb -r /dev/bus/usb/001/001
```
3. Alternatively, if your system or environment automatically matches the default or standard connected device path, you can directly run the request command without modifying the path:
```bash
termux-usb -r PUT_YOUR_FOUND_PATH_HERE
```
Note: A native Android permission dialog box will instantly appear on your screen. Tap OK to grant Termux sandbox bypass access to the USB port
## Run tool
```bash
python tool.py
```


# 🌟 Credits & Official Project Port
VoidKernel12/termux-mitool.git
