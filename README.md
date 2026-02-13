# 🚛 AI Fleet Monitoring System – Final Deployable Version

## Continuous Road Monitoring + Intelligent Driver/Cargo Switching  
Jetson Orin Nano | 3 USB Cameras | SIM7600 LTE + GPS | YOLOv8 | MediaPipe

---

![Platform](https://img.shields.io/badge/Platform-Jetson%20Orin%20Nano-green)
![AI](https://img.shields.io/badge/AI-YOLOv8%20%2B%20MediaPipe-orange)
![GPS](https://img.shields.io/badge/GPS-Geofencing%20%2B%20Speed-blue)
![Alerts](https://img.shields.io/badge/Alerts-Telegram%20%2B%20SMS-red)
![Status](https://img.shields.io/badge/Version-Final%20Deployable-success)

---

# 📌 System Overview

This is the **final production-grade version** of the AI Fleet Monitoring System.

It provides:

- 🛣 Continuous Road Object Detection
- 👤 Driver Drowsiness Detection
- 😴 Yawning Detection (MAR)
- 👀 Driver Attention Monitoring
- 📱 Phone Usage Detection
- 📦 Cargo Intrusion Detection
- ✋ Hand Detection in Cargo Area
- 📍 GPS Live Tracking
- 🚧 Geofencing Alerts
- 🚗 Overspeed Detection
- 📲 SMS Alerts via SIM7600
- 💬 Telegram Alerts
- 🌐 Live Web Dashboard
- ⚡ TurboJPEG Acceleration
- 🔁 Driver/Cargo Mode Switching

All AI runs locally on Jetson. No cloud inference required.

---

# 🧠 System Architecture

```

Driver Cam ─┐
Road Cam   ├── Jetson Orin Nano
Cargo Cam  ┘        │
│
YOLOv8 + MediaPipe + GPS + Geofence
│
├── Telegram Alerts
├── SMS Alerts (SIM7600)
└── Web Dashboard (Flask)

````

---

# 🧰 Hardware Requirements

## 1️⃣ Processing Unit
- NVIDIA Jetson Orin Nano (8GB recommended)
- Official power adapter
- Active cooling

## 2️⃣ Cameras (3x USB UVC)

| Device Path | Role |
|-------------|------|
| `/dev/video0` | Driver Camera |
| `/dev/video1` | Road Camera |
| `/dev/video2` | Cargo Camera |

## 3️⃣ Connectivity Module
SIM7600 USB LTE + GPS Module
- Active SIM (SMS enabled)
- GPS antenna connected

---

# ⚙️ Software Requirements

- Ubuntu (JetPack 5.x / 6.x)
- Python 3.8+
- ultralytics
- mediapipe
- opencv-python
- flask
- pyserial
- requests
- numpy
- turbojpeg (optional)

Install dependencies:

```bash
pip install ultralytics mediapipe flask opencv-python pyserial requests numpy
pip install PyTurboJPEG   # optional performance boost
````

---

# 🚦 Functional Modules

## 🛣 Road Monitoring (Always Active)

* YOLOv8 object detection
* Bounding boxes drawn in real-time
* Runs at fixed FPS

---

## 👤 Driver Monitoring Mode

Detects:

* Eye closure (EAR calculation)
* Drowsiness (frame accumulation logic)
* Yawning (MAR calculation)
* Driver looking away
* Phone usage detection (YOLO class 67)

Alerts triggered:

* DRIVER DROWSY
* DRIVER YAWNING
* DRIVER LOOKING AWAY
* PHONE USAGE

---

## 📦 Cargo Monitoring Mode

Detects:

* Object presence via YOLO
* Hand detection using MediaPipe
* Unauthorized cargo access

Alert triggered:

* UNAUTHORIZED CARGO ACCESS

---

## 📍 GPS Module

Reads from SIM7600:

* Latitude
* Longitude
* Speed (converted to km/h)

Logs to CSV:

```
timestamp,module,submodule,message
```

---

## 🚧 Geofencing

Configured by:

```python
GEOFENCE_LAT
GEOFENCE_LON
GEOFENCE_RADIUS_KM
```

If vehicle exits defined radius:

* GEOFENCE BREACH alert triggered

---

## 🚗 Overspeed Detection

Configured by:

```python
OVERSPEED_LIMIT = 60  # km/h
```

If exceeded:

* OVERSPEEDING alert triggered

---

## 🔁 Mode Switching

Web interface allows switching:

* `/set/driver`
* `/set/cargo`

Road camera remains active.
Secondary camera dynamically restarts with selected mode.

---

# 🌐 Web Dashboard

Access:

```
http://<jetson_ip>:5000
```

Displays:

* Road camera stream
* Secondary camera stream
* Mode switching controls
* Current active mode

---

# 🚨 Alert System

Supports:

* Telegram Alerts
* SMS Alerts via SIM7600
* Cooldown protection (10 seconds default)

Cooldown prevents alert flooding.

---

# 📁 Project Structure

```
ai_fleet/
│
├── ai_fleet.py
├── yolov8n.pt
├── ai_fleet_log.csv
└── README.md
```

---

# ▶️ Running the System

```bash
python3 ai_fleet.py
```

---

# 🔄 Auto Start (Optional)

Create systemd service:

```bash
sudo nano /etc/systemd/system/ai_fleet.service
```

Add:

```
[Unit]
Description=AI Fleet Final System
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/<username>/ai_fleet/ai_fleet.py
WorkingDirectory=/home/<username>/ai_fleet
Restart=always
User=<username>

[Install]
WantedBy=multi-user.target
```

Enable:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai_fleet
sudo systemctl start ai_fleet
```

---

# ⚡ Performance Features

* Threaded camera capture
* Fixed FPS control
* Queue buffering (size=1)
* TurboJPEG acceleration
* Alert cooldown logic
* Non-blocking GPS thread
* Separate AI processing threads

---

# 📊 Logging

All events stored in:

```
ai_fleet_log.csv
```

Includes:

* GPS updates
* Speed logs
* Alert logs
* System events

---

# 🎯 Final Capabilities

✔ Continuous road AI
✔ Driver fatigue intelligence
✔ Cargo intrusion detection
✔ GPS tracking
✔ Geofencing
✔ Overspeed monitoring
✔ SMS + Telegram alerts
✔ Live dashboard
✔ Mode switching
✔ Fully edge-based processing

---

# 🔐 Production Notes

Before deployment:

* Replace `<YOUR_BOT_TOKEN>`
* Replace `<CHAT_ID>`
* Replace `<PHONE>`
* Configure geofence coordinates
* Set overspeed limit
* Confirm camera device order

Now we’re aligned. 🚛
```
