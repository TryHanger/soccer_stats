import json
from config import CONFIG_PATH

def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"❌ Файл {CONFIG_PATH} не найден.")
        return {}
    except json.JSONDecodeError:
        print(f"❌ Ошибка в формате JSON файла {CONFIG_PATH}.")
        return {}
    
def add_team(name, team_id):
    config = load_config()
    config.setdefault("teams", {})
    config["teams"][name] = team_id
    
    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4, ensure_ascii=False)
    print(f"✅ Команда {name} (ID: {team_id}) добавлена в конфиг.")