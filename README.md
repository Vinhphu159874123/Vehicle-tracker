# 🚗 Vehicle Counting System

Project đếm xe vào/ra từ camera RTSP sử dụng YOLOv8 + BYTETrack

---

## 📁 Project Structure

```
Car tracker/
├── config.py              # ⚙️ Configuration (chỉnh parameters ở đây)
├── main.py               # 🎯 Main entry point (chạy offline)
├── app.py                # 🌐 Flask dashboard (chạy web interface)
│
├── detector.py           # 🔍 YOLO vehicle detector
├── tracker.py            # 🎯 BYTETrack wrapper
├── counter.py            # 📊 Line crossing counter
├── logger.py             # 💾 Data logging (CSV + SQLite)
│
├── utils/
│   ├── roi_selector.py   # 🖱️ Tool chọn ROI & line
│   └── visualization.py  # 🎨 Vẽ bbox, line, counts
│
├── data/                 # 📂 Videos, logs, database
├── models/               # 🤖 YOLO weights (auto download)
├── templates/            # 📄 HTML templates
├── static/               # 🎨 CSS/JS
└── requirements.txt      # 📦 Dependencies
```

---

## 🔄 System Flow

### **High-level Architecture:**

```
┌─────────────┐
│ Video/RTSP  │
└──────┬──────┘
       │ frames
       ↓
┌──────────────────┐
│  VehicleDetector │  ← YOLO detect vehicles
│  (detector.py)   │
└──────┬───────────┘
       │ detections [bbox, class, conf]
       ↓
┌──────────────────┐
│  ROI Filter      │  ← Bỏ detections ngoài ROI
└──────┬───────────┘
       │ filtered detections
       ↓
┌──────────────────┐
│  VehicleTracker  │  ← BYTETrack assign track_id
│  (tracker.py)    │
└──────┬───────────┘
       │ tracks [track_id, bbox, centroid]
       ↓
┌──────────────────┐
│  LineCounter     │  ← Đếm line crossing IN/OUT
│  (counter.py)    │
└──────┬───────────┘
       │ events [track_id, direction, timestamp]
       ↓
┌──────────────────┐
│  DataLogger      │  ← Log vào CSV + SQLite
│  (logger.py)     │
└──────┬───────────┘
       │
       ├─→ 📊 Dashboard (Flask)
       └─→ 💾 Database
```

---

## 🧩 Component Relationships

### **1. VehicleDetector (detector.py)**
**Input:** Frame (numpy array)  
**Output:** Detections (list of dict)

```python
{
    'bbox': [x1, y1, x2, y2],
    'confidence': 0.85,
    'class_id': 7,  # truck
    'class_name': 'truck'
}
```

**Dependencies:**
- `ultralytics.YOLO`
- `config` (YOLO_MODEL, CONFIDENCE_THRESHOLD, TARGET_CLASSES)

**Tasks bạn làm:**
- [ ] Load YOLO model
- [ ] Detect và filter theo confidence
- [ ] Filter theo class (car, motorcycle, truck, bus)
- [ ] Filter bbox quá nhỏ (MIN_BOX_AREA)
- [ ] Filter theo ROI polygon

---

### **2. VehicleTracker (tracker.py)**
**Input:** Detections (từ detector)  
**Output:** Tracks (list of dict)

```python
{
    'track_id': 42,
    'bbox': [x1, y1, x2, y2],
    'centroid': (cx, cy),
    'confidence': 0.85,
    'class_id': 7
}
```

**Dependencies:**
- `supervision.ByteTrack`
- `config` (TRACK_THRESH, TRACK_BUFFER, MATCH_THRESH)

**Tasks bạn làm:**
- [ ] Wrap ByteTrack từ supervision
- [ ] Convert detections → supervision.Detections format
- [ ] Update tracker
- [ ] Convert tracked results → dict format
- [ ] Tính centroid cho mỗi track

