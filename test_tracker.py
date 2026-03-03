"""
Test tracker.py
Chạy: python test_tracker.py
"""

from detector import VehicleDetector
from tracker import VehicleTracker
import cv2

print("=" * 50)
print("🧪 TEST TRACKER.PY")
print("=" * 50)

# Test 1: Load detector và tracker
print("\n📦 Test 1: Load components...")
try:
    detector = VehicleDetector()
    tracker = VehicleTracker()
    print("✅ Components loaded!")
except Exception as e:
    print(f"❌ Lỗi: {e}")
    exit()

# Test 2: Test với video
print("\n📦 Test 2: Test tracking với video...")
import os

video_paths = [
    "data/test_short.f243.webm",
    "test_short.f243.webm",
    "data/test_video.mp4"
]

video_path = None
for path in video_paths:
    if os.path.exists(path):
        video_path = path
        break

if not video_path:
    print("❌ Không tìm thấy video!")
    print("💡 Bỏ video vào data/ rồi chạy lại")
    exit()

print(f"   Video: {video_path}")

# Mở video
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("❌ Không mở được video!")
    exit()

print("\n🎬 Bắt đầu tracking...")
print("   Nhấn 'q' để thoát\n")

frame_count = 0
track_ids_seen = set()  # Lưu tất cả track_id đã thấy

for i in range(100):  # Chỉ test 100 frames đầu
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    
    # Detect
    detections = detector.detect(frame)
    
    # Track
    tracks = tracker.update(detections)
    
    # Lưu track IDs
    for track in tracks:
        track_ids_seen.add(track['track_id'])
    
    # Vẽ bbox + track_id
    for track in tracks:
        x1, y1, x2, y2 = track['bbox']
        track_id = track['track_id']
        conf = track['confidence']
        
        # Vẽ bbox màu xanh dương (khác detector màu xanh lá)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        
        # Vẽ track_id + confidence
        label = f"ID:{track_id} {conf:.2f}"
        cv2.putText(frame, label, (x1, y1-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        # Vẽ centroid (chấm tròn nhỏ)
        cx, cy = track['centroid']
        cv2.circle(frame, (int(cx), int(cy)), 5, (0, 0, 255), -1)
    
    # Vẽ info
    info = f"Frame: {frame_count} | Tracks: {len(tracks)} | Unique IDs: {len(track_ids_seen)}"
    cv2.putText(frame, info, (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    # Hiển thị
    cv2.imshow("Tracker Test", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Summary
print("\n" + "=" * 50)
print("📊 SUMMARY:")
print("=" * 50)
print(f"Processed frames: {frame_count}")
print(f"Total unique track IDs: {len(track_ids_seen)}")
print(f"Track IDs: {sorted(track_ids_seen)}")

if len(track_ids_seen) > 0:
    print("\n✅ TRACKING HOẠT ĐỘNG!")
    print("\n💡 Observations:")
    print("   - Track ID nên ổn định (cùng 1 xe giữ 1 ID)")
    print("   - Số unique IDs = số xe khác nhau trong video")
    print("   - Nếu ID nhảy linh tinh → cần tune TRACK_BUFFER/MATCH_THRESH")
else:
    print("\n⚠️ Không detect được xe nào!")
    print("💡 Thử:")
    print("   - Giảm CONFIDENCE_THRESHOLD trong config.py")
    print("   - Dùng video khác có nhiều xe hơn")

print("\n✅ Test hoàn tất!")
print("\n💡 Tiếp theo:")
print("   Code counter.py để đếm xe qua line")
