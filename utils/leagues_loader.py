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
    