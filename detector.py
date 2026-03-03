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
        
        # Khởi tạo frame counter nếu chưa có
        if not hasattr(self, '_frame_count'):
            self._frame_count = 0
        self._frame_count += 1
        
        # Chạy YOLO inference
        results = self.model(frame, verbose=False)
        
        result = results[0]
        
        # Debug: print tổng số detections trước khi filter
        total_boxes = len(result.boxes) if result.boxes is not None else 0
        
        # Loop qua detections và apply filters
        if result.boxes is not None and len(result.boxes) > 0:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy()
            
            for i in range(len(boxes)):
                class_id = int(class_ids[i])
                confidence = float(confidences[i])
                x1, y1, x2, y2 = boxes[i]
                class_name = result.names[class_id]
                
                width = x2 - x1
                height = y2 - y1
                area = width * height
                
                # Debug: in thông tin TRƯỚC KHI filter
                if i == 0 and self._frame_count % 30 == 0:  # Chỉ in object đầu tiên
                    print(f"   📦 Detection sample: class={class_name}({class_id}), conf={confidence:.2f}, area={area:.0f}")
                
                # Filter: class, confidence, area
                # TEMP: Comment class filter để test
                # if class_id not in config.TARGET_CLASSES:
                #     continue
                
                if config.TARGET_CLASSES is not None and class_id not in config.TARGET_CLASSES:
                    continue
                
                if confidence < config.CONFIDENCE_THRESHOLD:
                    continue
                
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
        
        # Debug print mỗi 30 frames
        if self._frame_count % 30 == 0:
            print(f"🔍 YOLO: {total_boxes} total | {len(detections)} after filter")
        
        return detections
    
    def filter_by_roi(self, detections, roi_polygon):
        """Lọc detections nằm trong ROI polygon"""
        
        # TEMP: DISABLE ROI filter để test line crossing
        if len(detections) > 0:
            print(f"⚠️ ROI Filter DISABLED - accepting all {len(detections)} detections")
        return detections
        
        if roi_polygon is None:
            return detections
        
        if not isinstance(roi_polygon, np.ndarray):
            roi_polygon = np.array(roi_polygon, dtype=np.int32)
        
        # Khởi tạo counter nếu chưa có
        if not hasattr(self, '_roi_frame_count'):
            self._roi_frame_count = 0
        self._roi_frame_count += 1
        
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
        
        # Debug print
        if self._roi_frame_count % 30 == 0 and len(detections) > 0:
            print(f"📍 ROI Filter: {len(detections)} before | {len(filtered_detections)} after")
        
        return filtered_detections
