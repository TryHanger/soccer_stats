import sqlite3
from config import DB_PATH

def save_league(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO leagues (url_id, league_name, country, start_date, end_date, matches_played, total_matches)
        VALUES (?, ?, ?, ?, ?, ?, ?)               
    """, (data["url_id"], data["league_name"], data["country"], data["start_date"], data["end_date"], data["matches_played"], data["total_matches"]))
    conn.commit()
    conn.close()
    
def save_unknown_league(league_name, leagues_dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO leagues (league_name)
        VALUES (?)               
    """, (league_name))
    
    league_id = cursor.lastrowid  # Получаем ID только что добавленной лиги
    conn.commit()
    conn.close()
    
    print(f"🟢 Лига '{league_name}' сохранена в БД (ID: {league_id})")
    return league_id


def get_league_id_from_db(league_name):
    """
    Ищем ID лиги в базе данных по названию.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM leagues WHERE name = ?", (league_name,))
    league = cursor.fetchone()
    
    conn.close()
    
    return league[0] if league else None