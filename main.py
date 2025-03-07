from scraper.pars_team import get_team_matches
from scraper.pars_game import parse_game
from database.create_db import create_db, recreate_db
from scraper.update_match import update_matches, update_all_teams
from scraper.pars_league import parse_league_info 
from scraper.pars_teams import get_teams
from utils.leagues_loader import load_config
from config import LEAGUES_PATH
from scraper.add_info import add_info
import json
import requests
import time
from bs4 import BeautifulSoup
from config import HEADERS

fsd = ['https://soccer365.ru/games/2234518/', 'https://soccer365.ru/games/2083820/', 'https://soccer365.ru/games/2231226/', 'https://soccer365.ru/games/2083815/',
       'https://soccer365.ru/games/2083801/', 'https://soccer365.ru/games/2083796/', 'https://soccer365.ru/games/2220600/', 'https://soccer365.ru/games/2083789/',
       'https://soccer365.ru/games/2174473/', 'https://soccer365.ru/games/2083772/', 'https://soccer365.ru/games/2174474/', 'https://soccer365.ru/games/2083765/',
       'https://soccer365.ru/games/2215059/', 'https://soccer365.ru/games/2146532/', 'https://soccer365.ru/games/2142933/', 'https://soccer365.ru/games/2200198/',
       'https://soccer365.ru/games/2083747/', 'https://soccer365.ru/games/2083731/', 'https://soccer365.ru/games/2174465/', 'https://soccer365.ru/games/2083726/']


# create_db()

recreate_db()

# iss = load_config()

add_info()

# link = "https://soccer365.ru/games/2231226/"
# response = requests.get(link, headers=HEADERS)
# if response.status_code != 200:
#     print(f"❌ Ошибка при получении {link}: {response.status_code}")

# soup = BeautifulSoup(response.text, "html.parser")
# print(soup)
# match_id = link.rstrip('/').split('/')[-1]
# print(match_id)


# for link in fsd: 
#     print(parse_game(link, iss))
#     time.sleep(1)

# print(parse_game("https://soccer365.ru/games/2142933/", iss))

# print(get_team_matches(12))
# print(get_teams(12))


# print(parse_league_info(18))

# print(get_teams(12))

# print(update_all_teams())
