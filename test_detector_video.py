"""
Test detector với video
Chạy: python test_detector_video.py
"""

from detector import VehicleDetector
import cv2
import time
import os

print("=" * 50)
print("🎥 TEST DETECTOR VỚI VIDEO")
print("=" * 50)

# Load detector
print("\n📦 Loading model...")
detector = VehicleDetector()
print("✅ Done!")

# Mở video - thử nhiều format
video_paths = [
    "data/test_short.f243.webm",   # Video vừa tải
    "test_short.f243.webm",
    "data/test_video.mp4",
    "data/test_video.webm"
]

video_path = None
for path in video_paths:
    if os.path.exists(path):
        video_path = path
        break

if not video_path:
    print(f"❌ Không tìm thấy video!")
    print(f"   Đã tìm: {video_paths}")
    exit()

print(f"\n📹 Mở video: {video_path}")
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"❌ Không mở được video: {video_path}")
    print("\n💡 Bạn cần:")
    print("   1. Bỏ video test vào: data/test_video.mp4")
    print("   2. Hoặc update video_path trong code")
    exit()

# Đọc thông tin video
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"✅ Video info:")
print(f"   - Size: {width}x{height}")
print(f"   - FPS: {fps}")
print(f"   - Total frames: {total_frames}")

print("\n🎬 Bắt đầu detect...")
print("   Nhấn 'q' để thoát")

frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("\n✅ Video kết thúc!")
        break
    
    frame_count += 1
    
    # Detect vehicles
    detections = detector.detect(frame)
    
    # Vẽ bbox
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        conf = det['confidence']
        cls_name = det['class_name']
        
        # Vẽ bbox màu xanh lá
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Vẽ label
        label = f"{cls_name} {conf:.2f}"
        cv2.putText(frame, label, (x1, y1-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Vẽ info
    info = f"Frame: {frame_count}/{total_frames} | Detections: {len(detections)}"
    cv2.putText(frame, info, (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    # Tính FPS
    elapsed = time.time() - start_time
    current_fps = frame_count / elapsed if elapsed > 0 else 0
    fps_text = f"FPS: {current_fps:.1f}"
    cv2.putText(frame, fps_text, (10, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    # Hiển thị
    cv2.imshow("Detector Test", frame)
    
    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n⚠️ User stopped!")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()

# Summary
elapsed = time.time() - start_time
avg_fps = frame_count / elapsed if elapsed > 0 else 0

print("\n" + "=" * 50)
print("📊 SUMMARY:")
print("=" * 50)
print(f"Processed frames: {frame_count}")
print(f"Total time: {elapsed:.1f}s")
print(f"Average FPS: {avg_fps:.1f}")
print("\n✅ Test hoàn tất!")
print("\n💡 Tiếp theo:")
print("   Code tracker.py để track xe")
