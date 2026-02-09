"""
BYTETracker Wrapper
Nhiệm vụ: Track objects qua các frames, gán track_id ổn định
"""

import numpy as np
import supervision as sv
import config


class VehicleTracker:
    """
    Wrapper cho BYTETrack từ supervision library
    """
    
    def __init__(self):
        """
        TODO: Bạn cần implement
        
        Tasks:
        1. Khởi tạo ByteTrack từ supervision
        2. Setup tracking parameters từ config
        
        Hints:
        - self.tracker = sv.ByteTrack(
              track_thresh=config.TRACK_THRESH,
              track_buffer=config.TRACK_BUFFER,
              match_thresh=config.MATCH_THRESH
          )
        """
        pass
    
    def update(self, detections):
        """
        Update tracker với detections từ frame hiện tại
        
        Args:
            detections: list of dict từ detector.detect()
        
        Returns:
            tracks: list of dict, mỗi dict có:
                {
                    'track_id': int,
                    'bbox': [x1, y1, x2, y2],
                    'centroid': (cx, cy),
                    'confidence': float,
                    'class_id': int
                }
        
        TODO: Bạn cần implement
        
        Tasks:
        1. Convert detections sang supervision Detections format
        2. Update tracker: tracked = self.tracker.update_with_detections(detections_sv)
        3. Convert tracked results về list of dict
        4. Tính centroid cho mỗi track
        
        Hints:
        - Detections format của supervision:
          detections_sv = sv.Detections(
              xyxy=np.array([bbox1, bbox2, ...]),
              confidence=np.array([conf1, conf2, ...]),
              class_id=np.array([cls1, cls2, ...])
          )
        - Centroid: cx = (x1+x2)/2, cy = (y1+y2)/2
        """
        pass
