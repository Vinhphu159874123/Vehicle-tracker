"""
YOLO Detector Wrapper
Nhiệm vụ: Load YOLO model và detect vehicles trong frame
"""

from ultralytics import YOLO
import numpy as np
import config


class VehicleDetector:
    """
    Wrapper class cho YOLO detector
    """
    
    def __init__(self):
        """
        TODO: Bạn cần implement
        
        Tasks:
        1. Load YOLO model từ config.YOLO_MODEL
        2. Set device (cuda nếu có GPU, cpu nếu không)
        3. Warm up model (chạy 1 lần dummy inference)
        
        Hints:
        - self.model = YOLO(config.YOLO_MODEL)
        - Check GPU: torch.cuda.is_available()
        """
        pass
    
    def detect(self, frame):
        """
        Detect vehicles trong frame
        
        Args:
            frame: numpy array (BGR image từ OpenCV)
        
        Returns:
            detections: list of dict, mỗi dict có:
                {
                    'bbox': [x1, y1, x2, y2],
                    'confidence': float,
                    'class_id': int,
                    'class_name': str
                }
        
        TODO: Bạn cần implement
        
        Tasks:
        1. Chạy YOLO inference: results = self.model(frame)
        2. Filter theo TARGET_CLASSES và CONFIDENCE_THRESHOLD
        3. Filter theo MIN_BOX_AREA (bỏ bbox quá nhỏ)
        4. Convert results về format dict như trên
        
        Hints:
        - results[0].boxes.xyxy: bbox coordinates
        - results[0].boxes.conf: confidence scores
        - results[0].boxes.cls: class IDs
        - Tính area: (x2-x1) * (y2-y1)
        """
        pass
    
    def filter_by_roi(self, detections, roi_polygon):
        """
        Lọc detections nằm trong ROI
        
        Args:
            detections: list of dict từ detect()
            roi_polygon: numpy array shape (N, 2) - polygon points
        
        Returns:
            filtered_detections: list of dict (chỉ giữ trong ROI)
        
        TODO: Bạn cần implement
        
        Tasks:
        1. Tính centroid của mỗi bbox: center = ((x1+x2)/2, (y1+y2)/2)
        2. Check centroid có trong polygon không
        3. Chỉ giữ detections có centroid trong ROI
        
        Hints:
        - Dùng cv2.pointPolygonTest(roi_polygon, center, False)
        - Return >= 0 là trong polygon
        """
        pass
