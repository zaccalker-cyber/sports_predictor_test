import sqlite3
from pathlib import Path



# BASE_DIR = Path(__file__).resolve().parent

# DB_PATH = BASE_DIR / "data" / "sports_events_test.db"

# conn = sqlite3.connect(DB_PATH)
# cursor = conn.cursor()

# def create_prediction():
    
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS predictions (
#         event_id TEXT PRIMARY KEY,
#         home_win_probability REAL,
#         away_win_probability REAL,
#         draw_probability REAL
#     )
#     """)
#     conn.commit()