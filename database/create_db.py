import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DB_PATH


def enable_foreign_keys(cursor):
    cursor.execute("PRAGMA foreign_keys = ON;")


def create_leagues_table(cursor):
    cursor.execute("""
        CREATE TABLE leagues (
            id INTEGER PRIMARY KEY,
            url_id  INTEGER,
            league_name TEXT NOT NULL,
            country TEXT,
            start_date DATE,
            end_date DATE,
            matches_played INTEGER,
            total_matches INTEGER
        );
    """)

def create_teams_table(cursor):
    cursor.execute("""
        CREATE TABLE teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team TEXT NOT NULL,
            stadium TEXT,
            UNIQUE (team)
        );
    """)


def create_matches_table(cursor):
    cursor.execute("""
        CREATE TABLE matches (
            id_match INTEGER PRIMARY KEY,
            league_id INTEGER,
            home_team INTEGER,
            away_team INTEGER,
            score_home INTEGER,
            score_away INTEGER,
            stadium TEXT,
            weather TEXT,
            referee TEXT,
            match_date DATE,
            FOREIGN KEY (league_id) REFERENCES leagues(id),
            FOREIGN KEY (home_team) REFERENCES teams(id),
            FOREIGN KEY (away_team) REFERENCES teams(id)
        );
    """)


def create_stats_table(cursor):
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


def create_commands_table(cursor):
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

def create_db():
    if os.path.exists(DB_PATH):
        print("✅ База данных уже существует. Создание не требуется.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        enable_foreign_keys(cursor)
        create_leagues_table(cursor)
        create_teams_table(cursor)
        create_matches_table(cursor)
        create_stats_table(cursor)
        create_commands_table(cursor)

        conn.commit()
        print("✅ База данных успешно создана!")
    except Exception as e:
        print(f"❌ Ошибка при создании базы данных: {e}")
        conn.rollback()
    finally:
        conn.close()


def recreate_db():
    """Перезаписывает базу данных: удаляет старую и создаёт новую."""
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print("🗑️ Старая база данных удалена.")
        except Exception as e:
            print(f"❌ Ошибка при удалении базы данных: {e}")
            return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        enable_foreign_keys(cursor)
        create_leagues_table(cursor)
        create_teams_table(cursor)
        create_matches_table(cursor)
        create_stats_table(cursor)
        create_commands_table(cursor)

        conn.commit()
        print("✅ Новая база данных успешно создана!")
    except Exception as e:
        print(f"❌ Ошибка при создании базы данных: {e}")
        conn.rollback()
    finally:
        conn.close()