---

### **3. LineCounter (counter.py)**
**Input:** Tracks (từ tracker)  
**Output:** Events (list of dict)

```python
{
    'track_id': 42,
    'direction': 'IN',  # hoặc 'OUT'
    'timestamp': 1707408000.5,
    'class_id': 7
}
```

**Dependencies:**
- `config` (LINE_START, LINE_END, MIN_TRACK_AGE, MIN_DISPLACEMENT, COUNTING_COOLDOWN)

**Internal State:**
- `track_history`: lưu centroids qua thời gian
- `counted_tracks`: track nào đã đếm + timestamp
- `track_start_time`: track xuất hiện lúc nào
- `count_in`, `count_out`: counters

**Tasks bạn làm:**
- [ ] Lưu centroid history cho mỗi track
- [ ] Check line crossing (đoạn thẳng cắt line)
- [ ] Phân biệt direction (IN/OUT)
- [ ] Apply filters:
  - Min track age (≥ 5 frames)
  - Min displacement (≥ 15 pixels)
  - Cooldown (3 giây không đếm lại)

**Algorithm Line Crossing (horizontal line):**
```python
# Line là y = line_y (horizontal)
centroid_prev = (x1, y1)
centroid_curr = (x2, y2)

if y1 < line_y and y2 >= line_y:
    direction = 'IN'  # đi từ trên xuống
elif y1 >= line_y and y2 < line_y:
    direction = 'OUT'  # đi từ dưới lên
```

---

### **4. DataLogger (logger.py)**
**Input:** Events (từ counter)  
**Output:** CSV + SQLite database

**Database Schema:**
```sql
-- Events table
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    direction TEXT,  -- 'IN' or 'OUT'
    track_id INTEGER,
    class_id INTEGER
);

-- Summary table
CREATE TABLE summary (
    id INTEGER PRIMARY KEY,
    start_time TEXT,
    end_time TEXT,
    count_in INTEGER,
    count_out INTEGER,
    interval_seconds INTEGER
);
```

**Tasks bạn làm:**
- [ ] Setup CSV file + header
- [ ] Setup SQLite tables
- [ ] Log mỗi event vào CSV + DB
- [ ] Save summary reports định kỳ
- [ ] Query statistics (hourly, daily)

---

### **5. Visualization (utils/visualization.py)**
Helper functions vẽ lên frame

**Functions:**
- `draw_detections()`: vẽ bbox + class label
- `draw_tracks()`: vẽ bbox + track_id
- `draw_roi()`: vẽ polygon ROI (semi-transparent)
- `draw_line()`: vẽ counting line
- `draw_counts()`: vẽ IN/OUT counters
- `draw_fps()`: vẽ FPS

---

### **6. ROI Selector (utils/roi_selector.py)**
Interactive tool để chọn ROI và line

**Usage:**
```bash
python utils/roi_selector.py
```

**Flow:**
1. Load first frame từ video/RTSP
2. User vẽ polygon ROI (click chuột)
3. User vẽ line (2 clicks)
4. Save vào `config.py`

**Tasks bạn làm:**
- [ ] Setup mouse callback
- [ ] Vẽ polygon interactively
- [ ] Vẽ line (2 điểm)
- [ ] Save vào config.py

---

## 🚀 Usage Workflow

### **Phase 1: Setup**

```bash
# 1. Cài dependencies
pip install -r requirements.txt

# 2. Bỏ video test vào data/
# Copy video vào: data/test_video.mp4

# 3. Update config.py
# Sửa VIDEO_SOURCE = "data/test_video.mp4"
```

---

### **Phase 2: Chọn ROI & Line**

```bash
python utils/roi_selector.py
```

**Instructions:**
- **ROI polygon:**
  - Left click: thêm điểm
  - Right click hoặc 'c': đóng polygon
  - 'r': reset
  - 'q': save

