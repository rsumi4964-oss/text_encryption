import sqlite3
import sys
import os

# Allow running this script directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DB_PATH

def init_db():
    print(f"Initializing database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user          TEXT,
            original_text TEXT,
            data          TEXT,
            timestamp     DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully ✅")

if __name__ == "__main__":
    init_db()
