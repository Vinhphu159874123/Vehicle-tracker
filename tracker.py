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
        """Khởi tạo BYTETracker"""
        self.tracker = sv.ByteTrack(
            track_activation_threshold=config.TRACK_THRESH,
            lost_track_buffer=config.TRACK_BUFFER,
            minimum_matching_threshold=config.MATCH_THRESH,
            frame_rate=30
        )
        print(f"✅ ByteTrack initialized (thresh={config.TRACK_THRESH}, buffer={config.TRACK_BUFFER})")
    
    def update(self, detections):
        """Update tracker và gán track_id cho mỗi detection"""
        tracks = []
        
        if not detections or len(detections) == 0:
            return tracks
        
        # Convert sang supervision.Detections format
        xyxy = []
        confidences = []
        class_ids = []
        
        for det in detections:
            xyxy.append(det['bbox'])
            confidences.append(det['confidence'])
            class_ids.append(det['class_id'])
        xyxy = np.array(xyxy, dtype=np.float32)
        confidences = np.array(confidences, dtype=np.float32)
        class_ids = np.array(class_ids, dtype=int)
        detections_sv = sv.Detections(
            xyxy=xyxy,
            confidence=confidences,
            class_id=class_ids
        )
        
        # Update tracker (gán track_id)
        detections_sv = self.tracker.update_with_detections(detections_sv)
        if detections_sv.tracker_id is not None:
            for i in range(len(detections_sv.xyxy)):
                x1, y1, x2, y2 = detections_sv.xyxy[i]
                centroid_x = (x1 + x2) / 2
                centroid_y = (y1 + y2) / 2
                
                track = {
                    'track_id': int(detections_sv.tracker_id[i]),
                    'bbox': [int(x1), int(y1), int(x2), int(y2)],
                    'centroid': (float(centroid_x), float(centroid_y)),
                    'confidence': float(detections_sv.confidence[i]),
                    'class_id': int(detections_sv.class_id[i])
                }
                
                tracks.append(track)
        
        return tracks
