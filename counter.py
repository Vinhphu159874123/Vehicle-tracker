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
        self.recent_count_events = []
        self.track_rearm_ready = defaultdict(lambda: True)
        self.verbose_logs = getattr(config, 'VERBOSE_LOGS', False)
        
        print(f"LineCounter initialized (line: {line_start} → {line_end})")
    
    def update(self, tracks):
        """Update counter và trả về events khi xe qua line"""
        events = []
        current_time = time.time()
        
        # DEBUG: In số tracks
        if self.verbose_logs and len(tracks) > 0:
            print(f"Counter received {len(tracks)} tracks")
        
        for track in tracks:
            track_id = track['track_id']
            centroid = track['centroid']
            class_id = track['class_id']
            class_name = track.get('class_name', f'class_{class_id}')

            # Re-arm only after the object moves sufficiently far from the line.
            if not self.track_rearm_ready[track_id]:
                dist_to_line = abs(self._signed_distance_to_line(centroid))
                if dist_to_line >= getattr(config, 'REARM_DISTANCE_FROM_LINE', 80):
                    self.track_rearm_ready[track_id] = True
                    if self.verbose_logs:
                        print(f"  Track #{track_id} re-armed (distance_to_line={dist_to_line:.1f}px)")
            
            self.track_history[track_id].append(centroid)
            
            if track_id not in self.track_start_time:
                self.track_start_time[track_id] = current_time
                if self.verbose_logs:
                    print(f"New track #{track_id} at {centroid}")
            
            if len(self.track_history[track_id]) < 2:
                continue
            
            prev_centroid = self.track_history[track_id][-2]
            curr_centroid = self.track_history[track_id][-1]
            
            crossed, direction = self._check_line_crossing(prev_centroid, curr_centroid)
            
            if crossed:
                if self.verbose_logs:
                    print(f"Track #{track_id} crossed line! {prev_centroid} → {curr_centroid}, direction={direction}")
            
            if not crossed or direction is None:
                continue

            if not self.track_rearm_ready[track_id]:
                if self.verbose_logs:
                    print(f"Track #{track_id} blocked by REARM (still too close to line)")
                continue
            
            # Check cooldown
            if track_id in self.counted_tracks:
                time_since_counted = current_time - self.counted_tracks[track_id]
                if time_since_counted < config.COUNTING_COOLDOWN:
                    if self.verbose_logs:
                        print(f"  Track #{track_id} blocked by COOLDOWN ({time_since_counted:.1f}s < {config.COUNTING_COOLDOWN}s)")
                    continue

            # Cross-track duplicate suppression: block near-identical crossing events
            duplicate_window = getattr(config, 'DUPLICATE_EVENT_WINDOW', 2.0)
            duplicate_distance = getattr(config, 'DUPLICATE_EVENT_DISTANCE', 220)
            is_duplicate = False
            for recent in reversed(self.recent_count_events):
                dt = current_time - recent['timestamp']
                if dt > duplicate_window:
                    break
                if recent['direction'] != direction:
                    continue
                if recent['class_name'] != class_name:
                    continue

                dist = np.sqrt(
                    (curr_centroid[0] - recent['centroid'][0])**2 +
                    (curr_centroid[1] - recent['centroid'][1])**2
                )
                if dist <= duplicate_distance:
                    is_duplicate = True
                    if self.verbose_logs:
                        print(
                            f"  Track #{track_id} blocked by DUPLICATE "
                            f"(dt={dt:.2f}s, dist={dist:.0f}px, class={class_name}, dir={direction})"
                        )
                    break

            if is_duplicate:
                continue
            
            # Check track age
            track_age = current_time - self.track_start_time[track_id]
            if track_age < config.MIN_TRACK_AGE:
                if self.verbose_logs:
                    print(f"Track #{track_id} blocked by AGE ({track_age:.2f}s < {config.MIN_TRACK_AGE}s)")
                continue
            
            # Check displacement
            first_centroid = self.track_history[track_id][0]
            total_displacement = np.sqrt(
                (curr_centroid[0] - first_centroid[0])**2 + 
                (curr_centroid[1] - first_centroid[1])**2
            )
            if total_displacement < config.MIN_DISPLACEMENT:
                if self.verbose_logs:
                    print(f"Track #{track_id} blocked by DISPLACEMENT ({total_displacement:.0f}px < {config.MIN_DISPLACEMENT}px)")
                continue
            
            # COUNT SUCCESS!
            if direction == 'IN':
                self.count_in += 1
            elif direction == 'OUT':
                self.count_out += 1
            
            self.counted_tracks[track_id] = current_time
            self.track_rearm_ready[track_id] = False
            self.recent_count_events.append({
                'timestamp': current_time,
                'centroid': curr_centroid,
                'direction': direction,
                'class_name': class_name
            })

            # Keep only recent events to bound memory and speed up duplicate checks
            self.recent_count_events = [
                e for e in self.recent_count_events
                if (current_time - e['timestamp']) <= duplicate_window
            ]
            if self.verbose_logs:
                print(f"COUNTED Track #{track_id} as {direction}! (IN={self.count_in}, OUT={self.count_out})")
            
            event = {
                'track_id': track_id,
                'direction': direction,
                'timestamp': current_time,
                'class_id': class_id,
                'class_name': class_name
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
                direction = 'OUT'
            else:
                direction = 'IN'
            
            if self.verbose_logs:
                print(f"  Line crossed! p1={p1} (sign={sign1:.0f}) → p2={p2} (sign={sign2:.0f}) → {direction}")
            return True, direction
        
        return False, None

    def _signed_distance_to_line(self, point):
        """Signed perpendicular distance from point to counting line in pixels."""
        x1, y1 = self.line_start
        x2, y2 = self.line_end
        px, py = point

        numerator = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
        denom = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if denom == 0:
            return 0.0
        return numerator / denom
    
    def get_counts(self):
        """Trả về số lượng xe IN/OUT/TOTAL"""
        return {
            'in': self.count_in,
            'out': self.count_out,
            'total': self.count_in + self.count_out
        }
