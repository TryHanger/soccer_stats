from datetime import datetime
from scraper.pars_team import get_team_matches
import requests
import re
from config import HEADERS
from bs4 import BeautifulSoup
from database.save_game_on_db import save_match, save_stats
from database.save_game_on_db import save_commands, match_exists
from scraper.pars_league import find_league_id

def parse_game(link, leagues):
    try:
        
        session = requests.Session()
        session.get("https://soccer365.ru/", headers=HEADERS)
        response = session.get(link, headers=HEADERS, allow_redirects=False)
        
        if response.status_code != 200:
            print(f"❌ Ошибка при получении {link}: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, "html.parser")
        match_id = link.rstrip('/').split('/')[-1]
        
        script_tag = soup.find("script", string=re.compile(r"game_id"))
        script_text = script_tag.string
        
        game_data = {
            "game_id": re.search(r"game_id\s*=\s*(\d+);", script_text).group(1),
            "game_competition_id": re.search(r"game_competition_id\s*=\s*(\d+);", script_text).group(1),
            "game_ht_id": re.search(r"game_ht_id\s*=\s*(\d+);", script_text).group(1),
            "game_at_id": re.search(r"game_at_id\s*=\s*(\d+);", script_text).group(1),
            "game_ht_title": re.search(r"game_ht_title\s*=\s*'([^']+)';", script_text).group(1),
            "game_at_title": re.search(r"game_at_title\s*=\s*'([^']+)';", script_text).group(1),
        }
        
        try:
            id_league_in_bd, leagues_dict = find_league_id(game_data["game_competition_id"], leagues)
        except  Exception as e:
            print(f"❌ Ошибка при поиске лиги {int(game_data['game_competition_id'])}: {e}")
        
        
        # Разбор информации о матче
        header = soup.find("div", id="game_events")
        if not header:
            print(f"⚠️ Не удалось найти блок с событиями для матча {match_id}")
            return
        
        try:

            left_data = header.find("div", class_="live_game left")
            right_data = header.find("div", class_="live_game right")

            """ Возможно не понадобится """
            team1_name = left_data.find("div", class_="live_game_ht").find("a").text.strip()
            team2_name = right_data.find("div", class_="live_game_at").find("a").text.strip()
            
            
            score1 = left_data.find("div", class_="live_game_goal").find("span").text.strip()
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
                    
                    if player_name_tag:
                        # Если есть ссылка — берём имя из неё
                        if player_name_tag.a:
                            player_name = player_name_tag.a.get_text(strip=True)
                        else:
                            # Если ссылки нет, берём текст напрямую из <span>
                            player_name = player_name_tag.get_text(strip=True)
                        
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

        try:
            save_match(game_data["game_id"], id_league_in_bd, team1_name, team2_name, score1, score2, stadium, weather, referee_name, match_datetime)
        except Exception as e:
            print(f"❌ Ошибка парсинга матча {match_id}: {e}")
        try:
            save_stats(game_data["game_id"], stats)
        except Exception as e:
            print(f"❌ Ошибка при сохранении статистики для матча {match_id}: {e}")
        try:
            # print(game_data["game_id"], team1_name, team1_players, team1_coach)
            save_commands(game_data["game_id"], team1_name, team1_players, team1_coach)
        except Exception as e:
            print(f"❌ Ошибка при сохранении команды {team1_name}: {e}")
        try:
            # print(game_data["game_id"], team2_name, team2_players, team2_coach)
            save_commands(game_data["game_id"], team2_name, team2_players, team2_coach)
        except Exception as e:
            print(f"❌ Ошибка при сохранении команды {team2_name}: {e}")
        
        if leagues_dict:
            return leagues_dict
        else:
            return leagues
    except Exception as e:
        print(f"❌ Ошибка при обработке {link}: {e}")