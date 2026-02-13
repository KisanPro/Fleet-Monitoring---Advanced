# ================= AI FLEET – FINAL DEPLOYABLE =================
# Road always active - Driver & Cargo switchable
# Fixed FPS + Advanced Driver + GPS + Geofencing + Speed
# ===============================================================

import cv2, time, threading, numpy as np, serial, requests, csv, math
from queue import Queue
from datetime import datetime
from flask import Flask, Response
from ultralytics import YOLO
import mediapipe as mp

# ---------------- CONFIG ----------------

DRIVER_CAM = 0
ROAD_CAM   = 1
CARGO_CAM  = 2

DRIVER_FPS = 12
ROAD_FPS   = 10
CARGO_FPS  = 10

MODEL_PATH = "yolov8n.pt"
CONF_THRES = 0.4

LOG_FILE = "ai_fleet_log.csv"

TELEGRAM_URL = "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage"
CHAT_ID = "<CHAT_ID>"
SMS_NUMBER = "<PHONE>"

MODE = "driver"

OVERSPEED_LIMIT = 60  # km/h
GEOFENCE_LAT = 13.2866
GEOFENCE_LON = 77.5953
GEOFENCE_RADIUS_KM = 0.5

ALERT_COOLDOWN = 10
last_alert_time = {}

# ---------------- LOGGING ----------------

def log_event(module, sub, msg):
    try:
        with open(LOG_FILE, "a", newline="") as f:
            csv.writer(f).writerow([
                datetime.now().isoformat(), module, sub, msg
            ])
    except:
        pass

# ---------------- ALERTS ----------------

def send_telegram(msg):
    try:
        requests.post(TELEGRAM_URL,
                      data={"chat_id": CHAT_ID, "text": msg},
                      timeout=2)
    except:
        pass

def send_alert(msg):
    now = time.time()
    if msg in last_alert_time and now - last_alert_time[msg] < ALERT_COOLDOWN:
        return
    last_alert_time[msg] = now

    send_telegram(msg)
    send_sms(msg)
    log_event("ALERT","SYSTEM",msg)

# ---------------- SIM7600X ----------------

def init_sim7600():
    for p in ["/dev/ttyUSB2","/dev/ttyUSB3","/dev/ttyUSB1","/dev/ttyUSB0"]:
        try:
            return serial.Serial(p,115200,timeout=1)
        except:
            continue
    return None

SIM = init_sim7600()

def send_sms(msg):
    if not SIM: return
    try:
        SIM.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        SIM.write(f'AT+CMGS="{SMS_NUMBER}"\r'.encode())
        time.sleep(0.5)
        SIM.write(msg.encode() + b'\x1A')
    except:
        pass

def read_gps():
    if not SIM: return None
    try:
        SIM.write(b'AT+CGPSINFO\r')
        time.sleep(0.5)
        for l in SIM.readlines():
            l=l.decode(errors="ignore")
            if "," in l:
                return l.strip()
    except:
        pass
    return None

# ---------------- GPS HELPERS ----------------

def parse_nmea(line):
    try:
        parts = line.split(",")
        lat = float(parts[1])
        lon = float(parts[3])
        speed = float(parts[7]) * 1.852
        return lat, lon, speed
    except:
        return None, None, None

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

# ---------------- JPEG ----------------

try:
    from turbojpeg import TurboJPEG
    jpeg = TurboJPEG()
    TURBO = True
except:
    jpeg = None
    TURBO = False

def encode(frame):
    if TURBO:
        try: return jpeg.encode(frame)
        except: pass
    return cv2.imencode(".jpg",frame)[1].tobytes()

# ---------------- CAMERA THREAD ----------------

class Cam(threading.Thread):
    def __init__(self, idx, q, name, fps):
        super().__init__(daemon=True)
        self.idx = idx
        self.q = q
        self.name = name
        self.delay = 1.0/fps
        self.running = True
        self.cap = cv2.VideoCapture(idx)

    def stop(self):
        self.running=False
        if self.cap: self.cap.release()

    def run(self):
        while self.running:
            start=time.time()
            ret,frm=self.cap.read()
            if ret:
                if self.q.full(): self.q.get_nowait()
                self.q.put(frm)
            sleep=self.delay-(time.time()-start)
            if sleep>0: time.sleep(sleep)

# ---------------- AI ----------------

yolo = YOLO(MODEL_PATH)
mp_face = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
mp_hands = mp.solutions.hands.Hands()

def ear(lm, idx):
    p=[lm[i] for i in idx]
    v=np.linalg.norm([p[1].x-p[5].x,p[1].y-p[5].y])
    h=np.linalg.norm([p[0].x-p[3].x,p[0].y-p[3].y])
    return v/h if h else 0

def mar(lm):
    top=lm[13]; bottom=lm[14]
    left=lm[78]; right=lm[308]
    v=abs(top.y-bottom.y)
    h=abs(left.x-right.x)
    return v/h if h else 0

