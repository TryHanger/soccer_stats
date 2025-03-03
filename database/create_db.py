import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DB_PATH


def create_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Включаем поддержку внешних ключей
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Таблица команд
    cursor.execute("""
        CREATE TABLE teams (
            id INTEGER PRIMARY KEY,
            team TEXT NOT NULL
        );
    """)

    # Таблица матчей
    cursor.execute("""
        CREATE TABLE matches (
            id_match INTEGER PRIMARY KEY,
            team1 INTEGER,
            team2 INTEGER,
            score1 INTEGER,
            score2 INTEGER,
            stadium TEXT,
            weather TEXT,
            referee TEXT,
            match_date DATE,
            FOREIGN KEY (team1) REFERENCES teams(id),
            FOREIGN KEY (team2) REFERENCES teams(id)
        );
    """)

    # Таблица статистики
    cursor.execute("""
        CREATE TABLE stats (
            id_match INTEGER,
            xg1 REAL,
            xg2 REAL,
            shots1 REAL,
            shots2 REAL,
            shotsongoal1 REAL,
            shotsongoal2 REAL,
            possession1 REAL,
            possession2 REAL,
            corner_kicks1 REAL,
            corner_kicks2 REAL,
            infringements1 REAL,
            infringements2 REAL,
            offsides1 REAL,
            offsides2 REAL,
            yellow_card1 REAL,
            yellow_card2 REAL,
            red_card1 REAL,
            red_card2 REAL,
            passes1 REAL,
            passes2 REAL,
            pass_accuracy1 REAL,
            pass_accuracy2 REAL,
            PRIMARY KEY (id_match),
            FOREIGN KEY (id_match) REFERENCES matches(id_match) ON DELETE CASCADE
        );
    """)
    
    cursor.execute("""
        CREATE TABLE commands (
            id_match INTEGER,
            id_team INTEGER,
            player1 TEXT,
            player2 TEXT,
            player3 TEXT,
            player4 TEXT,
            player5 TEXT,
            player6 TEXT,
            player7 TEXT,
            player8 TEXT,
            player9 TEXT,
            player10 TEXT,
            player11 TEXT,
            coach TEXT,
            PRIMARY KEY (id_match, id_team),
            FOREIGN KEY (id_match) REFERENCES matches(id_match) ON DELETE CASCADE,
            FOREIGN KEY (id_team) REFERENCES teams(id)
        );
    """)

    conn.commit()
    conn.close()
    print("✅ База данных создана!")
