"""
Test counter.py
Chạy: python test_counter.py
"""

from detector import VehicleDetector
from tracker import VehicleTracker
from counter import LineCounter
import cv2
import config

print("=" * 50)
print("🧪 TEST COUNTER.PY")
print("=" * 50)

# Test 1: Load components
print("\n📦 Test 1: Load components...")
try:
    detector = VehicleDetector()
    tracker = VehicleTracker()
    
    # Tạo line ở giữa màn hình (horizontal)
    # Sẽ update sau khi biết kích thước video
    counter = None
    print("✅ Detector + Tracker loaded!")
except Exception as e:
    print(f"❌ Lỗi: {e}")
    exit()

# Test 2: Test với video
print("\n📦 Test 2: Test counting với video...")
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

# Lấy kích thước video để vẽ line
ret, first_frame = cap.read()
if not ret:
    print("❌ Không đọc được frame!")
    exit()

height, width = first_frame.shape[:2]

# Tạo line ở giữa màn hình (đọc từ config)
if config.LINE_DIRECTION == "horizontal":
    line_y = height // 2
    line_start = (0, line_y)
    line_end = (width, line_y)
    print(f"   Line: y={line_y} (horizontal)")
else:  # vertical
    line_x = width // 2
    line_start = (line_x, 0)
    line_end = (line_x, height)
    print(f"   Line: x={line_x} (vertical)")

counter = LineCounter(line_start, line_end)

# Reset video về đầu
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

print("\n🎬 Bắt đầu counting...")
print("   Nhấn 'q' để thoát\n")

frame_count = 0
total_events = []

for i in range(200):  # Test 200 frames
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    
    # Pipeline: Detect → Track → Count
    detections = detector.detect(frame)
    tracks = tracker.update(detections)
    events = counter.update(tracks)
    
    # Lưu events
    total_events.extend(events)
    
    # Vẽ line (màu vàng)
    cv2.line(frame, line_start, line_end, (0, 255, 255), 3)
    
    # Vẽ tracks
    for track in tracks:
        x1, y1, x2, y2 = track['bbox']
        track_id = track['track_id']
        cx, cy = track['centroid']
        
        # Vẽ bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        
        # Vẽ track_id
        label = f"ID:{track_id}"
        cv2.putText(frame, label, (x1, y1-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        # Vẽ centroid
        cv2.circle(frame, (int(cx), int(cy)), 5, (0, 0, 255), -1)
    
    # Hiển thị events trong frame này
    for event in events:
        direction = event['direction']
        track_id = event['track_id']
        color = (0, 255, 0) if direction == 'IN' else (0, 0, 255)
        
        # Flash message
        msg = f"{direction}: ID {track_id}"
        cv2.putText(frame, msg, (width - 200, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    # Vẽ counts
    counts = counter.get_counts()
    info = f"IN: {counts['in']} | OUT: {counts['out']} | TOTAL: {counts['total']}"
    cv2.putText(frame, info, (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    
    cv2.putText(frame, f"Frame: {frame_count}", (10, height - 10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Hiển thị
    cv2.imshow("Counter Test", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Summary
print("\n" + "=" * 50)
print("📊 SUMMARY:")
print("=" * 50)
counts = counter.get_counts()
print(f"Processed frames: {frame_count}")
print(f"IN:    {counts['in']}")
print(f"OUT:   {counts['out']}")
print(f"TOTAL: {counts['total']}")
print(f"\nTotal events: {len(total_events)}")

if total_events:
    print("\n📋 Events log:")
    for i, event in enumerate(total_events, 1):
        print(f"  {i}. ID={event['track_id']} → {event['direction']} "
              f"(class={event['class_id']}) at {event['timestamp']:.2f}")

if counts['total'] > 0:
    print("\n✅ COUNTER HOẠT ĐỘNG!")
    print("\n💡 Observations:")
    print("   - Xe đi từ trên xuống qua line → IN")
    print("   - Xe đi từ dưới lên qua line → OUT")
    print("   - Cùng 1 ID chỉ đếm 1 lần (có cooldown)")
else:
    print("\n⚠️ Không đếm được xe nào!")
    print("💡 Có thể:")
    print("   - Xe không đi qua line (line ở vị trí sai)")
    print("   - Filter quá strict (MIN_TRACK_AGE, MIN_DISPLACEMENT)")
    print("   - Video quá ngắn")

print("\n✅ Test hoàn tất!")
print("\n💡 Tiếp theo:")
print("   - Tune line position (LINE_Y trong config)")
print("   - Adjust filters nếu đếm sai")
print("   - Code visualization.py để vẽ đẹp hơn")
