import time
from utils.leagues_loader import load_config
from scraper.pars_league import parse_league_info
from database.save_league import save_league
from scraper.pars_teams import get_teams
from scraper.pars_team import get_team_matches
from scraper.pars_game import parse_game
from database.save_game_on_db import match_exists


def add_info():
    leagues = load_config()
    print(leagues) 
    league_ids = [league['id'] for league in leagues if 'id' in league]

    for league_id in league_ids:
        print(league_id)
        league_data = parse_league_info(league_id)
        save_league(league_data)
        print(league_data)
        
        teams_list = get_teams(league_id)
        print(teams_list)
        
        team_ids = [team[1] for team in teams_list]
        print(team_ids)
        
        for team_id in team_ids:
            
            game_links = get_team_matches(team_id)
            print(game_links)
            
            for link in game_links:
                match_id = link.rstrip('/').split('/')[-1]
                if not match_id.isdigit():
                    print(f"❌ Ошибка: Некорректный match_id в ссылке {link}")
                    continue
                
                if match_exists(match_id):
                    print(f"⚠️ Матч {match_id} уже существует в базе данных")
                    continue
                
                leagues = parse_game(link, leagues)
                print(f"Матч спаршен {match_id}")
                
                time.sleep(1)