"""
Line Crossing Counter
Nhiệm vụ: Đếm xe qua line, phân biệt IN/OUT, chống đếm sai
"""

import numpy as np
from collections import defaultdict
import time
import config


class LineCounter:
    """
    Đếm vehicles crossing line với anti-noise filtering
    """
    
    def __init__(self, line_start, line_end):
        """
        Args:
            line_start: tuple (x1, y1)
            line_end: tuple (x2, y2)
        
        TODO: Bạn cần implement
        
        Tasks:
        1. Lưu line coordinates
        2. Khởi tạo counters: count_in, count_out
        3. Khởi tạo tracking dictionaries:
           - track_history: lưu centroids qua thời gian {track_id: [(x1,y1), (x2,y2), ...]}
           - counted_tracks: lưu tracks đã đếm {track_id: timestamp}
           - track_start_time: lưu thời điểm track xuất hiện {track_id: timestamp}
        """
        pass
    
    def update(self, tracks):
        """
        Update counter với tracks từ frame hiện tại
        
        Args:
            tracks: list of dict từ tracker.update()
        
        Returns:
            events: list of dict, mỗi event có:
                {
                    'track_id': int,
                    'direction': 'IN' hoặc 'OUT',
                    'timestamp': float,
                    'class_id': int
                }
        
        TODO: Bạn cần implement
        
        Tasks:
        1. Loop qua tất cả tracks
        2. Lưu centroid vào track_history
        3. Check line crossing:
           - Lấy centroid hiện tại và centroid trước đó
           - Check xem đoạn thẳng có cắt line không
        4. Apply anti-noise filters:
           - Min track age: track phải tồn tại >= MIN_TRACK_AGE frames
           - Min displacement: di chuyển >= MIN_DISPLACEMENT pixels
           - Cooldown: không đếm lại trong COUNTING_COOLDOWN giây
        5. Phân biệt hướng IN/OUT
        6. Update counters và return events
        
        Hints:
        - Check line crossing: dùng ccw algorithm hoặc cv2.clipLine
        - Direction (nếu horizontal line):
            - y trước < line_y và y sau >= line_y → IN (từ trên xuống)
            - y trước >= line_y và y sau < line_y → OUT (từ dưới lên)
        """
        pass
    
    def _check_line_crossing(self, p1, p2):
        """
        Check xem đoạn thẳng p1-p2 có cắt line không
        
        Args:
            p1: tuple (x1, y1) - điểm trước
            p2: tuple (x2, y2) - điểm hiện tại
        
        Returns:
            crossed: bool
            direction: 'IN', 'OUT', hoặc None
        
        TODO: Bạn cần implement
        
        Hints:
        - Nếu line horizontal (y cố định):
            - Check: (p1[1] < line_y < p2[1]) hoặc (p1[1] > line_y > p2[1])
        - Direction:
            - p1[1] < line_y < p2[1]: IN (đi từ trên xuống)
            - p1[1] > line_y > p2[1]: OUT (đi từ dưới lên)
        """
        pass
    
    def get_counts(self):
        """
        Return count_in và count_out hiện tại
        """
        pass
