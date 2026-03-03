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
        
        # DEBUG: In số tracks
        if len(tracks) > 0:
            print(f"🔍 Counter received {len(tracks)} tracks")
        
        for track in tracks:
            track_id = track['track_id']
            centroid = track['centroid']
            class_id = track['class_id']
            
            self.track_history[track_id].append(centroid)
            
            if track_id not in self.track_start_time:
                self.track_start_time[track_id] = current_time
                print(f"   🆕 New track #{track_id} at {centroid}")
            
            if len(self.track_history[track_id]) < 2:
                continue
            
            prev_centroid = self.track_history[track_id][-2]
            curr_centroid = self.track_history[track_id][-1]
            
            crossed, direction = self._check_line_crossing(prev_centroid, curr_centroid)
            
            if crossed:
                print(f"   🚦 Track #{track_id} crossed line! {prev_centroid} → {curr_centroid}, direction={direction}")
            
            if not crossed or direction is None:
                continue
            
            # Check cooldown
            if track_id in self.counted_tracks:
                time_since_counted = current_time - self.counted_tracks[track_id]
                if time_since_counted < config.COUNTING_COOLDOWN:
                    print(f"   ⏸️ Track #{track_id} blocked by COOLDOWN ({time_since_counted:.1f}s < {config.COUNTING_COOLDOWN}s)")
                    continue
            
            # Check track age
            track_age = current_time - self.track_start_time[track_id]
            if track_age < config.MIN_TRACK_AGE:
                print(f"   ⏸️ Track #{track_id} blocked by AGE ({track_age:.2f}s < {config.MIN_TRACK_AGE}s)")
                continue
            
            # Check displacement
            first_centroid = self.track_history[track_id][0]
            total_displacement = np.sqrt(
                (curr_centroid[0] - first_centroid[0])**2 + 
                (curr_centroid[1] - first_centroid[1])**2
            )
            if total_displacement < config.MIN_DISPLACEMENT:
                print(f"   ⏸️ Track #{track_id} blocked by DISPLACEMENT ({total_displacement:.0f}px < {config.MIN_DISPLACEMENT}px)")
                continue
            
            # COUNT SUCCESS!
            if direction == 'IN':
                self.count_in += 1
            elif direction == 'OUT':
                self.count_out += 1
            
            self.counted_tracks[track_id] = current_time
            print(f"   ✅ COUNTED Track #{track_id} as {direction}! (IN={self.count_in}, OUT={self.count_out})")
            
            event = {
                'track_id': track_id,
                'direction': direction,
                'timestamp': current_time,
                'class_id': class_id
            }
            events.append(event)
        
        return events
    
    def _check_line_crossing(self, p1, p2):
        """Check xem track có cắt line không, trả về direction - dùng cross product cho đường chéo"""
        
        # Lấy line coordinates
        x1, y1 = self.line_start
        x2, y2 = self.line_end
        
        # Cross product để check 2 bên của line
        # Nếu p1 và p2 ở 2 bên khác nhau của line → crossed
        def sign(px, py):
            """Tính cross product: (line_vec) × (point_vec)"""
            return (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
        
        sign1 = sign(p1[0], p1[1])
        sign2 = sign(p2[0], p2[1])
        
        # Nếu khác dấu → crossed line
        if sign1 * sign2 < 0:
            # Xác định direction dựa vào dấu
            # sign > 0: bên phải line (hoặc phía trên)
            # sign < 0: bên trái line (hoặc phía dưới)
            if sign1 > 0 and sign2 < 0:
                direction = 'IN'
            else:
                direction = 'OUT'
            
            print(f"   🚦 Line crossed! p1={p1} (sign={sign1:.0f}) → p2={p2} (sign={sign2:.0f}) → {direction}")
            return True, direction
        
        return False, None
    
    def get_counts(self):
        """Trả về số lượng xe IN/OUT/TOTAL"""
        return {
            'in': self.count_in,
            'out': self.count_out,
            'total': self.count_in + self.count_out
        }
