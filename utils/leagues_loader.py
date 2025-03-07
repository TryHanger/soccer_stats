import json
from config import LEAGUES_PATH

def load_config():
    try:
        with open(LEAGUES_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"❌ Файл {LEAGUES_PATH} не найден.")
        return {}
    except json.JSONDecodeError:
        print(f"❌ Ошибка в формате JSON файла {LEAGUES_PATH}.")
        return {}
    
def save_league_json(data):
    
    leagues = load_config()    
    
    new_league = {"id": data["url_id"], "name": data["league_name"], "tier": 1}
    leagues.append(new_league)
    
    with open(LEAGUES_PATH, "w", encoding="utf-8") as f:
        json.dump(leagues, f, ensure_ascii=False, indent=4)