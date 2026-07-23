import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "data" / "sports_events_test.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def create_database():
    

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        event_id TEXT PRIMARY KEY,

        season INTEGER,
        round INTEGER,

        event_date TEXT,
        event_time TEXT,

        home_team TEXT,
        away_team TEXT,

        home_score INTEGER,
        away_score INTEGER,

        venue TEXT,

        status TEXT,

        winner INTEGER
    )
    """)
    conn.commit()


def insert_event(event):

    cursor.execute("""
    INSERT OR REPLACE INTO events
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event["event_id"],
        event["season"],
        event["round"],
        event["event_date"],
        event["event_time"],
        event["home_team"],
        event["away_team"],
        event["home_score"],
        event["away_score"],
        event["venue"],
        event["status"],
        event["winner"]
    ))

def save():
    conn.commit()

def close():
    conn.close()