"""
Main Processing Pipeline
Chạy detection + tracking + counting pipeline
"""

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
    """
    Main system orchestrator
    """
    
    def __init__(self):
        """
        TODO: Bạn cần implement
        
        Tasks:
        1. Khởi tạo tất cả components:
           - detector = VehicleDetector()
           - tracker = VehicleTracker()
           - counter = LineCounter(config.LINE_START, config.LINE_END)
           - logger = DataLogger()
        2. Load ROI polygon từ config
        3. Setup video capture: cv2.VideoCapture(config.VIDEO_SOURCE)
        4. FPS tracking variables
        """
        pass
    
    def run(self):
        """
        Main processing loop
        
        TODO: Bạn cần implement
        
        Flow:
        1. Đọc frame từ video/RTSP
        2. Detect vehicles → detections
        3. Filter bằng ROI → detections_in_roi
        4. Track objects → tracks
        5. Count line crossing → events
        6. Log events
        7. Visualize (vẽ bbox, line, counts)
        8. Display frame (nếu DISPLAY_WINDOW = True)
        9. Lưu summary định kỳ (mỗi LOG_INTERVAL giây)
        10. Repeat
        
        Hints:
        - ret, frame = cap.read()
        - Tính FPS: dùng time.time()
        - Check 'q' để quit: cv2.waitKey(1) & 0xFF == ord('q')
        """
        pass
    
    def process_frame(self, frame):
        """
        Process 1 frame
        
        Args:
            frame: numpy array
        
        Returns:
            frame: frame đã vẽ
            events: list of counting events
        
        TODO: Bạn cần implement
        
        Tasks:
        1. detections = detector.detect(frame)
        2. detections_roi = detector.filter_by_roi(detections, roi_polygon)
        3. tracks = tracker.update(detections_roi)
        4. events = counter.update(tracks)
        5. Visualize everything
        
        Return:
        - frame đã vẽ
        - events (để log)
        """
        pass
    
    def cleanup(self):
        """
        Cleanup: release resources
        
        TODO: Implement
        - cap.release()
        - cv2.destroyAllWindows()
        """
        pass


def main():
    """
    Entry point
    
    TODO: Bạn cần implement
    
    Tasks:
    1. Check config (ROI, LINE phải được set)
    2. system = VehicleCountingSystem()
    3. system.run()
    4. Catch KeyboardInterrupt để cleanup gracefully
    """
    print("=== Vehicle Counting System ===")
    print(f"Video source: {config.VIDEO_SOURCE}")
    print(f"YOLO model: {config.YOLO_MODEL}")
    print()
    
    # TODO: Check prerequisites
    if config.ROI_POLYGON is None:
        print("ERROR: ROI chưa được set!")
        print("Chạy: python utils/roi_selector.py")
        return
    
    if config.LINE_START is None or config.LINE_END is None:
        print("ERROR: Line chưa được set!")
        print("Chạy: python utils/roi_selector.py")
        return
    
    # TODO: Run system
    pass


if __name__ == "__main__":
    main()
