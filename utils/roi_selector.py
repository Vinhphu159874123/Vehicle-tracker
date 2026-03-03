"""ROI Selector - Tool chọn ROI polygon và counting line"""

import cv2
import numpy as np
import sys
import os

# Add parent directory to path để import config
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import config


class ROISelector:
    """Interactive tool để chọn ROI và line"""
    
    def __init__(self, video_source):
        """Khởi tạo với video source và lấy first frame"""
        self.cap = cv2.VideoCapture(video_source)
        
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video source: {video_source}")
        
        ret, self.frame = self.cap.read()
        if not ret:
            raise ValueError("Cannot read first frame from video")
        
        self.original_frame = self.frame.copy()
        
        self.roi_points = []
        self.line_points = []
        self.current_point = None
        
        print(f"✅ ROISelector initialized with frame size: {self.frame.shape[:2]}")
    
    def select_roi(self):
        """Cho phép user vẽ polygon ROI bằng chuột"""
        self.roi_points = []
        self.frame = self.original_frame.copy()
        window_name = "Select ROI (Left click: add point, Right click/C: close, R: reset, Q: quit)"
        
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self._roi_mouse_callback)
        
        print("\n=== ROI Selection ===")
        print("Left click: thêm point vào polygon")
        print("Right click hoặc 'c': đóng polygon")
        print("'r': reset")
        print("'q': hoàn thành\n")
        
        while True:
            display_frame = self.frame.copy()
            
            if len(self.roi_points) > 0:
                for i, pt in enumerate(self.roi_points):
                    cv2.circle(display_frame, pt, 5, (0, 255, 0), -1)
                    if i > 0:
                        cv2.line(display_frame, self.roi_points[i-1], pt, (0, 255, 0), 2)
                
                if self.current_point is not None:
                    cv2.line(display_frame, self.roi_points[-1], self.current_point, (0, 255, 0), 1)
            
            cv2.imshow(window_name, display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.roi_points = []
                self.frame = self.original_frame.copy()
                print("Reset ROI")
            elif key == ord('c') and len(self.roi_points) >= 3:
                print(f"ROI polygon closed with {len(self.roi_points)} points")
                break
        
        cv2.destroyAllWindows()
        
        if len(self.roi_points) >= 3:
            self.frame = self.original_frame.copy()
            cv2.polylines(self.frame, [np.array(self.roi_points)], True, (0, 255, 0), 2)
            return self.roi_points
        else:
            print("⚠️ ROI không hợp lệ (cần ít nhất 3 điểm)")
            return None
    
    def select_line(self):
        """Cho phép user vẽ line bằng chuột"""
        self.line_points = []
        window_name = "Select Line (Click 2 points, R: reset, Q: quit)"
        
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self._line_mouse_callback)
        
        print("\n=== Line Selection ===")
        print("Click 2 điểm để tạo counting line")
        print("'r': reset")
        print("'q': hoàn thành\n")
        
        while True:
            display_frame = self.frame.copy()
            
            if len(self.line_points) == 1:
                cv2.circle(display_frame, self.line_points[0], 5, (0, 0, 255), -1)
                if self.current_point is not None:
                    cv2.line(display_frame, self.line_points[0], self.current_point, (0, 0, 255), 2)
            elif len(self.line_points) == 2:
                cv2.line(display_frame, self.line_points[0], self.line_points[1], (0, 0, 255), 3)
                cv2.circle(display_frame, self.line_points[0], 5, (0, 255, 0), -1)
                cv2.circle(display_frame, self.line_points[1], 5, (0, 255, 0), -1)
            
            cv2.imshow(window_name, display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.line_points = []
                print("Reset line")
        
        cv2.destroyAllWindows()
        
        if len(self.line_points) == 2:
            return tuple(self.line_points)
        else:
            print("⚠️ Line không hợp lệ (cần 2 điểm)")
            return None
    
    def _roi_mouse_callback(self, event, x, y, flags, param):
        """Mouse callback cho ROI selection"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.roi_points.append((x, y))
            print(f"Added point {len(self.roi_points)}: ({x}, {y})")
        
        elif event == cv2.EVENT_RBUTTONDOWN:
            if len(self.roi_points) >= 3:
                print(f"Closed polygon with {len(self.roi_points)} points")
        
        elif event == cv2.EVENT_MOUSEMOVE:
            self.current_point = (x, y)
    
    def _line_mouse_callback(self, event, x, y, flags, param):
        """Mouse callback cho line selection"""
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.line_points) < 2:
                self.line_points.append((x, y))
                print(f"Added point {len(self.line_points)}: ({x}, {y})")
        
        elif event == cv2.EVENT_MOUSEMOVE:
            self.current_point = (x, y)
    
    def save_to_config(self, roi_points, line):
        """Save ROI và line vào config.py"""
        if roi_points is None or line is None:
            print("⚠️ Không thể save: ROI hoặc line không hợp lệ")
            return
        
        # Get config.py path (trong parent directory)
        config_path = os.path.join(parent_dir, 'config.py')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        with open(config_path, 'w', encoding='utf-8') as f:
            for line_text in lines:
                if line_text.startswith('ROI_POLYGON'):
                    f.write(f"ROI_POLYGON = {roi_points}\n")
                elif line_text.startswith('LINE_START'):
                    f.write(f"LINE_START = {line[0]}\n")
                elif line_text.startswith('LINE_END'):
                    f.write(f"LINE_END = {line[1]}\n")
                else:
                    f.write(line_text)
        
        print("\n✅ Saved to config.py")
        print(f"ROI_POLYGON = {roi_points}")
        print(f"LINE_START = {line[0]}")
        print(f"LINE_END = {line[1]}")


if __name__ == "__main__":
    """Run ROI & Line selector tool"""
    print("=== ROI & Line Selector ===")
    print("Instructions:")
    print("1. Vẽ polygon ROI (left click để thêm điểm, right click để đóng)")
    print("2. Vẽ line (click 2 điểm)")
    print("3. Results sẽ được save vào config.py")
    print()
    
    video_source = sys.argv[1] if len(sys.argv) > 1 else config.VIDEO_SOURCE
    
    try:
        selector = ROISelector(video_source)
        
        roi_points = selector.select_roi()
        if roi_points is None:
            print("❌ ROI selection failed")
            sys.exit(1)
        
        line = selector.select_line()
        if line is None:
            print("❌ Line selection failed")
            sys.exit(1)
        
        selector.save_to_config(roi_points, line)
        
        selector.cap.release()
        cv2.destroyAllWindows()
        
        print("\n✅ ROI & Line selector completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

