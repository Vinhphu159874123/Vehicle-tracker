import numpy as np
from collections import defaultdict
import time
import config


class LineCounter:
    """Đếm xe qua line, phân biệt IN/OUT"""
    
    def __init__(self, line_start, line_end):
        """Khởi tạo counter với line coordinates"""
        self.line_start = line_start
        self.line_end = line_end
        
        if config.LINE_DIRECTION == "horizontal":
            self.line_y = line_start[1]
        else:
            self.line_x = line_start[0]
        
        self.count_in = 0
        self.count_out = 0
        
        self.track_history = defaultdict(list)
        self.counted_tracks = {}
        self.track_start_time = {}
        
        print(f"✅ LineCounter initialized (line: {line_start} → {line_end})")
    
    def update(self, tracks):
        """Update counter và trả về events khi xe qua line"""
        events = []
        current_time = time.time()
        
        for track in tracks:
            track_id = track['track_id']
            centroid = track['centroid']
            class_id = track['class_id']
            
            self.track_history[track_id].append(centroid)
            
            if track_id not in self.track_start_time:
                self.track_start_time[track_id] = current_time
            
            if len(self.track_history[track_id]) < 2:
                continue
            
            prev_centroid = self.track_history[track_id][-2]
            curr_centroid = self.track_history[track_id][-1]
            
            crossed, direction = self._check_line_crossing(prev_centroid, curr_centroid)
            
            if not crossed or direction is None:
                continue
            
            if track_id in self.counted_tracks:
                time_since_counted = current_time - self.counted_tracks[track_id]
                if time_since_counted < config.COUNTING_COOLDOWN:
                    continue
            
            track_age = current_time - self.track_start_time[track_id]
            if track_age < config.MIN_TRACK_AGE:
                continue
            
            first_centroid = self.track_history[track_id][0]
            total_displacement = np.sqrt(
                (curr_centroid[0] - first_centroid[0])**2 + 
                (curr_centroid[1] - first_centroid[1])**2
            )
            if total_displacement < config.MIN_DISPLACEMENT:
                continue
            
            if direction == 'IN':
                self.count_in += 1
            elif direction == 'OUT':
                self.count_out += 1
            
            self.counted_tracks[track_id] = current_time
            
            event = {
                'track_id': track_id,
                'direction': direction,
                'timestamp': current_time,
                'class_id': class_id
            }
            events.append(event)
        
        return events
    
    def _check_line_crossing(self, p1, p2):
        """Check xem track có cắt line không, trả về direction"""
        if config.LINE_DIRECTION == "horizontal":
            line_y = self.line_y
            
            if p1[1] < line_y <= p2[1]:
                return True, 'IN'
            elif p1[1] > line_y >= p2[1]:
                return True, 'OUT'
            else:
                return False, None
        else:
            line_x = self.line_x
            
            if p1[0] < line_x <= p2[0]:
                return True, 'IN'
            elif p1[0] > line_x >= p2[0]:
                return True, 'OUT'
            else:
                return False, None
    
    def get_counts(self):
        """Trả về số lượng xe IN/OUT/TOTAL"""
        return {
            'in': self.count_in,
            'out': self.count_out,
            'total': self.count_in + self.count_out
        }
