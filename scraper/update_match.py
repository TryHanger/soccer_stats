from datetime import datetime
from scraper.pars_team import get_team_matches
from database.check_matches import get_existing_matches
from scraper.pars_game import parse_game
from database.delete_match import delete_oldest_match
from utils.config_loader import load_config


def update_matches(team_id):
    # Получаем сохранённые матчи из базы
    
    existing_matches = get_existing_matches(team_id)
    existing_ids = {match["id"] for match in existing_matches}
    
    new_matches = get_team_matches(team_id)
    
    for link in new_matches:
        match_id = link.rstrip('/').split('/')[-1]
        
        if match_id not in existing_ids:
            print(f"Обновляем матч {match_id}")
            parse_game(team_id, link)
        else:
            print(f"Матч {match_id} уже есть в базе")
            
    # Оставляем только последние 20 матчей
    # if len(existing_matches) > 20:
    #     matches_to_delete = sorted(existing_matches, key=lambda match: match["date"])[:-10]

    #     for match in matches_to_delete:
    #         print(f"Удаляем матч {match['id']}")
    #         delete_oldest_match(match["id"])
            

def update_all_teams():
    config = load_config()
    teams = config.get("teams", {})
    print(teams)
    if not teams:
        print("⚠️ Список команд пуст. Добавьте команды в config.json!")
        return

    for team_name, team_id in teams.items():
        print(f"\n🔍 Обновляем матчи для {team_name} (ID: {team_id})")
        update_matches(team_id)