- **Counting line:**
  - Click 2 điểm
  - 'r': reset
  - 'q': save

→ Results được save vào `config.py`

---

### **Phase 3: Test offline**

```bash
python main.py
```

**Expected:**
- Cửa sổ OpenCV hiện frame
- Có bbox + track_id
- Có line + ROI
- Có counters (IN/OUT)
- Console in ra events
- Data saved vào `data/logs.db` và `data/vehicle_log.csv`

**Debug tips:**
- Nếu detect sai → giảm CONFIDENCE_THRESHOLD
- Nếu track rề rà → tăng MIN_TRACK_AGE, MIN_DISPLACEMENT
- Nếu đếm nhiều → tăng COUNTING_COOLDOWN

---

### **Phase 4: Dashboard**

```bash
python app.py
```

**Truy cập:** http://localhost:5000

**Features:**
- Live video stream
- Real-time counters (IN/OUT)
- Statistics charts
- WebSocket updates

---

## 🎯 Implementation Order (cho bạn)

### **Day 1: Core Pipeline**
1. ✅ `detector.py`: implement `detect()` và `filter_by_roi()`
2. ✅ `tracker.py`: implement `update()`
3. ✅ `counter.py`: implement `update()` và line crossing logic
4. ✅ `utils/visualization.py`: implement draw functions
5. ✅ `main.py`: implement `process_frame()` và `run()`

**Goal:** Chạy được offline với video, đếm đúng

---

### **Day 2: Tools & Logging**
1. ✅ `utils/roi_selector.py`: implement interactive selector
2. ✅ `logger.py`: implement logging functions
3. ✅ Test với real video/RTSP

**Goal:** Pipeline hoàn chỉnh, có logging

---

### **Day 3: Dashboard**
1. ✅ `app.py`: implement Flask routes + SocketIO
2. ✅ `templates/index.html`: implement frontend + WebSocket
3. ✅ Optional: add charts (Chart.js)

**Goal:** Dashboard hoàn chỉnh

---

## 🐛 Common Issues & Solutions

### **Issue 1: YOLO detect sai**
- Giảm `CONFIDENCE_THRESHOLD` xuống 0.3
- Check TARGET_CLASSES có đúng không
- Filter MIN_BOX_AREA để bỏ bbox xa

### **Issue 2: Track ID nhảy lung tung**
- Tăng `TRACK_BUFFER` (giữ lost tracks lâu hơn)
- Giảm `MATCH_THRESH` (khớp lỏng hơn)

### **Issue 3: Đếm sai (đếm nhiều lần)**
- Tăng `MIN_TRACK_AGE` (bỏ tracks quá ngắn)
- Tăng `COUNTING_COOLDOWN` (3-5 giây)
- Tăng `MIN_DISPLACEMENT` (bỏ di chuyển nhỏ)

### **Issue 4: RTSP lag/disconnect**
- Dùng buffer nhỏ: `cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)`
- Hoặc dùng library `av` thay OpenCV
- Thêm auto-reconnect logic

---

## 📚 References

- **YOLOv8 Docs:** https://docs.ultralytics.com/
- **Supervision Docs:** https://supervision.roboflow.com/
- **BYTETrack Paper:** https://arxiv.org/abs/2110.06864
- **Flask-SocketIO:** https://flask-socketio.readthedocs.io/

---

## ✅ TODO Checklist

- [ ] Implement detector.py
- [ ] Implement tracker.py
- [ ] Implement counter.py
- [ ] Implement visualization.py
- [ ] Implement roi_selector.py
- [ ] Implement logger.py
- [ ] Implement main.py
- [ ] Implement app.py
- [ ] Implement templates/index.html
- [ ] Test with video file
- [ ] Test with RTSP stream
- [ ] Deploy dashboard

---

**Good luck! 🚀 Bạn có thể bắt đầu từ detector.py → tracker.py → counter.py**

Nếu stuck thì ping tôi nhé!
