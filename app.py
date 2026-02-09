"""
Flask Dashboard
Real-time web interface để xem stream + statistics
"""

from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO, emit
import cv2
import threading
import time
from datetime import datetime

import config
from main import VehicleCountingSystem


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables
counting_system = None
current_frame = None
current_stats = {'count_in': 0, 'count_out': 0}


def video_processing_thread():
    """
    Background thread chạy counting system
    
    TODO: Bạn cần implement
    
    Tasks:
    1. Khởi tạo VehicleCountingSystem
    2. Loop process frames
    3. Update global current_frame và current_stats
    4. Emit stats qua SocketIO (real-time update)
    
    Hints:
    - socketio.emit('stats_update', data)
    - socketio.sleep(0.1) thay vì time.sleep()
    """
    pass


def generate_frames():
    """
    Generator function cho video stream
    
    Yields:
        bytes: JPEG frame
    
    TODO: Bạn cần implement
    
    Tasks:
    1. Lấy current_frame từ global
    2. Resize nếu cần (theo config.STREAM_FPS)
    3. Encode thành JPEG: cv2.imencode('.jpg', frame)
    4. Yield frame theo format multipart/x-mixed-replace
    
    Hints:
    - yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    """
    pass


@app.route('/')
def index():
    """
    Main dashboard page
    
    TODO: Render template
    """
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    """
    Video stream endpoint
    
    TODO: Return Response với generate_frames()
    """
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/stats')
def get_stats():
    """
    API endpoint để lấy statistics
    
    Returns:
        JSON: {
            'count_in': int,
            'count_out': int,
            'timestamp': str,
            'hourly_stats': [...]
        }
    
    TODO: Bạn cần implement
    
    Tasks:
    1. Lấy stats từ logger.get_stats()
    2. Combine với current counts
    3. Return JSON
    """
    pass


@socketio.on('connect')
def handle_connect():
    """
    WebSocket connection handler
    
    TODO: Emit initial stats khi client connect
    """
    print('Client connected')
    emit('stats_update', current_stats)


def main():
    """
    Start Flask app
    
    TODO: Bạn cần implement
    
    Tasks:
    1. Start video_processing_thread trong background
    2. Run socketio.run(app, ...)
    
    Hints:
    - thread = threading.Thread(target=video_processing_thread, daemon=True)
    - thread.start()
    """
    print("=== Flask Dashboard ===")
    print(f"Starting server at http://{config.FLASK_HOST}:{config.FLASK_PORT}")
    print()
    
    # TODO: Start background thread
    
    # TODO: Run Flask
    # socketio.run(app, host=config.FLASK_HOST, port=config.FLASK_PORT, debug=False)
    pass


if __name__ == '__main__':
    main()
