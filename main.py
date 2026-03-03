"""Main Processing Pipeline - Chạy detection + tracking + counting"""

import cv2
import time
import numpy as np
from datetime import datetime

import config
from detector import VehicleDetector
from tracker import VehicleTracker
from counter import LineCounter
from logger import DataLogger
from utils.visualization import *


class VehicleCountingSystem:
    """Main system orchestrator"""
    
    def __init__(self):
        """Khởi tạo tất cả components"""
        print("🚀 Initializing Vehicle Counting System...\n")
        
        self.detector = VehicleDetector()
        self.tracker = VehicleTracker()
        self.counter = LineCounter(config.LINE_START, config.LINE_END)
        self.logger = DataLogger()
        
        self.roi_polygon = np.array(config.ROI_POLYGON, dtype=np.int32)
        
        self.cap = cv2.VideoCapture(config.VIDEO_SOURCE)
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video source: {config.VIDEO_SOURCE}")
        
        self.fps = 0
        self.frame_count = 0
        self.start_time = datetime.now()
        self.last_summary_time = datetime.now()
        
        print("✅ All components initialized!\n")
    
    def run(self):
        """Main processing loop"""
        print("🎬 Starting main loop...\n")
        print("Press 'q' to quit\n")
        
        fps_start_time = time.time()
        fps_frame_count = 0
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("⚠️ End of video or cannot read frame")
                    break
                
                # Resize frame về kích thước cố định để ROI/line coordinates luôn đúng
                frame = cv2.resize(frame, (config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
                
                self.frame_count += 1
                
                frame, events = self.process_frame(frame)
                
                for event in events:
                    self.logger.log_event(event)
                    print(f"🚗 Vehicle {event['direction']}: Track #{event['track_id']}")
                
                fps_frame_count += 1
                if time.time() - fps_start_time >= 1.0:
                    self.fps = fps_frame_count / (time.time() - fps_start_time)
                    fps_start_time = time.time()
                    fps_frame_count = 0
                
                current_time = datetime.now()
                if (current_time - self.last_summary_time).total_seconds() >= config.LOG_INTERVAL:
                    counts = self.counter.get_counts()
                    self.logger.save_summary(
                        self.last_summary_time,
                        current_time,
                        counts['in'],
                        counts['out']
                    )
                    self.last_summary_time = current_time
                
                if config.DISPLAY_WINDOW:
                    cv2.imshow('Vehicle Counting System', frame)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("\n🛑 User requested quit")
                        break
        
        except KeyboardInterrupt:
            print("\n\n⏸️ Interrupted by user")
        
        finally:
            self.cleanup()
    
    def process_frame(self, frame):
        """Process 1 frame qua pipeline"""
        detections = self.detector.detect(frame)
        
        detections_roi = self.detector.filter_by_roi(detections, self.roi_polygon)
        
        tracks = self.tracker.update(detections_roi)
        
        events = self.counter.update(tracks)
        
        # Vẽ ROI và line
        frame = draw_roi(frame, self.roi_polygon)
        frame = draw_line(frame, config.LINE_START, config.LINE_END)
        
        # Vẽ detections (màu xanh lá) - hiển thị tất cả objects được detect
        frame = draw_detections(frame, detections_roi, color=(0, 255, 0))
        
        # Vẽ tracks (màu đỏ) - chỉ hiển thị tracked objects (mature tracks)
        frame = draw_tracks(frame, tracks)
        
        counts = self.counter.get_counts()
        frame = draw_counts(frame, counts['in'], counts['out'])
        frame = draw_fps(frame, self.fps)
        
        return frame, events
    
    def cleanup(self):
        """Cleanup resources"""
        print("\n🧹 Cleaning up...")
        
        counts = self.counter.get_counts()
        print(f"\n📊 Final counts:")
        print(f"   IN: {counts['in']}")
        print(f"   OUT: {counts['out']}")
        print(f"   TOTAL: {counts['total']}")
        print(f"   Frames processed: {self.frame_count}")
        
        self.cap.release()
        cv2.destroyAllWindows()
        
        print("\n✅ System stopped gracefully")


def main():
    """Entry point"""
    print("=== Vehicle Counting System ===")
    print(f"Video source: {config.VIDEO_SOURCE}")
    print(f"YOLO model: {config.YOLO_MODEL}")
    print()
    
    if config.ROI_POLYGON is None:
        print("❌ ERROR: ROI chưa được set!")
        print("Chạy: python utils/roi_selector.py")
        return
    
    if config.LINE_START is None or config.LINE_END is None:
        print("❌ ERROR: Line chưa được set!")
        print("Chạy: python utils/roi_selector.py")
        return
    
    try:
        system = VehicleCountingSystem()
        system.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

