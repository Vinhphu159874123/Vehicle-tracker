"""Data Logger - Lưu events vào CSV/SQLite và tạo reports"""

import csv
import sqlite3
from datetime import datetime
import pandas as pd
import config
import os


class DataLogger:
    """Log counting events và generate reports"""
    
    def __init__(self):
        """Khởi tạo CSV và SQLite database"""
        self.csv_file = config.LOG_FILE
        self.db_file = config.DATABASE_FILE
        
        self._setup_csv()
        self._setup_database()
        
        print(f"✅ DataLogger initialized")
        print(f"   CSV: {self.csv_file}")
        print(f"   DB: {self.db_file}")
    
    def _setup_csv(self):
        """Tạo CSV file với header nếu chưa có"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'direction', 'track_id', 'class_id'])
            print(f"📝 Created CSV file: {self.csv_file}")
    
    def _setup_database(self):
        """Tạo SQLite database và tables nếu chưa có"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                direction TEXT NOT NULL,
                track_id INTEGER NOT NULL,
                class_id INTEGER NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                count_in INTEGER NOT NULL,
                count_out INTEGER NOT NULL,
                interval_seconds REAL NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"💾 Database ready: {self.db_file}")
    
    def log_event(self, event):
        """Log 1 counting event vào CSV và database"""
        timestamp_str = datetime.fromtimestamp(event['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp_str,
                event['direction'],
                event['track_id'],
                event['class_id']
            ])
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO events (timestamp, direction, track_id, class_id) VALUES (?, ?, ?, ?)',
            (timestamp_str, event['direction'], event['track_id'], event['class_id'])
        )
        conn.commit()
        conn.close()
    
    def save_summary(self, start_time, end_time, count_in, count_out):
        """Lưu summary report cho 1 khoảng thời gian"""
        interval_seconds = (end_time - start_time).total_seconds()
        
        start_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO summary (start_time, end_time, count_in, count_out, interval_seconds) VALUES (?, ?, ?, ?, ?)',
            (start_str, end_str, count_in, count_out, interval_seconds)
        )
        conn.commit()
        conn.close()
        
        print(f"\n📊 Summary ({start_str} → {end_str}):")
        print(f"   IN: {count_in} | OUT: {count_out} | TOTAL: {count_in + count_out}")
        print(f"   Duration: {interval_seconds:.0f}s")
    
    def get_stats(self, hours=24):
        """Lấy statistics từ database trong N giờ qua"""
        conn = sqlite3.connect(self.db_file)
        
        query = f"""
            SELECT * FROM events 
            WHERE timestamp > datetime('now', '-{hours} hours')
            ORDER BY timestamp
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            return {
                'total_in': 0,
                'total_out': 0,
                'hourly_stats': []
            }
        
        total_in = len(df[df['direction'] == 'IN'])
        total_out = len(df[df['direction'] == 'OUT'])
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.floor('H')
        
        hourly = df.groupby(['hour', 'direction']).size().unstack(fill_value=0)
        hourly_stats = []
        
        for idx, row in hourly.iterrows():
            hourly_stats.append({
                'hour': idx.strftime('%Y-%m-%d %H:%M'),
                'in': int(row.get('IN', 0)),
                'out': int(row.get('OUT', 0))
            })
        
        return {
            'total_in': total_in,
            'total_out': total_out,
            'hourly_stats': hourly_stats
        }
