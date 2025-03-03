from datetime import datetime
from scraper.pars_team import get_team_matches
import requests
from config import HEADERS
from bs4 import BeautifulSoup
from database.save_game_on_db import save_match, save_stats
from database.save_game_on_db import save_commands, match_exists


def parse_game(team_id, link):
    # match_links = get_team_matches(team_id)
    # results = []
    
    # for link in match_links:
        response = requests.get(link, headers=HEADERS)
        if response.status_code != 200:
            print(f"Ошибка при получении {link}: {response.status_code}")
            # continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        # with open("error_page.html", "w", encoding="utf-8") as f:
        #     f.write(soup.prettify())
            
        match_id = link.rstrip('/').split('/')[-1]
            
        try:
            '''
            Разбор загаловка матча с названием команд и счетом
            '''
            header = soup.find("div", id="game_events")
            left_data = header.find("div", class_="live_game left")
            team1_name = left_data.find("div", class_="live_game_ht").find("a").text
            score1 = left_data.find("div", class_="live_game_goal").find("span").text
            right_data = header.find("div", class_="live_game right")
            team2_name = right_data.find("div", class_="live_game_at").find("a").text
            score2 = right_data.find("div", class_="live_game_goal").find("span").text
            date_header = header.find("h2")
            if date_header:
                header_text = date_header.text.strip()
                
                # Ищем дату и время с помощью split
                date_time = header_text.split(",")[-1].strip()
                # Преобразование строки в объект datetime
                match_datetime = datetime.strptime(date_time, "%d.%m.%Y %H:%M")
                                
            '''
            Разбор статистики матча
            '''
            stats_block = soup.find("div", class_="stats_items", style="float:left;")
            stats = {}

            # Проходим по каждому блоку статистики
            for stat in soup.find_all(class_="stats_item"):
                title = stat.find(class_="stats_title").text.strip()  # Название показателя
                values = [inf.text.strip() for inf in stat.find_all(class_="stats_inf")]  # Числовые значения
                if len(values) == 2:  # У каждого показателя два значения (для двух команд)
                    stats[title] = tuple(map(float, values))  # Преобразуем в float
            
            '''
            Стадион и погода
            '''
            preview = soup.find("div", class_="preview_item st")
            stadium = preview.find("div", class_="img16 std").text
            weather = preview.find("div", class_="img16 weath_tmp").text
            
            
            '''
            Игроки и тренера
            '''
            players_block = soup.find("div", class_="body_tab")

            if players_block:
                # Ищем все блоки composit_block
                composit_blocks = players_block.find_all("div", class_="сomposit_block")

                if len(composit_blocks) >= 4:
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

                    # Разбираем блоки
                    team1_players = extract_players(composit_blocks[0])
                    team2_players = extract_players(composit_blocks[1])
                    team1_coach = extract_coach(composit_blocks[2])
                    team2_coach = extract_coach(composit_blocks[3])

                    referee_block = soup.find("span", class_="preview_param", string="Арбитры")
                    first_referee_block = referee_block.find_next("div", class_="img16")
                    referee_name_tag = first_referee_block.find("a")
                    referee_name = referee_name_tag.get_text(strip=True)
            if not match_exists(match_id):    
                save_match(match_id, team1_name, team2_name, score1, score2, stadium, weather, referee_name, match_datetime)
                save_stats(match_id, stats)
                save_commands(match_id, team1_name, team1_players, team1_coach)
                save_commands(match_id, team2_name, team2_players, team2_coach)      
            else:
                print(f"Матч {match_id} уже существует в базе данных")
            
        except Exception as e:
            print(f"Ошибка при обработке {link}: {e}")
