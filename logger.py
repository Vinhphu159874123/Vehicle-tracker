"""
Data Logger
Nhiệm vụ: Lưu events vào CSV/Database, tạo summary reports
"""

import csv
import sqlite3
from datetime import datetime
import pandas as pd
import config


class DataLogger:
    """
    Log counting events và generate reports
    """
    
    def __init__(self):
        """
        TODO: Bạn cần implement
        
        Tasks:
        1. Setup CSV file (tạo file + header nếu chưa có)
        2. Setup SQLite database (tạo tables nếu chưa có)
        3. Khởi tạo counters cho summary
        
        Tables cần tạo:
        - events: id, timestamp, direction, track_id, class_id
        - summary: id, start_time, end_time, count_in, count_out, interval_seconds
        
        Hints:
        - CSV header: timestamp,direction,track_id,class_id,confidence
        - SQLite: dùng sqlite3.connect(config.DATABASE_FILE)
        """
        pass
    
    def log_event(self, event):
        """
        Log 1 counting event
        
        Args:
            event: dict từ counter.update()
                {
                    'track_id': int,
                    'direction': 'IN'/'OUT',
                    'timestamp': float,
                    'class_id': int
                }
        
        TODO: Bạn cần implement
        
        Tasks:
        1. Append vào CSV file
        2. Insert vào SQLite events table
        3. Update in-memory summary counters
        
        Hints:
        - CSV: dùng csv.writer, mode='a'
        - SQLite: dùng cursor.execute("INSERT INTO...")
        - Nhớ commit() sau insert
        """
        pass
    
    def save_summary(self, start_time, end_time, count_in, count_out):
        """
        Lưu summary report cho 1 khoảng thời gian
        
        Args:
            start_time: datetime
            end_time: datetime
            count_in: int
            count_out: int
        
        TODO: Bạn cần implement
        
        Tasks:
        1. Insert vào summary table
        2. Optional: in ra console
        
        Hints:
        - Tính interval_seconds: (end_time - start_time).total_seconds()
        """
        pass
    
    def get_stats(self, hours=24):
        """
        Lấy statistics từ database
        
        Args:
            hours: int - lấy data từ N giờ trước
        
        Returns:
            dict: {
                'total_in': int,
                'total_out': int,
                'hourly_stats': list of dict
            }
        
        TODO: Bạn cần implement
        
        Tasks:
        1. Query events từ database trong N giờ qua
        2. Tính tổng IN/OUT
        3. Group by hour để tạo hourly_stats
        
        Hints:
        - SQLite time: WHERE timestamp > datetime('now', '-24 hours')
        - Pandas groupby giúp group theo hour
        """
        pass
