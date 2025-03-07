import sqlite3
from config import DB_PATH

def match_exists(match_id):
    """Проверка, существует ли матч в базе данных."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM matches WHERE id_match = ?", (match_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def save_team(team_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM teams WHERE team = ?", (team_name, ))
    result = cursor.fetchone()
    
    if result:
        team_id = result[0]
    else:
        cursor.execute("INSERT INTO teams (team) VALUES (?)", (team_name, ))
        team_id = cursor.lastrowid
        
    conn.commit()
    conn.close()
    return team_id

def save_match(match_id, league_id, team1, team2, score1, score2, stadium, weather, referee, match_date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    team1_id = save_team(team1)
    team2_id = save_team(team2)
    
    cursor.execute("""
        INSERT INTO matches (id_match, league_id, home_team, away_team, score_home, score_away, stadium, weather, referee, match_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)               
    """, (match_id, league_id, team1_id, team2_id, score1, score2, stadium, weather, referee, match_date))
    conn.commit()
    conn.close()
    
    
def save_stats(match_id, stats):
    """Сохраняет статистику матча."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO stats (id_match, xg1, xg2, shots1, shots2, shotsongoal1, shotsongoal2, possession1, possession2,
                        corner_kicks1, corner_kicks2, infringements1, infringements2, offsides1, offsides2, 
                        yellow_card1, yellow_card2, red_card1, red_card2, passes1, passes2, pass_accuracy1, pass_accuracy2)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        match_id,
        stats.get('xG', (0, 0))[0], stats.get('xG', (0, 0))[1],
        stats.get('Удары', (0, 0))[0], stats.get('Удары', (0, 0))[1],
        stats.get('Удары в створ', (0, 0))[0], stats.get('Удары в створ', (0, 0))[1],
        stats.get('Владение %', (0, 0))[0], stats.get('Владение %', (0, 0))[1],
        stats.get('Угловые', (0, 0))[0], stats.get('Угловые', (0, 0))[1],
        stats.get('Нарушения', (0, 0))[0], stats.get('Нарушения', (0, 0))[1],
        stats.get('Офсайды', (0, 0))[0], stats.get('Офсайды', (0, 0))[1],
        stats.get('Желтые карточки', (0, 0))[0], stats.get('Желтые карточки', (0, 0))[1],
        stats.get('Красные карточки', (0, 0))[0], stats.get('Красные карточки', (0, 0))[1],
        stats.get('Передачи', (0, 0))[0], stats.get('Передачи', (0, 0))[1],
        stats.get('Точность передач %', (0, 0))[0], stats.get('Точность передач %', (0, 0))[1]
    ))

    conn.commit()
    conn.close()
    
def save_commands(match_id, team_name, players, coach):
    """Сохраняет состав команды на матч."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    team_id = save_team(team_name)

    cursor.execute("""
        INSERT INTO commands (id_match, id_team, player1, player2, player3, player4, player5, player6, player7, player8, player9,
                            player10, player11, coach)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (match_id, team_id, *players, coach))

    conn.commit()
    conn.close()