import sqlite3
from config import DB_PATH

def save_name_league(league_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO leagues (league_name) VALUES (?)", (league_name,))
    result = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return result
    
def get_id_by_name(league_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM leagues WHERE league_name = ?", (league_name,))
    result = cursor.fecthone()
    conn.close()
    
    return result[0] if result else None

def get_id_by_url(url_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM leagues WHERE url_id = ?", (url_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None
    
    
def save_league(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO leagues (url_id, league_name, country, start_date, end_date, matches_played, total_matches)
        VALUES (?, ?, ?, ?, ?, ?, ?)               
    """, (data["url_id"], data["league_name"], data["country"], data["start_date"], data["end_date"], data["matches_played"], data["total_matches"]))
    
    league_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return league_id