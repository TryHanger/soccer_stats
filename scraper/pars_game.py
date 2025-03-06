from datetime import datetime
from scraper.pars_team import get_team_matches
import requests
from config import HEADERS
from bs4 import BeautifulSoup
from database.save_game_on_db import save_match, save_stats
from database.save_game_on_db import save_commands, match_exists
from scraper.pars_league import get_league_id_by_name

def parse_game(link, leagues):
    try:
        # Получаем HTML страницы
        response = requests.get(link, headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ Ошибка при получении {link}: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, "html.parser")
        match_id = link.rstrip('/').split('/')[-1]

        # Разбор информации о матче
        header = soup.find("div", id="game_events")
        if not header:
            print(f"⚠️ Не удалось найти блок с событиями для матча {match_id}")
            return
        
        try:
            league_header = header.find("div", class_="block_header bkcenter").find("h2")
            league_name = league_header.text.split(",")[0].strip()
            league_id = get_league_id_by_name(league_name, leagues)
            
            
            left_data = header.find("div", class_="live_game left")
            right_data = header.find("div", class_="live_game right")

            team1_name = left_data.find("div", class_="live_game_ht").find("a").text.strip()
            score1 = left_data.find("div", class_="live_game_goal").find("span").text.strip()
            
            team2_name = right_data.find("div", class_="live_game_at").find("a").text.strip()
            score2 = right_data.find("div", class_="live_game_goal").find("span").text.strip()
            
            date_header = header.find("h2")
            match_datetime = None
            if date_header:
                date_time = date_header.text.strip().split(",")[-1].strip()
                match_datetime = datetime.strptime(date_time, "%d.%m.%Y %H:%M")
        except AttributeError:
            print(f"⚠️ Ошибка парсинга основной информации для матча {match_id}")
            return
        
        # Разбор статистики
        stats = {}
        for stat in soup.find_all(class_="stats_item"):
            title = stat.find(class_="stats_title").text.strip()
            values = [inf.text.strip() for inf in stat.find_all(class_="stats_inf")]
            if len(values) == 2:
                try:
                    stats[title] = tuple(map(float, values))
                except ValueError:
                    stats[title] = (None, None)

        # Разбор стадиона и погоды
        try:
            preview = soup.find("div", class_="preview_item st")
            stadium = preview.find("div", class_="img16 std").text.strip() if preview else "Не найдено"
            weather = preview.find("div", class_="img16 weath_tmp").text.strip() if preview else "Не найдено"
        except AttributeError:
            stadium, weather = "Не найдено", "Не найдено"

        # Разбор арбитра
        try:
            referee_block = soup.find("span", class_="preview_param", string="Арбитры")
            first_referee_block = referee_block.find_next("div", class_="img16")
            referee_name_tag = first_referee_block.find("a")
            referee_name = referee_name_tag.get_text(strip=True) if referee_name_tag else "Неизвестно"
        except AttributeError:
            referee_name = "Неизвестно"

        # Разбор игроков и тренеров
        team1_players, team2_players = [], []
        team1_coach, team2_coach = "Тренер не найден", "Тренер не найден"

        players_block = soup.find("div", class_="body_tab")
        if players_block:
            composit_blocks = players_block.find_all("div", class_="сomposit_block")

            def extract_players(block):
                players = []
                for player_row in block.find_all("tr"):
                    player_name_tag = player_row.find("span", class_="сomposit_player")
                    if player_name_tag and player_name_tag.a:
                        player_name = player_name_tag.a.get_text(strip=True)
                        players.append(player_name)
                return players

            def extract_coach(block):
                coach_title = block.find("div", class_="lp_title")
                if coach_title and "Главный тренер" in coach_title.get_text(strip=True):
                    coach_name_tag = block.find("span")
                    if coach_name_tag and coach_name_tag.a:
                        return coach_name_tag.a.get_text(strip=True)
                return "Тренер не найден"

            if len(composit_blocks) >= 4:
                team1_players = extract_players(composit_blocks[0])
                team2_players = extract_players(composit_blocks[1])
                team1_coach = extract_coach(composit_blocks[2])
                team2_coach = extract_coach(composit_blocks[3])

        # Сохранение данных в базу
        print(f"📊 Сохраняем матч {match_id} между {team1_name} и {team2_name}")
        save_match(match_id, league_id, team1_name, team2_name, score1, score2, stadium, weather, referee_name, match_datetime)
        save_stats(match_id, stats)
        save_commands(match_id, team1_name, team1_players, team1_coach)
        save_commands(match_id, team2_name, team2_players, team2_coach)

    except Exception as e:
        print(f"❌ Ошибка при обработке {link}: {e}")