"""
Visualization Utilities
Các hàm vẽ bbox, line, counts lên frame
"""

import cv2
import numpy as np


def draw_detections(frame, detections, color=(0, 255, 0)):
    """
    Vẽ bounding boxes lên frame
    
    Args:
        frame: numpy array
        detections: list of dict từ detector
        color: BGR tuple
    
    Returns:
        frame: frame đã vẽ
    
    TODO: Bạn cần implement
    
    Tasks:
    1. Loop qua detections
    2. Vẽ rectangle: cv2.rectangle()
    3. Vẽ label (class + confidence): cv2.putText()
    """
    pass


def draw_tracks(frame, tracks, color=(255, 0, 0)):
    """
    Vẽ tracked objects với track_id
    
    Args:
        frame: numpy array
        tracks: list of dict từ tracker
        color: BGR tuple
    
    Returns:
        frame: frame đã vẽ
    
    TODO: Bạn cần implement
    
    Tasks:
    1. Vẽ bbox với màu khác detection
    2. Vẽ track_id lên mỗi bbox
    3. Optional: vẽ centroid (chấm tròn nhỏ)
    """
    pass


def draw_roi(frame, roi_polygon, color=(0, 255, 255), alpha=0.3):
    """
    Vẽ ROI polygon (semi-transparent)
    
    Args:
        frame: numpy array
        roi_polygon: numpy array hoặc list of tuples
        color: BGR tuple
        alpha: transparency (0-1)
    
    Returns:
        frame: frame đã vẽ
    
    TODO: Bạn cần implement
    
    Tasks:
    1. Tạo overlay layer
    2. Fill polygon: cv2.fillPoly()
    3. Blend với frame: cv2.addWeighted()
    4. Vẽ contour: cv2.polylines()
    """
    pass


def draw_line(frame, line_start, line_end, color=(0, 0, 255), thickness=3):
    """
    Vẽ counting line
    
    Args:
        frame: numpy array
        line_start: tuple (x1, y1)
        line_end: tuple (x2, y2)
        color: BGR tuple
        thickness: int
    
    Returns:
        frame: frame đã vẽ
    
    TODO: Bạn cần implement
    
    Tasks:
    1. Vẽ line: cv2.line()
    2. Vẽ arrow heads ở 2 đầu (optional)
    """
    pass


def draw_counts(frame, count_in, count_out, position=(50, 50)):
    """
    Vẽ counters lên frame
    
    Args:
        frame: numpy array
        count_in: int
        count_out: int
        position: tuple (x, y) top-left
    
    Returns:
        frame: frame đã vẽ
    
    TODO: Bạn cần implement
    
    Tasks:
    1. Vẽ background box (semi-transparent)
    2. Vẽ text "IN: XX | OUT: YY"
    3. Dùng font to, màu nổi bật
    
    Hints:
    - cv2.rectangle() cho background
    - cv2.putText() cho text
    - Font: cv2.FONT_HERSHEY_SIMPLEX
    """
    pass


def draw_fps(frame, fps, position=(50, 100)):
    """
    Vẽ FPS lên frame
    
    TODO: Simple, bạn tự implement
    """
    pass