# ---------------- QUEUES ----------------

road_q=Queue(1)
second_q=Queue(1)
road_d=Queue(1)
second_d=Queue(1)

secondary_thread=None

# ---------------- ROAD LOOP ----------------

def road_loop():
    while True:
        f=road_q.get()
        r=yolo(f,conf=CONF_THRES,verbose=False)[0]
        for b in r.boxes.xyxy:
            x1,y1,x2,y2=map(int,b)
            cv2.rectangle(f,(x1,y1),(x2,y2),(0,255,0),2)
        if road_d.full(): road_d.get()
        road_d.put(f)

# ---------------- SECOND LOOP ----------------

def second_loop():
    global MODE
    drowsy=0

    while True:
        f=second_q.get()

        if MODE=="driver":
            rgb=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
            r=mp_face.process(rgb)

            if r.multi_face_landmarks:
                lm=r.multi_face_landmarks[0].landmark

                e=(ear(lm,[33,160,158,133,153,144])+
                   ear(lm,[362,385,387,263,373,380]))/2

                drowsy=drowsy+1 if e<0.18 else 0
                if drowsy>=12:
                    send_alert("⚠️ DRIVER DROWSY")
                    drowsy=0

                if mar(lm)>0.6:
                    send_alert("⚠️ DRIVER YAWNING")

                nose=lm[1]
                if nose.x<0.35 or nose.x>0.65:
                    send_alert("⚠️ DRIVER LOOKING AWAY")

            y=yolo(f,conf=0.4,verbose=False)[0]
            for cls in y.boxes.cls:
                if int(cls)==67:
                    send_alert("⚠️ PHONE USAGE")

        else:  # cargo
            r=yolo(f,conf=CONF_THRES,verbose=False)[0]
            for b in r.boxes.xyxy:
                x1,y1,x2,y2=map(int,b)
                cv2.rectangle(f,(x1,y1),(x2,y2),(255,0,0),2)
            h=mp_hands.process(cv2.cvtColor(f,cv2.COLOR_BGR2RGB))
            if h.multi_hand_landmarks:
                send_alert("⚠️ UNAUTHORIZED CARGO ACCESS")

        if second_d.full(): second_d.get()
        second_d.put(f)

# ---------------- GPS LOOP ----------------

def gps_loop():
    while True:
        g=read_gps()
        if g:
            lat,lon,speed=parse_nmea(g)

            if lat and lon:
                log_event("GPS","LIVE",f"{lat},{lon}")
                d=haversine(lat,lon,GEOFENCE_LAT,GEOFENCE_LON)
                if d>GEOFENCE_RADIUS_KM:
                    send_alert("⚠️ GEOFENCE BREACH")

            if speed:
                log_event("GPS","SPEED",speed)
                if speed>OVERSPEED_LIMIT:
                    send_alert("⚠️ OVERSPEEDING")

        time.sleep(5)

# ---------------- FLASK ----------------

app=Flask(__name__)

def gen(q):
    while True:
        f=q.get()
        yield b"--frame\r\nContent-Type:image/jpeg\r\n\r\n"+encode(f)+b"\r\n"

@app.route("/")
def ui():
    return f"""
    <h2>Current Mode: {MODE.upper()}</h2>
    <a href='/set/driver'>Driver</a> |
    <a href='/set/cargo'>Cargo</a><br><br>
    <img src=/road width=48%>
    <img src=/second width=48%>
    """

@app.route("/set/<mode>")
def set_mode(mode):
    global MODE, secondary_thread
    if mode in ["driver","cargo"]:
        MODE=mode
        if secondary_thread:
            secondary_thread.stop()
            time.sleep(1)
        fps=DRIVER_FPS if mode=="driver" else CARGO_FPS
        cam=DRIVER_CAM if mode=="driver" else CARGO_CAM
        secondary_thread=Cam(cam,second_q,mode.upper(),fps)
        secondary_thread.start()
    return "Mode changed to "+MODE

@app.route("/road")
def road_stream():
    return Response(gen(road_d),
        mimetype="multipart/x-mixed-replace;boundary=frame")

@app.route("/second")
def second_stream():
    return Response(gen(second_d),
        mimetype="multipart/x-mixed-replace;boundary=frame")

# ---------------- MAIN ----------------

if __name__=="__main__":
    Cam(ROAD_CAM,road_q,"ROAD",ROAD_FPS).start()
    secondary_thread=Cam(DRIVER_CAM,second_q,"DRIVER",DRIVER_FPS)
    secondary_thread.start()

    threading.Thread(target=road_loop,daemon=True).start()
    threading.Thread(target=second_loop,daemon=True).start()
    threading.Thread(target=gps_loop,daemon=True).start()

    app.run("0.0.0.0",5000,threaded=True)
