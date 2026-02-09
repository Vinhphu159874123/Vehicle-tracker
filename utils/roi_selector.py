"""
ROI Selector Tool
Tool tương tác để chọn ROI polygon và line position
"""

import cv2
import numpy as np
import sys
sys.path.append('..')
import config


class ROISelector:
    """
    Interactive tool để chọn ROI và line
    """
    
    def __init__(self, video_source):
        """
        Args:
            video_source: path to video hoặc RTSP URL
        
        TODO: Bạn cần implement
        
        Tasks:
        1. Open video/RTSP
        2. Grab first frame
        3. Initialize mouse callback data structures
        
        Hints:
        - cv2.VideoCapture(video_source)
        - cap.read() để lấy frame
        """
        pass
    
    def select_roi(self):
        """
        Cho phép user vẽ polygon ROI bằng chuột
        
        Returns:
            roi_points: list of tuples [(x1,y1), (x2,y2), ...]
        
        TODO: Bạn cần implement
        
        Tasks:
        1. Tạo window
        2. Set mouse callback
        3. User click để vẽ polygon (left click = thêm điểm)
        4. Right click hoặc 'c' = close polygon
        5. 'r' = reset, 'q' = quit
        
        Hints:
        - cv2.setMouseCallback(window_name, self._mouse_callback)
        - cv2.polylines() để vẽ polygon preview
        
        Instructions for user:
        - Left click: thêm điểm
        - Right click hoặc 'c': đóng polygon
        - 'r': reset
        - 'q': quit và save
        """
        pass
    
    def select_line(self):
        """
        Cho phép user vẽ line bằng chuột
        
        Returns:
            line: tuple ((x1,y1), (x2,y2))
        
        TODO: Bạn cần implement
        
        Tasks:
        1. User click 2 điểm để tạo line
        2. First click = start, second click = end
        3. 'r' = reset, 'q' = save
        
        Hints:
        - cv2.line() để vẽ line preview
        
        Instructions:
        - Click 2 điểm để tạo line
        - 'r': reset
        - 'q': save
        """
        pass
    
    def save_to_config(self, roi_points, line):
        """
        Save ROI và line vào config.py
        
        Args:
            roi_points: list of tuples
            line: tuple of 2 tuples
        
        TODO: Bạn cần implement
        
        Tasks:
        1. Đọc config.py
        2. Update ROI_POLYGON và LINE_START/LINE_END
        3. Ghi lại file
        
        Hints:
        - Đọc file as text, find dòng ROI_POLYGON, replace
        - Hoặc dùng configparser nếu muốn
        """
        pass


if __name__ == "__main__":
    """
    Usage:
    python roi_selector.py
    
    Hoặc:
    python roi_selector.py path/to/video.mp4
    """
    print("=== ROI & Line Selector ===")
    print("Instructions:")
    print("1. Vẽ polygon ROI (left click để thêm điểm, right click để đóng)")
    print("2. Vẽ line (click 2 điểm)")
    print("3. Results sẽ được save vào config.py")
    print()
    
    # TODO: Implement main flow
    # 1. Get video source (from argv or use config.VIDEO_SOURCE)
    # 2. selector = ROISelector(video_source)
    # 3. roi_points = selector.select_roi()
    # 4. line = selector.select_line()
    # 5. selector.save_to_config(roi_points, line)
    pass
