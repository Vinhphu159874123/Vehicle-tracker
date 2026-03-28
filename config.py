"""
Configuration file cho Vehicle Tracking System
Chỉnh tất cả parameters ở đây
"""

# ======================
# INPUT SOURCE
# ======================
# Chọn 1 trong 2:
# VIDEO_SOURCE = "data/test_video.mp4"  # Video file
# VIDEO_SOURCE = "rtsp://admin:8dg12345678@192.168.1.79:554/cam/realmonitor?channel=1&subtype=0"  # RTSP stream - Main stream (nét hơn)
VIDEO_SOURCE = "data/20260327143644.mp4"
# ======================
# YOLO DETECTION
# ======================
YOLO_MODEL = "best_yolo_v8n.pt"  # yolov8n.pt (nhanh) hoặc yolov8s.pt (chính xác hơn)
CONFIDENCE_THRESHOLD = 0.30  # Ngưỡng confidence - TĂNG để giảm false positives
IOU_THRESHOLD = 0.5          # Non-max suppression
# TARGET_CLASSES = [2, 3, 5, 7]  # COCO classes: 2=car, 3=motorcycle, 5=bus, 7=truck
TARGET_CLASSES = None  # BỎ class filter - chấp nhận tất cả (vì YOLO nhầm class do góc nhìn)
MIN_BOX_AREA = 500           # Bỏ bbox quá nhỏ (pixels^2) - TĂNG để lọc noise
TARGET_CLASS_NAMES = ["motorbike", "small_cart", "three_wheeler"]
# ======================
# ROI (Region of Interest)
# ======================
# Polygon points (x, y) - chạy roi_selector.py để lấy
# Format: [(x1,y1), (x2,y2), (x3,y3), (x4,y4), ...]
ROI_POLYGON = [(375, 176), (229, 124), (185, 142), (279, 384), (492, 650), (940, 695), (1073, 462), (603, 75), (380, 34), (378, 177)]

# ======================
# LINE CROSSING
# ======================
# Line coordinates: (x1, y1) -> (x2, y2)
# Chạy roi_selector.py để set
LINE_START = (507, 596)
LINE_END = (851, 323)

# Direction: "horizontal" hoặc "vertical"
# - "horizontal": Line nằm ngang (━━━), xe đi dọc (↑↓)
# - "vertical": Line nằm dọc (│), xe đi ngang (←→)
# LINE_DIRECTION = "horizontal"
LINE_DIRECTION = "vertical"


# ======================
# TRACKING
# ======================
# BYTETrack parameters
TRACK_THRESH = 0.45       # Detection confidence cho tracking
TRACK_BUFFER = 30         # Frames để giữ lost tracks
MATCH_THRESH = 0.8        # Matching threshold

# Anti-noise filters  
MIN_TRACK_AGE = 0.2       # Track phải tồn tại >= N GIÂY mới đếm (0.2s ~ 2 frames @ 9fps) - GIẢM để test
MIN_DISPLACEMENT = 10     # Di chuyển tối thiểu (pixels) - GIẢM để test
COUNTING_COOLDOWN = 10.0   # Giây cooldown sau khi đếm (tránh đếm lại)
REARM_DISTANCE_FROM_LINE = 120  # px: sau khi đếm, track phải rời xa line đủ ngưỡng mới được đếm lại
# Chống đếm trùng khi 1 xe bị tách thành nhiều track_id gần nhau
DUPLICATE_EVENT_WINDOW = 2.0   # Giây: 2 event quá gần thời gian sẽ bị so trùng
DUPLICATE_EVENT_DISTANCE = 220 # Pixels: 2 event quá gần vị trí sẽ coi là cùng 1 xe

# ======================
# LOGGING
# ======================
LOG_FILE = "data/vehicle_log.csv"    # CSV log
DATABASE_FILE = "data/logs.db"       # SQLite database
LOG_INTERVAL = 60                    # Lưu summary mỗi N giây

# ======================
# DASHBOARD
# ======================
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
STREAM_FPS = 15  # FPS cho web stream (thấp hơn realtime để tiết kiệm bandwidth)

# ======================
# DISPLAY (for debugging)
# ======================
DISPLAY_WINDOW = True    # Hiện cửa sổ OpenCV khi debug
DISPLAY_WIDTH = 1280     # Resize frame để hiển thị
DISPLAY_HEIGHT = 720

# Runtime logging control
VERBOSE_LOGS = False
