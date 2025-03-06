from scraper.pars_team import get_team_matches
from scraper.pars_game import parse_game
from database.create_db import create_db
from scraper.update_match import update_matches, update_all_teams
from scraper.pars_league import parse_league_info 
from scraper.pars_teams import get_teams

def main():
    # Создаем базу данных
    # create_db()
    
    # Парсим информацию о лиге
    league_info = parse_league_info(18)
    print(league_info)
    
    # Получаем команды в лиге
    teams = get_teams(12)
    print(teams)
    
    # # Обновляем все команды
    # update_all_teams()
    
    # # Парсим матчи для каждой команды
    # for team in teams:
    #     matches = get_team_matches(team['id'])
    #     for match in matches:
    #         # Парсим данные каждого матча
    #         match_data = parse_game(match['id'])
    #         # Сохраняем данные матча в базу данных
    #         update_matches(match_data)

if __name__ == "__main__":
    main()
