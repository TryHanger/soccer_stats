import sqlite3
from datetime import datetime
from config import DB_PATH


def get_existing_matches(team_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id_match, match_date FROM matches
        WHERE team1 = ? OR team2 = ?
        ORDER BY match_date ASC
    """, (team_id, team_id))
    
    matches = cursor.fetchall()
    conn.close()
    
    # Возвращаем список матчей в виде словарей
    return [{"id": row[0], "date": datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")} for row in matches]