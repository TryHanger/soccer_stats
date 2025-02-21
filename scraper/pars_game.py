from pars_team import get_team_matches
import requests
from config import HEADERS
from bs4 import BeautifulSoup


def parse_game(team_id):
    match_links = get_team_matches(team_id)
    results = []
    
    for link in match_links:
        response = requests.get(link, headers=HEADERS)
        if response.status_code != 200:
            print(f"Ошибка при получении {link}: {response.status_code}")
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        with open("error_page.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
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
            print(stats)
        except Exception as e:
            print(f"Ошибка при обработке {link}: {e}")

    return results

print(parse_game(2))
