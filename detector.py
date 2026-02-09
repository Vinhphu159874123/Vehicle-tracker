"""
YOLO Detector Wrapper
Nhiệm vụ: Load YOLO model và detect vehicles trong frame
"""

from ultralytics import YOLO
import numpy as np
import cv2
import config
import torch

class VehicleDetector:
    """
    Wrapper class cho YOLO detector
    """
    
    def __init__(self):
        """Load YOLO model và warm up"""
        self.model = YOLO(config.YOLO_MODEL)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        dummy_frame = np.zeros((640, 480, 3), dtype=np.uint8)
        _ = self.model(dummy_frame)
        print(f"YOLO model loaded on {self.device}")
    
    def detect(self, frame):
        """Detect vehicles và filter theo class, confidence, bbox area"""
        detections = []
        
        # Chạy YOLO inference
        results = self.model(frame, verbose=False)
        
        result = results[0]
        
        # Loop qua detections và apply filters
        if result.boxes is not None and len(result.boxes) > 0:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy()
            
            for i in range(len(boxes)):
                class_id = int(class_ids[i])
                confidence = float(confidences[i])
                x1, y1, x2, y2 = boxes[i]
                
                # Filter: class, confidence, area
                if class_id not in config.TARGET_CLASSES:
                    continue
                
                if confidence < config.CONFIDENCE_THRESHOLD:
                    continue
                width = x2 - x1
                height = y2 - y1
                area = width * height
                
                if area < config.MIN_BOX_AREA:
                    continue
                
                class_name = result.names[class_id]
                detection = {
                    'bbox': [int(x1), int(y1), int(x2), int(y2)],
                    'confidence': confidence,
                    'class_id': class_id,
                    'class_name': class_name
                }
                
                detections.append(detection)
        
        return detections
    
    def filter_by_roi(self, detections, roi_polygon):
        """Lọc detections nằm trong ROI polygon"""
        if roi_polygon is None:
            return detections
        
        if not isinstance(roi_polygon, np.ndarray):
            roi_polygon = np.array(roi_polygon, dtype=np.int32)
        
        filtered_detections = []
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            centroid_x = (x1 + x2) / 2
            centroid_y = (y1 + y2) / 2
            centroid = (centroid_x, centroid_y)
            
            # Check centroid trong polygon
            result = cv2.pointPolygonTest(roi_polygon, centroid, False)
            if result >= 0:
                filtered_detections.append(det)
        
        return filtered_detections
