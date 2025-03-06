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

# create_db()

recreate_db()

# print(load_config())

add_info()

# print(parse_league_info(18))

# print(get_teams(12))

# print(update_all_teams())