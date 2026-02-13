# 🚛 AI Fleet Monitoring System  
### Continuous Road Monitoring + Switchable Driver/Cargo Intelligence  
**Jetson Orin Nano | 3 USB Cameras | SIM7600 LTE + GPS**

---

![Platform](https://img.shields.io/badge/Platform-Jetson%20Orin%20Nano-green)
![OS](https://img.shields.io/badge/OS-Ubuntu%20JetPack-blue)
![AI](https://img.shields.io/badge/AI-YOLOv8%20%2B%20MediaPipe-orange)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

---

## 📌 Overview

The **AI Fleet Monitoring System** is a real-time edge AI platform for intelligent vehicle surveillance and safety monitoring.

It runs entirely on NVIDIA Jetson Orin Nano and provides:

- 🛣 Continuous road object detection
- 👤 Driver drowsiness detection
- 📦 Cargo intrusion monitoring
- 📍 GPS tracking
- 📲 SMS alerts
- 💬 Telegram alerts
- 🌐 Live web dashboard
- 🔁 Driver/Cargo mode switching

All inference runs locally at the edge. No cloud dependency required.

---

## 🏗 System Architecture

```

3x USB Cameras
(Driver | Road | Cargo)
│
▼
Jetson Orin Nano
YOLOv8 + MediaPipe + Flask
│
├── Telegram Alerts
├── SMS Alerts (SIM7600)
└── GPS Logging

````

---

## 🧰 Hardware Requirements

### 1️⃣ Processing Unit
- NVIDIA Jetson Orin Nano (8GB recommended)
- Official 19V power adapter
- Cooling fan (recommended)

### 2️⃣ Cameras (3x USB UVC Cameras)

| Device Path | Role |
|------------|------|
| `/dev/video0` | Driver Camera |
| `/dev/video1` | Road Camera |
| `/dev/video2` | Cargo Camera |

Use UVC-compatible USB webcams.

### 3️⃣ Connectivity Module
SIM7600 USB LTE + GPS Module  
- Active SIM card (SMS enabled)  
- GPS antenna connected  
- USB connection to Jetson  

---

## 🖥 Software Stack

| Component | Purpose |
|-----------|----------|
| Ubuntu (JetPack 5.x / 6.x) | Base OS |
| YOLOv8 | Road object detection |
| MediaPipe | Driver monitoring |
| OpenCV | Video capture |
| Flask | Web dashboard |
| PySerial | SIM7600 communication |
| Requests | Telegram API |
| CSV logging | Event storage |

---

## ⚙️ Installation

### Update System

```bash
sudo apt update
sudo apt upgrade -y
````

### Install Python Dependencies

```bash
pip install ultralytics mediapipe flask opencv-python pyserial requests numpy
```

Optional performance optimization:

```bash
pip install PyTurboJPEG
```

---

## 📷 Camera Verification

```bash
ls /dev/video*
```

Expected:

```
/dev/video0
/dev/video1
/dev/video2
```

Test cameras:

```bash
sudo apt install cheese
cheese
```

---

## 📡 SIM7600 Verification

Check USB ports:

```bash
ls /dev/ttyUSB*
```

Install minicom:

```bash
sudo apt install minicom
```

Test connection:

```bash
minicom -D /dev/ttyUSB2 -b 115200
```

Inside terminal:

```
AT
```

Expected response:

```
OK
```

Enable GPS:

```
AT+CGPS=1
```

---

## 🤖 YOLO Model Setup

### Option 1 – Auto Download

YOLOv8 model downloads automatically on first run.

### Option 2 – Recommended (TensorRT Engine)

```bash
yolo export model=yolov8n.pt format=engine
```

Place `yolov8n.engine` inside project directory.

---

## 💬 Telegram Bot Setup

1. Open Telegram
2. Search for `@BotFather`
3. Run:

```
/newbot
```

4. Copy the Bot Token
5. Send a message to your bot
6. Open:

```
https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
```

7. Copy `chat.id`

---

## 📁 Project Structure

```
ai_fleet/
│
├── ai_fleet.py
├── yolov8n.engine (optional)
├── ai_fleet_log.csv
└── README.md
```

---

## ▶️ Running the System

```bash
cd ai_fleet
python3 ai_fleet.py
```

---

## 🌐 Access Dashboard

Find Jetson IP:

```bash
hostname -I
```

Open in browser:

```
http://<jetson_ip>:5000
```

Dashboard shows:

* Road stream (always active)
* Driver or Cargo stream
* Mode switching controls
* Alert logs

---

## 🔁 System Modes

### 🚗 Road Monitoring

Always active.

### 👤 Driver Mode

* Road + Driver cameras active
* Drowsiness detection enabled

### 📦 Cargo Mode

* Road + Cargo cameras active
* Unauthorized access detection enabled

Switching mode:

* Releases secondary camera
* Activates selected camera
* Road feed continues uninterrupted

---

## 🚨 Alert System

| Event          | Action         |
| -------------- | -------------- |
| Driver Drowsy  | Telegram + SMS |
| Cargo Breach   | Telegram + SMS |
| High Vibration | SMS            |
| Door Open      | SMS            |

Alerts include timestamp and GPS location.

---

## 📍 GPS Logging

Every 5 seconds:

* Reads GPS from SIM7600
* Appends to `ai_fleet_log.csv`

Format:

```
timestamp,module,submodule,message
```

---

## 🔄 Auto Start on Boot (Optional)

Create service file:

```bash
sudo nano /etc/systemd/system/ai_fleet.service
```

Paste:

```
[Unit]
Description=AI Fleet System
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/<username>/ai_fleet/ai_fleet.py
WorkingDirectory=/home/<username>/ai_fleet
Restart=always
User=<username>

[Install]
WantedBy=multi-user.target
```

Enable service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai_fleet
sudo systemctl start ai_fleet
```

---

## 📊 Performance Recommendations

* Resolution: 640x480 for stable FPS
* Use TensorRT engine for faster inference
* Ensure active cooling
* Use powered USB hub if running 3 cameras

---

## 🛠 Troubleshooting

Camera not detected:

```bash
ls /dev/video*
```

SIM not detected:

```bash
ls /dev/ttyUSB*
```

GPS not locking:

```
AT+CGPS=1
```

Low FPS:
Reduce resolution inside script.

---

## 🎯 System Capabilities

* Continuous road monitoring
* Driver fatigue detection
* Cargo security detection
* GPS tracking
* SMS alerting
* Telegram alerting
* Live dashboard
* Fully edge-based AI inference

---

## 📜 License

Specify your license here (MIT / Apache 2.0 / Research Use Only).

---

## 👨‍🔬 Project Category

Edge AI Deployment
Embedded Systems
Fleet Safety & IoT Integration

```

---

You now have a clean, professional, GitHub-ready single file.

If you want next-level polish, I can generate:
- 📊 Performance benchmark section
- 🧠 AI model details section
- 🧪 Testing methodology
- 📦 Docker deployment version
- 📈 Architecture diagram in Mermaid

Your repo is now publication-grade. 🚛
```
