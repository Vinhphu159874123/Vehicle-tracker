# Vehicle Counting System - Quick Start Guide

## Step-by-step để chạy project:

### 1️⃣ Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Chuẩn bị video test
- Bỏ video vào folder `data/`
- Hoặc update RTSP URL trong `config.py`

### 3️⃣ Chọn ROI và Line
```bash
python utils/roi_selector.py
```
- Vẽ polygon ROI (click chuột)
- Vẽ line (2 clicks)

### 4️⃣ Test offline
```bash
python main.py
```

### 5️⃣ Chạy dashboard
```bash
python app.py
```
Truy cập: http://localhost:5000

---

## 📝 Implementation checklist:

**Ưu tiên cao (core features):**
- [ ] detector.py - YOLO detection + ROI filter
- [ ] tracker.py - BYTETrack wrapper
- [ ] counter.py - Line crossing logic
- [ ] main.py - Processing pipeline
- [ ] visualization.py - Draw functions

**Ưu tiên trung (tools):**
- [ ] roi_selector.py - Interactive ROI tool
- [ ] logger.py - CSV + SQLite logging

**Ưu tiên thấp (nice-to-have):**
- [ ] app.py - Flask dashboard
- [ ] index.html - Web interface

---

## 🐛 Debug tips:

**Nếu detect không chính xác:**
- Giảm `CONFIDENCE_THRESHOLD` trong config.py

**Nếu track nhảy lung tung:**
- Tăng `TRACK_BUFFER` và giảm `MATCH_THRESH`

**Nếu đếm nhiều lần:**
- Tăng `COUNTING_COOLDOWN` và `MIN_TRACK_AGE`

**Nếu RTSP bị lag:**
- Set buffer size: `cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)`

---

Xem chi tiết trong [README.md](README.md)
