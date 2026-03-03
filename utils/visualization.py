"""Visualization utilities - vẽ bbox, line, counts lên frame"""

import cv2
import numpy as np


def draw_detections(frame, detections, color=(0, 255, 0)):
    """Vẽ bounding boxes và labels cho detections"""
    for det in detections:
        bbox = det['bbox']
        class_name = det.get('class_name', 'unknown')
        class_id = det['class_id']
        confidence = det['confidence']
        
        x1, y1, x2, y2 = map(int, bbox)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Hiển thị class name và confidence
        label = f"{class_name}({class_id}) {confidence:.2f}"
        cv2.putText(frame, label, (x1, y1 - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    return frame


def draw_tracks(frame, tracks, color=(255, 0, 0)):
    """Vẽ tracked objects với track_id và centroid"""
    for track in tracks:
        bbox = track['bbox']
        track_id = track['track_id']
        centroid = track['centroid']
        
        x1, y1, x2, y2 = map(int, bbox)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        label = f"ID:{track_id}"
        cv2.putText(frame, label, (x1, y1 - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        cx, cy = map(int, centroid)
        cv2.circle(frame, (cx, cy), 4, (0, 255, 255), -1)
    
    return frame


def draw_roi(frame, roi_polygon, color=(0, 255, 255), alpha=0.3):
    """Vẽ ROI polygon với transparency"""
    overlay = frame.copy()
    
    if isinstance(roi_polygon, list):
        roi_polygon = np.array(roi_polygon, dtype=np.int32)
    
    cv2.fillPoly(overlay, [roi_polygon], color)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    cv2.polylines(frame, [roi_polygon], True, color, 2)
    
    return frame


def draw_line(frame, line_start, line_end, color=(0, 0, 255), thickness=3):
    """Vẽ counting line với arrow"""
    cv2.line(frame, line_start, line_end, color, thickness)
    
    return frame


def draw_counts(frame, count_in, count_out, position=(50, 50)):
    """Vẽ counters với background"""
    text = f"IN: {count_in} | OUT: {count_out} | TOTAL: {count_in + count_out}"
    x, y = position
    
    (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
    cv2.rectangle(frame, (x - 10, y - text_h - 10), (x + text_w + 10, y + 10), (0, 0, 0), -1)
    cv2.rectangle(frame, (x - 10, y - text_h - 10), (x + text_w + 10, y + 10), (0, 255, 0), 2)
    
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    return frame


def draw_fps(frame, fps, position=(50, 100)):
    """Vẽ FPS info"""
    text = f"FPS: {fps:.1f}"
    x, y = position
    
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    
    return frame
