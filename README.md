# 🚛 AI FLEET – Intelligent Driver & Cargo Monitoring System

AI Fleet is a real-time multi-camera vehicle safety and tracking system.

It combines:

- 🧠 AI-based Driver Monitoring (Drowsiness, Yawning, Phone Usage, Distraction)
- 📦 Cargo Security Monitoring
- 🛣 Road Object Detection
- 📍 GPS Tracking with Geofencing
- 🚨 Overspeed Detection
- 📲 Telegram + SMS Alerts
- 🌐 Live Web Dashboard

This system is designed for fleet vehicles, logistics trucks, and safety monitoring deployments.

---

# 🧩 SYSTEM ARCHITECTURE

The system runs 3 parallel modules:

1. **Road Camera Module**
   - Detects vehicles/objects using YOLOv8

2. **Driver/Cargo Camera Module (Switchable Mode)**
   - Driver Mode → Drowsiness, yawning, distraction, phone detection
   - Cargo Mode → Object detection + unauthorized hand detection

3. **GPS + SIM7600 Module**
   - Reads GPS coordinates
   - Checks geofence boundary
   - Monitors speed
   - Sends alerts

All modules stream to a live Flask web dashboard.

---

# 🛠 HARDWARE REQUIREMENTS

## Minimum Required:

| Component | Purpose |
|-----------|---------|
| PC / Laptop (i5 or better) OR Jetson Nano/Xavier | Main processing |
| 2–3 USB Cameras | Road + Driver + Cargo |
| SIM7600 4G LTE Module | GPS + SMS |
| Active SIM Card | SMS + Network |
| USB Cables | Connections |

Optional:
- GPU for faster YOLO inference
- Jetson device for edge deployment

---

# 💻 SOFTWARE REQUIREMENTS

- Python 3.9 – 3.11
- Ubuntu / Windows
- Internet connection (for Telegram alerts)

---

# 📦 STEP 1 – INSTALL PYTHON

Download Python from:
https://www.python.org/downloads/

During installation:
✔ Check “Add Python to PATH”

Verify installation:
```
python --version
```

---

# 📦 STEP 2 – CREATE PROJECT FOLDER

Create a folder:
```
AI_FLEET
```

Inside it, place:
- Your main Python script
- `yolov8n.pt` model file

Download YOLO model from:
https://github.com/ultralytics/ultralytics

---

# 📦 STEP 3 – INSTALL DEPENDENCIES

Open terminal inside project folder:

```
pip install ultralytics
pip install opencv-python
pip install mediapipe
pip install flask
pip install pyserial
pip install requests
pip install numpy
pip install turbojpeg
```

If TurboJPEG fails:
```
pip install PyTurboJPEG
```

---

# 📦 STEP 4 – TELEGRAM BOT SETUP

1. Open Telegram
2. Search: @BotFather
3. Create a new bot
4. Copy the Bot Token

Edit this line in the code:

```
TELEGRAM_URL = "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage"
```

Replace `<YOUR_BOT_TOKEN>`.

Then get your Chat ID:
- Open this link:
  ```
  https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
  ```
- Send a message to your bot first.
- Copy your chat_id.

Replace:
```
CHAT_ID = "<CHAT_ID>"
```

---

# 📦 STEP 5 – SMS SETUP (SIM7600)

Insert SIM card into SIM7600 module.

Connect module to PC via USB.

Replace:
```
SMS_NUMBER = "<PHONE>"
```

Use format:
```
+919XXXXXXXXX
```

Ensure drivers are installed for SIM7600.

On Linux check:
```
ls /dev/ttyUSB*
```

On Windows check:
Device Manager → COM Ports

---

# 📦 STEP 6 – CONFIGURE GEOFENCE

Edit:

```
GEOFENCE_LAT = 13.2866
GEOFENCE_LON = 77.5953
GEOFENCE_RADIUS_KM = 0.5
```

Use Google Maps to find coordinates.

---

# 📦 STEP 7 – RUN THE SYSTEM

In terminal:

```
python your_script_name.py
```

If successful, you will see Flask running.

Open browser:
```
http://localhost:5000
```

---

# 🌐 DASHBOARD FEATURES

- Live Road Camera Feed
- Live Driver/Cargo Feed
- Switch Modes:
  - Driver Mode
  - Cargo Mode

Click:
```
/set/driver
```
or
```
/set/cargo
```

---

# 🧠 DRIVER MODE FEATURES

Detects:

- Eye closure (Drowsiness)
- Yawning
- Looking away
- Mobile phone usage
- Overspeeding
- Geofence breach

Alerts sent via:
- Telegram
- SMS

---

# 📦 CARGO MODE FEATURES

Detects:

- Object presence
- Unauthorized hand access

Alerts sent instantly.

---

# 📍 GPS FEATURES

Every 5 seconds:

- Reads GPS location
- Logs coordinates
- Checks geofence
- Checks speed
- Sends alert if:
  - Outside geofence
  - Overspeeding

---

# 📁 LOG FILE

File created:
```
ai_fleet_log.csv
```

Contains:
- Timestamp
- Module
- Event
- Message

---

# 🚨 ALERT SYSTEM

Alert cooldown = 10 seconds

Prevents spamming.

Triggered by:
- Drowsiness
- Yawning
- Looking away
- Phone detection
- Unauthorized cargo access
- Geofence breach
- Overspeed

---

# 🔄 CAMERA CONFIGURATION

Edit camera indices:

```
DRIVER_CAM = 0
ROAD_CAM   = 1
CARGO_CAM  = 2
```

If camera not detected:
Change numbers until correct.

Test cameras using:
```
python -m cv2
```

---

# ⚡ PERFORMANCE TIPS

If system is slow:

- Reduce FPS:
  ```
  DRIVER_FPS = 10
  ROAD_FPS = 8
  ```

- Use smaller YOLO model:
  ```
  yolov8n.pt
  ```

- Use GPU if available

---

# 🧪 TESTING CHECKLIST

✔ Cameras detected  
✔ GPS returning data  
✔ SMS sending  
✔ Telegram alerts working  
✔ Dashboard loading  
✔ Log file generating  

---

# 🛡 SECURITY NOTES

- Do not expose Telegram token publicly
- Do not push SIM credentials to GitHub
- Use environment variables in production

---

# 🚀 DEPLOYMENT OPTIONS

You can deploy on:

- Laptop (Development)
- Jetson Nano (Edge)
- Xavier NX (Industrial)
- Industrial PC inside vehicle

---

# 📌 USE CASES

- Fleet Safety Monitoring
- Logistics Tracking
- Cold Chain Transport
- Smart Agriculture Transport
- Government Fleet Monitoring

---

# ⚠ TROUBLESHOOTING

If camera fails:
- Check USB ports
- Reduce resolution
- Restart system

If SMS fails:
- Check SIM network
- Check signal strength
- Verify COM port

If GPS fails:
- Move near open sky
- Check antenna

If YOLO error:
```
pip install ultralytics --upgrade
```

---

# 👨‍💻 AUTHOR

AI Fleet – Intelligent Monitoring System  
Designed for real-time vehicle safety and tracking deployments.

---

# 📄 LICENSE

For research, academic, and fleet deployment usage.
Modify responsibly.

