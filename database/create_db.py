import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scraper.config import DB_PATH


def create_db(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Таблица команд
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
            )
    """)

    # Таблица матчей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER NOT NULL,
            stat_name TEXT NOT NULL,
            team1_value REAL,
            team2_value REAL,
            FOREIGN KEY (match_id) REFERENCES matches(id)
        )
    """)

    # Таблица статистики
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER,
            stat_name TEXT,
            team1_value REAL,
            team2_value REAL,
            FOREIGN KEY (match_id) REFERENCES matches(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ База данных создана!")
