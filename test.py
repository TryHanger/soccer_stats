import sqlite3
from config import DB_PATH

def get_team_matches(team_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Включаем поддержку внешних ключей
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    query = """
    SELECT 
        matches.id_match,
        t1.team AS team1,
        t2.team AS team2,
        matches.score1,
        matches.score2,
        matches.stadium,
        matches.weather,
        matches.referee,
        matches.match_date
    FROM matches
    JOIN teams t1 ON matches.team1 = t1.id
    JOIN teams t2 ON matches.team2 = t2.id
    WHERE t1.team = ? OR t2.team = ?
    ORDER BY matches.match_date DESC;
    """
    
    cursor.execute(query, (team_name, team_name))
    matches = cursor.fetchall()
    conn.close()
    
    if matches:
        print(f"Матчи для команды '{team_name}':\n")
        for match in matches:
            print(f"ID матча: {match[0]}")
            print(f"{match[1]} {match[3]} - {match[4]} {match[2]}")
            print(f"Стадион: {match[5]}, Погода: {match[6]}, Судья: {match[7]}")
            print(f"Дата: {match[8]}\n")
    else:
        print(f"Матчи для команды '{team_name}' не найдены")

# Пример вызова
get_team_matches("Ливерпуль")